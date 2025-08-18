import os
import time
import redis
import pyodbc
import logging
from datetime import datetime
from typing import List, Tuple, Dict, Any

from Excel.ms_excel import compute_brain_info
from Helper import db_helper
from Office.new_word import generate_word_with_info
from Chart import tube, bar, gauge
from Quiz.report_info import *
from Excel.excel import master_file, master_sheet

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
DB_CONN_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1433;'
    'DATABASE=BBC;UID=mgh27;PWD=m2711gH9985;'
    'TrustServerCertificate=yes'
)
REPORTS_BASE_DIR = r'D:\WebSites\BBC\Reports'
MEDIA_BASE_DIR = r'D:\WebSites\BBC\Media\InsPic'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('report_scheduler.log'),
        logging.StreamHandler()
    ]
)


class ReportScheduler:
    def __init__(self):
        self.report_images = [
            'image16.png', 'image18.jpg', 'image21.jpg', 'image24.jpg', 'image27.jpg',
            'image30.jpg', 'image33.jpg', 'image36.jpg', 'image39.jpg', 'image42.png',
            'image45.png', 'image47.png', 'image51.png', 'image52.png', 'image55.png',
            'image56.png', 'image58.png', 'image59.png', 'image62.png', 'image63.png',
            'image66.png', 'image67.png', 'image70.png', 'image71.png', 'image75.png',
            'image76.png', 'image79.png', 'image80.png'
        ]

        self.category_def_color = {
            "دبیری": "#7030A0", "مدیریت": "#002060", "علوم پایه": "#0070C0",
            "هنر": "#00B0F0", "مهندسی سازه": "#00B050", "مهندسی صنعتی": "#92D050",
            "الکترونیک و کامپیوتر": "#FFFF00", "علوم انسانی": "#C55A11",
            "مالی و حسابداری": "#FF0000", "روانشناسی": "#C00000",
            "کشاورزی و امور دامی": "#002060", "حقوق و علوم سیاسی": "#0070C2",
            "خدمات فنی": "#00B0F0", "تکنسین فنی": "#00B050", "روابط عمومی": "#7030A0",
            "بالینی و درمانی": "#92D050", "تشخیصی و درمانی": "#FFFF02",
            "تکنسین کامپیوتر": "#FFC002"
        }

        self.fields_benchmark_name = [
            (('Reshteha_Tajrobi', ['رشته_پیشنهادی_تجربی', 'S1', 'S2', 'T1', 'T2']),
             ('Sayer_Tajrobi', ['سایر_تجربی', 'سایر_رنگ'])),
            (('Reshteha_Riazi', ['رشته_پیشنهادی_ریاضی', 'S1', 'S2', 'T1', 'T2']),
             ('Sayer_Riazi', ['سایر_ریاضی', 'سایر_رنگ'])),
            (('Reshteha_Ensani', ["رشته_پیشنهادی_انسانی", 'S1', 'S2', 'T1', 'T2']),
             ('Sayer_Ensani', ['سایر_انسانی', 'سایر_رنگ'])),
            (('Reshteha_Honar', ['رشته_پیشنهادی_هنر', 'S1', 'S2', 'T1', 'T2']),
             ('Sayer_Honar', ['_سایر_هنر_', 'سایر_رنگ']))
        ]

        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
        )

        try:
            self.db_conn = pyodbc.connect(DB_CONN_STRING)
            self.db_cursor = self.db_conn.cursor()
        except pyodbc.Error as e:
            logging.error(f"Database connection failed: {str(e)}")
            raise

    def _log_error(self, user_id: str, error: str) -> None:
        """Log errors to database with user context."""
        try:
            db_helper.update_record(
                self.db_conn, self.db_cursor,
                "redis_log",
                ["status", "state", "edited_time"],
                [f"Error: {error}", 3, datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?",
                [str(user_id)]
            )
        except Exception as e:
            logging.error(f"Failed to log error to database: {str(e)}")

    def _get_student_info(self, user_id: str) -> Tuple[Any, str]:
        """Retrieve student and institute information."""
        try:
            student_query = '''
                SELECT user_id, phone, first_name, last_name, logo
                FROM stu
                WHERE user_id = ?
            '''
            student = db_helper.search_table(
                self.db_conn, self.db_cursor, student_query, user_id
            )
            logo_path = None
            if student.logo:
                base_dir_pic = r'D:\WebSites\BBC\Media\InsPic'
                logo_path = os.path.join(base_dir_pic, student.logo)
            if not student:
                raise ValueError(f"Student with ID {user_id} not found")

            return student, logo_path

        except Exception as e:
            logging.error(f"Error getting student info: {str(e)}")
            self._log_error(user_id, str(e))
            raise

    def _create_report_directory(self, phone: str) -> str:
        """Create directory for report files."""
        user_directory = os.path.join(REPORTS_BASE_DIR, phone)
        try:
            os.makedirs(user_directory, exist_ok=True)
            logging.info(f"Directory '{user_directory}' created/exists")
            return user_directory
        except Exception as e:
            logging.error(f"Failed to create directory: {str(e)}")
            raise

    def _generate_charts(self, data: Dict, categories: List, user_directory: str) -> Tuple[List, Dict]:
        """Generate all required charts for the report."""
        report_pictures = []
        report_info = {}

        try:
            categories_bar = [
                'تصویری-فضایی', 'زبانی-کلامی', 'منطقی-ریاضی',
                'جسمی-حرکتی', 'موسیقیایی', 'بین فردی',
                'درون فردی', 'طبیعت گرا'
            ]
            colors = [
                '#3BABC5', '#E6C90B', '#49CFFF', '#FF75B5',
                '#8FD351', '#9472DE', '#F1AB37', '#FF6C6C'
            ]

            bar_path = bar.create_bar_chart(
                categories=categories_bar,
                title='ﻪﻧﺎﮔ ۸ ﯼﺎﻫﺵﻮﻫ ﺭﺩ ﺎﻤﺷ ﺖﯿﻌﺿﻭ ﻪﺑ ﯽﻠﮐ ﻩﺎﮕﻧ',
                values=[data[k] * 2 for k in [
                    "Visual_spatial", "Linguistic_verbal", "Logical_mathematical",
                    "Body_kinesthetic", "Musical", "Intrapersonal",
                    "Interpersonal", "Naturalistic"
                ]],
                colors=colors,
                rotation=45,
                size=6,
                path=user_directory,
                filename='bar'
            )
            report_pictures.append(f"{bar_path}.png")

            attributes = [
                ("Visual_spatial", "سلاام", gardner_visual_explain),
                ("Linguistic_verbal", "سلااام", gardner_linguistic_explain),
                ("Logical_mathematical", "سلاااام", gardner_logical_explain),
                ("Body_kinesthetic", "سلااااام", gardner_body_explain),
                ("Musical", "سلاااااام", gardner_musical_explain),
                ("Intrapersonal", "سلااااااام", gardner_intrapersonal_explain),
                ("Interpersonal", "سلاااااااام", gardner_interpersonal_explain),
                ("Naturalistic", "سلااااااااام", gardner_naturalistic_explain)
            ]

            for i, (attr, key, explain_func) in enumerate(attributes, start=1):
                value = data[attr]
                tube_path = tube.create_tube_chart(
                    charge_level=value,
                    color=colors[i - 1],
                    path=user_directory,
                    filename=f'tube{i}'
                )
                report_pictures.append(f"{tube_path}.png")
                report_info[key] = explain_func(value)

            sorted_categories = sorted(categories, key=lambda x: x["Value"], reverse=True)
            cat_bar_path = bar.create_bar_chart(
                categories=[item["Category"] for item in sorted_categories],
                title='',
                values=[int(item["Value"]) for item in sorted_categories],
                colors=[self.category_def_color[item["Category"]] for item in sorted_categories],
                rotation=90,
                size=9,
                path=user_directory,
                filename='secondbar'
            )
            report_pictures.append(f"{cat_bar_path}.png")

            for index, cat in enumerate(sorted_categories):
                value = max(cat["Value"], 10)
                gauge_path = gauge.create_gauge_chart(
                    value=value,
                    labels=[''] * 5,
                    colors=['#42b74a', '#cfdf28', '#ffbb10', '#f76420', '#cf2020'],
                    ranges=[(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)],
                    path=user_directory,
                    filename=f"gaugeSecond{index + 1}"
                )
                report_pictures.append(f"{gauge_path}.png")

            return report_pictures, report_info

        except Exception as e:
            logging.error(f"Error generating charts: {str(e)}")
            raise

    def _process_suggested_fields(self, fields: List) -> Tuple[List, str, str]:
        """Process and categorize suggested fields."""
        try:
            branch_groups = {}
            for item in fields:
                branch = item["BranchId"]
                branch_groups.setdefault(branch, []).append(item)

            grouped_array = [branch_groups[k] for k in sorted(branch_groups.keys())]
            final_list = []
            suggested_names = []
            other_names = []

            for branch in grouped_array:
                suggested = []
                other = []

                for field in branch:
                    condition = int(field["ReportCondition"])
                    if condition > 0:
                        suggested.append(field)
                        suggested_names.append(field["Field"])
                    else:
                        other.append(field)
                        if condition == 0:
                            other_names.append(field["Field"])

                final_list.append((suggested, other))

            return (
                final_list,
                ','.join(suggested_names),
                ','.join(other_names)
            )

        except Exception as e:
            logging.error(f"Error processing suggested fields: {str(e)}")
            raise

    def _prepare_field_matches(self, suggested_other: List) -> List:
        """Prepare field matches for report generation."""
        field_matches = []

        try:
            for branch in suggested_other:
                suggested_list = []
                other_list = []

                sorted_suggested = sorted(branch[0], key=lambda x: x['Personality'], reverse=True)
                if not sorted_suggested:
                    suggested_list.append([
                        'هیچ رشته ای یافت نشد!',
                        '*' * 0, '↑' * 10,
                        '*' * 0, '↑' * 10
                    ])
                else:
                    for field in sorted_suggested:
                        suggested_list.append([
                            field["Field"],
                            '↑' * len(field["IQStars"]),
                            '↑' * (10 - len(field["IQStars"])),
                            '↑' * len(field["PersonalityStars"]),
                            '↑' * (10 - len(field["PersonalityStars"]))
                        ])

                sorted_other = sorted(branch[1], key=lambda x: x['Personality'], reverse=True)
                if not sorted_other:
                    other_list.append([
                        'هیچ رشته ای یافت نشد!',
                        '↓' * 10
                    ])
                else:
                    for field in sorted_other:
                        other_list.append([
                            field["Field"],
                            '↓' * (10 - int(field["Color"]))
                        ])

                field_matches.append((suggested_list, other_list))

            return field_matches

        except Exception as e:
            logging.error(f"Error preparing field matches: {str(e)}")
            raise

    def generate_report(self, user_id: str) -> None:
        """Main method to generate report for a user."""
        try:
            start_time = time.time()

            student, logo_path = self._get_student_info(user_id)
            user_directory = self._create_report_directory(student[1])

            db_helper.update_record(
                self.db_conn, self.db_cursor,
                "redis_log",
                ["status", "state", "edited_time"],
                ["user info checking in scheduler", 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?",
                [str(user_id)]
            )

            data, fields, categories = compute_brain_info(
                self.db_conn, self.db_cursor, user_id,
                phone=student[1],
                master_file=master_file,
                master_sheet=master_sheet
            )

            suggested_other, suggested_names, other_names = self._process_suggested_fields(fields)

            query = 'SELECT user_id FROM hedayat_fields WHERE user_id = ?'
            exists = db_helper.search_table(self.db_conn, self.db_cursor, query, user_id)

            if exists is None:
                db_helper.insert_value(
                    self.db_conn, self.db_cursor,
                    "hedayat_fields",
                    "([user_id], [phone], [suggested], [other])",
                    (user_id, student[1], suggested_names, other_names)
                )
            else:
                db_helper.update_record(
                    self.db_conn, self.db_cursor,
                    "hedayat_fields",
                    ['suggested', 'other', 'edited_time'],
                    [suggested_names, other_names, datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "user_id = ?",
                    [user_id]
                )

            report_pictures, report_info = self._generate_charts(data, categories, user_directory)
            report_info.update({
                "#name": f"{student[2]} {student[3]}",
            })

            field_matches = self._prepare_field_matches(suggested_other)

            report_images = self.report_images.copy()
            if logo_path:
                report_images.append('image86.jpeg')
                report_pictures.append(logo_path)

            generate_word_with_info(
                list(report_info.keys()),
                list(report_info.values()),
                report_images,
                report_pictures,
                user_directory,
                field_matches,
                self.fields_benchmark_name,
                student[1],
                f"{student[2]} {student[3]}"
            )

            db_helper.update_record(
                self.db_conn, self.db_cursor,
                "redis_log",
                ["status", "state", "edited_time"],
                ["user info checked in scheduler", 2, datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "user_id = ?",
                [str(user_id)]
            )

            logging.info(
                f"Successfully generated report for user {user_id}. "
                f"Time taken: {time.time() - start_time:.2f} seconds"
            )

        except Exception as e:
            logging.error(f"Failed to generate report for user {user_id}: {str(e)}")
            self._log_error(user_id, str(e))
            raise

    def run(self) -> None:
        """Main scheduler loop."""
        logging.info("Report scheduler started Entekhab B2c")

        try:
            while True:
                user_id = self.redis.lpop("userERSReport")
                if user_id is None:
                    logging.debug("No users in queue, sleeping Entekhab B2c...")
                    time.sleep(10)
                    continue

                try:
                    logging.info(f"Processing user ID: {user_id}")
                    self.generate_report(user_id)
                    time.sleep(20)

                except Exception as e:
                    logging.error(f"Error processing user {user_id}: {str(e)}")
                    field_log = '([user_id], [message], [error_p])'
                    values_log = (
                        user_id, "Error processing user", str(e))
                    db_helper.insert_value(conn=self.db_conn, cursor=self.db_cursor, table_name='pdf_logs',
                                           fields=field_log, values=values_log)
                    continue
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user Entekhab B2c")
        except Exception as e:
            field_log = '([user_id], [message], [error_p])'
            values_log = (
                None, "Error processing user", str(e))
            db_helper.insert_value(conn=self.db_conn, cursor=self.db_cursor, table_name='pdf_logs',
                                   fields=field_log, values=values_log)
            logging.error(f"Scheduler crashed: {str(e)}")
            raise
        finally:
            self.db_conn.close()
            logging.info("Database connection closed")


if __name__ == "__main__":
    try:
        scheduler = ReportScheduler()
        scheduler.run()
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        raise
