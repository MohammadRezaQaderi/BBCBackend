import uuid, redis, json
from datetime import datetime

from Helper import db_helper
from Quiz.quiz_data import quiz_data_info
from Quiz.quiz_data_extractor import get_quiz_table_info


def submit_quiz_answer(conn, cursor, order_data, info):
    token = str(uuid.uuid4())
    # TODO first check the question and quiz id is possible
    # TODO get the array of the quiz and update it
    query_quiz_answer = db_helper.multi_search_table(
        conn, cursor, "quiz_answer",
        ["answers"],
        ["user_id", "quiz_id"],
        [info["user_id"], order_data["quiz_id"]],
    )
    # TODO here check the info of the null come with the []
    message = ""
    if order_data["state"] != "":
        row_count = db_helper.update_record(
            conn, cursor, "quiz_answer", ['state', 'edited_time'],
            [2, datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ? and quiz_id = ?",
            [info["user_id"], order_data["quiz_id"]]
        )
        return token, "آزمون شما به علت اتمام زمان به پایان رسید."
    if query_quiz_answer is None:
        if order_data[
            "question_Number"] != quiz_data_info[order_data["quiz_id"] - 1]["sections"][0]["questions"][0][
            "question_id"]:
            return None, "this question number is not valid reload qui"
        answers = {order_data["question_Number"]: order_data["question_Answer"]}
        answers_data = json.dumps(answers, ensure_ascii=False)
        name = get_stu_info(conn, cursor, info["user_id"])
        field = '([user_id], [phone], [quiz_id], [answers], [state], [name])'
        values = (
            info["user_id"], info["phone"], order_data["quiz_id"], answers_data, 1, name,)
        res_quiz_add_answer = db_helper.insert_value(conn=conn, cursor=cursor, table_name="quiz_answer",
                                                     fields=field, values=values)
    else:
        answers = json.loads(query_quiz_answer[0])
        answers[order_data["question_Number"]] = order_data["question_Answer"]
        answers_data = json.dumps(answers, ensure_ascii=False)
        answer_state = 1
        if order_data["question_Number"] == order_data["last_question_id"]:
            answer_state = 2
        row_count = db_helper.update_record(
            conn, cursor, "quiz_answer", ['answers', 'state', 'edited_time'],
            [answers_data, answer_state, datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user_id = ? and quiz_id = ?",
            [info["user_id"], order_data["quiz_id"]]
        )
    if order_data["question_Number"] == 484:
        redis_host = '127.0.0.1'
        redis_port = 6379
        redis_password = ''
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        key = "userERSReport"
        r.rpush(key, info["user_id"])
        r.close()
        field = '([user_id], [status], [phone])'
        values = (
            info["user_id"], "user add to queue to create", info["phone"])
        res_log_redis = db_helper.insert_value(conn=conn, cursor=cursor, table_name="redis_log", fields=field,
                                               values=values)
        message = "کارنامه‌ی شما تا لحظاتی  دیگر آماده خواهد شد."
    return token, message


def get_stu_info(conn, cursor, user_id):
    query = 'SELECT first_name, last_name FROM BBC.dbo.stu WHERE user_id = ?'
    res = db_helper.search_table(conn=conn, cursor=cursor, query=query, field=user_id)
    return res[0] + " " + res[1]


def select_stu_quiz_table_info(conn, cursor, order_data, info):
    quiz_info = get_quiz_table_info()
    query = 'SELECT quiz_id, state FROM BBC.dbo.quiz_answer WHERE user_id = ? ORDER BY quiz_id asc'
    res = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
    student_quiz_info = []
    if len(res) == 0:
        for index, q in enumerate(quiz_info):
            q["status"] = 0
            if index == 0:
                q["can_start"] = 1
            else:
                q["can_start"] = 0
            student_quiz_info.append(q)
    else:
        state_of_last_quiz = res[-1][1]
        quiz_answered = res[-1][0]
        for index, q in enumerate(quiz_info):
            if q['id'] < quiz_answered:
                q["status"] = 2
                q["can_start"] = 0
            elif q['id'] == quiz_answered:
                q["status"] = state_of_last_quiz
                if state_of_last_quiz == 2:
                    q["can_start"] = 0
                elif state_of_last_quiz == 1:
                    q["can_start"] = 1
            elif q['id'] == quiz_answered + 1:
                q["status"] = 0
                if state_of_last_quiz == 2:
                    q["can_start"] = 1
                else:
                    q["can_start"] = 0
            else:
                q["status"] = 0
                q["can_start"] = 0
            student_quiz_info.append(q)
    token = str(uuid.uuid4())
    return token, student_quiz_info


def select_stu_quiz_info(conn, cursor, order_data, info):
    token = str(uuid.uuid4())
    query = 'SELECT quiz_id, answers, state FROM BBC.dbo.quiz_answer WHERE user_id = ? ORDER BY quiz_id asc'
    res = db_helper.search_allin_table(conn=conn, cursor=cursor, query=query, field=info["user_id"])
    quiz_id = order_data["quiz_id"] - 1
    if len(res) == 0:
        if quiz_id == 0:
            quiz_info = quiz_data_info[quiz_id]
            return token, quiz_info, {}
        else:
            return None, [], {}
    elif res[-1][0] == order_data["quiz_id"]:
        if res[-1][2] == 2:
            return None, [], {}
        elif res[-1][2] == 1:
            quiz_info = quiz_data_info[quiz_id]
            quiz_answer = json.loads(res[-1][1])
            return token, quiz_info, quiz_answer
    elif res[-1][0] == order_data["quiz_id"] - 1:
        if res[-1][2] == 2:
            quiz_info = quiz_data_info[quiz_id]
            return token, quiz_info, {}
        else:
            return None, [], {}
    elif res[-1][0] < order_data["quiz_id"]:
        return None, [], {}
    elif res[-1][0] > order_data["quiz_id"]:
        return None, [], {}
    elif quiz_id > len(quiz_data_info):
        return token, [], {}
    quiz_info = quiz_data_info[quiz_id]
    return token, quiz_info, json.loads(res[-1][1])
