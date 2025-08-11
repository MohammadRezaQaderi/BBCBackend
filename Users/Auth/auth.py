import uuid
import json
from Helper import db_helper
from Helper.func_helper import password_format_check, check_security_code, random_with_n_digits
from Helper.otp_helper import send_otp_message
from Users.Consultant.consultant import select_con_info
from Users.HeadConsultant.head_consultant import select_hCon_info
from Users.Institute.institute import select_ins_info, insert_ins, verify_ins
from Users.OwnerConsultant.owner_consultant import select_oCon_info, insert_oCon, verify_oCon
from Users.Student.student import select_student_info


def create_token(conn, cursor, data):
    query = "SELECT token FROM ERNew.dbo.tokens WHERE user_id = ?"
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data[0])
    if res is None:
        while True:
            token = str(uuid.uuid4())
            token_check_query = "SELECT token FROM ERNew.dbo.tokens WHERE token = ?"
            token_exists = db_helper.search_table(conn=conn, cursor=cursor, query=token_check_query, field=token)
            if not token_exists:
                field = '([token], [user_id], [phone], [role])'
                values = (token, data[0], data[1], data[2])
                db_helper.insert_value(conn=conn, cursor=cursor, table_name="tokens", fields=field, values=values)
                return token
    else:
        return res[0]


def delete_token(conn, cursor, data):
    db_helper.delete_record(
        conn, cursor, "tokens",
        ["user_id"],
        [data["user_id"]]
    )


def check_signin(conn, cursor, data):
    phone = data["phone"]
    password = data["password"]
    query = 'SELECT user_id, password, role FROM ERNew.dbo.users WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is None:
        return None, " کاربری با این شماره تلفن موجود نمی‌باشد.", None
    db_password = res[1]
    if db_password == password:
        info = [res[0], phone, res[2]]
        token_user = create_token(conn=conn, cursor=cursor, data=info)
    else:
        return None, "رمز عبور شما درست نمی‌باشد.", None
    if res[2] == "ins":
        query = 'SELECT verify FROM ERNew.dbo.ins WHERE phone = ?'
        res_verify = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        if res_verify[0] == 0:
            delete_token(conn=conn, cursor=cursor, data={"user_id": res[0]})
            return None, "شما هنوز احراز هویت انجام نداده‌اید.", None
        token, info = select_ins_info(conn=conn, cursor=cursor, user_id=res[0])
    elif res[2] == "oCon":
        query = 'SELECT verify FROM ERNew.dbo.oCon WHERE phone = ?'
        res_verify = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        if res_verify[0] == 0:
            delete_token(conn=conn, cursor=cursor, data={"user_id": res[0]})
            return None, "شما هنوز احراز هویت انجام نداده‌اید.", None
        token, info = select_oCon_info(conn=conn, cursor=cursor, user_id=res[0])
    elif res[2] == "hCon":
        token, info = select_hCon_info(conn=conn, cursor=cursor, user_id=res[0])
    elif res[2] == "con":
        token, info = select_con_info(conn=conn, cursor=cursor, user_id=res[0])
    elif res[2] == "stu":
        token, info = select_student_info(conn=conn, cursor=cursor, user_id=res[0])
    return token_user, "", info


def check_signup(conn, cursor, data, redis_db):
    phone = data["phone"]
    password = data["password"]
    re_password = data["re_password"]
    role = data["role"]
    # if data.get("referral_code"):
    #     query = 'SELECT * FROM ERNew.dbo.exist_referral_code WHERE code = ?'
    #     res_referral = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["referral_code"])
    #     if not res_referral:
    #         return None, "کد معرف شما در سامانه موجود نیست."
    # else:
    #     return None, "کد معرف شما مشکل دارد."
    if password != re_password:
        return None, "رمز عبور و تکرار رمز عبور باهم تطابق ندارد."
    val, message = password_format_check(password=password)
    if val is None:
        return None, message
    query = 'SELECT user_id FROM ERNew.dbo.users WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is not None:
        return None, "این شماره تلفن موجود می‌باشد."
    field = '([phone], [password], [role])'
    values = (phone, password, role,)
    db_helper.insert_value(conn=conn, cursor=cursor, table_name="users", fields=field,
                           values=values)
    query = 'SELECT user_id FROM ERNew.dbo.users WHERE phone = ?'
    res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if role == "ins":
        token = insert_ins(conn=conn, cursor=cursor, data=data, user_id=res_user[0])
        cache = redis_db.cache("verify_cache_ER")
        cache_record = cache.get(phone)
        if cache_record is not None:
            cache.delete(phone)
        code = random_with_n_digits(5)
        res_otp = send_otp_message(code=code, phone=phone)
        cache.set(phone, json.dumps({"code": code}), 60 * 60 * 24 * 100)
        return token, "ثبت نام شما با موفقیت انجام شد."
    elif role == "oCon":
        token = insert_oCon(conn=conn, cursor=cursor, data=data, user_id=res_user[0])
        cache = redis_db.cache("verify_cache_ER")
        cache_record = cache.get(phone)
        if cache_record is not None:
            cache.delete(phone)
        code = random_with_n_digits(5)
        res_otp = send_otp_message(code=code, phone=phone)
        cache.set(phone, json.dumps({"code": code}), 60 * 60 * 24 * 100)
        return token, "ثبت نام شما با موفقیت انجام شد."


def check_send_sms(conn, cursor, data, redis_db):
    phone = data["phone"]
    type_otp = data["type"]
    if not check_security_code(data["code"], data["check"]):
        return None, "کد امنیتی وارد شده اشتباه است.", None
    query = 'SELECT phone, role FROM ERNew.dbo.users WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is None:
        return None, "کاربری با این شماره تلفن موجود نمی‌باشد.", None
    if res[1] == "ins" and type_otp == "verify":
        query = 'SELECT verify FROM ERNew.dbo.ins WHERE phone = ?'
        res_verify = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        if res_verify[0] == 1:
            return None, "شما از قبل احراز هویت نموده‌اید.", None
    if res[1] == "oCon" and type_otp == "verify":
        query = 'SELECT verify FROM ERNew.dbo.oCon WHERE phone = ?'
        res_verify = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        if res_verify[0] == 1:
            return None, "شما از قبل احراز هویت نموده‌اید.", None
    cache = redis_db.cache("verify_cache_ER")
    cache_record = cache.get(phone)
    if cache_record is not None:
        cache.delete(phone)
    code = random_with_n_digits(5)
    res_otp = send_otp_message(code=code, phone=phone)
    cache.set(res[0], json.dumps({"code": code}), 60 * 60 * 24 * 100)
    token = str(uuid.uuid4())
    return token, "", phone


def check_sms_verify(conn, cursor, data, redis_db):
    phone = data["phone"]
    code = data["code"]
    type_otp = data["type"]
    query = 'SELECT user_id, password, role FROM ERNew.dbo.users WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is None:
        return None, "کاربری با این شماره تلفن موجود نمی‌باشد.", None
    if type_otp == "otp":
        cache = redis_db.cache("verify_cache_ER")
        cache_record = cache.get(phone)
        if cache_record is not None:
            record = json.loads(cache_record)
            if int(code) == record["code"]:
                info = [res[0], phone, res[2]]
                token_user = create_token(conn=conn, cursor=cursor, data=info)
                if res[2] == "ins":
                    token, info = select_ins_info(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
                elif res[2] == "oCon":
                    token, info = select_oCon_info(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
                elif res[2] == "hCon":
                    token, info = select_hCon_info(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
                elif res[2] == "con":
                    token, info = select_con_info(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
            else:
                return None, "کد وارد شده صحیح نمی‌باشد.", None
        else:
            return None, "کدی برای این شماره تلفن در سامانه ثبت نشده. لطفا دوباره  درخواست دهید.", None
    else:
        cache = redis_db.cache("verify_cache_ER")
        cache_record = cache.get(phone)
        if cache_record is not None:
            record = json.loads(cache_record)
            if int(code) == record["code"]:
                info_token = [res[0], phone, res[2]]
                token_user = create_token(conn=conn, cursor=cursor, data=info_token)
                if res[2] == "ins":
                    token, info = verify_ins(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
                elif res[2] == "oCon":
                    token, info = verify_oCon(conn=conn, cursor=cursor, user_id=res[0])
                    return token_user, "", info
            else:
                return None, "کد وارد شده صحیح نمی‌باشد.", None
        else:
            return None, "کدی برای این شماره تلفن در سامانه ثبت نشده. لطفا دوباره  درخواست دهید.", None
