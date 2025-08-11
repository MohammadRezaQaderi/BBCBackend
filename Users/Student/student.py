import uuid
from datetime import datetime
from Helper import db_helper
from Helper.func_helper import password_format_check


def select_student_info(conn, cursor, user_id):
    try:
        query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized, hoshmand_access, fr_access, ins_id, con_id FROM BBC.dbo.stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
        query = 'SELECT name, logo FROM BBC.dbo.ins WHERE user_id = ?'
        res_ins = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.ins_id)
        query = 'SELECT first_name, last_name, user_id FROM BBC.dbo.con WHERE user_id = ?'
        res_con = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=res.con_id)
        token = str(uuid.uuid4())
        if not res:
            return token, None
        student_info = {
            "stu_id": res.stu_id,
            "user_id": user_id,
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
        print(">>>> student select_info error", e)
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            user_id, None, "select_student_info", "bbc_api",
            None, None, str(e))
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
        print(">>>> stu update_stu_user_profile error", e)
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.user_id, None, "select_student_info", "bbc_api",
            None, None, str(e))
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
        print(">>>> stu update_stu_password error", e)
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.user_id, None, "update_stu_password", "bbc_api",
            None, None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در تغییر اطلاعات پیش آمده"

# def update_stu_info(conn, cursor, order_data, info, finalized):
#     db_helper.update_record(
#         conn, cursor, "stu", ['first_name', 'last_name', 'sex', 'city', 'birth_date', 'field', 'quota', 'full_number',
#                               'rank', 'rank_all', 'last_rank', 'rank_zaban', 'full_number_zaban', 'rank_all_zaban',
#                               'rank_honar', 'full_number_honar', 'rank_all_honar', 'finalized', 'edited_time'],
#         [order_data["first_name"], order_data["last_name"], order_data["sex"], order_data["city"],
#          order_data["birth_date"], order_data["field"], order_data["quota"],
#          order_data["full_number"], order_data["rank"], order_data["rank_all"],
#          order_data["last_rank"], order_data["rank_zaban"], order_data["full_number_zaban"],
#          order_data["rank_all_zaban"], order_data["rank_honar"], order_data["full_number_honar"],
#          order_data["rank_all_honar"], finalized, datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?",
#         [str(info["user_id"])]
#     )
#     token = str(uuid.uuid4())
#     return token
#
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
#     query = 'SELECT stu_id, first_name, last_name, sex, city, sch_name, birth_date, logo, lock FROM BBC.dbo.stu WHERE user_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
#     token = str(uuid.uuid4())
#     return token, res[0], res[1], res[2], res[3], res[4], res[6], res[7], res[5], res[8]
#
#
# def select_student_fast_info(conn, cursor, info):
#     query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized FROM BBC.dbo.stu WHERE user_id = ?'
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
#     query_sp = 'SELECT special_list FROM BBC.dbo.sp_list WHERE user_id = ?'
#     res_sp = db_helper.search_table(conn=conn, cursor=cursor, query=query_sp, field=info["user_id"])
#     sp = []
#     if res_sp:
#         sp = json.loads(res_sp[0])
#     query_pick = 'SELECT pick_list FROM BBC.dbo.pick_list WHERE user_id = ?'
#     res_pick = db_helper.search_table(conn=conn, cursor=cursor, query=query_pick, field=info["user_id"])
#     pick = []
#     if res_pick:
#         pick = json.loads(res_pick[0])
#
#     return token, student_info, sp, pick
