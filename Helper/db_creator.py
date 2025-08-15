import pyodbc


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

        elif table == "ins":
            cursor.execute("""
                CREATE TABLE ins (
                    ins_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    name NVARCHAR(100) NOT NULL,
                    cap_id INT,
                    password NVARCHAR(50) NOT NULL,
                    logo VARCHAR(MAX) DEFAULT NULL,
                    probability_permission INT DEFAULT 1,
                    verify INT DEFAULT 1,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "con":
            cursor.execute("""
                CREATE TABLE con (
                    con_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    password NVARCHAR(50) NOT NULL,
                    first_name NVARCHAR(100) NOT NULL,
                    last_name NVARCHAR(100) NOT NULL,
                    sex INT DEFAULT 1,
                    ins_id INT NOT NULL,
                    adder_id INT NOT NULL,
                    editor_id INT NOT NULL,
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
                    password NVARCHAR(50) NOT NULL,
                    sex INT,
                    city NVARCHAR(100),
                    sch_name NVARCHAR(100),
                    birth_date NVARCHAR(4),
                    field INT,
                    quota INT,
                    full_number INT,
                    rank INT,
                    rank_all INT,
                    last_rank INT,
                    rank_zaban INT,
                    full_number_zaban INT,
                    rank_all_zaban INT,
                    rank_honar INT,
                    full_number_honar INT,
                    rank_all_honar INT,
                    hoshmand_access INT DEFAULT 0,
                    fr_access INT DEFAULT 0,
                    lock INT DEFAULT 0,
                    finalized INT DEFAULT 0,
                    fr_limit INT DEFAULT 1,
                    hoshmand_limit INT DEFAULT 1,
                    ag_pdf INT DEFAULT 0,
                    ag_pf INT DEFAULT 0,
                    con_finalized INT DEFAULT 0,
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,
                    adder_id INT NOT NULL,
                    editor_id INT NOT NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "capacity":
            cursor.execute("""
                CREATE TABLE capacity (
                    cap_id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    name NVARCHAR(200) NOT NULL,
                    hu INT DEFAULT 0,
                    ha INT DEFAULT 0,
                    fru INT DEFAULT 0,
                    fra INT DEFAULT 0,
                    agu INT DEFAULT 0,
                    aga INT DEFAULT 0,
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
                     phone NVARCHAR(12) NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
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
                     phone NVARCHAR(12) NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     ins_id INT NOT NULL,
                     con_id INT NOT NULL,
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
                     phone NVARCHAR(12) NOT NULL,
                     field INT NOT NULL,
                     special_list NVARCHAR(MAX) NOT NULL,
                     part INT NOT NULL,
                     ins_id INT NOT NULL,
                     con_id INT NOT NULL,
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
                     phone NVARCHAR(12) NOT NULL,
                     field INT NOT NULL,
                     trash_list NVARCHAR(MAX) NOT NULL,
                     part INT NOT NULL,
                     ins_id INT NOT NULL,
                     con_id INT NOT NULL,
                     created_time DATETIME DEFAULT GETDATE(),
                     edited_time DATETIME DEFAULT GETDATE()
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
                    role NVARCHAR(100) NULL,
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
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
                    create_chain_times INT DEFAULT 0,           
                    create_chain_hoshmand INT DEFAULT 0,    
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,        
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,      
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,  
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,                
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL, 
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "quiz_logs":
            cursor.execute("""
                CREATE TABLE quiz_logs (
                    id INT IDENTITY(1, 1) PRIMARY KEY,
                    user_id INT,
                    phone NVARCHAR(12),
                    end_point NCHAR(100),
                    func_name NCHAR(100),
                    data NVARCHAR(MAX),         
                    error_p NVARCHAR(MAX),         
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

        elif table == "api_logs":
            cursor.execute("""
                CREATE TABLE api_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT,
                    phone NVARCHAR(12),
                    end_point NCHAR(100),
                    func_name NCHAR(100),
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
                    end_point NCHAR(100),
                    func_name NCHAR(100),
                    data NVARCHAR(MAX),
                    ins_id INT,
                    con_id INT, 
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
                )
            """)
            conn.commit()
            print(f"The {table} table has been created.")

        elif table == "hoshmand_sp_logs":
            cursor.execute("""
                CREATE TABLE hoshmand_sp_logs (
                    id INT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
                    user_id INT NOT NULL,
                    phone NVARCHAR(12) NOT NULL,
                    sp NVARCHAR(MAX),
                    sp_input NVARCHAR(MAX),
                    data NVARCHAR(MAX),
                    ins_id INT,
                    con_id INT, 
                    error_p NVARCHAR(MAX),         
                    created_time DATETIME DEFAULT GETDATE(),
                    edited_time DATETIME DEFAULT GETDATE(),
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
                    ins_id INT NOT NULL,
                    con_id INT NOT NULL,
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
    database='BBC',
    UID='mgh27',
    PWD='m2711gH9985',
    TrustServerCertificate='yes'
)
cursor_db = conn_db.cursor()

drop_all_tables(conn_db, cursor_db, ['users', 'ins', 'con', 'stu', 'capacity', 'spfr', 'trfr', 'spfrb', 'trfrb', 'pickfield_logs',
                 'tokens', 'hoshmand_questions', 'hoshmand_examtype', 'hoshmand_major',
                 'hoshmand_province', 'hoshmand_tables', 'hoshmand_universities', 'hoshmand_chains', 'hoshmand_fields',
                 'hoshmand_info', 'hoshmand_logs', 'quiz_answer', 'result_state', 'quiz_logs', 'hedayat_fields',
                 'redis_log', 'error_log', 'api_logs', 'hoshmand_sp_logs'])
check_data_base(conn_db, cursor_db,
                ['users', 'ins', 'con', 'stu', 'capacity', 'spfr', 'trfr', 'spfrb', 'trfrb', 'pickfield_logs',
                 'tokens', 'hoshmand_questions', 'hoshmand_examtype', 'hoshmand_major',
                 'hoshmand_province', 'hoshmand_tables', 'hoshmand_universities', 'hoshmand_chains', 'hoshmand_fields',
                 'hoshmand_info', 'hoshmand_logs', 'quiz_answer', 'result_state', 'quiz_logs', 'hedayat_fields',
                 'redis_log', 'error_log', 'api_logs', 'hoshmand_sp_logs'])


cursor_db.execute("""
        INSERT INTO users (phone, password, role)
        VALUES (?, ?, ?)
    """, ("09216272502", "123456", "ins"))
conn_db.commit()

cursor_db.execute("""
        INSERT INTO ins (user_id, phone, password, name, cap_id)
        VALUES (?, ?, ?, ?, ?)
    """, (1, "09216272502", "123456", "ins", 1))
conn_db.commit()

cursor_db.execute("""
        INSERT INTO capacity (user_id, phone, name)
        VALUES (?, ?, ?)
    """, (1, "09216272502", "ins"))
conn_db.commit()