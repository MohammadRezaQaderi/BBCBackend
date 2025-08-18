from fastapi import FastAPI, Request, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
import os

from Helper.func_helper import db_connection
from Users.Institute.institute import update_user_ins_pic
from Users.users import *

app = FastAPI()


async def check(conn, cursor, data):
    if data.get("token"):
        if data["token"] is not None:
            query = "SELECT user_id, phone, role FROM tokens WHERE token = ?"
            res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["token"])
            if res is None:
                cursor.close()
                conn.close()
                return False, "نشست شما به پایان رسیده  لطفا یکبار خروج کرده و سپس ورود شوید.", None
            else:
                return True, "", {"user_id": res.user_id, "phone": res.phone, "role": res.role}
        else:
            cursor.close()
            conn.close()
            return False, "اطلاعات دریافتی شما دچار مشکل شده لطفا یکبار خروج کرده و سپس ورود شوید.", None
    else:
        cursor.close()
        conn.close()
        return False, "اطلاعات دریافتی شما دچار مشکل شده لطفا یکبار خروج کرده و سپس ورود شوید.", None


@app.post("/bbc_api/signin")
async def signin_api(request: Request):
    method_type = "SIGNIN"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        if action == "signin":
            return signin(conn=conn, cursor=cursor, order_data=order_data["data"])
        else:
            print("signin action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        print(">>>> endpoint log error", e)
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/signin", "signin_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        print(">>>> endpoint log error", e)
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/signin", "signin_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/bbc_api/insert_request")
async def insert_api(request: Request):
    method_type = "INSERT"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["UPDATE", "SELECT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "add_consultant":
            return add_consultant(conn, cursor, order_data["data"], info)
        elif action == "add_student":
            return add_student(conn, cursor, order_data["data"], info)
        else:
            print("insert action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        print(">>>> endpoint log error", e)
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/insert_request", "insert_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        print(">>>> endpoint log error", e)
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/insert_request", "insert_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/bbc_api/update_request")
async def update_api(request: Request):
    method_type = "UPDATE"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["SELECT", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "update_user":
            return update_user(conn, cursor, order_data["data"], info)
        elif action == "update_consultant":
            return update_consultant(conn, cursor, order_data["data"], info)
        elif action == "update_student_info":
            return update_student_info(conn, cursor, order_data["data"], info)
        elif action == "update_student_consult":
            return update_student_consult(conn, cursor, order_data["data"], info)
        elif action == "update_password":
            return update_password(conn, cursor, order_data["data"], info)
        elif action == "update_student_access":
            return update_student_access(conn, cursor, order_data["data"], info)
        elif action == "update_ag_access":
            return update_ag_access(conn, cursor, order_data["data"], info)
        elif action == "update_permission":
            return update_student_permission(conn, cursor, order_data["data"], info)
        else:
            print("update action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/update_request", "update_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/update_request", "update_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


# todo here not checked and not refactor
@app.post("/bbc_api/select_request")
async def select_api(request: Request):
    method_type = "SELECT"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["UPDATE", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "select_dashboard_info":
            return new_dash(conn, cursor, order_data["data"], info)
        elif action == "select_consultants":
            return select_con_list(conn, cursor, order_data["data"], info)
        elif action == "select_cons_stu":
            return select_cons_stu(conn, cursor, order_data["data"], info)
        elif action == "select_students":
            return select_stu_list(conn, cursor, order_data["data"], info)
        elif action == "select_student_data":
            return select_stu_data(conn, cursor, order_data["data"], info)
        elif action == "select_students_pf":
            return select_stu_pf_list(conn, cursor, order_data["data"], info)
        elif action == "select_report":
            return select_stu_report_list(conn, cursor, order_data["data"], info)
        # elif action == "select_student_info":
        #     return select_stu_info(conn, cursor, order_data["data"], info)
        # elif action == "select_student_field_info":
        #     return select_student_field_info(conn, cursor, order_data["data"], info)
        # elif action == "select_student_field_info_pdf":
        #     return select_student_field_info_pdf(conn, cursor, order_data["data"], info)
        ######
        elif action == "select_student_info":
            return student_info(conn, cursor, order_data["data"], info)
        else:
            print("select action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/select_request", "select_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/select_request", "select_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/bbc_api/delete_request")
async def delete_api(request: Request):
    method_type = "DELETE"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["SELECT", "INSERT", "UPDATE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "delete_token":
            return delete_token(conn, cursor, order_data["data"], info)
        else:
            print("delete action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/delete_request", "delete_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/delete_request", "delete_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/fieldpick_api/update_request")
async def update_api(request: Request):
    method_type = "UPDATE"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["SELECT", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "update_spfr_list":
            return update_spfr_list(conn, cursor, order_data["data"], info)
        elif action == "update_trfr_list":
            return update_trfr_list(conn, cursor, order_data["data"], info)
        elif action == "update_spfrb_list":
            return update_spfrb_list(conn, cursor, order_data["data"], info)
        elif action == "update_trfrb_list":
            return update_trfrb_list(conn, cursor, order_data["data"], info)
        else:
            print("update action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "fieldpick_api/update_request", "update_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "fieldpick_api/update_request", "update_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/fieldpick_api/select_request")
async def select_api(request: Request):
    method_type = "SELECT"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["UPDATE", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        action = order_data["method_type"]
        if action == "fp_majors":
            return fp_majors(conn, cursor, order_data["data"], info)
        elif action == "fp_universities":
            return fp_universities(conn, cursor, order_data["data"], info)
        elif action == "fp_cities":
            return fp_cities(conn, cursor, order_data["data"], info)
        elif action == "fp_provinces":
            return fp_provinces(conn, cursor, order_data["data"], info)
        elif action == "fp_exam_types":
            return fp_exam_types(conn, cursor, order_data["data"], info)
        elif action == "fp_search_fields":
            return fp_search_fields(conn, cursor, order_data["data"], info)

        elif action == "fr_majors":
            return fr_majors(conn, cursor, order_data["data"], info)
        elif action == "fr_provinces":
            return fr_provinces(conn, cursor, order_data["data"], info)
        elif action == "fr_universities":
            return fr_universities(conn, cursor, order_data["data"], info)
        elif action == "fr_search_fields":
            return fr_search_fields(conn, cursor, order_data["data"], info)

        elif action == "select_spfr_list":
            return select_spfr_list(conn, cursor, order_data["data"], info)
        elif action == "select_trfr_list":
            return select_trfr_list(conn, cursor, order_data["data"], info)

        elif action == "frb_majors":
            return frb_majors(conn, cursor, order_data["data"], info)
        elif action == "frb_provinces":
            return frb_provinces(conn, cursor, order_data["data"], info)
        elif action == "frb_universities":
            return frb_universities(conn, cursor, order_data["data"], info)
        elif action == "frb_search_fields":
            return frb_search_fields(conn, cursor, order_data["data"], info)

        elif action == "select_spfrb_list":
            return select_spfrb_list(conn, cursor, order_data["data"], info)
        elif action == "select_trfrb_list":
            return select_trfrb_list(conn, cursor, order_data["data"], info)
        else:
            print("select action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "fieldpick_api/select_request", "select_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "fieldpick_api/select_request", "select_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/quiz_api/update_request")
async def update_api(request: Request):
    method_type = "UPDATE"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["SELECT", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "update_quiz_answer":
            return update_quiz_answer(conn, cursor, order_data["data"], info)
        else:
            print("update action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "quiz_api/update_request", "update_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "quiz_api/update_request", "update_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/quiz_api/select_request")
async def select_api(request: Request):
    method_type = "SELECT"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["UPDATE", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        action = order_data["method_type"]
        if action == "select_quiz_table_info":
            return select_quiz_table_info(conn, cursor, order_data["data"], info)
        elif action == "select_quiz_info":
            return select_quiz_info(conn, cursor, order_data["data"], info)
        else:
            print("select action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "quiz_api/select_request", "select_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "quiz_api/select_request", "select_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/hoshmand_api/update_request")
async def update_api(request: Request):
    method_type = "UPDATE"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["SELECT", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        action = order_data["method_type"]
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        if action == "update_hoshmand_info":
            return update_hoshmand_info(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_questions":
            return update_hoshmand_questions(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_examtype":
            return update_hoshmand_examtype(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_major":
            return update_hoshmand_major(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_province":
            return update_hoshmand_province(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_tables":
            return update_hoshmand_tables(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_chains":
            return update_hoshmand_chains(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_fields":
            return update_hoshmand_fields(conn, cursor, order_data["data"], info)
        elif action == "update_hoshmand_sp_list":
            return update_hoshmand_sp_list(conn, cursor, order_data["data"], info)
        else:
            print("update action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "hoshmand_api/update_request", "update_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "hoshmand_api/update_request", "update_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/hoshmand_api/select_request")
async def select_api(request: Request):
    method_type = "SELECT"
    try:
        order_data = await request.json()
        conn, cursor = await db_connection()
        if "method_type" in order_data:
            method = order_data["method_type"]
            if method.upper() in ["UPDATE", "INSERT", "DELETE"]:
                return {"status": 200, "tracking_code": None, "method_type": method_type,
                        "error": "شما دسترسی به این سرویس‌ را ندارید."}
        if "data" not in order_data.keys():
            return {"status": 200, "tracking_code": None, "method_type": method_type,
                    "error": "اطلاعات از سمت شما ارسال نشده است."}
        state, state_message, info = await check(conn, cursor, order_data["data"])
        if not state:
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        action = order_data["method_type"]
        if action == "select_hoshmand_info":
            return select_hoshmand_info(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_questions":
            return select_hoshmand_questions(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_examtype":
            return select_hoshmand_examtype(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_major":
            return select_hoshmand_major(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_province":
            return select_hoshmand_province(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_tables":
            return select_hoshmand_tables(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_chains":
            return select_hoshmand_chains(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_chain_code":
            return select_hoshmand_chain_code(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_fields":
            return select_hoshmand_fields(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_sp_list":
            return select_hoshmand_sp_list(conn, cursor, order_data["data"], info)
        elif action == "select_hoshmand_list":
            return select_hoshmand_list(conn, cursor, order_data["data"], info)
        else:
            print("select action >>>>>>>>>>>>>>>>>>>>", action)
            return {"status": 405, "tracking_code": None, "method_type": None,
                    "error": "سرویس مورد نظر در دسترس نیست."}
    except KeyError as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "hoshmand_api/select_request", "select_api",
            None, str("%s با اطلاعات شما ارسال نشده است." % str(e)))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 401, "tracking_code": None, "method_type": method_type,
                "error": "%s با اطلاعات شما ارسال نشده است." % str(e)}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "hoshmand_api/select_request", "select_api",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 500, "tracking_code": None, "method_type": None,
                "error": "مشکلی در ارتباط با سرویس‌ها پیش آمده است. درحال بررسی هستیم."}


@app.post("/bbc_api/update_user_ins_file")
async def update_user_ins_file(
        pic: UploadFile = Form(...),
        name: str = Form(...),
        last_pic: str = Form(...),
        token: str = Form(...),
):
    try:
        conn, cursor = await db_connection()
        order_data = {"token": token}
        state, state_message, info = await check(conn, cursor, order_data)
        if not state:
            cursor.close()
            conn.close()
            return {"status": 404, "tracking_code": None, "method_type": "AUTH",
                    "error": state_message}
        generate_random_name = str(uuid.uuid4())
        new_file_name = generate_random_name + "." + pic.filename.split(".")[1]
        pic.filename = new_file_name
        file_path = f"D:/WebSites/BBC/Media/InsPic/{pic.filename}"
        last_path = f"D:/WebSites/BBC/Media/InsPic/{last_pic}"
        data = {"name": name, "pic": pic.filename}
        if info.get("role") == "ins":
            token, data, message = update_user_ins_pic(conn, cursor, data, info)
        else:
            cursor.close()
            conn.close()
            return {"status": 200, "tracking_code": None, "method_type": "AUTH",
                    "error": "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."}
        if os.path.exists(last_path):
            os.remove(last_path)
        else:
            print("The file does not exist")
        with open(file_path, "wb") as file_object:
            file_object.write(pic.file.read())
        if token:
            return {"status": 200, "tracking_code": token, "method_type": "UPDATE",
                    "response": {"data": data, "message": message}}
        else:
            return {"status": 200, "tracking_code": None, "method_type": "UPDATE",
                    "error": "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."}
    except Exception as e:
        conn, cursor = await db_connection()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            None, None, "bbc_api/update_user_ins_file", "update_user_ins_file",
            None, str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='api_logs', fields=field_log,
                               values=values_log)
        cursor.close()
        conn.close()
        return {"status": 200, "tracking_code": None, "method_type": "UPDATE",
                "error": "متاسفانه برای تغییر اطلاعات شما مشکلی پیش آمده با پشتیبانی ارتباط بگیرید."}


@app.get("/bbc_api/get_user_pic/{filename}")
async def get_user_pic(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Media/InsPic/' + filename)
    return FileResponse(file_path, filename=filename)


@app.get("/bbc_api/pdf_notebook/{filename}")
async def get_pdf_notebook(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Docs/' + filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/bbc_api/notebook_image/{filename}")
async def get_notebook_pic(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Pics/NoteBook/' + filename)
    return FileResponse(file_path, filename=filename)


@app.get("/bbc_api/get_pic_info/field/{filename}")
async def get_pic_info_field(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Pics/Field/' + filename)
    return FileResponse(file_path, filename=filename)


@app.get("/quiz_api/get_report_student/{phone}")
async def get_report(phone: str):
    conn, cursor = await db_connection()
    query = 'SELECT user_id FROM stu WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is None:
        raise HTTPException(status_code=320, detail="این دانش‌آموز موجود نیست.")
    else:
        # if res[1] == 0:
        #     raise HTTPException(status_code=323,
        #                         detail="شما به کارنامه‌ی خود دسترسی ندارید موضوع را از مشاور خود پیگیری نمایید.")
        query = 'SELECT quiz_id, state FROM quiz_answer WHERE user_id = ? order by edited_time desc'
        res_score = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=res[0])
        if len(res_score) < 7:
            raise HTTPException(status_code=321, detail="در حال حاضر آزمون‌های شما به پایان نرسیده است.")
        else:
            if res_score[-1][1] != 2:
                raise HTTPException(status_code=321, detail="در حال حاضر آزمون‌های شما به پایان نرسیده است.")
    file_path = os.path.join('D:/WebSites/BBC/Reports/', phone, 'Report.pdf')
    folder_check = os.path.join('D:/WebSites/BBC/Reports/', phone)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="Report.pdf")
    else:
        if os.path.exists(folder_check):
            raise HTTPException(status_code=322, detail="در حال حاضر آزمون‌های شما به پایان نرسیده است.")
        else:
            raise HTTPException(status_code=404, detail="File not found")


@app.get("/quiz_api/get_pic_info/quiz/{filename}")
async def get_pic_info_field(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Pics/Quiz/' + filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/quiz_api/get_quiz_pic/{filename}")
async def get_quiz_pic(filename: str):
    file_path = os.path.join('D:/WebSites/BBC/Quiz/' + filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/quiz_api/get_voice/{filename}")
async def get_voice(filename: str):
    file_path = os.path.join('D:/WebSites/NewER/Voices/' + filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")
