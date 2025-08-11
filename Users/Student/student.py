import json
import uuid
import redis
from datetime import datetime
from Helper import db_helper
from Helper.func_helper import password_format_check


def insert_student(conn, cursor, order_data, user_id):
    field = '([user_id], [code], [phone])'
    values = (
        user_id, order_data["referral_code"], order_data["phone"],)
    res_add_stu = db_helper.insert_value(conn=conn, cursor=cursor, table_name="referral_code", fields=field,
                                         values=values)
    field = '([user_id], [first_name], [last_name], [phone], [password], [sex], [city], [birth_date])'
    values = (
        user_id, order_data["first_name"], order_data["last_name"], order_data["phone"],
        order_data["password"], order_data["sex"], order_data["city"], order_data["birth_date"],)
    res_add_stu = db_helper.insert_value(conn=conn, cursor=cursor, table_name="stu", fields=field,
                                         values=values)
    token = str(uuid.uuid4())
    return token


def select_student_login(conn, cursor, user_id):
    query = 'SELECT stu_id, first_name, last_name, sex, city, sch_name, birth_date, logo, lock FROM ERS.dbo.stu WHERE user_id = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
    token = str(uuid.uuid4())
    return token, res[0], res[1], res[2], res[3], res[4], res[6], res[7], res[5], res[8]


def select_student_info(conn, cursor, info):
    query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized, gl_access, glf_access, fr_access, sp_access FROM ERS.dbo.stu WHERE user_id = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
    token = str(uuid.uuid4())
    if not res:
        return token, None, "اطلاعات یافت نشد."

    student_info = {
        "stu_id": res[0],
        "user_id": info["user_id"],
        "first_name": res[1],
        "last_name": res[2],
        "sex": res[3],
        "city": res[4],
        "birth_date": res[5],
        "field": res[6],
        "quota": res[7],
        "full_number": res[8],
        "rank": res[9],
        "rank_all": res[10],
        "last_rank": res[11],
        "rank_zaban": res[12],
        "full_number_zaban": res[13],
        "rank_all_zaban": res[14],
        "rank_honar": res[15],
        "full_number_honar": res[16],
        "rank_all_honar": res[17],
        "lock": res[18],
        "finalized": res[19],
        "gl_access": res[20],
        "glf_access": res[21],
        "fr_access": res[22],
        "sp_access": res[23],
    }

    return token, student_info, ""


def update_stu_user_profile(conn, cursor, order_data, info):
    db_helper.update_record(
        conn, cursor, "stu", ['first_name', 'last_name', 'edited_time'],
        [order_data["first_name"], order_data["last_name"],
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(info["user_id"])]
    )
    token = str(uuid.uuid4())
    return token, {"first_name": order_data["first_name"], "last_name": order_data["last_name"]}


def update_stu_info(conn, cursor, order_data, info, finalized):
    db_helper.update_record(
        conn, cursor, "stu", ['first_name', 'last_name', 'sex', 'city', 'birth_date', 'field', 'quota', 'full_number',
                              'rank', 'rank_all', 'last_rank', 'rank_zaban', 'full_number_zaban', 'rank_all_zaban',
                              'rank_honar', 'full_number_honar', 'rank_all_honar', 'finalized', 'edited_time'],
        [order_data["first_name"], order_data["last_name"], order_data["sex"], order_data["city"],
         order_data["birth_date"], order_data["field"], order_data["quota"],
         order_data["full_number"], order_data["rank"], order_data["rank_all"],
         order_data["last_rank"], order_data["rank_zaban"], order_data["full_number_zaban"],
         order_data["rank_all_zaban"], order_data["rank_honar"], order_data["full_number_honar"],
         order_data["rank_all_honar"], finalized, datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?",
        [str(info["user_id"])]
    )
    token = str(uuid.uuid4())
    return token


def update_user_stu_pic(conn, cursor, order_data):
    method_type = "UPDATE"
    db_helper.update_record(
        conn, cursor, "stu", ['first_name', 'last_name', 'logo', 'edited_time'],
        [order_data["first_name"], order_data["last_name"], order_data["pic"],
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ?", [str(order_data["user_id"])]
    )
    token = str(uuid.uuid4())
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"data": {"first_name": order_data["first_name"], "last_name": order_data["last_name"],
                                  "pic": order_data["pic"]},
                         "message": "اطلاعات شما با موفقیت تغییر یافت."}}


def update_stu_password(conn, cursor, order_data, info):
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


def select_student_fast_info(conn, cursor, info):
    query = 'SELECT stu_id, first_name, last_name, sex, city, birth_date, field, quota, full_number, rank, rank_all, last_rank, rank_zaban, full_number_zaban, rank_all_zaban, rank_honar, full_number_honar, rank_all_honar, lock, finalized FROM ERS.dbo.stu WHERE user_id = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
    token = str(uuid.uuid4())
    if not res:
        return token, None

    student_info = {
        "stu_id": res[0],
        "user_id": info["user_id"],
        "first_name": res[1],
        "last_name": res[2],
        "sex": res[3],
        "city": res[4],
        "birth_date": res[5],
        "field": res[6],
        "quota": res[7],
        "full_number": res[8],
        "rank": res[9],
        "rank_all": res[10],
        "last_rank": res[11],
        "rank_zaban": res[12],
        "full_number_zaban": res[13],
        "rank_all_zaban": res[14],
        "rank_honar": res[15],
        "full_number_honar": res[16],
        "rank_all_honar": res[17],
        "lock": res[18],
        "finalized": res[19]
    }

    query_sp = 'SELECT special_list FROM ERS.dbo.sp_list WHERE user_id = ?'
    res_sp = db_helper.search_table(conn=conn, cursor=cursor, query=query_sp, field=info["user_id"])
    sp = []
    if res_sp:
        sp = json.loads(res_sp[0])
    query_pick = 'SELECT pick_list FROM ERS.dbo.pick_list WHERE user_id = ?'
    res_pick = db_helper.search_table(conn=conn, cursor=cursor, query=query_pick, field=info["user_id"])
    pick = []
    if res_pick:
        pick = json.loads(res_pick[0])

    return token, student_info, sp, pick
