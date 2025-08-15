import json
import time
import uuid
from datetime import datetime

from Helper import db_helper
from Helper.func_helper import delete_unneeded_table


def change_hoshmand_info(conn, cursor, data, info):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_info 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [terms_accepted], [current_step])'
            values = (
                info["user_id"], info["phone"], data["terms_accepted"], data["current_step"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_info', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_info",
                ['terms_accepted', 'current_step', 'edited_time'],
                [data["terms_accepted"], data["current_step"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(info["user_id"])]
            )
        token = str(uuid.uuid4())
        return token, {"terms_accepted": data["terms_accepted"],
                       "current_step": data["current_step"]}, "اطلاعات ذخیره شد"
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_info",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, None, "مشکلی در دریافت اطلاعات رخ داده است."


def change_hoshmand_questions(conn, cursor, data, info):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_questions 
                    WHERE user_id = ?
                    '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [examtype], [univercity], [major], [obligation], [method])'
            values = (
                info["user_id"], info["phone"], data["examtype"], data["univercity"], data["major"],
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
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(
                conn, cursor,
                ["hoshmand_examtype", "hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities",
                 "hoshmand_chains", "hoshmand_fields"], info["user_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_questions",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_examtype(conn, cursor, data, info):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_examtype 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [examtypes])'
            values = (
                info["user_id"], info["phone"], json.dumps(data["data"], ensure_ascii=False),
                data["examtypes"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_examtype', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_examtype",
                ['data', 'examtypes', 'edited_time'],
                [json.dumps(data["data"], ensure_ascii=False), data["examtypes"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(
                conn, cursor,
                ["hoshmand_major", "hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                 "hoshmand_fields"], info["user_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_examtype",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_major(conn, cursor, data, info):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_major 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [majors], [major1], [major2], [major3], [major4])'
            values = (
                info["user_id"], info["phone"], json.dumps(data["data"], ensure_ascii=False),
                data["majors"],
                data["major1"],
                data["major2"], data["major3"], data["major4"])
            db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_major', fields=field,
                                   values=values)
        else:
            db_helper.update_record(
                conn, cursor, "hoshmand_major",
                ['data', 'majors', 'major1', 'major2', 'major3', 'major4', 'edited_time'],
                [json.dumps(data["data"], ensure_ascii=False), data["majors"], data["major1"],
                 data["major2"], data["major3"], data["major4"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                                   "hoshmand_fields"], info["user_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_major",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_province(conn, cursor, data, info):
    try:
        query = '''
                    SELECT 
                        *
                    FROM hoshmand_province 
                    WHERE user_id = ?
                '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data], [province1], [province2], [province3], [province4], [province5], [province6])'
            values = (
                info["user_id"], info["phone"], json.dumps(data["data"], ensure_ascii=False),
                data["province1"],
                data["province2"], data["province3"], data["province4"], data["province5"],
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
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_tables", "hoshmand_universities", "hoshmand_chains",
                                   "hoshmand_fields"], info["user_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_province",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_tables(conn, cursor, data, info):
    try:
        query = '''
                SELECT 
                    *
                FROM hoshmand_tables 
                WHERE user_id = ?
            '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [data_table1], [data_table2])'
            values = (
                info["user_id"], info["phone"], json.dumps(data["skills"], ensure_ascii=False),
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
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_chains", "hoshmand_fields"], info["user_id"])
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_tables",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_chains(conn, cursor, data, info):
    try:
        query = '''
                SELECT 
                    *
                FROM hoshmand_chains 
                WHERE user_id = ?
            '''
        hoshmand_data = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
        if not hoshmand_data:
            field = '([user_id], [phone], [chains], [majors], [universities], [deleted_chains])'
            values = (
                info["user_id"], info["phone"], json.dumps(data["chains"], ensure_ascii=False),
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
                "user_id = ?", [str(info["user_id"])]
            )
            delete_unneeded_table(conn, cursor,
                                  ["hoshmand_fields"], info["user_id"])

        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_chains",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_fields(conn, cursor, data, info):
    try:
        db_helper.update_record(
            conn, cursor, "hoshmand_fields",
            ['field_list', 'selected_list', 'edited_time'],
            [json.dumps(data["fields_list"], ensure_ascii=False),
             json.dumps(data["selected_list"], ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [str(info["user_id"])]
        )
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_fields",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."


def change_hoshmand_sp_list(conn, cursor, data, info):
    try:
        db_helper.update_record(
            conn, cursor, "hoshmand_fields",
            ['selected_list', 'trash_list', 'edited_time'],
            [json.dumps(data["selected_list"], ensure_ascii=False),
             json.dumps(data["trash_list"], ensure_ascii=False),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user_id = ?", [str(info["user_id"])]
        )
        token = str(uuid.uuid4())
        return token, "اطلاعات ذخیره شد."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [end_point], [func_name], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "hoshmand_api/hoshmand", "change_hoshmand_sp_list",
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='hoshmand_logs', fields=field_log,
                               values=values_log)
        return None, "مشکلی در دخیره اطلاعات رخ داده است."
