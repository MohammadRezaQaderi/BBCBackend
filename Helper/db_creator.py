import pyodbc

from func_helper import generate_discount_code


def check_data_base(conn, cursor, tables):
    for table in tables:
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = ?
        """, (table,))
        if cursor.fetchone():
            print(f"The {table} table exists.")
            continue

        if table == "users":
            cursor.execute("""
                CREATE TABLE users (
                    user_id INT IDENTITY(1, 1) PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    password NVARCHAR(50) NOT NULL,
                    role NVARCHAR(100) NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "stu":
            cursor.execute("""
                CREATE TABLE stu (
                    stu_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    first_name NVARCHAR(50) NOT NULL,
                    last_name NVARCHAR(50) NOT NULL,
                    sex INT,
                    city NVARCHAR(100),
                    sch_name NVARCHAR(100),
                    birth_date NVARCHAR(4),
                    field INT,
                    quota INT,
                    full_number INT,
                    rank INT,
                    rank_all INt,
                    last_rank INT,
                    rank_zaban INT,
                    full_number_zaban INT,
                    rank_all_zaban INT,
                    rank_honar INT,
                    full_number_honar INt,
                    rank_all_honar INT,
                    password NVARCHAR(50) NOT NULL,
                    logo VARCHAR(MAX),
                    gl_access INT DEFAULT 0,
                    glf_access INT DEFAULT 0,
                    fr_access INT DEFAULT 0,
                    sp_access INT DEFAULT 0,
                    lock INT DEFAULT 0,
                    finalized INT DEFAULT 0,
                    verify INT DEFAULT 0,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "spgl":
            cursor.execute("""
                CREATE TABLE spgl (
                    list_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    field INT NOT NULL,
                    special_list NVARCHAR(MAX) NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "trgl":
            cursor.execute("""
                CREATE TABLE trgl (
                    list_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    field INT NOT NULL,
                    trash_list NVARCHAR(MAX) NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "fspgl":
            cursor.execute("""
                 CREATE TABLE fspgl (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "ftrgl":
            cursor.execute("""
                 CREATE TABLE ftrgl (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "spglf":
            cursor.execute("""
                 CREATE TABLE spglf (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "trglf":
            cursor.execute("""
                 CREATE TABLE trglf (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "spfr":
            cursor.execute("""
                 CREATE TABLE spfr (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "trfr":
            cursor.execute("""
                 CREATE TABLE trfr (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "spfrb":
            cursor.execute("""
                 CREATE TABLE spfrb (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     part INT NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "trfrb":
            cursor.execute("""
                 CREATE TABLE trfrb (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     part INT NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "speed":
            cursor.execute("""
                 CREATE TABLE speed (
                     speed_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     major_list NVARCHAR(MAX) NOT NULL,
                     uni_list NVARCHAR(MAX) NOT NULL,
                     period_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "pick_list":
            cursor.execute("""
                 CREATE TABLE pick_list (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     pick_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "sp_list":
            cursor.execute("""
                 CREATE TABLE sp_list (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "tr_list":
            cursor.execute("""
                 CREATE TABLE tr_list (
                     list_id INT IDENTITY(1, 1) PRIMARY KEY,
                     user_id INT NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     phone NVARCHAR(12) NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
                 )
             """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "pickfield_logs":
            cursor.execute("""
                CREATE TABLE pickfield_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT,
                    phone NVARCHAR(12),
                    sp NVARCHAR(MAX),
                    sp_input NVARCHAR(MAX),
                    data NVARCHAR(MAX),         
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "tokens":
            cursor.execute("""
                CREATE TABLE tokens (
                    token_id INT IDENTITY(1, 1) PRIMARY KEY,
                    token VARCHAR(MAX) NOT NULL,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "payment":
            cursor.execute("""
                CREATE TABLE payment (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    payment_id INT NOT NULL,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    state NVARCHAR(100),
                    status NVARCHAR(100),
                    price INT,
                    discount_price INT,
                    track_id NVARCHAR(100),
                    result NVARCHAR(100) NULL,
                    discount_id INT DEFAULT NULL,
                    saleReferenceId NVARCHAR(50) NULL,
                    message TEXT, 
                    token NVARCHAR(MAX),                 
                    product_data NVARCHAR(MAX),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "payment_log":
            cursor.execute("""
                CREATE TABLE payment_log (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    payment_id INT NOT NULL,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    state NVARCHAR(100),
                    status NVARCHAR(100),
                    price INT,
                    discount_price INT,
                    track_id NVARCHAR(100),
                    result NVARCHAR(100) NULL,
                    discount_id INT DEFAULT NULL,
                    saleReferenceId NVARCHAR(50) NULL,
                    message TEXT,  
                    token NVARCHAR(MAX),       
                    product_data NVARCHAR(MAX),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "estimate_free":
            cursor.execute("""
                CREATE TABLE estimate_free (
                    estimate_id INT IDENTITY(1, 1) PRIMARY KEY,
                    group_name NVARCHAR(50) NOT NULL,  
                    courses NVARCHAR(MAX) NOT NULL,    
                    percentages NVARCHAR(MAX) NOT NULL, 
                    year INT NOT NULL,
                    original_rank INT NOT NULL,
                    base_rank INT NOT NULL,
                    min_rank INT NOT NULL,
                    max_rank INT NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()

        elif table == "comments":
            cursor.execute("""
                CREATE TABLE comments (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    first_name NVARCHAR(200),  
                    last_name NVARCHAR(200),    
                    comment NVARCHAR(MAX),
                    rating FLOAT DEFAULT 5.0,
                    persian_date NVARCHAR(MAX),
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    first_name_user NVARCHAR(50) NOT NULL,
                    last_name_user NVARCHAR(50) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "estimate":
            cursor.execute("""
                CREATE TABLE estimate (
                    estimate_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    group_name NVARCHAR(50),
                    savabegh_years NVARCHAR(MAX),
                    savabegh_grades NVARCHAR(MAX),
                    savabegh_courses NVARCHAR(MAX),
                    savabegh_scores NVARCHAR(MAX),
                    konkoor_year INT,
                    konkoor_courses NVARCHAR(MAX),
                    konkoor_scores NVARCHAR(MAX),
                    taraaz_total INT,
                    taraaz_savabegh INT,
                    taraaz_savabegh_user INT,
                    taraaz_konkoor INT,
                    taraaz_konkoor_user INT,
                    rank INT,
                    quota INT,            
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "estimate_logs":
            cursor.execute("""
                CREATE TABLE estimate_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    sp NVARCHAR(MAX),
                    sp_input NVARCHAR(MAX),
                    data NVARCHAR(MAX),         
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_logs":
            cursor.execute("""
                CREATE TABLE hoshmand_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    sp NVARCHAR(MAX),
                    sp_input NVARCHAR(MAX),
                    data NVARCHAR(MAX),         
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_info":
            cursor.execute("""
                CREATE TABLE hoshmand_info (
                    id INT IDENTITY(1, 1),
                    user_id INT NOT NULL PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    terms_accepted BIT DEFAULT 0,
                    current_step INT DEFAULT 1,
                    creat_chain_times INT DEFAULT 0,           
                    creat_chain_hoshmand INT DEFAULT 0,           
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_questions":
            cursor.execute("""
                CREATE TABLE hoshmand_questions (
                    id INT IDENTITY(1, 1),
                    user_id INT NOT NULL PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    examtype INT DEFAULT 3,
                    univercity INT DEFAULT 3,
                    major INT DEFAULT 3,           
                    obligation NVARCHAR(MAX) DEFAULT '0,1',
                    method NVARCHAR(MAX) DEFAULT 'با آزمون,صرفا با سوابق تحصیلی',         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_examtype":
            cursor.execute("""
                CREATE TABLE hoshmand_examtype (
                    id INT IDENTITY(1, 1),
                    user_id INT NOT NULL PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    data NVARCHAR(MAX),
                    examtypes NVARCHAR(MAX),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_major":
            cursor.execute("""
                    CREATE TABLE hoshmand_major (
                        id INT IDENTITY(1, 1),
                        user_id INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        data NVARCHAR(MAX),
                        major1 NVARCHAR(MAX),
                        major2 NVARCHAR(MAX),
                        major3 NVARCHAR(MAX),
                        major4 NVARCHAR(MAX),
                        majors NVARCHAR(MAX),
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_province":
            cursor.execute("""
                    CREATE TABLE hoshmand_province (
                        id INT IDENTITY(1, 1),
                        user_id INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        data NVARCHAR(MAX),
                        province1 NVARCHAR(MAX),
                        province2 NVARCHAR(MAX),
                        province3 NVARCHAR(MAX),
                        province4 NVARCHAR(MAX),
                        province5 NVARCHAR(MAX),
                        province6 NVARCHAR(MAX),
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_tables":
            cursor.execute("""
                    CREATE TABLE hoshmand_tables (
                        id INT IDENTITY(1, 1),
                        user_id INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        data_table1 NVARCHAR(MAX),
                        data_table2 NVARCHAR(MAX),
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_universities":
            cursor.execute("""
                    CREATE TABLE hoshmand_universities (
                        id INT IDENTITY(1, 1),
                        user_id INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        uni1 NVARCHAR(MAX),
                        uni2 NVARCHAR(MAX),
                        uni3 NVARCHAR(MAX),
                        uni4 NVARCHAR(MAX),
                        uni5 NVARCHAR(MAX),
                        uni6 NVARCHAR(MAX),
                        uni7 NVARCHAR(MAX),
                        uni8 NVARCHAR(MAX),
                        uni9 NVARCHAR(MAX),
                        uni10 NVARCHAR(MAX),
                        uni11 NVARCHAR(MAX),
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_chains":
            cursor.execute("""
                    CREATE TABLE hoshmand_chains (
                        id INT IDENTITY(1, 1),
                        user_id INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        chains NVARCHAR(MAX),
                        majors NVARCHAR(MAX),
                        universities NVARCHAR(MAX),
                        deleted_chains NVARCHAR(MAX),
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_fields":
            cursor.execute("""
                    CREATE TABLE hoshmand_fields (
                        id INT IDENTITY(1, 1),
                        [user_id] INT NOT NULL PRIMARY KEY,
                        phone NVARCHAR(12) NOT NULL,
                        all_list NVARCHAR(MAX),
                        field_list NVARCHAR(MAX),
                        selected_list NVARCHAR(MAX),
                        trash_list NVARCHAR(MAX),
                        hoshmand_list NVARCHAR(MAX),
                        is_hoshmand  BIT DEFAULT 0,
                        created_time DATETIME DEFAULT GETDATE(),
                        edited_time DATETIME DEFAULT GETDATE(),
                    )
                """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "quiz_answer":
            cursor.execute("""
                CREATE TABLE quiz_answer (
                    quiz_answer_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    name NVARCHAR(200) NOT NULL,
                    quiz_id INT NOT NULL,
                    answers NVARCHAR(MAX) NOT NULL,
                    state INT NOT NULL,                        
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "result_state":
            cursor.execute("""
                CREATE TABLE result_state (
                    result_state_id INT IDENTITY(1, 1),
                    user_id INT NOT NULL PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    t_state NVARCHAR(100) NULL,
                    r_state NVARCHAR(100) NULL,
                    e_state NVARCHAR(100) NULL,
                    a_state NVARCHAR(100) NULL,
                    m_state NVARCHAR(100) NULL,
                    f_state NVARCHAR(100) NULL,
                    i_state NVARCHAR(100) NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "quiz_log":
            cursor.execute("""
                CREATE TABLE quiz_log (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT,
                    q_id INT,
                    phone NVARCHAR(12),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "redis_log":
            cursor.execute("""
                CREATE TABLE redis_log (
                    id INT IDENTITY(1, 1),
                    user_id INT PRIMARY KEY,
                    status VARCHAR(MAX),
                    state INT DEFAULT 0,
                    phone NVARCHAR(12),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "error_log":
            cursor.execute("""
                CREATE TABLE error_log (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT,
                    q_id INT,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hedayat_fields":
            cursor.execute("""
                CREATE TABLE hedayat_fields (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT,
                    phone NVARCHAR(12),
                    suggested NVARCHAR(MAX),
                    other NVARCHAR(MAX),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "discount":
            cursor.execute("""
                CREATE TABLE discount (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    code VARCHAR(10),
                    status NVARCHAR(100),
                    discount_percentage FLOAT,
                    used INT DEFAULT 0,
                    count INT DEFAULT 10000,
                    used_apply INT DEFAULT 0,
                    count_apply INT DEFAULT 0,
                    expire_time DATETIME DEFAULT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "using_discount":
            cursor.execute("""
                CREATE TABLE using_discount (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    code VARCHAR(10),
                    status NVARCHAR(100),
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "telegram_bot":
            cursor.execute("""
                CREATE TABLE telegram_bot (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    payment_id INT not null,
                    code NVARCHAR(100),
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "referral_code":
            cursor.execute("""
                CREATE TABLE referral_code (
                    id INT IDENTITY(1, 1),
                    code NVARCHAR(100),
                    user_id INT NOT NULL PRIMARY KEY,
                    phone NVARCHAR(12) NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "exist_referral_code":
            cursor.execute("""
                CREATE TABLE exist_referral_code (
                    id INT IDENTITY(1, 1),
                    code NVARCHAR(100),
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "pdf_logs":
            cursor.execute("""
                CREATE TABLE pdf_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT,
                    message NVARCHAR(MAX),
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")


def drop_all_tables(conn, cursor, tables):
    for table in tables:
        try:
            if cursor.tables(table=table, tableType='TABLE').fetchone():
                cursor.execute(f"DROP TABLE {table}")
                conn.commit()
                print(f"The {table} table has been dropped.")
            else:
                print(f"The {table} table does not exist.")
        except pyodbc.Error as e:
            print(f"An error occurred while dropping the {table} table: {e}")


conn_db = pyodbc.connect(
    driver='ODBC Driver 17 for SQL Server',
    host='localhost,1433',
    database='ERS',
    UID='mgh27',
    PWD='m2711gH9985',
    TrustServerCertificate='yes'
)
cursor_db = conn_db.cursor()

# drop_all_tables(conn_db, cursor_db,
#                 ["hoshmand_questions", "hoshmand_examtype", "hoshmand_major", "hoshmand_province", "hoshmand_tables",
#                  "hoshmand_universities", "hoshmand_chains", "hoshmand_fields", "hoshmand_info", "hoshmand_logs"])
# drop_all_tables(conn_db, cursor_db, ["hoshmand_fields"])
check_data_base(conn_db, cursor_db,
                ['users', 'stu', 'spgl', 'trgl', 'fspgl', 'ftrgl', 'spglf', 'trglf', 'spfr', 'trfr', 'spfrb', 'trfrb',
                 'speed', 'pick_list', 'sp_list', 'tr_list', 'tokens', 'payment_log', 'payment', 'product',
                 "estimate_free", "comments", "estimate", "hoshmand_questions", "hoshmand_examtype", "hoshmand_major",
                 "hoshmand_province", "hoshmand_tables", "hoshmand_universities", "hoshmand_chains", "hoshmand_fields",
                 "hoshmand_info", "quiz_answer", "result_state", "quiz_log", "redis_log", "error_log", "hedayat_fields",
                 "hoshmand_logs", "discount", "using_discount", "telegram_bot", "estimate_logs", "pickfield_logs",
                 "referral_code", "pdf_logs", "exist_referral_code"])

# discounts = [
#     {'code': generate_discount_code(5), 'percentage': 0.1, 'status': 'ACTIVE',
#      'expire_time': '2025-09-30 21:00:00.000'},
#     {'code': generate_discount_code(5), 'percentage': 0.1, 'status': 'ACTIVE',
#      'expire_time': '2025-09-30 21:00:00.000'},
#     {'code': generate_discount_code(5), 'percentage': 0.1, 'status': 'ACTIVE',
#      'expire_time': '2025-09-30 21:00:00.000'},
#     {'code': generate_discount_code(5), 'percentage': 0.99, 'status': 'ACTIVE',
#      'expire_time': '2025-08-10 17:30:00.000'},
#     {'code': generate_discount_code(5), 'percentage': 0.99, 'status': 'ACTIVE',
#      'expire_time': '2025-08-10 17:30:00.000'}
# ]
#
# for discount in discounts:
#     cursor_db.execute("""
#         INSERT INTO discount (code, discount_percentage, status, expire_time)
#         VALUES (?, ?, ?, ?)
#     """, (discount['code'], discount['percentage'], discount['status'], discount['expire_time']))
# conn_db.commit()
cursor_db.execute("""
        INSERT INTO exist_referral_code (code)
        VALUES (?)
    """, ("elprofesor"))
conn_db.commit()
