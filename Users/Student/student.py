import uuid
import json
from datetime import datetime

from Helper import db_helper
from Helper.func_helper import password_format_check


def select_student_info(conn, cursor, user_id):
    try:
        query = 'SELECT stu_id, phone, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized, hoshmand_access, fr_access, ins_id, con_id FROM stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
        query = 'SELECT name, logo FROM ins WHERE user_id = ?'
        res_ins = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.ins_id)
        query = 'SELECT first_name, last_name, user_id FROM con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.con_id)
        token = str(uuid.uuid4())
        if not res:
            return token, None
        student_info = {
            "role": "stu",
            "stu_id": res.stu_id,
            "user_id": user_id,
            "phone": res.phone,
            "first_name": res.first_name,
            "last_name": res.last_name,
            "sex": res.sex,
            "city": res.city,
            "birth_date": res.birth_date,
            "field": res.field,
            "quota": res.quota,
            "full_number": res.full_number,
            "rank": res.rank,
            "rank_all": res.rank_all,
            "last_rank": res.last_rank,
            "rank_zaban": res.rank_zaban,
            "full_number_zaban": res.full_number_zaban,
            "rank_all_zaban": res.rank_all_zaban,
            "rank_honar": res.rank_honar,
            "full_number_honar": res.full_number_honar,
            "rank_all_honar": res.rank_all_honar,
            "lock": res.lock,
            "finalized": res.finalized,
            "hoshmand_access": res.hoshmand_access,
            "fr_access": res.fr_access,
            "ins_id": res.ins_id,
            "con_id": res.con_id,
            "name": res_ins.name,
            "con_name": res_con.first_name + " " + res_con.last_name,
            "pic": res_ins.logo,
        }

        return token, student_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            user_id, None, "bbc_api/stu", "select_student_info",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_student_info_ag(conn, cursor, user_id):
    try:
        query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, rank, lock, finalized, ag_access, ag_pdf, ag_pf FROM stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
        token = str(uuid.uuid4())
        if not res:
            return token, None
        student_info = {
            "role": "stu",
            "stu_id": res.stu_id,
            "user_id": user_id,
            "first_name": res.first_name,
            "last_name": res.last_name,
            "sex": res.sex,
            "city": res.city,
            "birth_date": res.birth_date,
            "field": res.field,
            "quota": res.quota,
            "rank": res.rank,
            "lock": res.lock,
            "finalized": res.finalized,
            "ag_pdf": res.ag_pdf,
            "ag_access": res.ag_access,
            "ag_pf": res.ag_pf,
        }
        return token, student_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            user_id, None, "bbc_api/stu", "select_student_info",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_student_data(conn, cursor, order_data, info):
    try:
        query = '''
            SELECT user_id, first_name, last_name, phone, sex, city, birth_date, field, quota, full_number,
                   rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar,
                   full_number_honar, rank_all_honar, hoshmand_access, fr_access, ag_access, fr_limit, hoshmand_limit, finalized
            FROM stu
            WHERE user_id = ?
            ORDER BY created_time DESC
        '''
        res_stu = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=(order_data["stu_id"],))
        token = str(uuid.uuid4())
        if not res_stu:
            return token, {}
        else:
            s = {
                "name": f"{res_stu.first_name} {res_stu.last_name}",
                "first_name": res_stu.first_name,
                "last_name": res_stu.last_name,
                "user_id": order_data["stu_id"],
                "phone": res_stu.phone,
                "sex": res_stu.sex,
                "city": res_stu.city,
                "birth_date": res_stu.birth_date,
                "field": res_stu.field,
                "quota": res_stu.quota,
                "full_number": res_stu.full_number,
                "rank": res_stu.rank,
                "rank_all": res_stu.rank_all,
                "last_rank": res_stu.last_rank,
                "rank_zaban": res_stu.rank_zaban,
                "full_number_zaban": res_stu.full_number_zaban,
                "rank_all_zaban": res_stu.rank_all_zaban,
                "rank_honar": res_stu.rank_honar,
                "full_number_honar": res_stu.full_number_honar,
                "rank_all_honar": res_stu.rank_all_honar,
                "hoshmand": res_stu.hoshmand_access,
                "FR": res_stu.fr_access,
                "AG": res_stu.ag_access,
                "finalized": res_stu.finalized,
                "hoshmand_limit": res_stu.hoshmand_limit,
                "fr_limit": res_stu.fr_limit,
            }
            return token, s
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "select_student_data",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_stu_fp_info(conn, cursor, order_data, info):
    try:
        query = '''
                    SELECT user_id, first_name, last_name, phone, sex, city, birth_date, field, quota, full_number, 
                       rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar,
                       full_number_honar, rank_all_honar, finalized, ins_id, ag_pf
                    FROM stu 
                    WHERE user_id = ?
                       '''
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        query = 'SELECT probability_permission FROM ins WHERE user_id = ?'
        res_ins = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.ins_id)
        probability_show = res_ins.probability_permission
        token = str(uuid.uuid4())
        stu_info = {"first_name": res.first_name, 'last_name': res.last_name, 'sex': res.sex,
                    'birth_date': res.birth_date, 'city': res.city,
                    'field': res.field, 'quota': res.quota,
                    'full_number': res.full_number, 'rank': res.rank,
                    'rank_all': res.rank_all, 'last_rank': res.last_rank, 'finalized': res.finalized,
                    'rank_zaban': res.rank_zaban, 'full_number_zaban': res.full_number_zaban,
                    'rank_all_zaban': res.rank_all_zaban, 'rank_honar': res.rank_honar,
                    'full_number_honar': res.full_number_honar, 'rank_all_honar': res.rank_all_honar,
                    "probability_show": probability_show,
                    "AGAccess": res.ag_pf}
        return token, stu_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "select_stu_fp_info",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def select_stu_fp_field(conn, cursor, order_data, info):
    try:
        query = '''
                    SELECT user_id, first_name, last_name, phone, sex, city, birth_date, field, quota, full_number, 
                       rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar,
                       full_number_honar, rank_all_honar, finalized, ins_id, con_id, con_finalized, ag_pf
                    FROM stu 
                    WHERE user_id = ?
                       '''
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        query = 'SELECT user_id, first_name, last_name FROM con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.con_id)
        query = 'SELECT name, probability_permission FROM ins WHERE user_id = ?'
        res_ins = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.ins_id)
        con_name = ""
        if res_con and len(res_con) >= 3:
            con_name = f"{res_con.first_name} {res_con.last_name}"
        token = str(uuid.uuid4())
        stu_info = {"first_name": res.first_name, 'last_name': res.last_name, 'sex': res.sex,
                    'birth_date': res.birth_date, 'city': res.city,
                    'field': res.field, 'quota': res.quota,
                    'full_number': res.full_number, 'rank': res.rank,
                    'rank_all': res.rank_all, 'last_rank': res.last_rank, 'finalized': res.finalized,
                    'rank_zaban': res.rank_zaban, 'full_number_zaban': res.full_number_zaban,
                    'rank_all_zaban': res.rank_all_zaban, 'rank_honar': res.rank_honar,
                    'full_number_honar': res.full_number_honar, 'rank_all_honar': res.rank_all_honar,
                    "institute_name": res_ins.name, "c_id": res_con.user_id,
                    "c_name": con_name, "con_finalized": res.con_finalized,
                    "probability_show": res_ins.probability_permission,
                    "AGAccess": res.ag_pf}
        return token, stu_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "select_stu_fp_field",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, None


def update_stu_user_profile(conn, cursor, order_data, info):
    try:
        row_count = db_helper.update_record(
            conn, cursor, "stu", ['first_name', 'last_name', 'edited_time'],
            [order_data["first_name"], order_data["last_name"],
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(info["user_id"])]
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
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "update_stu_user_profile",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده", None


def update_stu_password(conn, cursor, order_data, info):
    try:
        val, message = password_format_check(order_data["password"])
        if order_data["password"] != order_data["re_password"]:
            return None, "رمز عبور و تکرار رمز عبور باهم تطابق ندارد."
        if not val:
            return None, message
        db_helper.update_record(
            conn, cursor, "users", ["password", "edited_time"], [
                order_data["password"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ], "user_id = ?", [str(info["user_id"])]
        )
        db_helper.update_record(
            conn, cursor, "stu", ["password", "edited_time"], [
                order_data["password"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ], "user_id = ?", [str(info["user_id"])]
        )
        token = str(uuid.uuid4())
        return token, "رمز عبور شما با موفقیت تغییر کرد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "update_stu_password",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده"


def update_stu_info(conn, cursor, order_data, info, finalized):
    try:
        query = 'SELECT finalized FROM stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        update_finalized = finalized
        if res.finalized == 0:
            update_finalized = 1
        else:
            update_finalized = 2
        row_count = db_helper.update_record(
            conn, cursor, "stu",
            ['first_name', 'last_name', 'sex', 'city', 'birth_date', 'field', 'quota', 'full_number',
             'rank', 'rank_all', 'last_rank', 'rank_zaban', 'full_number_zaban', 'rank_all_zaban',
             'rank_honar', 'full_number_honar', 'rank_all_honar', 'finalized', 'edited_time'],
            [order_data["first_name"], order_data["last_name"], order_data["sex"], order_data["city"],
             order_data["birth_date"], order_data["field"], order_data["quota"],
             order_data["full_number"], order_data["rank"], order_data["rank_all"],
             order_data["last_rank"], order_data["rank_zaban"], order_data["full_number_zaban"],
             order_data["rank_all_zaban"], order_data["rank_honar"], order_data["full_number_honar"],
             order_data["rank_all_honar"], update_finalized, datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?",
            [str(order_data["stu_id"])]
        )
        if row_count > 0:
            token = str(uuid.uuid4())
            return token, "اطلاعات با موفقیت تغییر یافت.", update_finalized
        else:
            return None, "اطلاعات کاربر تغییر نیافت.", finalized
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "bbc_api/stu", "update_stu_info",
            json.dumps(order_data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده", finalized

#
# def update_user_stu_pic(conn, cursor, order_data):
#     method_type = "UPDATE"
#     db_helper.update_record(
#         conn, cursor, "stu", ['first_name', 'last_name', 'logo', 'edited_time'],
#         [order_data["first_name"], order_data["last_name"], order_data["pic"],
#          datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(order_data["user_id"])]
#     )
#     token = str(uuid.uuid4())
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"data": {"first_name": order_data["first_name"], "last_name": order_data["last_name"],
#                                   "pic": order_data["pic"]},
#                          "message": "اطلاعات شما با موفقیت تغییر یافت."}}
#
#
# def select_student_login(conn, cursor, user_id):
#     query = 'SELECT stu_id, first_name, last_name, sex, city, sch_name, birth_date, logo, lock FROM stu WHERE user_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
#     token = str(uuid.uuid4())
#     return token, res[0], res[1], res[2], res[3], res[4], res[6], res[7], res[5], res[8]
#
#
# def select_student_fast_info(conn, cursor, info):
#     query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized FROM stu WHERE user_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
#     token = str(uuid.uuid4())
#     if not res:
#         return token, None
#
#     student_info = {
#         "stu_id": res[0],
#         "user_id": info["user_id"],
#         "first_name": res[1],
#         "last_name": res[2],
#         "sex": res[3],
#         "city": res[4],
#         "birth_date": res[5],
#         "field": res[6],
#         "quota": res[7],
#         "full_number": res[8],
#         "rank": res[9],
#         "rank_all": res[10],
#         "last_rank": res[11],
#         "rank_zaban": res[12],
#         "full_number_zaban": res[13],
#         "rank_all_zaban": res[14],
#         "rank_honar": res[15],
#         "full_number_honar": res[16],
#         "rank_all_honar": res[17],
#         "lock": res[18],
#         "finalized": res[19]
#     }
#
#     query_sp = 'SELECT special_list FROM sp_list WHERE user_id = ?'
#     res_sp = db_helper.search_table(conn=conn, cursor=cursor, query=query_sp, field=info["user_id"])
#     sp = []
#     if res_sp:
#         sp = json.loads(res_sp[0])
#     query_pick = 'SELECT pick_list FROM pick_list WHERE user_id = ?'
#     res_pick = db_helper.search_table(conn=conn, cursor=cursor, query=query_pick, field=info["user_id"])
#     pick = []
#     if res_pick:
#         pick = json.loads(res_pick[0])
#
#     return token, student_info, sp, pick
