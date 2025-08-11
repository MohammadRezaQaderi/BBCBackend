def insert_value(conn, cursor, table_name, fields, values):
    sqlScript = 'INSERT INTO ' + table_name + ' ' + fields + ' VALUES (' + '?, ' * len(values)
    sqlScript = sqlScript[:len(sqlScript) - 2] + ')'
    response = cursor.execute(sqlScript, values)
    conn.commit()
    return response


def update_record(conn, cursor, table_name, update_fields, update_values, condition, condition_values):
    try:
        set_clause = ", ".join(f"{field} = ?" for field in update_fields)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        params = update_values + condition_values
        cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print(f"Error updating record: {e}")
        return 0


def delete_record(conn, cursor, table_name, condition_fields, condition_values):
    try:
        where_clause = " AND ".join(f"{field} = ?" for field in condition_fields)
        sql = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(sql, condition_values)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        print(f"Error deleting record: {e}")
        return 0


def multi_search_table(conn, cursor, table_name, select_fields, condition_fields, condition_values):
    select_clause = ", ".join(select_fields)
    where_clause = " AND ".join(f"{field} = ?" for field in condition_fields)
    sql = f"SELECT {select_clause} FROM {table_name} WHERE {where_clause}"
    cursor.execute(sql, condition_values)
    row = cursor.fetchone()
    conn.commit()
    return row


def search_table(conn, cursor, query, field):
    response = cursor.execute(query, field)
    row = response.fetchone()
    conn.commit()
    return row


def search_allin_table(conn, cursor, query, field):
    response = cursor.execute(query, field)
    res = response.fetchall()
    conn.commit()
    return res


def search_fetchall(conn, cursor, query):
    response = cursor.execute(query)
    res = response.fetchall()
    conn.commit()
    return res
