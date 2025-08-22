import uuid
import json
from datetime import datetime

from Helper import db_helper
from Helper.func_helper import password_format_check, random_phone_number, id_generator


def select_con_info(conn, cursor, user_id):
    try:
        query = 'SELECT con_id, phone, first_name, last_name, sex, ins_id FROM con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
        query = 'SELECT name, logo FROM ins WHERE user_id = ?'
        res_ins = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res_con.ins_id)
        token = str(uuid.uuid4())
        info = {"phone": res_con.phone, "user_id": user_id, "id": res_con.con_id, "first_name": res_con.first_name,
                "last_name": res_con.last_name, "role": "con", "name": res_ins.name, "sex": res_con.sex,
                "ins_id": res_con.ins_id, "pic": res_ins.logo}
        return token, info
    except Exception as e:
        print(">>>> con select_info error", e)
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            user_id, None, "bbc_api/con", "select_con_info",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def insert_con_stu(conn, cursor, order_data, info):
    try:
        phone = random_phone_number(conn, cursor, 8)
        password = id_generator()
        field = '([phone], [password], [role])'
        values = (phone, password, 'stu',)
        res_add_user = db_helper.insert_value(conn=conn, cursor=cursor, table_name="users", fields=field,
                                              values=values)
        query = 'SELECT user_id FROM users WHERE phone = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
        query = 'SELECT ins_id FROM con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if res_con is None:
            return None, "اطلاعات دریافتی مشاور شما مشکل دارد."
        # todo here check the hcon id is exist and for this ins
        field = '([user_id], [phone], [first_name], [last_name], [sex], [birth_date], [city], [field], [quota], [ins_id], [con_id], [password], [adder_id], [editor_id])'
        values = (
            res_user[0], phone, order_data["first_name"], order_data["last_name"],
            order_data["sex"], order_data["birth_date"], order_data["province"], int(order_data["field"]),
            int(order_data["quota"]), res_con.ins_id, info["user_id"], password,
            info["user_id"], info["user_id"],)
        res_add_stu = db_helper.insert_value(conn=conn, cursor=cursor, table_name="stu", fields=field,
                                             values=values)
        token = str(uuid.uuid4())
        return token, "دانش‌آموز با موفقیت اضافه شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/con", "insert_con_stu",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در افزودن دانش‌آموز پیش آمده"


def update_con_user_profile(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "con", ['first_name', 'last_name', 'edited_time'],
            [order_data["first_name"], order_data["last_name"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [info["user_id"]]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "اطلاعات با موفقیت تغییر یافت.", {"first_name": order_data["first_name"],
                                                            "last_name": order_data["last_name"]}
        else:
            return None, "اطلاعات کاربر تغییر نیافت.", None
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/con", "update_con_user_profile",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده", None


def update_con_password(conn, cursor, order_data, info):
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
            conn, cursor, "con", ['password', 'edited_time'],
            [order_data["password"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [info["user_id"]]
        )
        token = str(uuid.uuid4())
        return token, "رمز عبور شما با موفقیت تغییر کرد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/con", "update_con_password",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده"


def select_con_dashboard(conn, cursor, order_data, info):
    try:
        query = 'SELECT ins_id FROM con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        ins_cap_query = 'SELECT hu, ha, fru, fra, agu, aga FROM capacity WHERE user_id = ?'
        res_cap = db_helper.search_table(conn=conn, cursor=cursor, query=ins_cap_query, field=res_con.ins_id)

        queries = {
            'stu_count': 'SELECT count(*) FROM stu WHERE con_id = ?',
            'con_finalized': 'SELECT count(*) FROM stu WHERE con_id = ? and con_finalized = 1',
            'finish_quiz': 'SELECT count(*) FROM quiz_answer WHERE con_id = ? and quiz_id = 7 and state = 2',
            'started_quiz': 'SELECT count(distinct (user_id)) FROM quiz_answer WHERE con_id = ?',
            'all_can_quiz': 'SELECT count(*) FROM stu WHERE con_id = ? and ag_access = 1'
        }

        results = {}
        for key, query in queries.items():
            results[key] = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])

        token = str(uuid.uuid4())
        cons_info = {
            "HU": res_cap.hu,
            "HA": res_cap.ha,
            "FRU": res_cap.fru,
            "FRA": res_cap.fra,
            "AGU": res_cap.agu,
            "AGA": res_cap.aga,
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
            info.get("user_id"), info.get("phone"), "bbc_api/con", "select_con_dashboard",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_con_student(conn, cursor, order_data, info):
    try:
        query = '''
                SELECT user_id, first_name, last_name, phone, sex, password, rank, field,
                   hoshmand_access, ag_access, fr_access, finalized, fr_limit, hoshmand_limit
                FROM stu
                WHERE con_id = ?
                ORDER BY created_time DESC
            '''
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=(info["user_id"],))
        stu_data = []
        if not res_stu:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
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
            info.get("user_id"), info.get("phone"), "bbc_api/con", "select_con_student",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_con_student_pf(conn, cursor, order_data, info):
    try:
        if order_data["kind"] == 0:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field FROM stu WHERE con_id = ? order by created_time desc'
        elif order_data["kind"] == 1:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field FROM stu WHERE con_id = ? and hoshmand_access = 1 order by created_time desc'
        elif order_data["kind"] == 2:
            query = 'SELECT user_id, first_name, last_name, hoshmand_access, fr_access, finalized, con_finalized, field FROM stu WHERE con_id = ? and fr_access = 1 order by created_time desc'
        else:
            return None, None
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        stu_data = []
        if len(res_stu) == 0:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
            s = {"name": stu.first_name + " " + stu.last_name, "user_id": stu.user_id, "hoshmand": stu.hoshmand_access,
                 "FR": stu.fr_access, "finalized": stu.finalized, "con_finalized": stu.con_finalized,
                 "field": stu.field}
            stu_data.append(s)
        token = str(uuid.uuid4())
        return token, stu_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/con", "select_con_student_pf",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_con_report_pf(conn, cursor, order_data, info):
    try:
        query = 'SELECT user_id, phone, first_name, last_name, field FROM stu WHERE con_id = ? and ag_access = 1 order by created_time desc'
        res_stu = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        stu_data = []
        if len(res_stu) == 0:
            token = str(uuid.uuid4())
            return token, stu_data
        for stu in res_stu:
            s = {"name": stu.first_name + " " + stu.last_name, "user_id": stu.user_id, "field": stu.field,
                 "phone": stu.phone}
            stu_data.append(s)
        token = str(uuid.uuid4())
        return token, stu_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/con", "select_con_report_pf",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None
