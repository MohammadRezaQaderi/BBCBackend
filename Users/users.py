import json
import time
import uuid
from datetime import datetime

from Helper import db_helper
from Users.Auth.auth import check_signin, token_remove
from Users.Consultant.consultant import insert_con_stu, update_con_user_profile, update_con_password
from Users.Institute.institute import insert_ins_con, insert_ins_stu, update_ins_user_profile, update_ins_password
from Users.Student.student import update_stu_user_profile, update_stu_password, update_stu_info

uni_info = ["دانشگاه‌های شاخص سراسر کشور", "دانشگاه‌های برتر استان(های) بومی", "سایر دانشگاه‌های استان(های) بومی",
            "دانشگاه‌های برتر استان‌های همسایه", "سایر دانشگاه‌های استان‌های همسایه",
            "دانشگاه‌های برتر استان‌های نزدیک", "سایر دانشگاه‌های استان‌های نزدیک",
            "دانشگاه‌های برتر استان‌های با فاصله زیاد", "سایر دانشگاه‌های استان‌های با فاصله زیاد",
            "دانشگاه‌های برتر دیگر استان‌های کشور", "سایر دانشگاه‌های دیگر استان‌های کشور"]
major_info = ["رشته‌های اولویت ۱", "رشته‌های اولویت ۲", "رشته‌های اولویت ۳", "رشته‌های اولویت ۴"]


def check_user_request(conn, cursor, order_data, info):
    if info.get("role") == "ins":
        query = 'SELECT ins_id FROM BBC.dbo.stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        if res.ins_id != info.get("user_id"):
            return False
    elif info.get("role") == "con":
        query = 'SELECT con_id FROM BBC.dbo.stu WHERE user_id = ?'
        res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=order_data["stu_id"])
        if res.con_id != info.get("user_id"):
            return False
    else:
        if info.get("user_id") != int(order_data["stu_id"]):
            return False
    return False


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
    if info.get("role") == ["ins", "con", "stu"]:
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
# def update_consultant(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     if info.get("role") == "ins":
#         token, message = update_ins_con(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     elif info.get("role") == "hCon":
#         token, message = update_hCon_con(conn, cursor, order_data, info)
#         cursor.close()
#         conn.close()
#         if token:
#             return {"status": 200, "tracking_code": token, "method_type": method_type,
#                     "response": {"message": message}}
#         else:
#             return {"status": 200, "tracking_code": None, "method_type": method_type,
#                     "error": message}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def finalize_student_info(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     token = update_stu_info(conn, cursor, order_data, info, 2)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"message": "اطلاعات شما با موفقیت ثبت‌نهایی شد."}}
#
#

#
#
# # The users functionality
# def student_info(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     token, dash_info, message = select_student_info(conn, cursor, info)
#     if not token:
#         return {"status": 200, "tracking_code": token, "method_type": method_type,
#                 "error": message}
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"data": dash_info}}
#
#
# # Field Pick
# def accept_check_user_info(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query = 'SELECT finalized FROM BBC.dbo.stu WHERE user_id = ?'
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
#
#
# def fp_majors(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, majors = get_majors(conn, cursor, order_data)
#     if majors is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": majors}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fp_exam_types(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, exam_types = get_exam_types(conn, cursor, order_data)
#     if exam_types is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": exam_types}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fp_universities(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, universities = get_universities(conn, cursor, order_data)
#     if universities is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": universities}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fp_cities(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, cities = get_cities(conn, cursor, order_data)
#     if cities is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": cities}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fp_provinces(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, provinces = get_provinces(conn, cursor, order_data)
#     if provinces is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": provinces}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fp_search_fields(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, fields, message = search_fields(conn, cursor, order_data, info)
#     if fields is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": fields}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": message}
#
#
# # Free Pick
# def fr_majors(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, majors = get_majors_fr(conn, cursor, order_data)
#     if majors is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": majors}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fr_provinces(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, provinces = get_provinces_fr(conn, cursor, order_data)
#     if provinces is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": provinces}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fr_universities(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, universities = get_universities_fr(conn, cursor, order_data)
#     if universities is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": universities}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def fr_search_fields(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, fields, message = search_fields_fr(conn, cursor, order_data, info)
#     if fields is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": fields}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": message}
#
#
# # Free Other Pick
# def frb_majors(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, majors = get_majors_frb(conn, cursor, order_data)
#     if majors is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": majors}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def frb_provinces(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, provinces = get_provinces_frb(conn, cursor, order_data)
#     if provinces is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": provinces}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def frb_universities(conn, cursor, order_data):
#     method_type = "SELECT"
#     tracking_code, universities = get_universities_frb(conn, cursor, order_data)
#     if universities is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": universities}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "مشکلی در اطلاعات شما پیش آمده با پشتیبانی در ارتباط باشید."}
#
#
# def frb_search_fields(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     print(method_type)
#     tracking_code, fields, message = search_fields_frb(conn, cursor, order_data, info)
#     if fields is not None:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#                 "response": fields}
#     else:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": message}
#
#
# # users list
# def update_spgl_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     tracking_code, message = update_spgl(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def update_spfr_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     tracking_code, message = update_spfr(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def select_spfr_list(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, data = get_spfr(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": data}
#
#
# def update_trfr_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     tracking_code, message = update_trfr(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def select_trfr_list(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, data = get_trfr(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": data}
#
#
# def update_spfrb_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     tracking_code, message = update_spfrb(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def select_spfrb_list(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, data = get_spfrb(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": data}
#
#
# def update_trfrb_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     tracking_code, message = update_trfrb(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def select_trfrb_list(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     tracking_code, data = get_trfrb(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": tracking_code, "method_type": method_type,
#             "response": data}
#
#
# # Hoshmand Functionality
# def get_hoshmand_info(conn, cursor, data, info):
#     try:
#         method_type = "SELECT"
#         query = '''
#                 SELECT
#                     terms_accepted,
#                     current_step
#                 FROM BBC.dbo.hoshmand_info
#                 WHERE user_id = ?
#                 '''
#         hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#         if not hoshmand_data:
#             field = '([user_id], [phone])'
#             values = (
#                 info.get("user_id"), info.get("phone"))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_info', fields=field,
#                                    values=values)
#         info = {
#             "terms_accepted": hoshmand_data[0] if hoshmand_data and hoshmand_data[0] else 0,
#             "current_step": hoshmand_data[1] if hoshmand_data and hoshmand_data[1] else 1,
#         }
#         token = str(uuid.uuid4())
#         cursor.close()
#         conn.close()
#
#         return {
#             "status": 200,
#             "tracking_code": token,
#             "method_type": method_type,
#             "response": info
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "status": 401,
#             "tracking_code": None,
#             "method_type": None,
#             "response": "error in try form"
#         }
#
#
# def update_hoshmand_info(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#             SELECT
#                 *
#             FROM BBC.dbo.hoshmand_info
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [terms_accepted], [current_step])'
#         values = (
#             info.get("user_id"), info.get("phone"), order_data["terms_accepted"], order_data["current_step"])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_info', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_info",
#             ['terms_accepted', 'current_step', 'edited_time'],
#             [order_data["terms_accepted"], order_data["current_step"],
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         # delete_unneeded_table(
#         #     conn, cursor,
#         #     ["hoshmand_examtype", "hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities",
#         #      "hoshmand_chains", "hoshmand_fields"], info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "data": {
#                 "terms_accepted": order_data["terms_accepted"],
#                 "current_step": order_data["current_step"]
#             },
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_questions(conn, cursor, data, info):
#     method_type = "SELECT"
#     query = '''
#         SELECT
#             examtype,
#             univercity,
#             major,
#             obligation,
#             method
#         FROM BBC.dbo.hoshmand_questions
#         WHERE user_id = ?
#         '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [examtype], [univercity], [major], [obligation], [method])'
#         values = (
#             info.get("user_id"), info.get("phone"), 3, 3, 3,
#             '0,1', 'با آزمون,صرفا با سوابق تحصیلی')
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_questions', fields=field,
#                                values=values)
#     info_response = {
#         "examtype": hoshmand_data[0] if hoshmand_data and hoshmand_data[0] else 3,
#         "univercity": hoshmand_data[1] if hoshmand_data and hoshmand_data[1] else 3,
#         "major": hoshmand_data[2] if hoshmand_data and hoshmand_data[2] else 3,
#         "obligation": hoshmand_data[3] if hoshmand_data else '0,1',
#         "method": hoshmand_data[4] if hoshmand_data else 'با آزمون,صرفا با سوابق تحصیلی',
#     }
#     update_step_hoshmand(conn, cursor, 1, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": info_response
#     }
#
#
# def update_hoshmand_questions(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#             SELECT
#                 *
#             FROM BBC.dbo.hoshmand_questions
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [examtype], [univercity], [major], [obligation], [method])'
#         values = (
#             info.get("user_id"), info.get("phone"), order_data["examtype"], order_data["univercity"], order_data["major"],
#             order_data["obligation"], order_data["method"])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_questions', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_questions",
#             ['examtype', 'univercity', 'major', 'obligation', 'method', 'edited_time'],
#             [order_data["examtype"], order_data["univercity"], order_data["major"],
#              order_data["obligation"], order_data["method"],
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(
#             conn, cursor,
#             ["hoshmand_examtype", "hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities",
#              "hoshmand_chains", "hoshmand_fields"], info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_examtype(conn, cursor, data, info):
#     method_type = "SELECT"
#     query = '''
#             SELECT
#                 data,
#                 examtypes
#             FROM BBC.dbo.hoshmand_examtype
#             WHERE user_id = ?
#         '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     query_question = 'select obligation, method from BBC.dbo.hoshmand_questions where user_id = ?'
#     question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#     query_student = 'select sex, field, city, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     field = str(student[1])
#     if student[3] != 0 and student[3]:
#         field += "," + str(4)
#     if student[4] != 0 and student[4]:
#         field += "," + str(5)
#     exam_types = []
#     sql = 'exec Note.smart.Get_TypeExamTurns_new ?, ?, ?, ?, ?, ?, ?'
#     values = (
#         field, student[0], student[2].split(",")[0], None, 1404, str(question[0]), str(question[1])
#     )
#     recs = []
#     is_empty = 0
#     try:
#         cursor.execute(sql, values)
#         recs = cursor.fetchall()
#         cursor.commit()
#     except Exception as e:
#         is_empty = 2
#         print(">>> excp in get_hoshmand_examtype", e)
#         field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#         values_log = (
#             info.get("user_id"), info.get("phone"), "Get_TypeExamTurns_new", json.dumps(values, ensure_ascii=False),
#             json.dumps(data, ensure_ascii=False), str(e))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                values=values_log)
#     if len(recs) == 0:
#         is_empty = 1
#     for res in recs:
#         exam_types.append(res[0])
#     if not hoshmand_data:
#         user_data = None
#     else:
#         user_data = json.loads(hoshmand_data[0])
#     update_step_hoshmand(conn, cursor, 2, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "is_empty": is_empty,
#             "exam_types": exam_types,
#             "user_data": user_data,
#         }
#     }
#
#
# def update_hoshmand_examtype(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#             SELECT
#                 *
#             FROM BBC.dbo.hoshmand_examtype
#             WHERE user_id = ?
#         '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [data], [examtypes])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(order_data["data"], ensure_ascii=False), order_data["examtypes"])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_examtype', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_examtype",
#             ['data', 'examtypes', 'edited_time'],
#             [json.dumps(order_data["data"], ensure_ascii=False), order_data["examtypes"],
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(
#             conn, cursor,
#             ["hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
#              "hoshmand_fields"], info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_major(conn, cursor, data, info):
#     method_type = "SELECT"
#     query = '''
#             SELECT
#                 data,
#                 majors
#             FROM BBC.dbo.hoshmand_major
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     query_examtypes = '''
#             SELECT
#                 examtypes
#             FROM BBC.dbo.hoshmand_examtype
#             WHERE user_id = ?
#             '''
#     hoshmand_examtypes = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtypes, field=info.get("user_id"))
#     query_question = 'select obligation, method from BBC.dbo.hoshmand_questions where user_id = ?'
#     question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#     query_student = 'select sex, field, city, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     majors = []
#     field = str(student[1])
#     if student[3] != 0 and student[3]:
#         field += "," + str(4)
#     if student[4] != 0 and student[4]:
#         field += "," + str(5)
#     sql = 'exec Note.smart.Get_Majors_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#     values = (
#         field, student[0], student[2].split(",")[0], hoshmand_examtypes[0], None, 1404, str(question[0]),
#         str(question[1]), None, None
#     )
#     recs = []
#     try:
#         cursor.execute(sql, values)
#         recs = cursor.fetchall()
#         cursor.commit()
#     except Exception as e:
#         print(">>> excp in get_hoshmand_major", e)
#         field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#         values_log = (
#             info.get("user_id"), info.get("phone"), "Get_Majors_new", json.dumps(values, ensure_ascii=False),
#             json.dumps(data, ensure_ascii=False), str(e))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                values=values_log)
#     for res in recs:
#         majors.append(res[0])
#     if not hoshmand_data:
#         user_data = None
#     else:
#         user_data = json.loads(hoshmand_data[0])
#     update_step_hoshmand(conn, cursor, 3, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "majors": majors,
#             "user_data": user_data,
#         }
#     }
#
#
# def update_hoshmand_major(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#             SELECT
#                 *
#             FROM BBC.dbo.hoshmand_major
#             WHERE user_id = ?
#         '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [data], [majors], [major1], [major2], [major3], [major4])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(order_data["data"], ensure_ascii=False), order_data["majors"],
#             order_data["major1"],
#             order_data["major2"], order_data["major3"], order_data["major4"])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_major', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_major",
#             ['data', 'majors', 'major1', 'major2', 'major3', 'major4', 'edited_time'],
#             [json.dumps(order_data["data"], ensure_ascii=False), order_data["majors"], order_data["major1"],
#              order_data["major2"], order_data["major3"], order_data["major4"],
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(conn, cursor,
#                               ["hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
#                                "hoshmand_fields"], info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_province(conn, cursor, data, info):
#     method_type = "SELECT"
#     query = '''
#             SELECT
#                 data
#             FROM BBC.dbo.hoshmand_province
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     query_student = 'select sex, field, city, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     majors = []
#     if not hoshmand_data:
#         query_majors = 'select majors from BBC.dbo.hoshmand_major where user_id = ?'
#         majors_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_majors, field=info.get("user_id"))
#         query_examtype = 'select examtypes from BBC.dbo.hoshmand_examtype where user_id = ?'
#         examtype_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtype, field=info.get("user_id"))
#         query_question = 'select obligation, method from BBC.dbo.hoshmand_questions where user_id = ?'
#         question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#         field = str(student[1])
#         if student[3] != 0 and student[3]:
#             field += "," + str(4)
#         if student[4] != 0 and student[4]:
#             field += "," + str(5)
#         sql = 'exec Note.smart.Get_Provinces_new ?, ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             field, student[0], student[2].split(",")[0], examtype_res[0] if examtype_res[0] else None,
#             majors_res[0] if majors_res[0] else None, None, 1404, str(question[0]), str(question[1])
#         )
#         recs = []
#         try:
#             cursor.execute(sql, values)
#             recs = cursor.fetchall()
#             cursor.commit()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_province", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Get_Provinces_new", json.dumps(values, ensure_ascii=False),
#                 json.dumps(data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         user_data = [
#             {
#                 "id": "box-1",
#                 "title": "استان(های) بومی و محل زندگی شما",
#                 "items": [],
#                 "readOnly": False,
#             },
#             {
#                 "id": "box-2",
#                 "title": "استان‌های همسایه و نزدیک به استان بومی",
#                 "items": [],
#                 "readOnly": False,
#             },
#             {
#                 "id": "box-3",
#                 "title": "استان‌های نزدیک (به لحاظ فرهنگی یا مسافتی)",
#                 "items": [],
#                 "readOnly": False,
#             },
#             {
#                 "id": "box-4",
#                 "title": "استان‌های با فاصله نسبتا زیاد",
#                 "items": [],
#                 "readOnly": False,
#             },
#             {
#                 "id": "box-5",
#                 "title": "سایر استان‌های کل کشور که ممکن است بروید",
#                 "items": [],
#                 "readOnly": False,
#             },
#             {
#                 "id": "box-6",
#                 "title": "استان‌هایی که به هیچ عنوان در آن‌ها تحصیل نخواهید کرد",
#                 "items": [],
#                 "readOnly": False,
#             },
#         ]
#         for item in recs:
#             if 0 <= item[1] <= 4:
#                 user_data[item[1]]["items"].append(item[0])
#         province1 = ",".join(user_data[0]["items"])
#         province2 = ",".join(user_data[1]["items"])
#         province3 = ",".join(user_data[2]["items"])
#         province4 = ",".join(user_data[3]["items"])
#         province5 = ",".join(user_data[4]["items"])
#
#         field = '([user_id], [phone], [data], [province1], [province2], [province3], [province4], [province5], [province6])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(user_data, ensure_ascii=False), province1,
#             province2, province3, province4, province5, ""
#         )
#         db_helper.insert_value(
#             conn=conn,
#             cursor=cursor,
#             table_name='hoshmand_province',
#             fields=field,
#             values=values
#         )
#     else:
#         user_data = json.loads(hoshmand_data[0])
#     update_step_hoshmand(conn, cursor, 4, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "majors": majors,
#             "user_data": user_data,
#         }
#     }
#
#
# def update_hoshmand_province(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#                 SELECT
#                     *
#                 FROM BBC.dbo.hoshmand_province
#                 WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [data], [province1], [province2], [province3], [province4], [province5], [province6])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(order_data["data"], ensure_ascii=False), order_data["province1"],
#             order_data["province2"], order_data["province3"], order_data["province4"], order_data["province5"],
#             order_data["province6"])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_province', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_province",
#             ['data', 'province1', 'province2', 'province3', 'province4', 'province5', 'province6', 'edited_time'],
#             [json.dumps(order_data["data"], ensure_ascii=False), order_data["province1"],
#              order_data["province2"], order_data["province3"], order_data["province4"], order_data["province5"],
#              order_data["province6"],
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(conn, cursor,
#                               ["hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
#                                "hoshmand_fields"], info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_tables(conn, cursor, data, info):
#     method_type = "SELECT"
#     start_select = time.time()
#     query = '''
#             SELECT
#                 data_table1,
#                 data_table2
#             FROM BBC.dbo.hoshmand_tables
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     query_student = 'select sex, field, city, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     query_examtype = 'select examtypes from BBC.dbo.hoshmand_examtype where user_id = ?'
#     examtypes_result = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtype, field=info.get("user_id"))
#     exam_types = examtypes_result[0].split(',') if examtypes_result and examtypes_result[0] else []
#     query_question = 'select obligation, method from BBC.dbo.hoshmand_questions where user_id = ?'
#     question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#     if not hoshmand_data:
#         field_state = str(student[1])
#         if student[3] != 0 and student[3]:
#             field_state += "," + str(4)
#         if student[4] != 0 and student[4]:
#             field_state += "," + str(5)
#         finish_select = time.time()
#         print("finish_select ", start_select - finish_select)
#         major_start = time.time()
#         query_majors = 'select major1, major2, major3, major4, majors from BBC.dbo.hoshmand_major where user_id = ?'
#         majors = db_helper.search_table(conn=conn, cursor=cursor, query=query_majors, field=info.get("user_id"))
#         sql = 'exec Note.smart.Get_Major_TypeExamTurn_Block_States_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             field_state, student[0], student[2].split(",")[0],
#             examtypes_result[0] if examtypes_result else None,
#             majors[0], majors[1], majors[2], majors[3], 1404, str(question[0]), str(question[1])
#         )
#         recs = []
#         try:
#             cursor.execute(sql, values)
#             recs = cursor.fetchall()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_tables", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Get_Major_TypeExamTurn_Block_States_new",
#                 json.dumps(values, ensure_ascii=False),
#                 json.dumps(data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         num_skill_categories = 4
#         skills_table = [
#             {"name": major_info[i], "values": [0] * len(exam_types), "data": majors[i]}
#             for i in range(num_skill_categories)
#         ]
#         exam_type_index = {exam_type: idx for idx, exam_type in enumerate(exam_types)}
#         for exam_type, category in recs:
#             if exam_type in exam_type_index and 1 <= category <= num_skill_categories:
#                 exam_idx = exam_type_index[exam_type]
#                 skills_table[category - 1]["values"][exam_idx] = 1
#         major_finish = time.time()
#         print("major ", major_finish - major_start)
#
#         province_start = time.time()
#
#         query_province = 'select province1, province2, province3, province4, province5 from BBC.dbo.hoshmand_province where user_id = ?'
#         province = db_helper.search_table(conn=conn, cursor=cursor, query=query_province, field=info.get("user_id"))
#         sql = 'exec Note.smart.Get_University_Blocks_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             field_state, student[0],
#             examtypes_result[0] if examtypes_result else None,
#             majors[4], student[2].split(",")[0], province[0], province[1], province[2], province[3], province[4], 1404,
#             str(question[0]), str(question[1])
#         )
#         recs_majors = []
#         try:
#             cursor.execute(sql, values)
#             recs_majors = cursor.fetchall()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_tables", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Get_University_Blocks_new", json.dumps(values, ensure_ascii=False),
#                 json.dumps(data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         province_finish = time.time()
#         print("province ", province_finish - province_start)
#         create_start = time.time()
#         num_uni_categories = 11
#         universities_table = [
#             {"name": uni_info[i], "values": [0] * len(exam_types), "data": ""}
#             for i in range(num_uni_categories)
#         ]
#
#         uni_dict = {}
#         for category, uni_name, city in recs_majors:
#             if 1 <= category <= num_uni_categories:
#                 if category not in uni_dict:
#                     uni_dict[category] = []
#                 uni_dict[category].append(uni_name)
#
#         uni = [""] * 11
#         for category in uni_dict:
#             if 1 <= category <= 11:
#                 uni[category - 1] = ",".join(uni_dict[category])
#                 universities_table[category - 1]["data"] = uni[category - 1]
#         create_finish = time.time()
#         print("create ", create_finish - create_start)
#
#         uni_start = time.time()
#         query_uni = 'select id from BBC.dbo.hoshmand_universities where user_id = ?'
#         uni_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_uni, field=info.get("user_id"))
#         if uni_res:
#             db_helper.delete_record(
#                 conn, cursor, 'hoshmand_universities',
#                 ["user_id"],
#                 [str(info.get("user_id"))]
#             )
#         field = '([user_id], [phone], [uni1], [uni2], [uni3], [uni4], [uni5], [uni6], [uni7], [uni8], [uni9], [uni10], [uni11])'
#         values = (
#             info.get("user_id"), info.get("phone"), uni[0], uni[1], uni[2], uni[3], uni[4], uni[5], uni[6], uni[7], uni[8],
#             uni[9], uni[10])
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_universities', fields=field,
#                                values=values)
#         uni_finish = time.time()
#         print("uni ", uni_finish - uni_start)
#         block_start = time.time()
#         sql = 'exec Note.smart.Get_University_TypeExamTurn_Block_States_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             field_state, student[0], student[2].split(",")[0],
#             examtypes_result[0] if examtypes_result else None,
#             uni[0], uni[1], uni[2], uni[3], uni[4], uni[5], uni[6], uni[7], uni[8], uni[9], uni[10], 1404,
#             str(question[0]), str(question[1])
#         )
#         recs_data = []
#         try:
#             cursor.execute(sql, values)
#             recs_data = cursor.fetchall()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_tables", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Get_University_TypeExamTurn_Block_States_new",
#                 json.dumps(values, ensure_ascii=False),
#                 json.dumps(data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         block_finish = time.time()
#         print("block ", block_finish - block_start)
#         table_start = time.time()
#
#         for exam_type, category in recs_data:
#             if exam_type in exam_type_index and 1 <= category <= num_uni_categories:
#                 exam_idx = exam_type_index[exam_type]
#                 universities_table[category - 1]["values"][exam_idx] = 1
#         table_finish = time.time()
#         print("table ", table_finish - table_start)
#         field = '([user_id], [phone], [data_table1], [data_table2])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(skills_table, ensure_ascii=False),
#             json.dumps(universities_table, ensure_ascii=False)
#         )
#         db_helper.insert_value(
#             conn=conn,
#             cursor=cursor,
#             table_name='hoshmand_tables',
#             fields=field,
#             values=values
#         )
#
#     else:
#         universities_table = json.loads(hoshmand_data[1])
#         skills_table = json.loads(hoshmand_data[0])
#     update_step_hoshmand(conn, cursor, 5, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "skills": skills_table,
#             "universities": universities_table,
#             "priorities": exam_types,
#         }
#     }
#
#
# def update_hoshmand_tables(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#                 SELECT
#                     *
#                 FROM BBC.dbo.hoshmand_tables
#                 WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     # chains = prepare_chain_data(conn, cursor, info, order_data)
#     if not hoshmand_data:
#         field = '([user_id], [phone], [data_table1], [data_table2])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(order_data["skills"], ensure_ascii=False),
#             json.dumps(order_data["universities"], ensure_ascii=False))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_tables', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_tables",
#             ['data_table1', 'data_table2', 'edited_time'],
#             [json.dumps(order_data["skills"], ensure_ascii=False),
#              json.dumps(order_data["universities"], ensure_ascii=False),
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(conn, cursor,
#                               ["hoshmand_chains", "hoshmand_fields"], info.get("user_id"))
#
#     # field = '([user_id], [phone], [chains], [deleted_chains])'
#     # values = (
#     #     info.get("user_id"), info.get("phone"), json.dumps(chains, ensure_ascii=False), json.dumps([], ensure_ascii=False))
#     # db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_chains', fields=field,
#     #                        values=values)
#
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_chains(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query = '''
#            SELECT
#                chains,
#                deleted_chains
#            FROM BBC.dbo.hoshmand_chains
#            WHERE user_id = ?
#            '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         start_select = time.time()
#         query_student = 'select sex, field, city, rank_zaban, rank_honar, quota from BBC.dbo.stu where user_id = ?'
#         student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#         query_question = 'select obligation, method, univercity, major from BBC.dbo.hoshmand_questions where user_id = ?'
#         question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#         field = str(student[1])
#         if student[3] != 0 and student[3]:
#             field += "," + str(4)
#         if student[4] != 0 and student[4]:
#             field += "," + str(5)
#         sorting_major_uni = False
#         if question[2] > question[3]:
#             sorting_major_uni = True
#         finish_select = time.time()
#         print("select ", finish_select - start_select)
#         sql = 'exec Note.smart.Create_Chanis_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             info.get("user_id"), student[5], field, student[0],
#             student[2].split(",")[0], str(question[0]), str(question[1]), 1404, sorting_major_uni, "BBC"
#         )
#         recs = []
#         start_recs = time.time()
#         try:
#             cursor.execute(sql, values)
#             recs = cursor.fetchall()
#             cursor.commit()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_chains", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Create_Chanis_new", json.dumps(values, ensure_ascii=False),
#                 json.dumps(order_data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#
#         processed_recs = []
#         if recs:
#             combined_json = ''.join([part for tup in recs for part in tup])
#             try:
#                 parsed_data = json.loads(combined_json)
#                 processed_recs = parsed_data.get('results', [])
#             except json.JSONDecodeError as e:
#                 print(f"Error parsing JSON: {e}")
#                 try:
#                     fixed_json = combined_json.replace('",', '",').replace('", "', '", "')
#                     parsed_data = json.loads(fixed_json)
#                     processed_recs = parsed_data.get('results', [])
#                 except:
#                     processed_recs = []
#         finish_recs = time.time()
#         print("recs ", finish_recs - start_recs)
#         field = '([user_id], [phone], [chains], [deleted_chains])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(processed_recs, ensure_ascii=False),
#             json.dumps([], ensure_ascii=False))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_chains', fields=field,
#                                values=values)
#     else:
#         processed_recs = json.loads(hoshmand_data[0])
#     update_step_hoshmand(conn, cursor, 6, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "chains": processed_recs,
#             "hand_chains": json.loads(hoshmand_data[0]) if hoshmand_data and hoshmand_data[0] else [],
#             "deleted_chains": json.loads(hoshmand_data[1]) if hoshmand_data and hoshmand_data[1] else [],
#         }
#     }
#
#
# def update_hoshmand_chains(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#             SELECT
#                 *
#             FROM BBC.dbo.hoshmand_chains
#             WHERE user_id = ?
#         '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         field = '([user_id], [phone], [chains], [majors], [universities], [deleted_chains])'
#         values = (
#             info.get("user_id"), info.get("phone"), json.dumps(order_data["chains"], ensure_ascii=False), order_data['majors'], \
#             order_data['universities'], json.dumps(order_data["deleted_chains"], ensure_ascii=False))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_chains', fields=field,
#                                values=values)
#     else:
#         db_helper.update_record(
#             conn, cursor, "hoshmand_chains",
#             ['chains', 'majors', 'universities', 'deleted_chains', 'edited_time'],
#             [json.dumps(order_data["chains"], ensure_ascii=False), order_data['majors'], order_data['universities'],
#              json.dumps(order_data["deleted_chains"], ensure_ascii=False),
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#         delete_unneeded_table(conn, cursor,
#                               ["hoshmand_fields"], info.get("user_id"))
#
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def prepare_chain_data(conn, cursor, info, order_data):
#     query_majors = 'SELECT major1, major2, major3, major4 FROM BBC.dbo.hoshmand_major WHERE user_id = ?'
#     majors_result = db_helper.search_table(conn=conn, cursor=cursor, query=query_majors, field=info.get("user_id"))
#
#     query_universities = 'SELECT uni1, uni2, uni3, uni4, uni5, uni6, uni7, uni8, uni9, uni10, uni11 FROM BBC.dbo.hoshmand_universities WHERE user_id = ?'
#     universities_result = db_helper.search_table(conn=conn, cursor=cursor, query=query_universities,
#                                                  field=info.get("user_id"))
#
#     query_examtype = 'SELECT examtypes FROM BBC.dbo.hoshmand_examtype WHERE user_id = ?'
#     examtypes_result = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtype, field=info.get("user_id"))
#     exam_types = examtypes_result[0].split(',') if examtypes_result and examtypes_result[0] else []
#
#     majors_list = []
#     if majors_result:
#         majors_list = [
#             [m.strip() for m in majors_result[0].split(',') if m.strip()] if majors_result[0] else [],
#             [m.strip() for m in majors_result[1].split(',') if m.strip()] if majors_result[1] else [],
#             [m.strip() for m in majors_result[2].split(',') if m.strip()] if majors_result[2] else [],
#             [m.strip() for m in majors_result[3].split(',') if m.strip()] if majors_result[3] else [],
#         ]
#
#     universities_list = []
#     if universities_result:
#         universities_list = [
#             [u.strip() for u in universities_result[0].split(',') if u.strip()] if universities_result[0] else [],
#             [u.strip() for u in universities_result[1].split(',') if u.strip()] if universities_result[1] else [],
#             [u.strip() for u in universities_result[2].split(',') if u.strip()] if universities_result[2] else [],
#             [u.strip() for u in universities_result[3].split(',') if u.strip()] if universities_result[3] else [],
#             [u.strip() for u in universities_result[4].split(',') if u.strip()] if universities_result[4] else [],
#             [u.strip() for u in universities_result[5].split(',') if u.strip()] if universities_result[5] else [],
#             [u.strip() for u in universities_result[6].split(',') if u.strip()] if universities_result[6] else [],
#             [u.strip() for u in universities_result[7].split(',') if u.strip()] if universities_result[7] else [],
#             [u.strip() for u in universities_result[8].split(',') if u.strip()] if universities_result[8] else [],
#             [u.strip() for u in universities_result[9].split(',') if u.strip()] if universities_result[9] else [],
#             [u.strip() for u in universities_result[10].split(',') if u.strip()] if universities_result[10] else [],
#         ]
#
#     chains = []
#
#     skills_data = order_data.get("skills", [])
#     universities_data = order_data.get("universities", [])
#
#     for exam_idx, exam_type in enumerate(exam_types):
#         enabled_skill_categories = [
#             (skill_idx, skill["name"])
#             for skill_idx, skill in enumerate(skills_data)
#             if skill["values"][exam_idx] == 1
#         ]
#
#         enabled_uni_categories = [
#             (uni_idx, uni["name"])
#             for uni_idx, uni in enumerate(universities_data)
#             if uni["values"][exam_idx] == 1
#         ]
#
#         for skill_idx, skill_name in enabled_skill_categories:
#             for uni_idx, uni_name in enabled_uni_categories:
#                 chains.append({
#                     "TypeExamTurn": exam_type,
#                     "Majors": majors_list[skill_idx],
#                     "Universities": universities_list[uni_idx],
#                     "skill_category": skill_name,
#                     "university_category": uni_name
#                 })
#
#     return chains
#
#
# def get_hoshmand_chain_code(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query_student = 'select sex, field, city, rank, quota, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     fields = []
#     field = str(student[1])
#     if student[5] != 0 and student[5]:
#         field += "," + str(4)
#     if student[6] != 0 and student[6]:
#         field += "," + str(5)
#     sql = 'exec Note.smart.Get_Chain_Fields_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
#     values = (
#         field, student[4], order_data["codes"], student[3],
#         1, 1000, 1404, None, None, None
#     )
#     recs = []
#     try:
#         cursor.execute(sql, values)
#         recs = cursor.fetchall()
#         cursor.commit()
#     except Exception as e:
#         print(">>> excp in get_hoshmand_chain_code", e)
#         field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#         values_log = (
#             info.get("user_id"), info.get("phone"), "Get_Chain_Fields_new", json.dumps(values, ensure_ascii=False),
#             json.dumps(order_data, ensure_ascii=False), str(e))
#         db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                values=values_log)
#
#     cursor.commit()
#     for res in recs:
#         cap = res[19]
#         if res[19] is None:
#             cap = res[20]
#         response = {
#             'filedCode': res[1], 'field': res[7], 'city': res[5] + "-" + res[6], 'university': res[8],
#             'admission': res[10],
#             'kind': res[11],
#             'obligation': res[13], 'period': res[12],
#             'explain': res[14], 'admissionKind': res[21],
#             'capacity': cap,
#         }
#         fields.append(response)
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "data": fields,
#         }
#     }
#
#
# def get_hoshmand_fields(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query = '''
#             SELECT
#                 all_list,
#                 field_list,
#                 selected_list,
#                 is_hoshmand
#             FROM BBC.dbo.hoshmand_fields
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     if not hoshmand_data:
#         query_student = 'select sex, field, city, rank, quota, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#         student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#         query_question = 'select obligation, method, univercity, major from BBC.dbo.hoshmand_questions where user_id = ?'
#         question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=info.get("user_id"))
#         query = 'SELECT suggested, other FROM BBC.dbo.hedayat_fields WHERE user_id = ?'
#         res_hedayat = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#         suggested_fields = None
#         other_fields = None
#         if res_hedayat is not None:
#             suggested_fields = res_hedayat.suggested
#             other_fields = res_hedayat.other
#         sorting_major_uni = False
#         if question[2] > question[3]:
#             sorting_major_uni = True
#         field = str(student[1])
#         if student[5] != 0 and student[5]:
#             field += "," + str(4)
#         if student[6] != 0 and student[6]:
#             field += "," + str(5)
#         fields = []
#         sql = 'exec Note.smart.Get_Fields_By_Chains_new ?, ?, ?, ?, ?, ?, ?, ?'
#         values = (
#             info.get("user_id"), field, student[4], student[3], 1404, suggested_fields, other_fields, "BBC"
#             # , 1, 1000,  student[0], student[2].split(",")[0],
#             # str(question[0]), str(question[1]), sorting_major_uni
#         )
#         recs = []
#         try:
#             cursor.execute(sql, values)
#             recs = cursor.fetchall()
#             cursor.commit()
#         except Exception as e:
#             print(">>> excp in get_hoshmand_fields", e)
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Get_Fields_By_Chains_new", json.dumps(values, ensure_ascii=False),
#                 json.dumps(order_data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         for res in recs:
#             cap = res.FirstSemesterCapacity
#             if res.FirstSemesterCapacity is None:
#                 cap = res.SecondSemesterCapacity
#             response = {
#                 'filedCode': res.CodeReshteh, 'field': res.Major,
#                 'city': res.EducationProvince + "-" + res.EducationCity,
#                 'university': res.University,
#                 'admission': res.AdmissionTurn, 'kind': res.Method,
#                 'obligation': res.Obligation, 'period': res.TypeExamTurn,
#                 'explain': res.Description, 'admissionKind': res.Acceptance,
#                 'capacity': cap,
#                 'hedayat': None if res_hedayat is None else res.HedayatRank
#             }
#             fields.append(response)
#         try:
#             field_json = json.dumps(fields, ensure_ascii=False)
#             empty_list_json = json.dumps([], ensure_ascii=False)
#             field_json = str(field_json) if field_json else ''
#             empty_list_json = str(empty_list_json) if empty_list_json else ''
#             field = '([user_id], [phone], [all_list], [field_list], [selected_list], [trash_list], [hoshmand_list])'
#             values = (
#                 info.get("user_id"),
#                 info.get("phone"),
#                 field_json,
#                 field_json,
#                 empty_list_json,
#                 empty_list_json,
#                 empty_list_json
#             )
#
#             query = f"""
#             INSERT INTO hoshmand_fields {field}
#             VALUES (?, ?, CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)),
#                     CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)))
#             """
#             # cursor.execute("SET TEXTSIZE 2147483647")
#             # cursor.execute("SET ANSI_WARNINGS ON")
#             # cursor.execute("SET ANSI_PADDING ON")
#             cursor.execute(query, values)
#             conn.commit()
#
#         except Exception as e:
#             print(f"Error inserting record >>>>>>>>>>: {e}")
#             conn.rollback()
#         selected_list = []
#         is_hoshmand = False
#     else:
#         fields = json.loads(hoshmand_data[1])
#         selected_list = json.loads(hoshmand_data[2])
#         is_hoshmand = True if hoshmand_data[3] == 1 else False
#     update_step_hoshmand(conn, cursor, 7, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "data": fields,
#             "selected_list": selected_list,
#             "is_hoshmand": is_hoshmand
#         }
#     }
#
#
# def update_hoshmand_fields(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     db_helper.update_record(
#         conn, cursor, "hoshmand_fields",
#         ['field_list', 'selected_list', 'edited_time'],
#         [json.dumps(order_data["fields_list"], ensure_ascii=False),
#          json.dumps(order_data["selected_list"], ensure_ascii=False),
#          datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#         "user_id = ?", [str(info.get("user_id"))]
#     )
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def get_hoshmand_sp_list(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     query = '''
#             SELECT
#                 selected_list,
#                 trash_list,
#                 hoshmand_list
#             FROM BBC.dbo.hoshmand_fields
#             WHERE user_id = ?
#             '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     token, dash_info, message = select_student_info(conn, cursor, info)
#     update_step_hoshmand(conn, cursor, 8, info.get("user_id"))
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "trash_list": json.loads(hoshmand_data[1]) if hoshmand_data[1] else [],
#             "selected_list": json.loads(hoshmand_data[0]),
#             "hoshmand_list": json.loads(hoshmand_data[2]) if hoshmand_data[2] else [],
#             "user_data": dash_info
#         }
#     }
#
#
# def update_hoshmand_sp_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     db_helper.update_record(
#         conn, cursor, "hoshmand_fields",
#         ['selected_list', 'trash_list', 'edited_time'],
#         [json.dumps(order_data["selected_list"], ensure_ascii=False),
#          json.dumps(order_data["trash_list"], ensure_ascii=False),
#          # json.dumps(order_data["hoshmand_list"], ensure_ascii=False),
#          datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#         "user_id = ?", [str(info.get("user_id"))]
#     )
#     token = str(uuid.uuid4())
#     cursor.close()
#     conn.close()
#     return {
#         "status": 200,
#         "tracking_code": token,
#         "method_type": method_type,
#         "response": {
#             "message": "اطلاعات ذخیره شد"
#         }
#     }
#
#
# def delete_unneeded_table(conn, cursor, tables, id):
#     for table in tables:
#         db_helper.delete_record(
#             conn, cursor, table,
#             ["user_id"],
#             [str(id)]
#         )
#
#
# def get_hoshmand_list(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     query = '''
#         SELECT chains
#         FROM BBC.dbo.hoshmand_chains
#         WHERE user_id = ?
#     '''
#     hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     query_student = 'select field, rank, quota, rank_zaban, rank_honar from BBC.dbo.stu where user_id = ?'
#     student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=info.get("user_id"))
#     field = str(student.field)
#     if student.rank_zaban != 0 and student.rank_zaban:
#         field += "," + str(4)
#     if student.rank_honar != 0 and student.rank_honar:
#         field += "," + str(5)
#     code_reshteh_list = []
#     query = 'SELECT suggested, other FROM BBC.dbo.hedayat_fields WHERE user_id = ?'
#     res_hedayat = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info.get("user_id"))
#     suggested_fields = None
#     other_fields = None
#     if res_hedayat is not None:
#         suggested_fields = res_hedayat.suggested
#         other_fields = res_hedayat.other
#     if hoshmand_data and hoshmand_data[0]:
#         chain = json.loads(hoshmand_data[0])
#         for group in chain:
#             if "CodeReshteh" in group:
#                 sorted_data = sorted(group["CodeReshteh"], key=lambda x: x['RowId'])
#                 x = [item['CodeReshteh'] for item in sorted_data]
#                 code_reshteh_list.extend(x)
#     json_code = {"CodeReshteh": code_reshteh_list}
#     fields = []
#     sql = 'exec Note.smart.Delete_Fields ?, ?, ?, ?, ?, ?'
#     values = (
#         json.dumps(json_code, ensure_ascii=False), field, student.quota, student.rank, suggested_fields, other_fields
#     )
#     recs = []
#     try:
#         cursor.execute(sql, values)
#         recs = cursor.fetchall()
#         cursor.commit()
#     except Exception as e:
#         print(">>> excp in get_hoshmand_list", e)
#         try:
#             field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
#             values_log = (
#                 info.get("user_id"), info.get("phone"), "Delete_Fields", json.dumps(values, ensure_ascii=False),
#                 json.dumps(order_data, ensure_ascii=False), str(e))
#             db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
#                                    values=values_log)
#         except Exception as e:
#             print("eeeeeeeeee", e)
#             return {
#                 "status": 200,
#                 "response": {
#                     "is_hoshmand": 0
#                 },
#                 "tracking_code": None
#             }
#     try:
#         for res in recs:
#             cap = res.FirstSemesterCapacity
#             if res.FirstSemesterCapacity is None:
#                 cap = res.SecondSemesterCapacity
#             response = {
#                 'filedCode': res.CodeReshteh, 'field': res.Major,
#                 'city': res.EducationProvince + "-" + res.EducationCity,
#                 'university': res.University,
#                 'admission': res.AdmissionTurn,
#                 'kind': res.Method,
#                 'obligation': res.Obligation, 'period': res.TypeExamTurn,
#                 'explain': res.Description, 'admissionKind': res.Acceptance,
#                 'capacity': cap,
#                 'hedayat': None if res_hedayat is None else res.HedayatRank
#             }
#             fields.append(response)
#         db_helper.update_record(
#             conn, cursor, "hoshmand_fields",
#             ['is_hoshmand', 'selected_list', 'hoshmand_list', 'edited_time'],
#             [1, json.dumps(fields, ensure_ascii=False),
#              json.dumps(fields, ensure_ascii=False),
#              datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#             "user_id = ?", [str(info.get("user_id"))]
#         )
#     except Exception as e:
#         print(">>>>>> exception", e)
#     try:
#         query = '''
#         SELECT
#             all_list,
#             field_list,
#             selected_list,
#             is_hoshmand
#         FROM BBC.dbo.hoshmand_fields
#         WHERE user_id = ?
#         '''
#         hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=str(info.get("user_id")))
#     except Exception as e:
#         print(">>>>>> ", e)
#     token = str(uuid.uuid4())
#     return {
#         "status": 200,
#         "response": {
#             "data": json.loads(hoshmand_data.all_list),
#             "selected_list": json.loads(hoshmand_data.selected_list),
#             "is_hoshmand": 1
#         },
#         "tracking_code": token
#     }
#
#
# # Quiz Functionality
# def update_quiz_answer(conn, cursor, order_data, info):
#     method_type = "UPDATE"
#     token, message = submit_quiz_answer(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"message": message}}
#
#
# def select_quiz_table_info(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     token, data = select_stu_quiz_table_info(conn, cursor, order_data, info)
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"data": data}}
#
#
# def select_quiz_info(conn, cursor, order_data, info):
#     method_type = "SELECT"
#     token, data, quiz_answers = select_stu_quiz_info(conn, cursor, order_data, info)
#     if not data:
#         cursor.close()
#         conn.close()
#         return {"status": 200, "tracking_code": None, "method_type": method_type,
#                 "error": "آزمون مورد نظر شما در دسترس شما نیست."}
#     cursor.close()
#     conn.close()
#     return {"status": 200, "tracking_code": token, "method_type": method_type,
#             "response": {"data": data, "quizAnswers": quiz_answers}}
