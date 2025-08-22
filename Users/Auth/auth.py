import uuid
import json
from Helper import db_helper
from Users.Consultant.consultant import select_con_info
from Users.Institute.institute import select_ins_info
from Users.Student.student import select_student_info


def create_token(conn, cursor, data):
    try:
        query = "SELECT token FROM tokens WHERE user_id = ?"
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data[0])
        if res is None:
            while True:
                token = str(uuid.uuid4())
                token_check_query = "SELECT token FROM tokens WHERE token = ?"
                token_exists = db_helper.search_table(conn=conn, cursor=cursor, query=token_check_query, field=token)
                if not token_exists:
                    field = '([token], [user_id], [phone], [role])'
                    values = (token, data[0], data[1], data[2])
                    db_helper.insert_value(conn=conn, cursor=cursor, table_name="tokens", fields=field, values=values)
                    return token
        else:
            return res[0]
    except Exception as e:
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/auth", "create_token",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None


def token_remove(conn, cursor, data, info):
    try:
        res = db_helper.delete_record(
            conn, cursor, "tokens",
            ["user_id"],
            [info["user_id"]]
        )
        return res
    except Exception as e:
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/auth", "delete_token",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None


def check_signin(conn, cursor, data):
    try:
        phone = data["phone"]
        password = data["password"]
        query = 'SELECT user_id, password, role FROM users WHERE phone = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        if res is None:
            return None, " کاربری با این شماره تلفن موجود نمی‌باشد.", None
        db_password = res.password
        if db_password == password:
            info = [res.user_id, phone, res.role]
            token_user = create_token(conn=conn, cursor=cursor, data=info)
        else:
            return None, "رمز عبور شما درست نمی‌باشد.", None
        if res.role == "ins":
            token, info = select_ins_info(conn=conn, cursor=cursor, user_id=res.user_id)
        elif res.role == "con":
            token, info = select_con_info(conn=conn, cursor=cursor, user_id=res.user_id)
        elif res.role == "stu":
            token, info = select_student_info(conn=conn, cursor=cursor, user_id=res.user_id)
        return token_user, "", info
    except Exception as e:
        print(">>>>>> auth check signin error", e)
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/auth", "check_signin",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در ورود شما رخ داده است.", None
