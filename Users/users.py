import json
import time
import uuid
from datetime import datetime

from Helper import db_helper
from Users.Auth.auth import check_signin, token_remove
from Users.Consultant.consultant import insert_con_stu, update_con_user_profile, update_con_password, \
    select_con_dashboard, select_con_student
from Users.FieldPick.field_pick import update_spfr, update_trfr, update_spfrb, update_trfrb, get_majors, \
    get_universities, get_cities, get_provinces, get_exam_types, search_fields, get_majors_fr, get_provinces_fr, \
    get_universities_fr, search_fields_fr, get_spfr, get_trfr, get_majors_frb, get_provinces_frb, get_universities_frb, \
    search_fields_frb, get_spfrb, get_trfrb
from Users.Hoshmand.hoshmand import change_hoshmand_info, change_hoshmand_questions, change_hoshmand_examtype, \
    change_hoshmand_major, change_hoshmand_province, change_hoshmand_tables, change_hoshmand_chains, \
    change_hoshmand_fields, change_hoshmand_sp_list, get_hoshmand_questions, get_hoshmand_examtype, get_hoshmand_major, \
    get_hoshmand_province, get_hoshmand_tables, get_hoshmand_chains, get_hoshmand_chain_code, get_hoshmand_fields, \
    get_hoshmand_sp_list, get_hoshmand_list
from Users.Institute.institute import insert_ins_con, insert_ins_stu, update_ins_user_profile, update_ins_password, \
    select_new_ins_dashboard, select_ins_consultant, select_ins_cons_stu, select_ins_student, update_ins_con
from Users.Quiz.quiz import submit_quiz_answer, select_stu_quiz_table_info, select_stu_quiz_info
from Users.Student.student import update_stu_user_profile, update_stu_password, update_stu_info, select_student_data

uni_info = ["دانشگاه‌های شاخص سراسر کشور", "دانشگاه‌های برتر استان(های) بومی", "سایر دانشگاه‌های استان(های) بومی",
            "دانشگاه‌های برتر استان‌های همسایه", "سایر دانشگاه‌های استان‌های همسایه",
            "دانشگاه‌های برتر استان‌های نزدیک", "سایر دانشگاه‌های استان‌های نزدیک",
            "دانشگاه‌های برتر استان‌های با فاصله زیاد", "سایر دانشگاه‌های استان‌های با فاصله زیاد",
            "دانشگاه‌های برتر دیگر استان‌های کشور", "سایر دانشگاه‌های دیگر استان‌های کشور"]
major_info = ["رشته‌های اولویت ۱", "رشته‌های اولویت ۲", "رشته‌های اولویت ۳", "رشته‌های اولویت ۴"]


def check_user_request(conn, cursor, order_data, info):
    if info.get("role") == "ins":
        query = 'SELECT ins_id FROM stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        if res.ins_id != info.get("user_id"):
            return False
    elif info.get("role") == "con":
        query = 'SELECT con_id FROM stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        if res.con_id != info.get("user_id"):
            return False
    else:
        if info.get("user_id") != int(order_data["stu_id"]):
            return False
    return True


def delete_token(conn, cursor, data, info):
    method_type = "DELETE"
    token = str(uuid.uuid4())
    res = token_remove(conn, cursor, data)
    if not res:
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"message": "نشد"}}
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"message": "شد"}}


def signin(conn, cursor, order_data):
    method_type = "SIGNIN"
    tracking_code, message, info = check_signin(conn=conn, cursor=cursor, data=order_data)
    if info is None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": message}
    elif tracking_code:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": info}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "اطلاعات شما در سامانه یافت نشد"}


def add_consultant(conn, cursor, order_data, info):
    method_type = "INSERT"
    if info.get("role") == "ins":
        token, message = insert_ins_con(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


def add_student(conn, cursor, order_data, info):
    method_type = "INSERT"
    if info.get("role") == "ins":
        token, message = insert_ins_stu(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    elif info.get("role") == "con":
        token, message = insert_con_stu(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


def update_user(conn, cursor, order_data, info):
    method_type = "UPDATE"
    if info.get("role") == "ins":
        token, message, data = update_ins_user_profile(conn, cursor, order_data, info)
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"data": data, "message": message}}
        else:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
    elif info.get("role") == "con":
        token, message, data = update_con_user_profile(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"data": data, "message": message}}
        else:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}

    elif info.get("role") == "stu":
        token, message, data = update_stu_user_profile(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"data": data, "message": message}}
        else:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


def update_password(conn, cursor, order_data, info):
    method_type = "UPDATE"
    if info.get("role") == "ins":
        token, message = update_ins_password(conn, cursor, order_data, info)
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"message": message}}
    elif info.get("role") == "con":
        token, message = update_con_password(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"message": message}}
    elif info.get("role") == "stu":
        token, message = update_stu_password(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"message": message}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


def update_student_info(conn, cursor, order_data, info):
    method_type = "UPDATE"
    have_access = check_user_request(conn, cursor, order_data, info)
    if not have_access:
        return {"status": 200, "tracking_code": None, "method_type": method_type, "error": "اطلاعات هم‌خوانی ندارد"}
    if info.get("role") in ["ins", "con", "stu"]:
        token, message, finalized = update_stu_info(conn, cursor, order_data, info, order_data["finalized"])
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message, "finalized": finalized}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


def update_consultant(conn, cursor, order_data, info):
    method_type = "UPDATE"
    if info.get("role") == "ins":
        token, message = update_ins_con(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"message": message}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def student_info(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, dash_info, message = select_student_info(conn, cursor, info)
    if not token:
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "error": message}
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"data": dash_info}}


def new_dash(conn, cursor, order_data, info):
    method_type = "SELECT"
    if info.get("role") == "ins":
        token, dash_info = select_new_ins_dashboard(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"data": dash_info}}
    elif info.get("role") == "con":
        token, dash_info = select_con_dashboard(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"data": dash_info}}
    elif info.get("role") == "stu":
        token, dash_info, finalized = select_stu_dashboard(conn, cursor, order_data)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"data": dash_info, "finalized": finalized}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def select_con_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    if info.get("role") == "ins":
        token, con_info = select_ins_consultant(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"con": con_info}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def select_cons_stu(conn, cursor, order_data, info):
    method_type = "SELECT"
    if info.get("role") == "ins":
        token, con_info = select_ins_cons_stu(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"con": con_info}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def select_stu_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    if info.get("role") == "ins":
        token, stu_info = select_ins_student(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"stu": stu_info}}
    elif info.get("role") == "con":
        token, stu_info = select_con_student(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": token, "method_type": method_type,
                "response": {"stu": stu_info}}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def select_stu_data(conn, cursor, order_data, info):
    method_type = "SELECT"
    have_access = check_user_request(conn, cursor, order_data, info)
    if not have_access:
        return {"status": 200, "tracking_code": None, "method_type": method_type, "error": "اطلاعات هم‌خوانی ندارد"}
    if info.get("role") in ["ins", "con", "stu"]:
        token, data = select_student_data(conn, cursor, order_data, info)
        cursor.close()
        conn.close()
        if token:
            return {"status": 200, "tracking_code": token, "method_type": method_type,
                    "response": {"stu": data}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": message}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "شما به این متد دسترسی ندارید."}


# Field Pick API
def update_spfr_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    tracking_code, message = update_spfr(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": {"message": message}}


def update_trfr_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    tracking_code, message = update_trfr(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": {"message": message}}


def select_spfr_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, data = get_spfr(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": data}


def select_trfr_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, data = get_trfr(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": data}


def update_spfrb_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    tracking_code, message = update_spfrb(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": {"message": message}}


def update_trfrb_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    tracking_code, message = update_trfrb(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": {"message": message}}


def select_spfrb_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, data = get_spfrb(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": data}


def select_trfrb_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, data = get_trfrb(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
            "response": data}


# Global Functionality
def fp_majors(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, majors = get_majors(conn, cursor, order_data, info)
    if majors is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": majors}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fp_universities(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, universities = get_universities(conn, cursor, order_data, info)
    if universities is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": universities}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fp_cities(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, cities = get_cities(conn, cursor, order_data, info)
    if cities is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": cities}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fp_provinces(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, provinces = get_provinces(conn, cursor, order_data, info)
    if provinces is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": provinces}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fp_exam_types(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, exam_types = get_exam_types(conn, cursor, order_data, info)
    if exam_types is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": exam_types}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fp_search_fields(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, fields, message = search_fields(conn, cursor, order_data, info)
    if fields is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": fields}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": message}


# Free Pick Functionality
def fr_majors(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, majors = get_majors_fr(conn, cursor, order_data, info)
    if majors is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": majors}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fr_provinces(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, provinces = get_provinces_fr(conn, cursor, order_data, info)
    if provinces is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": provinces}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fr_universities(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, universities = get_universities_fr(conn, cursor, order_data, info)
    if universities is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": universities}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def fr_search_fields(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, fields, message = search_fields_fr(conn, cursor, order_data, info)
    if fields is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": fields}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": message}


# Free Other Pick Functionality
def frb_majors(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, majors = get_majors_frb(conn, cursor, order_data, info)
    if majors is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": majors}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def frb_provinces(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, provinces = get_provinces_frb(conn, cursor, order_data, info)
    if provinces is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": provinces}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def frb_universities(conn, cursor, order_data, info):
    method_type = "SELECT"
    tracking_code, universities = get_universities_frb(conn, cursor, order_data, info)
    if universities is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": universities}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}


def frb_search_fields(conn, cursor, order_data, info):
    method_type = "SELECT"
    print(method_type)
    tracking_code, fields, message = search_fields_frb(conn, cursor, order_data, info)
    if fields is not None:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
                "response": fields}
    else:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": message}


# Quiz Functionality
def update_quiz_answer(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = submit_quiz_answer(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"message": message}}


def select_quiz_table_info(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, data = select_stu_quiz_table_info(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"data": data}}


def select_quiz_info(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, data, quiz_answers = select_stu_quiz_info(conn, cursor, order_data, info)
    if not data:
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": method_type,
                "error": "آزمون مورد نظر شما در دسترس شما نیست."}
    cursor.close()
    conn.close()
    return {"status": 200, "tracking_code": token, "method_type": method_type,
            "response": {"data": data, "quizAnswers": quiz_answers}}


# Hoshmand Functionality
def update_hoshmand_info(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, data, message = change_hoshmand_info(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "data": data,
            "message": message
        }
    }


def update_hoshmand_questions(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_questions(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_examtype(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_examtype(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_major(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_major(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_province(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_province(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_tables(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_tables(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_chains(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_chains(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_fields(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_fields(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def update_hoshmand_sp_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, message = change_hoshmand_sp_list(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "message": message
        }
    }


def select_hoshmand_info(conn, cursor, data, info):
    method_type = "SELECT"
    token, info = get_hoshmand_info(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": info
    }


def select_hoshmand_questions(conn, cursor, data, info):
    method_type = "SELECT"
    token, info = get_hoshmand_questions(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": info_response
    }


def select_hoshmand_examtype(conn, cursor, data, info):
    method_type = "SELECT"
    token, is_empty, exam_types, user_data = get_hoshmand_examtype(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "is_empty": is_empty,
            "exam_types": exam_types,
            "user_data": user_data,
        }
    }


def select_hoshmand_major(conn, cursor, data, info):
    method_type = "SELECT"
    token, majors, user_data = get_hoshmand_major(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "majors": majors,
            "user_data": user_data,
        }
    }


def select_hoshmand_province(conn, cursor, data, info):
    method_type = "SELECT"
    # todo here returns have error
    token, majors, user_data = get_hoshmand_province(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "majors": majors,
            "user_data": user_data,
        }
    }


def select_hoshmand_tables(conn, cursor, data, info):
    method_type = "SELECT"
    token, skills_table, universities_table, exam_types, lock = get_hoshmand_tables(conn, cursor, data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "skills": skills_table,
            "universities": universities_table,
            "priorities": exam_types,
            "lock": lock,
        }
    }


def select_hoshmand_chains(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, chains, deleted_chains = get_hoshmand_chains(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "chains": chains,
            "hand_chains": [],
            "deleted_chains": deleted_chains,
        }
    }


def select_hoshmand_chain_code(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, fields = get_hoshmand_chain_code(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "data": fields,
        }
    }


def select_hoshmand_fields(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, fields, selected_list, is_hoshmand = get_hoshmand_fields(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "data": fields,
            "selected_list": selected_list,
            "is_hoshmand": is_hoshmand
        }
    }


def select_hoshmand_sp_list(conn, cursor, order_data, info):
    method_type = "SELECT"
    token, trash_list, selected_list, hoshmand_list, dash_info = get_hoshmand_sp_list(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "tracking_code": token,
        "method_type": method_type,
        "response": {
            "trash_list": trash_list,
            "selected_list": selected_list,
            "hoshmand_list": hoshmand_list,
            "user_data": dash_info
        }
    }


def select_hoshmand_list(conn, cursor, order_data, info):
    method_type = "UPDATE"
    token, data, selected_list, is_hoshmand = get_hoshmand_list(conn, cursor, order_data, info)
    cursor.close()
    conn.close()
    return {
        "status": 200,
        "method_type": method_type,
        "response": {
            "data": data,
            "selected_list": selected_list,
            "is_hoshmand": is_hoshmand
        },
        "tracking_code": token
    }

# def update_stu_info(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     if info.get("role") == "ins":
#         token, message, finalized = update_ins_stu(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message, "finalized": finalized}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     if info.get("role") == "oCon":
#         token, message, finalized = update_oCon_stu(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message, "finalized": finalized}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     elif info.get("role") == "hCon":
#         token, message, finalized = update_hCon_stu(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message, "finalized": finalized}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     elif info.get("role") == "con":
#         token, message, finalized = update_con_stu(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message, "finalized": finalized}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}

# def accept_check_user_info(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query = 'SELECT finalized FROM stu WHERE user_id = ?'
#     res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if res is None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "اطلاعات دریافتی شما دچار مشکل شده لطفا یکبار خروج کرده و سپس ورود کنید"}
#     elif res[0] == 0:
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "ابتدا اطلاعات خود را ثبت اولیه نمایید."}
#     token, dash_info, message = select_student_info(conn, cursor, info)
#     if not token:
#         return {"status": 200, "tracking_code": token, "method_type": method_type,
#                 "error": message}
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"data": dash_info}}
