import pyodbc
from walrus import *
import string
import random
from datetime import datetime
import math
from Helper import db_helper


async def db_connection():
    try:
        conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', host='localhost,1433',
                              database='BBC', UID='mgh27',
                              PWD='m2711gH9985', TrustServerCertificate='yes')
        cursor = conn.cursor()
        return conn, cursor
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise


async def redis_connection():
    redis_db = Database(host='127.0.0.1', port=6379, db=1)
    return redis_db


def check_security_code(code, check):
    if str(code) == str(check):
        return True
    if str(code) == str(check).lower():
        return True
    if str(code) == str(check).upper():
        return True
    else:
        return False


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def password_format_check(password):
    val = True
    message = ''
    if len(password) < 6:
        message = 'طول  رمز شما بایستی حداقل 6 کاراکتر باشد.'
        val = False
    if len(password) > 20:
        message = 'طول رمز شما بایستی حداکثر 20 کاراکتر باشد.'
        val = False
    if val:
        return val, ''
    else:
        return val, message


def random_phone_number(conn, cursor, n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    phone = '009' + str(random.randint(range_start, range_end))
    query = 'SELECT * FROM users WHERE phone = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=phone)
    if res is None:
        return phone
    else:
        return random_phone_number(conn=conn, cursor=cursor, n=n)


def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def code_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_discount_code(length=8, prefix="", suffix=""):
    characters = string.ascii_uppercase + string.digits

    random_part = ''.join(random.choice(characters) for _ in range(length))

    discount_code = f"{prefix}{random_part}{suffix}"

    return discount_code


def update_step_hoshmand(conn, cursor, number, user_id):
    db_helper.update_record(
        conn, cursor, "hoshmand_info", ["current_step", "edited_time"], [
            number,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ], "user_id = ?", [user_id]
    )


def delete_unneeded_table(conn, cursor, tables, id):
    for table in tables:
        db_helper.delete_record(
            conn, cursor, table,
            ["user_id"],
            [str(id)]
        )
