import pandas as pd
import pyodbc
from datetime import datetime

conn = pyodbc.connect(
    driver='ODBC Driver 17 for SQL Server',
    server='localhost,1433',
    database='BBC',
    uid='mgh27',
    pwd='m2711gH9985',
    TrustServerCertificate='yes'
)


def check_phone_numbers(excel_file_path):
    df = pd.read_excel(excel_file_path)
    phone_numbers = [str(num) for num in df.iloc[:, 0] if pd.notna(num)]

    results = []
    count_of_can_update = 0
    count_of_not_exist = 0
    update_errors = []

    for phone in phone_numbers:
        phone_str = str(phone)
        if not phone_str.startswith('0'):
            phone_str = '0' + phone_str

        cursor = conn.cursor()
        try:
            query = """
            SELECT first_name, last_name, city 
            FROM stu 
            WHERE phone = ?
            """
            cursor.execute(query, phone_str)
            row = cursor.fetchone()

            if row:
                first_name, last_name, city = row
                city_part = city.split(",")[0] if city else None
                exists = True

                try:
                    update_query = """
                    UPDATE stu 
                    SET lock = ?, edited_time = ?
                    WHERE phone = ?
                    """
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(update_query, (1, current_time, phone_str))
                    conn.commit()
                    count_of_can_update += 1
                except Exception as update_error:
                    conn.rollback()
                    update_errors.append({
                        'phone': phone_str,
                        'error': str(update_error)
                    })
                    print(f"Failed to update phone {phone_str}: {update_error}")
            else:
                count_of_not_exist += 1
                first_name, last_name, city_part = None, None, None
                exists = False

            results.append({
                'original_number': phone,
                'formatted_number': phone_str,
                'exists_in_db': exists,
                'first_name': first_name,
                'last_name': last_name,
                'city': city_part,
                'update_status': 'Success' if exists and not update_errors else 'Failed' if exists and update_errors else 'N/A'
            })

        except Exception as e:
            print(f"Error processing phone {phone_str}: {e}")
            results.append({
                'original_number': phone,
                'formatted_number': phone_str,
                'exists_in_db': 'Error',
                'first_name': None,
                'last_name': None,
                'city': None,
                'update_status': 'Processing Error'
            })
        finally:
            cursor.close()

    results_df = pd.DataFrame(results)
    output_file = 'phone_number_check_results_with_details2.xlsx'
    results_df.to_excel(output_file, index=False)

    if update_errors:
        errors_df = pd.DataFrame(update_errors)
        errors_df.to_excel('update_errors2.xlsx', index=False)
        print(f"Update errors saved to update_errors.xlsx")

    print(f"Results saved to {output_file}")
    print(f"count_of_can_update: {count_of_can_update}")
    print(f"count_of_not_exist: {count_of_not_exist}")

    if update_errors:
        print(f"count_of_update_errors: {len(update_errors)}")

    return results_df


if __name__ == "__main__":
    excel_file_path = 'phone_numbers2.xlsx'
    results = check_phone_numbers(excel_file_path)
    print(results)
