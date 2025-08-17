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
        query = 'SELECT glu, gla, fru, fra, agu, aga, glfu, glfa FROM capacity WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res_con.ins_id)
        token = str(uuid.uuid4())
        cons_info = {"GLU": res[0], "GLA": res[1], "FRU": res[2], "FRA": res[3], "AGU": res[4], "AGA": res[5],
                     "GLFU": res[6], "GLFA": res[7], }
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
                   hoshmand_access, fr_access, finalized, fr_limit, hoshmand_limit
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
                "fr_access": stu.fr_access,
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
#
# def select_con_student_data(conn, cursor, order_data, info):
#     query = '''
#             SELECT user_id, first_name, last_name, phone, sex, city, birth_date, field, quota, full_number,
#                    rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar,
#                    full_number_honar, rank_all_honar, gl_access, fr_access, ag_access, finalized, con_id, gl_limit, glf_limit, fr_limit, glf_access
#             FROM stu
#             WHERE user_id = ?
#             ORDER BY created_time DESC
#         '''
#     res_stu = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(order_data["stu_id"],))
#     if not res_stu:
#         token = str(uuid.uuid4())
#         return token, stu_data, ""
#     else:
#         if res_stu[23] == info["user_id"]:
#             token = str(uuid.uuid4())
#             s = {
#                 "name": f"{res_stu[1]} {res_stu[2]}",
#                 "user_id": res_stu[0],
#                 "phone": res_stu[3],
#                 "sex": res_stu[4],
#                 "city": res_stu[5],
#                 "birth_date": res_stu[6],
#                 "field": res_stu[7],
#                 "quota": res_stu[8],
#                 "full_number": res_stu[9],
#                 "rank": res_stu[10],
#                 "rank_all": res_stu[11],
#                 "last_rank": res_stu[12],
#                 "rank_zaban": res_stu[13],
#                 "full_number_zaban": res_stu[14],
#                 "rank_all_zaban": res_stu[15],
#                 "rank_honar": res_stu[16],
#                 "full_number_honar": res_stu[17],
#                 "rank_all_honar": res_stu[18],
#                 "GL": res_stu[19],
#                 "FR": res_stu[20],
#                 "AG": res_stu[21],
#                 "GLF": res_stu[27],
#                 "finalized": res_stu[22],
#                 "gl_limit": res_stu[24],
#                 "glf_limit": res_stu[25],
#                 "fr_limit": res_stu[26],
#             }
#             return token, s, ""
#         else:
#             return None, None, "اطلاعات دانش‌آموز و مشاور هم‌خواتی تدارد."
#
#
#
#

#
# def update_con_stu(conn, cursor, order_data, info):
#     query = 'SELECT con_id, finalized FROM stu WHERE user_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
#     if res[0] == info["user_id"]:
#         if res[1] == 0:
#             finalized = 1
#         else:
#             finalized = 2
#         db_helper.update_record(
#             conn, cursor, "stu",
#             ["sex", "birth_date", "city", "field", "quota", "full_number", "rank", "rank_all", "last_rank",
#              "rank_zaban", "full_number_zaban", "rank_all_zaban", "rank_honar", "full_number_honar", "rank_all_honar",
#              "finalized", "editor_id", "edited_time"], [
#                 order_data["sex"],
#                 order_data["birth_date"], order_data["province"], order_data["field"], order_data["quota"],
#                 order_data["full_number"], order_data["rank"], order_data["rank_all"],
#                 order_data["last_rank"], order_data["rank_zaban"], order_data["full_number_zaban"],
#                 order_data["rank_all_zaban"], order_data["rank_honar"], order_data["full_number_honar"],
#                 order_data["rank_all_honar"], finalized, info["user_id"],
#                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             ], "user_id = ?", [str(order_data["stu_id"])]
#         )
#         token = str(uuid.uuid4())
#         return token, "اطلاعات دانش‌آموز نهایی شد.", finalized
#     else:
#         return None, "اطلاعات دانش‌آموز و مشاور هم‌خواتی تدارد.", res[1]
#
#
# def insert_con_stu(conn, cursor, order_data, user_id, password, phone):
#     field = '([user_id], [phone], [first_name], [last_name], [national_id], [sex], [ins_id], [hCon_id], [con_id], [password], [birth_date], [city], [field], [quota], [full_number], [rank], [rank_all], [last_rank], [rank_zaban], [full_number_zaban], [rank_all_zaban], [rank_honar], [full_number_honar], [rank_all_honar], [haveGL], [haveFR], [haveAG], [finalized], [hCon_finalized], [con_finalized], [adder_id], [editor_id], [DC_Created_Time], [DC_Edited_Time])'
#     values = (user_id, phone, order_data["first_name"], order_data["last_name"], order_data["national_id"],
#               int(order_data["sex"]), order_data["ins_id"], order_data["hCon_id"], order_data["user_id"],
#               password, order_data["birth_date"], order_data["province"], int(order_data["field"]),
#               int(order_data["quota"]), int(order_data["full_number"]),
#               int(order_data["rank"]), int(order_data["rank_all"]), int(order_data["last_rank"]),
#               int(order_data["rank_zaban"]), int(order_data["full_number_zaban"]),
#               int(order_data["rank_all_zaban"]), int(order_data["rank_honar"]), int(order_data["full_number_honar"]),
#               int(order_data["rank_all_honar"]), order_data["GL"],
#               order_data["FR"], order_data["AG"], 0, 0, 0, order_data["user_id"], order_data["user_id"],
#               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#               datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
#     res_add_stu = db_helper.insert_value(conn=conn, cursor=cursor, table_name="stu", fields=field,
#                                          values=values)
#     query_cap = 'SELECT * FROM capacity WHERE user_id = ?'
#     res_cap = db_helper.search_table(conn=conn, cursor=cursor, query=query_cap, field=order_data["ins_id"])
#     query_cap = 'SELECT * FROM capacity WHERE user_id = ?'
#     res_cap = db_helper.search_table(conn=conn, cursor=cursor, query=query_cap, field=order_data["ins_id"])
#     GLA = int(res_cap[4])
#     GLU = int(res_cap[3])
#     FRA = int(res_cap[6])
#     FRU = int(res_cap[5])
#     AGA = int(res_cap[8])
#     AGU = int(res_cap[7])
#     if order_data["GL"] != 0:
#         GLA = GLA - 1
#         GLU = GLU + 1
#     if order_data["FR"] != 0:
#         FRA = FRA - 1
#         FRU = FRU + 1
#     if order_data["AG"] != 0:
#         AGA = AGA - 1
#         AGU = AGU + 1
#     db_helper.update_record(conn, cursor, 'capacity',
#                             ['GLU', 'GLA', 'FRU', 'FRA', 'AGU', 'AGA'],
#                             [GLU, GLA, FRU, FRA, AGU, AGA],
#                             'user_id = ' + str(order_data["ins_id"]))
#     conn.commit()
#     token = str(uuid.uuid4())
#     return token
#
#
# def update_con_stu_finilize(conn, cursor, order_data):
#     query = 'SELECT * FROM stu WHERE national_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["national_id"])
#     db_helper.update_record(conn, cursor, 'stu',
#                             ['first_name', 'last_name', 'sex', 'birth_date', 'city',
#                              'field', 'quota', 'full_number', 'rank', 'rank_all', 'last_rank',
#                              'rank_zaban', 'rank_all_zaban', 'full_number_zaban', 'rank_honar', 'rank_all_honar',
#                              'full_number_honar', 'finalized', 'editor_id'],
#                             [order_data["first_name"], order_data["last_name"], order_data["sex"],
#                              order_data["birth_date"],
#                              order_data["province"], order_data["field"], order_data["quota"],
#                              order_data["full_number"], order_data["rank"], order_data["rank_all"],
#                              order_data["last_rank"], order_data["rank_zaban"], order_data["rank_all_zaban"],
#                              order_data["full_number_zaban"], order_data["rank_honar"], order_data["rank_all_honar"],
#                              order_data["full_number_honar"], 1, order_data["user_id"]],
#                             'user_id = ' + str(res[1]))
#     token = str(uuid.uuid4())
#     return token
#
#
# def update_con_stu_pf_finalize(conn, cursor, order_data, info):
#     query = 'SELECT con_id, con_finalized FROM stu WHERE user_id = ?'
#     res_stu = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
#     if info["user_id"] != res_stu[0]:
#         return None, "شما مشاور این دانش‌آموز نیستد."
#     if res_stu[1] == 1:
#         return None, "دانش‌آموز شما قبلا توسط شما تایید شده است."
#     row_count = db_helper.update_record(
#         conn, cursor, "stu", ['con_finalized', 'editor_id', 'edited_time'],
#         [1, info["user_id"],
#          datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(order_data["stu_id"])]
#     )
#     if row_count > 0:
#         token = str(uuid.uuid4())
#         return token, "دانش‌آموز شما تایید نهایی شد."
#     else:
#         return None, "اطلاعات کاربر تغییر نیافت."
