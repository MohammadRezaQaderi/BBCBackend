import pandas as pd
import pyodbc
from datetime import datetime, timedelta
import pytz

persian_headers = {
    'id': 'شناسه',
    'payment_id': 'شناسه پرداخت',
    'user_id': 'شناسه کاربر',
    'phone': 'تلفن',
    # 'state': 'وضعیت پرداخت',
    'status': 'وضعیت نهایی',
    'price': 'مبلغ',
    'discount_price': 'مبلغ پس از تخفیف',
    # 'track_id': 'کد پیگیری',
    'result': 'نتیجه',
    # 'discount_id': 'شناسه تخفیف',
    # 'saleReferenceId': 'کد مرجع',
    # 'message': 'پیام',
    # 'token': 'توکن',
    # 'product_data': 'اطلاعات محصول',
    # 'created_time': 'زمان ایجاد',
    # 'edited_time': 'زمان ویرایش'
}


def get_payment_report(start_date=None, end_date=None):
    try:
        conn = pyodbc.connect(
            driver='SQL Server',
            server='localhost,1433',
            database='ERS',
            uid='mgh27',
            pwd='m2711gH9985',
            TrustServerCertificate='yes'
        )

        if not start_date or not end_date:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=2)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include full end day

        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

        query = """
        WITH UsersWithNoSuccess AS (
            SELECT DISTINCT user_id
            FROM payment
            WHERE user_id NOT IN (
                SELECT DISTINCT user_id 
                FROM payment 
                WHERE status = 'SUCCESS' 
                AND edited_time BETWEEN ? AND ?
            )
        )
        SELECT p.*
        FROM payment p
        INNER JOIN UsersWithNoSuccess u ON p.user_id = u.user_id
        WHERE p.edited_time BETWEEN ? AND ?
        ORDER BY p.edited_time DESC
        """

        df = pd.read_sql(query, conn, params=[start_date_str, end_date_str, start_date_str, end_date_str])

        df = df.rename(columns=persian_headers)

        # tehran = pytz.timezone('Asia/Tehran')
        # if 'زمان ایجاد' in df.columns:
        #     df['زمان ایجاد'] = pd.to_datetime(df['زمان ایجاد']).dt.tz_localize('UTC').dt.tz_convert(tehran)
        # if 'زمان ویرایش' in df.columns:
        #     df['زمان ویرایش'] = pd.to_datetime(df['زمان ویرایش']).dt.tz_localize('UTC').dt.tz_convert(tehran)

        return df

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def save_to_excel(df, filename='payment_report.xlsx'):
    try:
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')

        df.to_excel(writer, sheet_name='Payments', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Payments']

        persian_format = workbook.add_format({
            'font_name': 'B Nazanin',
            'font_size': 11,
            'align': 'right',
            'valign': 'vcenter'
        })

        worksheet.set_column('A:Z', 20, persian_format)

        worksheet.freeze_panes(1, 0)

        for idx, col in enumerate(df):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(idx, idx, max_len)

        writer.close()
        print(f"Report saved to {filename}")
        return True

    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")
        return False


if __name__ == "__main__":
    date_range = input("Enter date range (YYYY-MM-DD to YYYY-MM-DD) or press Enter for last 2 days: ")

    if date_range:
        try:
            start_date, end_date = date_range.split(' to ')
        except ValueError:
            print("Invalid date range format. Please use 'YYYY-MM-DD to YYYY-MM-DD'")
            exit()
    else:
        start_date = end_date = None

    report_df = get_payment_report(start_date, end_date)

    if report_df is not None and not report_df.empty:
        filename = f"payment_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        save_to_excel(report_df, filename)
    else:
        print("No data found matching the criteria.")