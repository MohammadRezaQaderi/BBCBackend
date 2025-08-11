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
                              database='ERS', UID='mgh27',
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


# def get_price_payment(price):
#     return int(price) * 10000


def get_payment_id(conn, cursor):
    payment_id = random.randint(1, 9999999)
    query = 'SELECT * FROM ERS.dbo.payment WHERE payment_id = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=payment_id)
    if res is None:
        return payment_id
    else:
        return get_payment_id(conn=conn, cursor=cursor)


def format_baskets(baskets):
    formatted_baskets = ", ".join(
        "({})".format(", ".join("'{}'".format(item) for item in basket)) if basket else "()"
        for basket in baskets
    )
    return '({})'.format(formatted_baskets) if formatted_baskets else '()'


def format_importance_list(importance_list):
    return '({})'.format(", ".join("'{}'".format(item) for item in importance_list))


def round_value(value):
    if value is None:
        return None
    last_two_digits = value % 100
    if last_two_digits >= 50:
        return math.ceil(value / 100) * 100
    else:
        return math.floor(value / 100) * 100


def to_international_phone(phone):
    if phone.startswith('+98'):
        return phone
    elif phone.startswith('0'):
        return '+98' + phone[1:]
    elif phone.startswith('98'):
        return '+' + phone
    else:
        return '+98' + phone


PACKAGES_DATA = {
    "GL": 1150000,
    "FR": 400000,
    "AG": 350000
}


def get_price_payment(data, discount_percentage):
    """
    Calculate total price based on user counts for GL, FR, AG

    Args:
        data: Dictionary containing GL, FR, AG user counts
              Example: {"GL": 20, "FR": 10, "AG": 50}

    Returns:
        Total price in Rials
    """
    price = 21010000
    new_value = price
    if discount_percentage:
        new_value = round(price * (1 - discount_percentage))
    return price, new_value


def update_step_hoshmand(conn, cursor, number, user_id):
    # todo try except
    db_helper.update_record(
        conn, cursor, "hoshmand_info", ["current_step", "edited_time"], [
            number,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ], "user_id = ?", [user_id]
    )


def generate_discount_code(length=8, prefix="", suffix=""):
    characters = string.ascii_uppercase + string.digits

    random_part = ''.join(random.choice(characters) for _ in range(length))

    discount_code = f"{prefix}{random_part}{suffix}"

    return discount_code
