import json
import time
import uuid
from datetime import datetime

from Helper import db_helper
from Helper.func_helper import delete_unneeded_table, update_step_hoshmand
from Users.Student.student import select_student_info

uni_info = ["دانشگاه‌های شاخص سراسر کشور", "دانشگاه‌های برتر استان(های) بومی", "سایر دانشگاه‌های استان(های) بومی",
            "دانشگاه‌های برتر استان‌های همسایه", "سایر دانشگاه‌های استان‌های همسایه",
            "دانشگاه‌های برتر استان‌های نزدیک", "سایر دانشگاه‌های استان‌های نزدیک",
            "دانشگاه‌های برتر استان‌های با فاصله زیاد", "سایر دانشگاه‌های استان‌های با فاصله زیاد",
            "دانشگاه‌های برتر دیگر استان‌های کشور", "سایر دانشگاه‌های دیگر استان‌های کشور"]
major_info = ["رشته‌های اولویت ۱", "رشته‌های اولویت ۲", "رشته‌های اولویت ۳", "رشته‌های اولویت ۴"]


def change_hoshmand_info(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_info 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [terms_accepted], [current_step])'
            values = (
                data["stu_id"], stu_phone, data["terms_accepted"], data["current_step"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_info', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_info",
                ['terms_accepted', 'current_step', 'edited_time'],
                [data["terms_accepted"], data["current_step"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
        token = str(uuid.uuid4())
        return token, {"terms_accepted": data["terms_accepted"],
                       "current_step": data["current_step"]}, "اطلاعات ذخیره شد"
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_info",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, "مشکلی در دریافت اطلاعات رخ داده است."


def change_hoshmand_questions(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_questions 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [examtype], [univercity], [major], [obligation], [method])'
            values = (
                data["stu_id"], stu_phone, data["examtype"], data["univercity"], data["major"],
                data["obligation"], data["method"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_questions', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_questions",
                ['examtype', 'univercity', 'major', 'obligation', 'method', 'edited_time'],
                [data["examtype"], data["univercity"], data["major"],
                 data["obligation"], data["method"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(
                conn, cursor,
                ["hoshmand_examtype", "hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities",
                 "hoshmand_chains", "hoshmand_fields"], data["stu_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_questions",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_examtype(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_examtype 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [examtypes])'
            values = (
                data["stu_id"], stu_phone, json.dumps(data["data"], ensure_ascii=False),
                data["examtypes"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_examtype', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_examtype",
                ['data', 'examtypes', 'edited_time'],
                [json.dumps(data["data"], ensure_ascii=False), data["examtypes"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(
                conn, cursor,
                ["hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                 "hoshmand_fields"], data["stu_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_examtype",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_major(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_major 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [majors], [major1], [major2], [major3], [major4])'
            values = (
                data["stu_id"], stu_phone, json.dumps(data["data"], ensure_ascii=False),
                data["majors"], data["major1"], data["major2"], data["major3"], data["major4"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_major', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_major",
                ['data', 'majors', 'major1', 'major2', 'major3', 'major4', 'edited_time'],
                [json.dumps(data["data"], ensure_ascii=False), data["majors"], data["major1"],
                 data["major2"], data["major3"], data["major4"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                                   "hoshmand_fields"], data["stu_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_major",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_province(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_province 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [province1], [province2], [province3], [province4], [province5], [province6])'
            values = (
                data["stu_id"], stu_phone, json.dumps(data["data"], ensure_ascii=False),
                data["province1"], data["province2"], data["province3"], data["province4"], data["province5"],
                data["province6"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_province', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_province",
                ['data', 'province1', 'province2', 'province3', 'province4', 'province5', 'province6', 'edited_time'],
                [json.dumps(data["data"], ensure_ascii=False), data["province1"],
                 data["province2"], data["province3"], data["province4"], data["province5"],
                 data["province6"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                                   "hoshmand_fields"], data["stu_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_province",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_tables(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                SELECT 
                    *
                FROM hoshmand_tables 
                WHERE user_id = ?
            '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data_table1], [data_table2])'
            values = (
                data["stu_id"], stu_phone, json.dumps(data["skills"], ensure_ascii=False),
                json.dumps(data["universities"], ensure_ascii=False))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_tables', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_tables",
                ['data_table1', 'data_table2', 'edited_time'],
                [json.dumps(data["skills"], ensure_ascii=False),
                 json.dumps(data["universities"], ensure_ascii=False),
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_chains", "hoshmand_fields"], data["stu_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_tables",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_chains(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                SELECT 
                    *
                FROM hoshmand_chains 
                WHERE user_id = ?
            '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [chains], [majors], [universities], [deleted_chains])'
            values = (
                data["stu_id"], stu_phone, json.dumps(data["chains"], ensure_ascii=False),
                data['majors'], data['universities'], json.dumps(data["deleted_chains"], ensure_ascii=False))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_chains', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_chains",
                ['chains', 'majors', 'universities', 'deleted_chains', 'edited_time'],
                [json.dumps(data["chains"], ensure_ascii=False), data['majors'], data['universities'],
                 json.dumps(data["deleted_chains"], ensure_ascii=False),
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_fields"], data["stu_id"])

        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_chains",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_fields(conn, cursor, data, info, stu_phone):
    try:
        db_helper.update_record(
            conn, cursor, "hoshmand_fields",
            ['field_list', 'selected_list', 'edited_time'],
            [json.dumps(data["fields_list"], ensure_ascii=False),
             json.dumps(data["selected_list"], ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [str(data["stu_id"])]
        )
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_fields",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_sp_list(conn, cursor, data, info, stu_phone):
    try:
        db_helper.update_record(
            conn, cursor, "hoshmand_fields",
            ['selected_list', 'trash_list', 'edited_time'],
            [json.dumps(data["selected_list"], ensure_ascii=False),
             json.dumps(data["trash_list"], ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [str(data["stu_id"])]
        )
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "change_hoshmand_sp_list",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def get_hoshmand_info(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        terms_accepted,
                        current_step
                    FROM hoshmand_info 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone])'
            values = (
                data["stu_id"], stu_phone)
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_info', fields=field,
                                   values=values)
        info_response = {
            "terms_accepted": hoshmand_data.terms_accepted if hoshmand_data and hoshmand_data.terms_accepted else 0,
            "current_step": hoshmand_data.current_step if hoshmand_data and hoshmand_data.current_step else 1,
        }
        token = str(uuid.uuid4())
        return token, info_response
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_info",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None


def get_hoshmand_questions(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                SELECT 
                    examtype,
                    univercity,
                    major,
                    obligation,
                    method
                FROM hoshmand_questions 
                WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [examtype], [univercity], [major], [obligation], [method])'
            values = (
                data["stu_id"], stu_phone, 3, 3, 3,
                '0,1', 'با آزمون,صرفا با سوابق تحصیلی')
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_questions', fields=field,
                                   values=values)
        info_response = {
            "examtype": hoshmand_data.examtype if hoshmand_data and hoshmand_data.examtype else 3,
            "univercity": hoshmand_data.univercity if hoshmand_data and hoshmand_data.univercity else 3,
            "major": hoshmand_data.major if hoshmand_data and hoshmand_data.major else 3,
            "obligation": hoshmand_data.obligation if hoshmand_data else '0,1',
            "method": hoshmand_data.method if hoshmand_data else 'با آزمون,صرفا با سوابق تحصیلی',
        }
        update_step_hoshmand(conn, cursor, 1, data["stu_id"])
        token = str(uuid.uuid4())
        return token, info_response
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_questions",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None


def get_hoshmand_examtype(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        data,
                        examtypes
                    FROM hoshmand_examtype 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        query_question = 'select obligation, method from hoshmand_questions where user_id = ?'
        question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=data["stu_id"])
        query_student = 'select sex, field, city, rank_zaban, rank_honar from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        field = str(student.field)
        if student.rank_zaban != 0 and student.rank_zaban:
            field += "," + str(4)
        if student.rank_honar != 0 and student.rank_honar:
            field += "," + str(5)
        exam_types = []
        sql = 'exec Note.smart.Get_TypeExamTurns_new ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, student.sex, student.city.split(",")[0], None, 1404, str(question.obligation), str(question.method)
        )
        recs = []
        is_empty = 0
        try:
            cursor.execute(sql, values)
            recs = cursor.fetchall()
            cursor.commit()
        except Exception as e:
            is_empty = 2
            field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
            values_log = (
                data["stu_id"], stu_phone, "Get_TypeExamTurns_new", json.dumps(values, ensure_ascii=False),
                json.dumps(data, ensure_ascii=False), str(e))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                   values=values_log)
        if len(recs) == 0:
            is_empty = 1
        for res in recs:
            exam_types.append(res[0])
        if not hoshmand_data:
            user_data = None
        else:
            user_data = json.loads(hoshmand_data[0])
        update_step_hoshmand(conn, cursor, 2, data["stu_id"])
        token = str(uuid.uuid4())
        return token, is_empty, exam_types, user_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_examtype",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, 2, None, None


def get_hoshmand_major(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        data,
                        majors
                    FROM hoshmand_major 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        query_examtypes = '''
                    SELECT 
                        examtypes
                    FROM hoshmand_examtype 
                    WHERE user_id = ?
                    '''
        hoshmand_examtypes = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtypes,
                                                    field=data["stu_id"])
        query_question = 'select obligation, method from hoshmand_questions where user_id = ?'
        question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=data["stu_id"])
        query_student = 'select sex, field, city, rank_zaban, rank_honar from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        majors = []
        field = str(student.field)
        if student.rank_zaban != 0 and student.rank_zaban:
            field += "," + str(4)
        if student.rank_honar != 0 and student.rank_honar:
            field += "," + str(5)
        sql = 'exec Note.smart.Get_Majors_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, student.sex, student.city.split(",")[0], hoshmand_examtypes.examtypes, None, 1404,
            str(question.obligation),
            str(question.method), None, None
        )
        recs = []
        try:
            cursor.execute(sql, values)
            recs = cursor.fetchall()
            cursor.commit()
        except Exception as e:
            field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
            values_log = (
                data["stu_id"], stu_phone, "Get_Majors_new", json.dumps(values, ensure_ascii=False),
                json.dumps(data, ensure_ascii=False), str(e))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                   values=values_log)
        for res in recs:
            majors.append(res[0])
        if not hoshmand_data:
            user_data = None
        else:
            user_data = json.loads(hoshmand_data.data)
        update_step_hoshmand(conn, cursor, 3, data["stu_id"])
        token = str(uuid.uuid4())
        return token, majors, hoshmand_examtypes.examtypes
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_major",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None


def get_hoshmand_province(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        data
                    FROM hoshmand_province 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        query_student = 'select sex, field, city, rank_zaban, rank_honar from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        majors = []
        if not hoshmand_data:
            query_majors = 'select majors from hoshmand_major where user_id = ?'
            majors_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_majors, field=data["stu_id"])
            query_examtype = 'select examtypes from hoshmand_examtype where user_id = ?'
            examtype_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtype, field=data["stu_id"])
            query_question = 'select obligation, method from hoshmand_questions where user_id = ?'
            question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=data["stu_id"])
            field = str(student.field)
            if student.rank_zaban != 0 and student.rank_zaban:
                field += "," + str(4)
            if student.rank_honar != 0 and student.rank_honar:
                field += "," + str(5)
            sql = 'exec Note.smart.Get_Provinces_new ?, ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                field, student.sex, student.city.split(",")[0],
                examtype_res.examtypes if examtype_res.examtypes else None,
                majors_res.majors if majors_res.majors else None, None, 1404, str(question.obligation),
                str(question.method)
            )
            recs = []
            try:
                cursor.execute(sql, values)
                recs = cursor.fetchall()
                cursor.commit()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Get_Provinces_new", json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            user_data = [
                {
                    "id": "box-1",
                    "title": "استان(های) بومی و محل زندگی شما",
                    "items": [],
                    "readOnly": False,
                },
                {
                    "id": "box-2",
                    "title": "استان‌های همسایه و نزدیک به استان بومی",
                    "items": [],
                    "readOnly": False,
                },
                {
                    "id": "box-3",
                    "title": "استان‌های نزدیک (به لحاظ فرهنگی یا مسافتی)",
                    "items": [],
                    "readOnly": False,
                },
                {
                    "id": "box-4",
                    "title": "استان‌های با فاصله نسبتا زیاد",
                    "items": [],
                    "readOnly": False,
                },
                {
                    "id": "box-5",
                    "title": "سایر استان‌های کل کشور که ممکن است بروید",
                    "items": [],
                    "readOnly": False,
                },
                {
                    "id": "box-6",
                    "title": "استان‌هایی که به هیچ عنوان در آن‌ها تحصیل نخواهید کرد",
                    "items": [],
                    "readOnly": False,
                },
            ]
            for item in recs:
                if 0 <= item[1] <= 4:
                    user_data[item[1]]["items"].append(item[0])
            province1 = ",".join(user_data[0]["items"])
            province2 = ",".join(user_data[1]["items"])
            province3 = ",".join(user_data[2]["items"])
            province4 = ",".join(user_data[3]["items"])
            province5 = ",".join(user_data[4]["items"])

            field = '([user_id], [phone], [data], [province1], [province2], [province3], [province4], [province5], [province6])'
            values = (
                data["stu_id"], stu_phone, json.dumps(user_data, ensure_ascii=False), province1,
                province2, province3, province4, province5, ""
            )
            db_helper.insert_value(
                conn=conn,
                cursor=cursor,
                table_name='hoshmand_province',
                fields=field,
                values=values
            )
        else:
            user_data = json.loads(hoshmand_data.data)
        update_step_hoshmand(conn, cursor, 4, data["stu_id"])
        token = str(uuid.uuid4())
        return token, majors, user_data
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_province",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None


def get_hoshmand_tables(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        data_table1,
                        data_table2
                    FROM hoshmand_tables 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        query_student = 'select sex, field, city, rank_zaban, rank_honar, lock from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        if student.lock == 0:
            return None, None, None, None, 0
        query_examtype = 'select examtypes from hoshmand_examtype where user_id = ?'
        examtypes_result = db_helper.search_table(conn=conn, cursor=cursor, query=query_examtype, field=data["stu_id"])
        exam_types = examtypes_result.examtypes.split(',') if examtypes_result and examtypes_result.examtypes else []
        query_question = 'select obligation, method from hoshmand_questions where user_id = ?'
        question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=data["stu_id"])
        if not hoshmand_data:
            field_state = str(student.field)
            if student.rank_zaban != 0 and student.rank_zaban:
                field_state += "," + str(4)
            if student.rank_honar != 0 and student.rank_honar:
                field_state += "," + str(5)
            query_majors = 'select major1, major2, major3, major4, majors from hoshmand_major where user_id = ?'
            majors = db_helper.search_table(conn=conn, cursor=cursor, query=query_majors, field=data["stu_id"])
            sql = 'exec Note.smart.Get_Major_TypeExamTurn_Block_States_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                field_state, student.sex, student.city.split(",")[0],
                examtypes_result.examtypes if examtypes_result else None,
                majors.major1, majors.major2, majors.major3, majors.major4, 1404, str(question.obligation),
                str(question.method)
            )
            recs = []
            try:
                cursor.execute(sql, values)
                recs = cursor.fetchall()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Get_Major_TypeExamTurn_Block_States_new",
                    json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            num_skill_categories = 4
            skills_table = [
                {"name": major_info[i], "values": [0] * len(exam_types), "data": majors[i]}
                for i in range(num_skill_categories)
            ]
            exam_type_index = {exam_type: idx for idx, exam_type in enumerate(exam_types)}
            for exam_type, category in recs:
                if exam_type in exam_type_index and 1 <= category <= num_skill_categories:
                    exam_idx = exam_type_index[exam_type]
                    skills_table[category - 1]["values"][exam_idx] = 1
            query_province = 'select province1, province2, province3, province4, province5 from hoshmand_province where user_id = ?'
            province = db_helper.search_table(conn=conn, cursor=cursor, query=query_province, field=data["stu_id"])
            sql = 'exec Note.smart.Get_University_Blocks_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                field_state, student.sex,
                examtypes_result.examtypes if examtypes_result else None,
                majors.majors, student.city.split(",")[0], province.province1, province.province2, province.province3,
                province.province4, province.province5,
                1404,
                str(question.obligation), str(question.method)
            )
            recs_majors = []
            try:
                cursor.execute(sql, values)
                recs_majors = cursor.fetchall()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Get_University_Blocks_new", json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            num_uni_categories = 11
            universities_table = [
                {"name": uni_info[i], "values": [0] * len(exam_types), "data": ""}
                for i in range(num_uni_categories)
            ]

            uni_dict = {}
            for category, uni_name, city in recs_majors:
                if 1 <= category <= num_uni_categories:
                    if category not in uni_dict:
                        uni_dict[category] = []
                    uni_dict[category].append(uni_name)

            uni = [""] * 11
            for category in uni_dict:
                if 1 <= category <= 11:
                    uni[category - 1] = ",".join(uni_dict[category])
                    universities_table[category - 1]["data"] = uni[category - 1]
            query_uni = 'select id from hoshmand_universities where user_id = ?'
            uni_res = db_helper.search_table(conn=conn, cursor=cursor, query=query_uni, field=data["stu_id"])
            if uni_res:
                db_helper.delete_record(
                    conn, cursor, 'hoshmand_universities',
                    ["user_id"],
                    [str(data["stu_id"])]
                )
            field = '([user_id], [phone], [uni1], [uni2], [uni3], [uni4], [uni5], [uni6], [uni7], [uni8], [uni9], [uni10], [uni11])'
            values = (
                data["stu_id"], stu_phone, uni[0], uni[1], uni[2], uni[3], uni[4], uni[5], uni[6], uni[7], uni[8],
                uni[9], uni[10])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_universities', fields=field,
                                   values=values)
            sql = 'exec Note.smart.Get_University_TypeExamTurn_Block_States_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                field_state, student.sex, student.city.split(",")[0],
                examtypes_result.examtypes if examtypes_result else None,
                uni[0], uni[1], uni[2], uni[3], uni[4], uni[5], uni[6], uni[7], uni[8], uni[9], uni[10], 1404,
                str(question.obligation), str(question.method)
            )
            recs_data = []
            try:
                cursor.execute(sql, values)
                recs_data = cursor.fetchall()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Get_University_TypeExamTurn_Block_States_new",
                    json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            for exam_type, category in recs_data:
                if exam_type in exam_type_index and 1 <= category <= num_uni_categories:
                    exam_idx = exam_type_index[exam_type]
                    universities_table[category - 1]["values"][exam_idx] = 1
            field = '([user_id], [phone], [data_table1], [data_table2])'
            values = (
                data["stu_id"], stu_phone, json.dumps(skills_table, ensure_ascii=False),
                json.dumps(universities_table, ensure_ascii=False)
            )
            db_helper.insert_value(
                conn=conn,
                cursor=cursor,
                table_name='hoshmand_tables',
                fields=field,
                values=values
            )
        else:
            universities_table = json.loads(hoshmand_data.data_table2)
            skills_table = json.loads(hoshmand_data.data_table1)
        update_step_hoshmand(conn, cursor, 5, data["stu_id"])
        token = str(uuid.uuid4())
        return token, skills_table, universities_table, exam_types, student.lock
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_tables",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None, None, None


def get_hoshmand_chains(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                   SELECT 
                       chains,
                       deleted_chains
                   FROM hoshmand_chains 
                   WHERE user_id = ?
                   '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            query_student = 'select sex, field, city, rank_zaban, rank_honar, quota from stu where user_id = ?'
            student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
            query_question = 'select obligation, method, univercity, major from hoshmand_questions where user_id = ?'
            question = db_helper.search_table(conn=conn, cursor=cursor, query=query_question, field=data["stu_id"])
            field = str(student.field)
            if student.rank_zaban != 0 and student.rank_zaban:
                field += "," + str(4)
            if student.rank_honar != 0 and student.rank_honar:
                field += "," + str(5)
            sorting_major_uni = False
            if question.univercity > question.major:
                sorting_major_uni = True
            sql = 'exec Note.smart.Create_Chanis_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                data["stu_id"], student.quota, field, student.sex,
                student.city.split(",")[0], str(question.obligation), str(question.method), 1404, sorting_major_uni,
                "BBC"
            )
            recs = []
            try:
                cursor.execute(sql, values)
                recs = cursor.fetchall()
                cursor.commit()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Create_Chanis_new", json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)

            processed_chains = []
            deleted_chains = []
            if recs:
                combined_json = ''.join([part for tup in recs for part in tup])
                try:
                    parsed_data = json.loads(combined_json)
                    processed_chains = parsed_data.get('results', [])
                except json.JSONDecodeError as e:
                    try:
                        fixed_json = combined_json.replace('",', '",').replace('", "', '", "')
                        parsed_data = json.loads(fixed_json)
                        processed_chains = parsed_data.get('results', [])
                    except:
                        processed_chains = []
            field = '([user_id], [phone], [chains], [deleted_chains])'
            values = (
                data["stu_id"], stu_phone, json.dumps(processed_chains, ensure_ascii=False),
                json.dumps([], ensure_ascii=False))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_chains', fields=field,
                                   values=values)

        else:
            processed_chains = json.loads(hoshmand_data.chains)
            deleted_chains = json.loads(
                hoshmand_data.deleted_chains) if hoshmand_data and hoshmand_data.deleted_chains else []
        update_step_hoshmand(conn, cursor, 6, data["stu_id"])
        token = str(uuid.uuid4())
        return token, processed_chains, deleted_chains
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_chains",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None


def get_hoshmand_chain_code(conn, cursor, data, info, stu_phone):
    try:
        query_student = 'select sex, field, city, rank, quota, rank_zaban, rank_honar from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        fields = []
        field = str(student.field)
        if student.rank_zaban != 0 and student.rank_zaban:
            field += "," + str(4)
        if student.rank_honar != 0 and student.rank_honar:
            field += "," + str(5)
        sql = 'exec Note.smart.Get_Chain_Fields_new ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, student.quota, data["codes"], student.rank,
            1, 1000, 1404, None, None, None
        )
        recs = []
        try:
            cursor.execute(sql, values)
            recs = cursor.fetchall()
            cursor.commit()
        except Exception as e:
            field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
            values_log = (
                data["stu_id"], stu_phone, "Get_Chain_Fields_new", json.dumps(values, ensure_ascii=False),
                json.dumps(data, ensure_ascii=False), str(e))
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                   values=values_log)

        for res in recs:
            cap = res[19]
            if res[19] is None:
                cap = res[20]
            response = {
                'filedCode': res[1], 'field': res[7], 'city': res[5] + "-" + res[6], 'university': res[8],
                'admission': res[10],
                'kind': res[11],
                'obligation': res[13], 'period': res[12],
                'explain': res[14], 'admissionKind': res[21],
                'capacity': cap,
            }
            fields.append(response)
        token = str(uuid.uuid4())
        return token, fields
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_chain_code",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None


def get_hoshmand_fields(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                    SELECT 
                        all_list,
                        field_list,
                        selected_list, 
                        is_hoshmand
                    FROM hoshmand_fields 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if not hoshmand_data:
            query_student = 'select sex, field, city, rank, quota, rank_zaban, rank_honar from stu where user_id = ?'
            student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
            query = 'SELECT suggested, other FROM hedayat_fields WHERE user_id = ?'
            res_hedayat = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
            suggested_fields = None
            other_fields = None
            if res_hedayat is not None:
                suggested_fields = res_hedayat.suggested
                other_fields = res_hedayat.other
            field = str(student.field)
            if student.rank_zaban != 0 and student.rank_zaban:
                field += "," + str(4)
            if student.rank_honar != 0 and student.rank_honar:
                field += "," + str(5)
            fields = []
            sql = 'exec Note.smart.Get_Fields_By_Chains_new ?, ?, ?, ?, ?, ?, ?, ?'
            values = (
                data["stu_id"], field, student.quota, student.rank, 1404, suggested_fields, other_fields, "BBC"
            )
            recs = []
            try:
                cursor.execute(sql, values)
                recs = cursor.fetchall()
                cursor.commit()
            except Exception as e:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Get_Fields_By_Chains_new", json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            for res in recs:
                cap = res.FirstSemesterCapacity
                if res.FirstSemesterCapacity is None:
                    cap = res.SecondSemesterCapacity
                response = {
                    'filedCode': res.CodeReshteh, 'field': res.Major,
                    'city': res.EducationProvince + "-" + res.EducationCity,
                    'university': res.University,
                    'admission': res.AdmissionTurn, 'kind': res.Method,
                    'obligation': res.Obligation, 'period': res.TypeExamTurn,
                    'explain': res.Description, 'admissionKind': res.Acceptance,
                    'capacity': cap,
                    'hedayat': None if res_hedayat is None else res.HedayatRank
                }
                fields.append(response)
            try:
                field_json = json.dumps(fields, ensure_ascii=False)
                empty_list_json = json.dumps([], ensure_ascii=False)
                field_json = str(field_json) if field_json else ''
                empty_list_json = str(empty_list_json) if empty_list_json else ''
                field = '([user_id], [phone], [all_list], [field_list], [selected_list], [trash_list], [hoshmand_list])'
                values = (
                    data["stu_id"],
                    stu_phone,
                    field_json,
                    field_json,
                    empty_list_json,
                    empty_list_json,
                    empty_list_json
                )

                query = f"""
                    INSERT INTO hoshmand_fields {field}
                    VALUES (?, ?, CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)), 
                            CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)), CAST(? AS NVARCHAR(MAX)))
                    """
                cursor.execute(query, values)
                conn.commit()

            except Exception as e:
                print(f"Error inserting record >>>>>>>>>>: {e}")
                conn.rollback()
            selected_list = []
            is_hoshmand = False
        else:
            fields = json.loads(hoshmand_data.field_list)
            selected_list = json.loads(hoshmand_data.selected_list)
            is_hoshmand = True if hoshmand_data.is_hoshmand == 1 else False
        update_step_hoshmand(conn, cursor, 7, data["stu_id"])
        token = str(uuid.uuid4())
        return token, fields, selected_list, is_hoshmand
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_fields",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None, False


def get_hoshmand_sp_list(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                SELECT 
                    selected_list,
                    trash_list, 
                    hoshmand_list
                FROM hoshmand_fields 
                WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        # todo here check user info con ins check
        token, dash_info, message = select_student_info(conn, cursor, info)
        update_step_hoshmand(conn, cursor, 8, data["stu_id"])
        token = str(uuid.uuid4())
        trash_list = json.loads(hoshmand_data.trash_list) if hoshmand_data.trash_list else []
        selected_list = json.loads(hoshmand_data.selected_list)
        hoshmand_list = json.loads(hoshmand_data.hoshmand_list) if hoshmand_data.hoshmand_list else []
        return token, trash_list, selected_list, hoshmand_list, dash_info
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_sp_list",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None, None, None


def get_hoshmand_list(conn, cursor, data, info, stu_phone):
    try:
        query = '''
                SELECT chains
                FROM hoshmand_chains 
                WHERE user_id = ?
            '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        query_student = 'select field, rank, quota, rank_zaban, rank_honar from stu where user_id = ?'
        student = db_helper.search_table(conn=conn, cursor=cursor, query=query_student, field=data["stu_id"])
        field = str(student.field)
        if student.rank_zaban != 0 and student.rank_zaban:
            field += "," + str(4)
        if student.rank_honar != 0 and student.rank_honar:
            field += "," + str(5)
        code_reshteh_list = []
        query = 'SELECT suggested, other FROM hedayat_fields WHERE user_id = ?'
        res_hedayat = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        suggested_fields = None
        other_fields = None
        if res_hedayat is not None:
            suggested_fields = res_hedayat.suggested
            other_fields = res_hedayat.other
        if hoshmand_data and hoshmand_data.chains:
            chain = json.loads(hoshmand_data.chains)
            for group in chain:
                if "CodeReshteh" in group:
                    sorted_data = sorted(group["CodeReshteh"], key=lambda x: x['RowId'])
                    x = [item['CodeReshteh'] for item in sorted_data]
                    code_reshteh_list.extend(x)
        json_code = {"CodeReshteh": code_reshteh_list}
        fields = []
        sql = 'exec Note.smart.Delete_Fields ?, ?, ?, ?, ?, ?'
        values = (
            json.dumps(json_code, ensure_ascii=False), field, student.quota, student.rank, suggested_fields,
            other_fields
        )
        recs = []
        try:
            cursor.execute(sql, values)
            recs = cursor.fetchall()
            cursor.commit()
        except Exception as e:
            try:
                field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
                values_log = (
                    data["stu_id"], stu_phone, "Delete_Fields", json.dumps(values, ensure_ascii=False),
                    json.dumps(data, ensure_ascii=False), str(e))
                db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_sp_logs', fields=field_log,
                                       values=values_log)
            except Exception as e:
                return None, None, None, 0
        try:
            for res in recs:
                cap = res.FirstSemesterCapacity
                if res.FirstSemesterCapacity is None:
                    cap = res.SecondSemesterCapacity
                response = {
                    'filedCode': res.CodeReshteh, 'field': res.Major,
                    'city': res.EducationProvince + "-" + res.EducationCity,
                    'university': res.University,
                    'admission': res.AdmissionTurn,
                    'kind': res.Method,
                    'obligation': res.Obligation, 'period': res.TypeExamTurn,
                    'explain': res.Description, 'admissionKind': res.Acceptance,
                    'capacity': cap,
                    'hedayat': None if res_hedayat is None else res.HedayatRank
                }
                fields.append(response)
            db_helper.update_record(
                conn, cursor, "hoshmand_fields",
                ['is_hoshmand', 'selected_list', 'hoshmand_list', 'edited_time'],
                [1, json.dumps(fields, ensure_ascii=False),
                 json.dumps(fields, ensure_ascii=False),
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(data["stu_id"])]
            )
        except Exception as e:
            print(">>>>>> exception", e)
        try:
            query = '''
                SELECT 
                    all_list,
                    field_list,
                    selected_list, 
                    is_hoshmand
                FROM hoshmand_fields 
                WHERE user_id = ?
                '''
            hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=str(data["stu_id"]))
        except Exception as e:
            print(">>>>>> ", e)
        token = str(uuid.uuid4())
        data = json.loads(hoshmand_data.all_list)
        selected_list = json.loads(hoshmand_data.selected_list)
        return token, data, selected_list, 1
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            data["stu_id"], stu_phone, "hoshmand_api/hoshmand", "get_hoshmand_list",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, None, 0
