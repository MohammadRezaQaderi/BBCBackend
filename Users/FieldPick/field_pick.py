import uuid
import json

from Helper import db_helper


def get_majors(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        cities = data["cities"]
        university_name = data["universityName"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        native_province = data["nativeProvince"]
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        city = None
        if len(cities) >= 1:
            city = ""
            for i, cit in enumerate(cities):
                if i != len(cities) - 1:
                    city = city + cit + ','
                else:
                    city = city + cit
        sql = 'exec Note.dbo.Get_Majors ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, city, uni_name, sex, native_province, None, None, None, "ALLNOTES")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        majors = []
        tracking_code = str(uuid.uuid4())
        if uni_name is None:
            for res in recs:
                majors.append(res[0])
        else:
            for res in recs:
                majors.append(res[0])
        return tracking_code, majors
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_Majors",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_exam_types(conn, cursor, data, info):
    values = ()
    try:
        cities = data["cities"]
        university_name = data["universityName"]
        majors = data["majors"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        major = None
        if len(majors) > 0:
            major = ""
            for i, mj in enumerate(majors):
                if i != len(majors) - 1:
                    major = major + mj + ','
                else:
                    major = major + mj
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        if second_field != "NULL":
            field = second_field
        city = None
        if len(cities) >= 1:
            city = ""
            for i, cit in enumerate(cities):
                if i != len(cities) - 1:
                    city = city + cit + ','
                else:
                    city = city + cit
        sql = 'exec Note.dbo.Get_TypeExamTurns ?, ?, ?, ?, ?, ?, ?, ?'
        values = (field, city, uni_name, major, sex, None, None, "ALLNOTES")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        exam_types = []
        tracking_code = str(uuid.uuid4())
        if uni_name is None:
            for res in recs:
                exam_types.append(res[0])
        else:
            for res in recs:
                exam_types.append(res[0])
        return tracking_code, exam_types
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_TypeExamTurns",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_universities(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        cities = data["cities"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        native_province = data["nativeProvince"]
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        city = None
        if len(cities) >= 1:
            city = ""
            for i, cit in enumerate(cities):
                if i != len(cities) - 1:
                    city = city + cit + ','
                else:
                    city = city + cit
        sql = 'exec Note.dbo.Get_Universities ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, city, sex, native_province, None, None, None, "ALLNOTES")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        universities = []
        tracking_code = str(uuid.uuid4())
        if cities is None:
            for res in recs:
                universities.append(res[0])
        else:
            for res in recs:
                universities.append(res[0])
        return tracking_code, universities
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_Universities",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_cities(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        field = data["field"]
        second_field = data["secondField"]
        native_province = data["nativeProvince"]
        if second_field != "NULL":
            field = second_field
        cities = None
        if len(provinces) >= 1:
            cities = ""
            for i, province in enumerate(provinces):
                if i != len(provinces) - 1:
                    cities = cities + province + ','
                else:
                    cities = cities + province
        sql = 'exec Note.dbo.Get_Cities ?, ?, ?, ?, ?, ?'
        values = (field, cities, native_province, None, None, "ALLNOTES")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        city = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            city.append(res[0])
        return tracking_code, city
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_Cities",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_provinces(conn, cursor, data, info):
    values = ()
    try:
        field = data["field"]
        second_field = data["secondField"]
        native_province = data["nativeProvince"]
        if second_field != "NULL":
            field = second_field
        sql = 'exec Note.dbo.Get_Provinces ?, ?, ?, ?, ?'
        values = (field, native_province, None, None, "ALLNOTES")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        provinces = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            provinces.append(res[0])

        return tracking_code, provinces
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_Provinces",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def search_fields(conn, cursor, data, info):
    values = ()
    try:
        accept_way = data["acceptWay"]
        provinces = data["provinces"]
        cities = data["cities"]
        university_name = data["universityName"]
        field_name = data["fieldName"]
        period_type = data["periodType"]
        acceptance_chance = data["acceptanceChance"]
        service_commitment = data["serviceCommitment"]
        sex = data["sex"]
        rank_in_all = data["rank_in_all"]
        quota = data["quota"]
        field = data["field"]
        second_field = data["secondField"]
        native_province = data["nativeProvince"]
        query = 'SELECT rank_zaban, rank_honar, finalized FROM stu WHERE user_id = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_user is None:
            return None, None, "این دانش‌آموز ثبت نشده است."
        if second_field != "NULL":
            field = second_field
            if int(second_field) == 4:
                if res_user[0] == 0:
                    return None, None, "شما رشته زبان را انتخاب نکرده‌اید."
            else:
                if res_user[1] == 0:
                    return None, None, "شما رشته هنر را انتخاب نکرده‌اید."
        if accept_way == "NULL":
            accept_way = None
        if acceptance_chance == "NULL":
            acceptance_chance = None
        if res_user[2] == 0:
            return None, None, "اطلاعات ثبت نهایی نشده است."
        fields = []
        tracking_code = str(uuid.uuid4())
        cit = None
        if len(cities) >= 1:
            cit = ""
            for i, city in enumerate(cities):
                if i != len(cities) - 1:
                    cit = cit + city + ','
                else:
                    cit = cit + city
        prov = None
        if len(provinces) >= 1:
            prov = ""
            for i, province in enumerate(provinces):
                if i != len(provinces) - 1:
                    prov = prov + province + ','
                else:
                    prov = prov + province
        periods = None
        if len(period_type) >= 1:
            periods = ""
            for i, period in enumerate(period_type):
                if i != len(period_type) - 1:
                    periods = periods + period + ','
                else:
                    periods = periods + period
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        fil_name = None
        if len(field_name) >= 1:
            fil_name = ""
            for i, fil in enumerate(field_name):
                if i != len(field_name) - 1:
                    fil_name = fil_name + fil + ','
                else:
                    fil_name = fil_name + fil
        sql = 'exec Note.dbo.Get_Fields ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, None, None, prov, cit, None, None, sex, quota, fil_name, uni_name, rank_in_all, accept_way,
            service_commitment, acceptance_chance, periods, native_province, None, 1000, None, "ALLNOTES",
            None, None, None
        )
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
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
        return tracking_code, fields, ""
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Get_Fields",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, [], "مشکلی در جستجوی شما موجود هست."


# Free functionality
def get_majors_fr(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        university_name = data["universityName"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        sql = 'exec Note.dbo.Azad_Get_Majors ?, ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, uni_name, sex, part_time, dorm, None, "AZAD_SARASARI")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        majors = []
        tracking_code = str(uuid.uuid4())
        if uni_name is None:
            for res in recs:
                majors.append(res[0])
        else:
            for res in recs:
                majors.append(res[0])
        return tracking_code, majors
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Majors",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_universities_fr(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        sql = 'exec Note.dbo.Azad_Get_Universities ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, sex, part_time, dorm, None, "AZAD_SARASARI")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        universities = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            universities.append(res[0])
        return tracking_code, universities
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Universities",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_provinces_fr(conn, cursor, data, info):
    values = ()
    try:
        field = data["field"]
        sex = data["sex"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        if second_field != "NULL":
            field = second_field
        sql = 'exec Note.dbo.Azad_Get_Provinces ?, ?, ?, ?, ?, ?'
        values = (field, sex, part_time, dorm, None, "AZAD_SARASARI")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        provinces = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            provinces.append(res[0])
        return tracking_code, provinces
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Provinces",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def search_fields_fr(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        university_name = data["universityName"]
        field_name = data["fieldName"]
        sex = data["sex"]
        rank_in_all = data["rank_in_all"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        field = data["field"]
        second_field = data["secondField"]
        query = 'SELECT rank_zaban, rank_honar, finalized FROM stu WHERE user_id = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_user is None:
            return None, None, "این دانش‌آموز ثبت نشده است."

        if second_field != "NULL":
            field = second_field
            if int(second_field) == 4:
                if res_user[0] == 0:
                    return None, None, "شما رشته زبان را انتخاب نکرده‌اید."
            else:
                if res_user[1] == 0:
                    return None, None, "شما رشته هنر را انتخاب نکرده‌اید."
        if res_user[2] == 0:
            return None, None, "اطلاعات ثبت نهایی نشده است."
        fields = []
        tracking_code = str(uuid.uuid4())
        prov = None
        if len(provinces) >= 1:
            prov = ""
            for i, province in enumerate(provinces):
                if i != len(provinces) - 1:
                    prov = prov + province + ','
                else:
                    prov = prov + province
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        fil_name = None
        if len(field_name) >= 1:
            fil_name = ""
            for i, fil in enumerate(field_name):
                if i != len(field_name) - 1:
                    fil_name = fil_name + fil + ','
                else:
                    fil_name = fil_name + fil
        sql = 'exec Note.dbo.Azad_Get_Fields ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, prov, fil_name, uni_name, sex, part_time, dorm, None, 1000, None, "AZAD_SARASARI", rank_in_all, 1
        )
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        for res in recs:
            response = {
                'filedCode': int(str(res[9]) + str(res[1])), 'field': res[2], 'city': res[3], 'university': res[0],
                'selfGoverning': 'خودگردان' if res[5] == 1 else 'غیر خودگردان',
                "branch": res[4],
                'sex': res[6], 'partTime': res[7],
                'dorm': res[8], 'first': res[10], 'second': 0 if res[11] is None else res[11],
                'admissionKind': res.Acceptance
            }
            fields.append(response)
        return tracking_code, fields, ""
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Fields",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, [], "مشکلی در جستجوی شما موجود هست."


# fr list check
def update_spfr(conn, cursor, data, info):
    values = ()
    try:
        special_list = data["special_list"]
        query = 'SELECT field, phone FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, "اطلاعات شما یافت نشد."
        query = 'SELECT list_id FROM spfr WHERE user_id = ?'
        res_list = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        field = '([user_id], [field], [special_list], [editor_id], [phone])'
        if res_list is not None:
            db_helper.delete_record(
                conn, cursor, "spfr",
                ["user_id"],
                [data["stu_id"]]
            )
        values = (
            data["stu_id"], res_student.field, special_list, info["user_id"], res_student.phone,)
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='spfr', fields=field,
                               values=values)
        token = str(uuid.uuid4())
        return token, "لیست شما با موفقیت تغییر یافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "update_spfr",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, "لیست شما تغییر پیدا نکرد لطفا دوباره تلاش کنید."


def get_spfr(conn, cursor, data, info):
    try:
        query = 'SELECT field FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, []
        query = 'SELECT special_list FROM spfr WHERE user_id = ?'
        res_list = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        token = str(uuid.uuid4())
        if res_list is None:
            return token, []
        return token, json.loads(res_list.special_list)
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "get_spfr",
            json.dumps([], ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def update_trfr(conn, cursor, data, info):
    values = ()
    try:
        trash_list = data["trash_list"]
        query = 'SELECT field, phone FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, "اطلاعات شما یافت نشد."
        query = 'SELECT list_id FROM trfr WHERE user_id = ?'
        res_list = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        field = '([user_id], [field], [trash_list], [editor_id], [phone])'
        if res_list is not None:
            db_helper.delete_record(
                conn, cursor, "trfr",
                ["user_id"],
                [data["stu_id"]]
            )
        values = (
            data["stu_id"], res_student.field, trash_list, info["user_id"], res_student.phone)
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='trfr', fields=field,
                               values=values)
        token = str(uuid.uuid4())
        return token, "لیست شما با موفقیت تغییر یافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "update_trfr",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, "لیست شما تغییر پیدا نکرد لطفا دوباره تلاش کنید."


def get_trfr(conn, cursor, data, info):
    try:
        query = 'SELECT field FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, []
        query = 'SELECT trash_list FROM trfr WHERE user_id = ?'
        res_list = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        token = str(uuid.uuid4())
        if res_list is None:
            return token, []
        return token, json.loads(res_list.trash_list)
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "get_trfr",
            json.dumps([], ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


# Free Other functionality

def get_majors_frb(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        university_name = data["universityName"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        sql = 'exec Note.dbo.Azad_Get_Majors ?, ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, uni_name, sex, part_time, dorm, None, "AZAD_KARSHENASIP")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        majors = []
        token = str(uuid.uuid4())
        if uni_name is None:
            for res in recs:
                majors.append(res[0])
        else:
            for res in recs:
                majors.append(res[0])
        return token, majors
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Majors",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_universities_frb(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        sex = data["sex"]
        field = data["field"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        if second_field != "NULL":
            field = second_field
        province = None
        if len(provinces) >= 1:
            province = ""
            for i, pro in enumerate(provinces):
                if i != len(provinces) - 1:
                    province = province + pro + ','
                else:
                    province = province + pro
        sql = 'exec Note.dbo.Azad_Get_Universities ?, ?, ?, ?, ?, ?, ?'
        values = (field, province, sex, part_time, dorm, None, "AZAD_KARSHENASIP")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        universities = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            universities.append(res[0])
        return tracking_code, universities
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Universities",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def get_provinces_frb(conn, cursor, data, info):
    values = ()
    try:
        field = data["field"]
        sex = data["sex"]
        second_field = data["secondField"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        if second_field != "NULL":
            field = second_field
        sql = 'exec Note.dbo.Azad_Get_Provinces ?, ?, ?, ?, ?, ?'
        values = (field, sex, part_time, dorm, None, "AZAD_KARSHENASIP")
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        provinces = []
        tracking_code = str(uuid.uuid4())
        for res in recs:
            provinces.append(res[0])
        return tracking_code, provinces
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Provinces",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def search_fields_frb(conn, cursor, data, info):
    values = ()
    try:
        provinces = data["provinces"]
        university_name = data["universityName"]
        field_name = data["fieldName"]
        sex = data["sex"]
        rank_in_all = data["rank_in_all"]
        part_time = data["partTime"]
        dorm = data["Dorm"]
        field = data["field"]
        query = 'SELECT finalized FROM stu WHERE user_id = ?'
        res_user = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_user is None:
            return None, None, "این دانش‌آموز ثبت نشده است."
        fields = []
        tracking_code = str(uuid.uuid4())
        prov = None
        if len(provinces) >= 1:
            prov = ""
            for i, province in enumerate(provinces):
                if i != len(provinces) - 1:
                    prov = prov + province + ','
                else:
                    prov = prov + province
        uni_name = None
        if len(university_name) >= 1:
            uni_name = ""
            for i, name in enumerate(university_name):
                if i != len(university_name) - 1:
                    uni_name = uni_name + name + ','
                else:
                    uni_name = uni_name + name
        fil_name = None
        if len(field_name) >= 1:
            fil_name = ""
            for i, fil in enumerate(field_name):
                if i != len(field_name) - 1:
                    fil_name = fil_name + fil + ','
                else:
                    fil_name = fil_name + fil
        sql = 'exec Note.dbo.Azad_Get_Fields ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (
            field, prov, fil_name, uni_name, sex, part_time, dorm, None, 1000, None, "AZAD_KARSHENASIP", rank_in_all, 1
        )
        cursor.execute(sql, values)
        recs = cursor.fetchall()
        cursor.commit()
        for res in recs:
            response = {
                'filedCode': int(str(res[7]) + str(res[1])), 'field': res[2], 'city': res[3], 'university': res[0],
                'sex': res[4], 'partTime': res[5],
                'dorm': res[6],
                'admissionKind': res.Acceptance
            }
            fields.append(response)
        return tracking_code, fields, ""
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "Azad_Get_Fields",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, [], "مشکل در جستجو پیش آمده"


# frb list check
def update_spfrb(conn, cursor, data, info):
    values = ()
    try:
        part = data["part"]
        field_stu = data["field"]
        special_list = data["special_list"]
        query = 'SELECT phone FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, "اطلاعات شما یافت نشد."
        res_list = db_helper.multi_search_table(
            conn, cursor, "spfrb",
            ["list_id", "phone"],
            ["user_id", "part", "field"],
            [data["stu_id"], part, field_stu]
        )
        field = '([user_id], [field], [part], [special_list], [phone], [editor_id])'
        if res_list is not None:
            db_helper.delete_record(
                conn, cursor, "spfrb",
                ["user_id", "part", "field"],
                [data["stu_id"], part, field_stu],
            )
        values = (
            data["stu_id"], field_stu, part, special_list, res_student.phone, info["user_id"],)
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='spfrb', fields=field,
                               values=values)
        token = str(uuid.uuid4())
        return token, "لیست شما با موفقیت تغییر یافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "update_spfrb",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, "لیست شما تغییر پیدا نکرد لطفا دوباره تلاش کنید."


def get_spfrb(conn, cursor, data, info):
    try:
        field = data["field"]
        part = data["part"]
        query = 'SELECT field FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, []
        res_list = db_helper.multi_search_table(
            conn, cursor, "spfrb",
            ["special_list"],
            ["user_id", "part", "field"],
            [data["stu_id"], part, field]
        )
        token = str(uuid.uuid4())
        if res_list is None:
            return token, []
        return token, json.loads(res_list.special_list)
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "get_spfrb",
            json.dumps([], ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []


def update_trfrb(conn, cursor, data, info):
    values = ()
    try:
        part = data["part"]
        field_stu = data["field"]
        trash_list = data["trash_list"]
        query = 'SELECT phone FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, "اطلاعات شما یافت نشد."
        res_list = db_helper.multi_search_table(
            conn, cursor, "trfrb",
            ["list_id", "phone"],
            ["user_id", "part", "field"],
            [data["stu_id"], part, field_stu]
        )
        field = '([user_id], [field], [part], [trash_list], [phone], [editor_id])'
        if res_list is not None:
            db_helper.delete_record(
                conn, cursor, "trfrb",
                ["user_id", "part", "field"],
                [data["stu_id"], part, field_stu]
            )
        values = (
            data["stu_id"], field_stu, part, trash_list, res_student.phone, info["user_id"],)
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='trfrb', fields=field,
                               values=values)
        token = str(uuid.uuid4())
        return token, "لیست شما با موفقیت تغییر یافت."
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "update_trfrb",
            json.dumps(values, ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, "لیست شما تغییر پیدا نکرد لطفا دوباره تلاش کنید."


def get_trfrb(conn, cursor, data, info):
    try:
        field = data["field"]
        part = data["part"]
        query = 'SELECT phone FROM stu WHERE user_id = ?'
        res_student = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=data["stu_id"])
        if res_student is None:
            return None, []
        res_list = db_helper.multi_search_table(
            conn, cursor, "trfrb",
            ["trash_list"],
            ["user_id", "part", "field"],
            [data["stu_id"], part, field]
        )
        token = str(uuid.uuid4())
        if res_list is None:
            return token, []
        return token, json.loads(res_list[0])
    except Exception as e:
        conn.rollback()
        field_log = '([user_id], [phone], [sp], [sp_input], [data], [error_p])'
        values_log = (
            info.get("user_id"), info.get("phone"), "get_spfrb",
            json.dumps([], ensure_ascii=False),
            json.dumps(data, ensure_ascii=False), str(e))
        db_helper.insert_value(conn=conn, cursor=cursor, table_name='pickfield_logs', fields=field_log,
                               values=values_log)
        return None, []
