import uuid
import json
from datetime import datetime

from Helper import db_helper
from Helper.func_helper import id_generator, random_phone_number, password_format_check


def select_ins_info(conn, cursor, user_id):
    try:
        query = 'SELECT ins_id, name, phone, probability_permission, logo FROM ins WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
        token = str(uuid.uuid4())
        info = {
            "phone": res.phone, "user_id": user_id, "id": res.ins_id, "name": res.name, "role": "ins", "pic": res.logo,
            "permission": res.probability_permission
        }
        return token, info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            user_id, None, "bbc_api/ins", "select_ins_info",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_new_ins_dashboard(conn, cursor, order_data, info):
    try:
        user_id = info["user_id"]

        queries = {
            'capacity': 'SELECT hu, ha, fru, fra, agu, aga FROM capacity WHERE user_id = ?',
            'con_count': 'SELECT count(*) FROM con WHERE ins_id = ?',
            'stu_count': 'SELECT count(*) FROM stu WHERE ins_id = ?',
            'con_finalized': 'SELECT count(*) FROM stu WHERE ins_id = ? and con_finalized = 1',
            'finish_quiz': 'SELECT count(*) FROM quiz_answer WHERE ins_id = ? and quiz_id = 7 and state = 2',
            'started_quiz': 'SELECT count(distinct (user_id)) FROM quiz_answer WHERE ins_id = ?',
            'all_can_quiz': 'SELECT count(*) FROM stu WHERE ins_id = ? and ag_access = 1'
        }

        results = {}
        for key, query in queries.items():
            results[key] = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)

        token = str(uuid.uuid4())
        cons_info = {
            "HU": results["capacity"][0],
            "HA": results["capacity"][1],
            "FRU": results['capacity'][2],
            "FRA": results['capacity'][3],
            "AGU": results['capacity'][4],
            "AGA": results['capacity'][5],
            "con_count": results['con_count'][0],
            "stu_count": results['stu_count'][0],
            "con_finalized": results['con_finalized'][0],
            "finish_quiz": results['finish_quiz'][0],
            "started_quiz": results['started_quiz'][0],
            "all_can_quiz": results['all_can_quiz'][0]
        }

        return token, cons_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_new_ins_dashboard",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def insert_ins_con(conn, cursor, order_data, info):
    try:
        query = 'SELECT user_id FROM users WHERE phone = ?'
        res_check_user_phone = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["phone"])
        if res_check_user_phone is not None:
            return None, "شماره تلفن وارد شده در سامانه موجود می‌باشد لطفا شماره تلفن دیگری وارد نمایید."
        password = id_generator()
        field = '([phone], [password], [role])'
        values = (order_data["phone"], password, 'con',)
        res_add_user = db_helper.insert_value(conn=conn, cursor=cursor, table_name="users", fields=field,
                                              values=values)
        query = 'SELECT user_id FROM users WHERE phone = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["phone"])
        field = '([user_id], [phone], [first_name], [last_name], [sex], [ins_id], [password], [adder_id], [editor_id])'
        values = (
            res_user.user_id, order_data["phone"], order_data["first_name"], order_data["last_name"],
            order_data["sex"], info["user_id"], password, info["user_id"],
            info["user_id"],)
        res_add_con = db_helper.insert_value(conn=conn, cursor=cursor, table_name="con", fields=field,
                                             values=values)
        token = str(uuid.uuid4())
        return token, "مشاور با موفقیت اضافه شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "insert_ins_con",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در افزودن مشاور پیش آمده"


def insert_ins_stu(conn, cursor, order_data, info):
    try:
        phone = random_phone_number(conn, cursor, 8)
        password = id_generator()
        field = '([phone], [password], [role])'
        values = (phone, password, 'stu',)
        res_add_user = db_helper.insert_value(conn=conn, cursor=cursor, table_name="users", fields=field,
                                              values=values)
        query = 'SELECT user_id FROM users WHERE phone = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        field = '([user_id], [phone], [first_name], [last_name], [sex], [birth_date], [city], [field], [quota], [ins_id], [con_id], [password], [adder_id], [editor_id])'
        values = (
            res_user[0], phone, order_data["first_name"], order_data["last_name"],
            order_data["sex"], order_data["birth_date"], order_data["province"], int(order_data["field"]),
            int(order_data["quota"]), info["user_id"], order_data["con_id"], password,
            info["user_id"], info["user_id"],)
        res_add_stu = db_helper.insert_value(conn=conn, cursor=cursor, table_name="stu", fields=field,
                                             values=values)
        token = str(uuid.uuid4())
        return token, "دانش‌آموز با موفقیت اضافه شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "insert_ins_stu",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در افزودن دانش‌آموز پیش آمده"


def update_ins_user_profile(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "ins", ['name', 'edited_time'],
            [order_data["name"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [info["user_id"]]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "اطلاعات با موفقیت تغییر یافت.", {"name": order_data["name"]}
        else:
            return None, "اطلاعات کاربر تغییر نیافت.", None
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_user_profile",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده", None


def update_ins_password(conn, cursor, order_data, info):
    try:
        val, message = password_format_check(order_data["password"])
        if order_data["password"] != order_data["re_password"]:
            return None, "رمز عبور و تکرار رمز عبور باهم تطابق ندارد."
        if not val:
            return None, message
        row_count = db_helper.update_record(
            conn, cursor, "users", ['password', 'edited_time'],
            [order_data["password"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [info["user_id"]]
        )
        row_count = db_helper.update_record(
            conn, cursor, "ins", ['password', 'edited_time'],
            [order_data["password"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [info["user_id"]]
        )
        token = str(uuid.uuid4())
        return token, "رمز عبور شما با موفقیت تغییر کرد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_password",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده"


def update_user_ins_pic(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "ins", ['name', 'logo', 'edited_time'],
            [order_data["name"], order_data["pic"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [info["user_id"]]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, {"name": order_data["name"], "pic": order_data["pic"]}, "اطلاعات شما با موفقیت تغییر یافت."
        else:
            return None, None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_user_ins_pic",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."


def update_ins_stu_access(conn, cursor, order_data, info):
    try:
        query = 'SELECT hu, ha, fru, fra, agu, aga FROM capacity WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(info["user_id"],))
        if not res:
            return None, "ظرفیت کاربر یافت نشد."
        hu, ha, fru, fra, agu, aga = res.hu, res.ha, res.fru, res.fra, res.agu, res.aga
        kind = order_data["kind"]
        if kind == "hoshmand":
            if ha == 0:
                return None, "شما ظرفیت برای افزودن دانش‌آموز برای انتخاب رشته هوشمند ندارید."
            update_fields = ["hoshmand_access", "hoshmand_limit", "editor_id", "edited_time"]
            update_values = [1, order_data["limitation"], info["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            ha -= 1
            hu += 1
            capacity_update_fields = ["ha", "hu", "edited_time"]
            capacity_update_values = [ha, hu, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        elif kind == "FR":
            if fra == 0:
                return None, "شما ظرفیت برای افزودن دانش‌آموز برای انتخاب رشته آزاد ندارید."
            update_fields = ["fr_access", "fr_limit", "editor_id", "edited_time"]
            update_values = [1, order_data["limitation"], info["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            fra -= 1
            fru += 1
            capacity_update_fields = ["fra", "fru", "edited_time"]
            capacity_update_values = [fra, fru, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        elif kind == "AG":
            if aga == 0:
                return None, "شما ظرفیت برای افزودن دانش‌آموز برای هدایت شغلی ندارید."
            update_fields = ["ag_access", "editor_id", "edited_time"]
            update_values = [1, info["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            aga -= 1
            agu += 1
            capacity_update_fields = ["aga", "agu", "edited_time"]
            capacity_update_values = [aga, agu, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        else:
            return None, "نوع دسترسی نامعتبر است."
        student_condition = "user_id = ?"
        student_condition_values = [order_data["stu_id"]]
        student_updated = db_helper.update_record(
            conn, cursor, "stu", update_fields, update_values, student_condition, student_condition_values
        )

        if student_updated == 0:
            return None, "خطا در بروزرسانی اطلاعات دانش‌آموز."
        capacity_condition = "user_id = ?"
        capacity_condition_values = [info["user_id"]]
        capacity_updated = db_helper.update_record(
            conn, cursor, "capacity", capacity_update_fields, capacity_update_values, capacity_condition,
            capacity_condition_values
        )

        if capacity_updated == 0:
            return None, "خطا در بروزرسانی ظرفیت کاربر."
        token = str(uuid.uuid4())
        return token, "عملیات با موفقیت انجام شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_stu_access",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."


def update_ins_ag_access(conn, cursor, order_data, info):
    try:
        if order_data["kind"] == "AGAccess":
            row_count = db_helper.update_record(
                conn, cursor, "stu", ['ag_pf', 'edited_time'],
                [order_data["value"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [order_data["stu_id"]]
            )
        elif order_data["kind"] == "AGPDF":
            row_count = db_helper.update_record(
                conn, cursor, "stu", ['ag_pdf', 'edited_time'],
                [order_data["value"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [order_data["stu_id"]]
            )
        else:
            return None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."
        if row_count > 0:
            return str(uuid.uuid4()), "اطلاعات شما با موفقیت تغییر یافت."
        else:
            return None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_ag_access",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."


def update_ins_permission(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "ins", ['probability_permission', 'edited_time'],
            [order_data["permission"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [info["user_id"]]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "نمایش احتمال قبولی‌ها تغییر یافت. برای اعمال به دانش‌آموزان خود اعلام کنید که از سامانه یکبار خروج کرده و دوباره برگردند.", \
                order_data["permission"]
        else:
            return None, "تغییرات شما اعمال نشد. لطفا از پشتیبانی پیگیری بفرمایید.", 0
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_permission",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."


def select_ins_consultant(conn, cursor, order_data, info):
    try:
        con_data = []
        query = 'SELECT user_id, phone, first_name, last_name, sex, password FROM con WHERE ins_id = ? order by created_time desc'
        res_con = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        token = str(uuid.uuid4())

        if len(res_con) == 0:
            return token, con_data
        else:
            for con in res_con:
                c = {"first_name": con.first_name, "last_name": con.last_name, "user_id": con.user_id,
                     "phone": con.phone,
                     "sex": con.sex, "password": con.password}
                con_data.append(c)
        return token, con_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_ins_consultant",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_ins_cons_stu(conn, cursor, order_data, info):
    try:
        query = 'SELECT user_id, first_name, last_name FROM con WHERE ins_id = ? order by created_time desc'
        res_con = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        con_data = []
        if len(res_con) == 0:
            token = str(uuid.uuid4())
            return token, []
        for con in res_con:
            c = {"name": con.first_name + " " + con.last_name, "con_id": con.user_id}
            con_data.append(c)
        token = str(uuid.uuid4())
        return token, con_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_ins_cons_stu",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_ins_student(conn, cursor, order_data, info):
    try:
        query = '''
                SELECT user_id, first_name, last_name, phone, sex, password, rank, field,
                       hoshmand_access, ag_access, fr_access, finalized, con_id, fr_limit, hoshmand_limit
                FROM stu
                WHERE ins_id = ?
                ORDER BY created_time DESC
            '''
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=(info["user_id"],))
        stu_data = []
        if not res_stu:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
            query = 'SELECT first_name, last_name FROM con WHERE user_id = ?'
            res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(stu.con_id,))
            con_name = ""
            if res_con and len(res_con) >= 2:
                con_name = f"{res_con.first_name} {res_con.last_name}"
            s = {
                "name": f"{stu.first_name} {stu.last_name}",
                "user_id": stu.user_id,
                "phone": stu.phone,
                "sex": stu.sex,
                "password": stu.password,
                "hoshmand": stu.hoshmand_access,
                "FR": stu.fr_access,
                "AG": stu.ag_access,
                "hoshmand_limit": stu.hoshmand_limit,
                "fr_limit": stu.fr_limit,
                "con_id": stu.con_id,
                "con_name": con_name,
                "finalized": stu.finalized,
                "rank": stu.rank,
                "field": stu.field,
            }
            stu_data.append(s)

        token = str(uuid.uuid4())
        return token, stu_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_ins_student",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_ins_student_pf(conn, cursor, order_data, info):
    try:
        if order_data["kind"] == 0:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field, con_id FROM stu WHERE ins_id = ? order by created_time desc'
        elif order_data["kind"] == 1:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field, con_id FROM stu WHERE ins_id = ? and hoshmand_access = 1 order by created_time desc'
        elif order_data["kind"] == 2:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field, con_id FROM stu WHERE ins_id = ? and fr_access = 1 order by created_time desc'
        else:
            return None, None
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        stu_data = []
        if len(res_stu) == 0:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
            query = 'SELECT first_name, last_name FROM con WHERE user_id = ?'
            res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(stu.con_id,))
            con_name = ""
            if res_con and len(res_con) >= 2:
                con_name = f"{res_con.first_name} {res_con.last_name}"
            s = {"name": stu.first_name + " " + stu.last_name, "user_id": stu.user_id, "hoshmand": stu.hoshmand_access,
                 "FR": stu.fr_access, "finalized": stu.finalized, "con_finalized": stu.con_finalized,
                 "field": stu.field, "con_name": con_name, }
            stu_data.append(s)
        token = str(uuid.uuid4())
        return token, stu_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_ins_student_pf",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def update_ins_con(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "con", ['first_name', 'last_name', 'sex', 'editor_id', 'edited_time'],
            [order_data["first_name"], order_data["last_name"], order_data["sex"],
             info["user_id"],
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(order_data["consultant_id"])]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "اطلاعات مشاور با موفقیت تغییر یافت."
        else:
            return None, "اطلاعات کاربر تغییر نیافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_con",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def update_ins_stu_con(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "stu", ['con_id', 'gl_limit', 'glf_limit', 'fr_limit', 'editor_id', 'edited_time'],
            [order_data["con_id"], order_data["gl_limit"], order_data["glf_limit"], order_data["fr_limit"],
             info["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [order_data["stu_id"]]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "اطلاعات مشاور دانش‌آموز با موفقیت تغییر یافت."
        else:
            return None, "اطلاعات کاربر تغییر نیافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "update_ins_stu_con",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "اطلاعات کاربر تغییر نیافت."


def select_ins_report_pf(conn, cursor, order_data, info):
    try:
        query = 'SELECT user_id, phone, first_name, last_name, field, con_id, ag_pdf, ag_pf FROM stu WHERE ins_id = ? and ag_access = 1 order by created_time desc'
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        stu_data = []
        if len(res_stu) == 0:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
            query = 'SELECT first_name, last_name FROM con WHERE user_id = ?'
            res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(stu.con_id,))
            con_name = ""
            if res_con and len(res_con) >= 2:
                con_name = f"{res_con.first_name} {res_con.last_name}"
            s = {"name": stu.first_name + " " + stu.last_name, "user_id": stu.user_id, "field": stu.field,
                 "phone": stu.phone, "con_name": con_name, "AGAccess": stu.ag_pf, "AGPDF": stu.ag_pdf}
            stu_data.append(s)
        token = str(uuid.uuid4())
        return token, stu_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/ins", "select_ins_report_pf",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None
