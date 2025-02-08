import sqlite3
from time import time

# Special  functions:


def make_request(request, params):
    """
    :param request: string
    :param params: List
    :return: result (List[Tuple])
    """
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute(request, params).fetchall()
    connect.close()
    return result


def make_interferation(request, params):
    """
    :param request: string
    :param params: List
    :return: result (List[Tuple])
    """
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute(request, params)
    connect.commit()
    connect.close()


def get_id_type(num):
    """
    :param num: int
    :return: id (int)
    """
    result = make_request("SELECT id FROM Types WHERE num_in_ege = ?", [num])
    if not result:
        return -1
    return result[0][0]


def get_status_task(id_message):
    """
    :param id_message: int
    :return: status (int)
    """
    result = make_request("SELECT status FROM Tasks WHERE ID = ?", [id_message])
    if not result:
        return -1
    return result[0][0]


def get_status_user(id_message):
    """
    :param id_message: int
    :return: status (int)
    """
    result = make_request("SELECT status FROM Users WHERE ID = ?", [id_message])
    if not result:
        return -1
    return result[0][0]


def get_status_message(id_message):
    result = make_request("SELECT status FROM Messages WHERE ID = ?", [id_message])
    if not result:
        return -1
    return result[0][0]


# Add functions:


def add_task(data):
    """dict (text, answer, difficulty, num_in_ege, date, source)"""
    current = [
        data["text"],
        data["answer"],
        data["difficulty"],
        get_id_type(data["num_in_ege"]),
        data["source"],
        time(),
        1,
    ]
    make_interferation(
        "INSERT INTO Tasks (text, answer, difficulty, source, ID_type, date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        current,
    )


def add_user(data):
    """dict (name, surname, patronymic, email, password, telephone, age, country, role (student, teacher, admin), about, path (path to the photo))"""
    current = [
        data["name"],
        data["surname"],
        data["patronymic"],
        data["email"],
        data["password"],
        data["telephone"],
        data["age"],
        data["country"],
        data["role"],
        data["about"],
        data["path"],
        time(),
        1,
    ]
    make_interferation(
        "INSERT INTO Users (name, surname, patronymic, email, password, telephone, age, country, role, about, path, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        current,
    )


def add_attempt(data):
    """dict (ID_user, ID_task, is_right, ID_course)"""
    current = [
        data["ID_user"],
        data["ID_task"],
        data["is_right"],
        data["answer"],
        time(),
        data["ID_result"],
        data["ID_course"],
    ]
    make_interferation(
        "INSERT INTO Attempt (ID_user, ID_task, is_right, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        current,
    )


def add_result(data):
    """dict (score, time, ID_user, ID_option)"""
    current = [data["score"], data["time"], data["ID_user"], data["ID_option"]]
    make_interferation(
        "INSERT INTO Results (score, time, ID_user, ID_option) VALUES (?, ?, ?, ?)",
        current,
    )


def add_student_into_course(data):
    """dict (ID_user, ID_course)"""
    current = [data["ID_user"], data["ID_course"]]
    make_interferation(
        "INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current
    )


def add_teacher_into_course(data):
    """dict (ID_user, ID_course)"""
    current = [data["ID_user"], data["ID_user"]]
    make_interferation(
        "INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current
    )


def add_file(data):
    """dict (ID_task, path, type)"""
    current = [data["ID_task"], data["path"], data["type"]]
    make_interferation(
        "INSERT INTO Files (ID_task, path, type) VALUES (?, ?, ?)", current
    )


def add_message(data):
    """dict (name, text, ID_user, date)"""
    current = [data["name"], data["text"], data["ID_user"], data["date"], 1]
    make_interferation(
        "INSERT INTO Messages (name, text, ID_user, date, status) VALUES (?, ?, ?, ?, ?)",
        current,
    )


def add_teacher_into_group(group_id, teacher_id):
    """int group_id, int teacher_id"""
    current = [group_id, teacher_id]
    make_interferation(
        "INSERT INTO Groups_Teachers (ID_group, ID_user) VALUES (?, ?)", current
    )


def add_student_into_group(group_id, student_id):
    """int group_id, int student_id"""
    current = [group_id, student_id]
    make_interferation(
        "INSERT INTO Groups_Students (ID_group, ID_user) VALUES (?, ?)", current
    )


def add_group(name, user_id, token):
    """
    params: name: str
    params: user_of_creator: int
    params: token: str
    """
    current = [name]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute(
        "INSERT INTO Groups (name, ID_user, token) VALUES (?, ?)",
        [name, user_id, token],
    )
    group_id = cursor.execute(
        "SELECT max(ID) FROM Groups WHERE name = ?", current
    ).fetchone()[0]
    connect.commit()
    connect.close()
    add_teacher_into_group(group_id, user_id)


def add_option(data) -> int:
    """
    params: data: Dict[name:str, user_id:int, date:int]
    return: int - Номер варианта, который был добавлен в базу данных.
    """
    current = [data["name"], data["user_id"], time(), data["date"]]
    make_interferation(
        "INSERT INTO Options (name, ID_user, date1, date2) VALUES (?, ?, ?, ?)", current
    )
    result = make_request("SELECT max(ID) FROM Options", [])
    return result[0][0]


def add_task_into_option(option_id, task_id):
    """
    params: option_id: int
    params: task_id: int
    """
    make_interferation(
        "INSERT INTO Tasks_Options (ID_task, ID_option) VALUES (?, ?)",
        [task_id, option_id],
    )


def add_option_into_group(option_id, group_id):
    """
    params: option_id: int
    params: group_id: int
    """
    make_interferation(
        "INSERT INTO Groups_Options (ID_group, ID_option) VALUES (?, ?)",
        [group_id, option_id],
    )


# Get functions:


def get_all_tasks(status):
    """int status (1-active, 2-banned, 3-deleted)"""
    result = make_request("SELECT * FROM Tasks WHERE status = ?", [status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status(1-active)]


def get_answers(status):
    """int status (1-active, 2-banned, 3-deleted)"""
    result = make_request("SELECT id, answer FROM Tasks WHERE ", [status])
    return result  # [(id, answer)...]


def get_courses(status):
    """int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Courses WHERE status = ? ORDER BY date", [status]
    )
    return result  # [(id, name, about, is_public, date, status)]


def get_course(course_id):
    """int course_id"""
    result = make_request("SELECT * FROM Courses WHERE ID = ?", [course_id])
    return result  # [(id, name, about, is_public, date, status)]


def get_groups_for_teacher(teacher_id):
    """int teacher_id"""
    result = make_request(
        "SELECT Groups.ID, Groups.name, Groups.token FROM Groups JOIN Groups_Teachers ON Groups.ID = Groups_Teachers.ID_group WHERE Groups_Teachers.ID_user = ?",
        [teacher_id],
    )
    return result  # [(id, name, token)]


def get_groups_for_student(student_id):
    """int student_id"""
    result = make_request(
        "SELECT Groups.ID, Groups.name, Groups.token FROM Groups JOIN Groups_Students ON Groups.ID = Groups_Students.ID_group WHERE Groups_Students.ID_user = ?",
        [student_id],
    )
    return result  # [(id, name, token)]


def get_options_for_group(group_id):
    """
    :param group_id: int
    :return: List[Tuple(id:int, name:int, id_of_creator:int, date1:int, date2:int)]
    """
    result = make_request(
        "SELECT Options.ID, Options.name, Options.ID_user, Options.date1, Options.date2 FROM Options JOIN Groups_Options ON Groups_Options.ID_option = Options.ID WHERE ID_group = ?",
        [group_id],
    )
    return result


def get_students_for_group(group_id):
    """
    :param group_id: int
    :return: List[Tuple(id:int, name:str, surname:str)]
    """
    result = make_request(
        "SELECT Users.id, name, surname FROM Users JOIN Groups_Students ON Users.id = Groups_Students.ID_user WHERE ID_group = ?",
        [group_id],
    )
    return result


def get_teachers_for_group(group_id):
    """
    :param group_id: int
    :return: List[Tuple(id:int, name:str, surname:str)]
    """
    result = make_request(
        "SELECT Users.id, name, surname FROM Users JOIN Groups_Teachers ON Users.id = Groups_Teachers.ID_user WHERE ID_group = ?",
        [group_id],
    )
    return result

def get_user(user_id, status):
    """int user_id, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Users WHERE id = ? AND status = ?", [user_id, status]
    )
    return result  # [(name, surname, patronymic, email, password, age, country, role (user, user, admin), about, path (path to the photo)), date, status (1-active, 2-banned, 3-deleted)]


def get_user_role(user_id, status):
    """int user_id, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT role FROM Users WHERE id = ? AND status = ?", [user_id, status]
    )
    return result[0][0]


def get_user_id(email, status):
    """str email, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Users WHERE email = ? AND status = ?", [email, status]
    )
    if not result:
        return -1
    return result[0][0]  # id


def get_options_for_user_in_group(user_id, group_id):
    """
    :param user_id: int
    :param group_id: int
    :return: List[Tuple[id:int, name:str, user_id:int, date1:int (Дата добавления варианта), date2:int (Дата сдачи)]]
    """
    result = make_request(
        "SELECT * FROM Options JOIN Groups_Options ON Options.ID = Groups_Options.ID_option WHERE ID_group = ? AND ID_Option IN (SELECT ID_option FROM Results WHERE ID_user = ?)",
        [group_id, user_id],
    )
    return result


def get_options_for_user_in_group_not_done(user_id, group_id):
    """
    :param user_id: int
    :param group_id: int
    :return: List[Tuple[id:int, name:str, user_id:int, date1:int, date2:int]]
    """
    result = make_request(
        "SELECT * FROM Options JOIN Groups_Options ON Options.ID = Groups_Options.ID_option WHERE ID_group = ? AND ID_Option NOT IN (SELECT ID_option FROM Results WHERE ID_user = ?)",
        [group_id, user_id],
    )
    return result


def get_results_for_option_user(user_id, option_id):
    """
    :param user_id: int
    :param option_id: int
    :return: List[Tuple[id:int, score:int, time:int, user_id:int, option_id:int]]
    """
    """int user_id, int option_id"""
    result = make_request(
        "SELECT * FROM Results WHERE ID_option = ? AND ID_user = ?",
        [option_id, user_id],
    )
    return result


def get_task_count_for_option(option_id) -> int:
    """
    :param option_id: int
    :return: int - the count of tasks associated with the given option_id.
    """
    result = make_request(
        "SELECT COUNT(*) FROM Tasks_Options WHERE option_id = ?", [option_id]
    )
    if not result:
        return 0
    return result[0][0]


def get_answer(task_id):
    """int task_id"""
    result = make_request("SELECT answer FROM Tasks WHERE id = ?", [task_id])
    if not result:
        return ""
    return result[0][0]  # answer (string)


def get_group(group_id):
    """
    :param group_id: int
    :return: List[Tuple(id:int, name:str, id_of_creator:int, token:str)]
    """
    result = make_request("SELECT * FROM Groups WHERE ID = ?", [group_id])
    return result


def get_group_id(token):
    """
    params: token: str
    return: List[Tuple(id:int))
    """
    result = make_request("SELECT ID FROM Groups WHERE token = ?", [token])
    return result


def get_options():
    """
    return: List[Tuple(id:int, name:str, ID_user:int, date1:int, date2:int)]
    """
    result = make_request("SELECT * FROM Options", [])
    return result


def get_cnt_options_for_teacher(user_id):
    """
    params: user_id:int
    return: List[Tuple(id:int)]
    """
    result = make_request(
        "SELECT DISTINCT ID FROM Options WHERE ID_user = ?", [user_id]
    )
    return result


def get_cnt_groups_for_teacher(user_id):
    """
    params: user_id:int
    return: List[Tuple(id:int)]
    """
    result = make_request("SELECT DISTINCT ID FROM Groups WHERE ID_user = ?", [user_id])
    return result


def get_task(task_id, status):
    """int task_id, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Tasks WHERE ID = ? AND status = ?", [task_id, status]
    )
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]


def get_tasks_by_params(params, status):
    """dict {ID_type:(x1, x2, x3, ...), difficulty:(x1, x2, x3, ...))"""
    mas1 = [str(i) for i in params["ID_type"] if i != None]
    mas2 = [str(i) for i in params["difficulty"] if i != None]
    s1 = "(" + ", ".join(mas1) + ")"
    s2 = "(" + ", ".join(mas2) + ")"
    request = (
        "SELECT * FROM Tasks WHERE ID_type IN "
        + s1
        + " AND difficulty IN"
        + s2
        + "AND status = ?"
    )
    result = make_request(request, [status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]


def get_cnt_tasks_for_user(user_id, status):
    result = make_request(
        "SELECT DISTINCT ID_task FROM Attempts JOIN Users ON Attempts.ID_user = Users.ID WHERE is_correct = 1 AND ID_User = ? AND status = ?",
        [user_id, status],
    )
    return result


def get_cnt_types_for_user(user_id):
    result = make_request(
        "SELECT DISTINCT ID_type FROM Attempts JOIN Tasks ON Attempts.ID_task = Tasks.ID WHERE is_correct = 1 AND ID_User = ?",
        [user_id],
    )
    return result


def get_tasks_by_type(type_id, status):
    """int type_id, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Tasks WHERE ID_type = ? AND status = ?", [type_id, status]
    )
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]


def get_tasks_by_difficulty(difficulty, status):
    """int difficulty, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Tasks WHERE difficulty = ? AND status = ?", [difficulty, status]
    )
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]


def get_tasks_by_source(source, status):
    """str source, int status (1-active, 2-banned, 3-deleted)"""
    result = make_request(
        "SELECT * FROM Tasks WHERE source = ? AND status = ?", [source, status]
    )
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]


def get_tasks_for_course(course_id):
    """int course_id"""
    result = make_request(
        "SELECT * FROM Course_Tasks JOIN Tasks ON Tasks.ID = Course_Tasks.ID_task WHERE ID_course = ?",
        [course_id],
    )
    return result  # [(ID, ID_course, ID_task, is_required, ID, text, answer, difficulty, ID_type, source, solution, status)]

def get_blocks_for_course(course_id):
    """
    params: course_id:int
    return: List[Tuple()]
    """
    part1 = make_request("SELECT * FROM Blocks JOIN Tasks ON Tasks.ID = Blocks.ID_block WHERE ID_course = ? AND type = 1", [course_id])
    part2 = make_request("SELECT * FROM Blocks JOIN Lessons ON Lessons.ID = Blocks.ID_block WHERE ID_course = ? AND type = 2", [course_id])
    result = part1 + part2
    return result


def get_files_for_information(lesson_id):
    """int lesson_id"""
    result = make_request("SELECT * FROM Information WHERE ID_lesson = ?", [lesson_id])
    return result  # [(id, path, ID_lesson)]


def get_attempts_of_user_task(user_id, task_id):
    """int user_id, int task_id"""
    result = make_request(
        "SELECT * FROM Attempts WHERE ID_user = ? AND ID_task = ? ORDER BY date",
        [user_id, task_id],
    )
    return result  # [(ID, ID_user, ID_task, answer, is_correct, date, ID_course)]


def get_attempts_by_task_type(user_id):
    """int user_id"""
    result = make_request(
        "SELECT Attempts.date, Attempts.is_correct, ID_type, Types.name FROM Attempts JOIN Tasks JOIN Types ON Attempts.ID_task = Tasks.ID AND Tasks.ID_type = Types.ID WHERE Attempts.ID_user = ? ORDER BY Types.name",
        [user_id],
    )
    return result  # [(date, is_correct, ID_type, Types.name)]


def get_attempts_of_user(user_id):
    """int user_id"""
    result = make_request("SELECT * FROM Attempts WHERE ID_user = ?", [user_id])
    return result  # (ID, ID_user, ID_task, is_right, date)


def get_type_name(type_id):
    """int type_id"""
    result = make_request("SELECT name FROM Type WHERE ID = ?", [type_id])
    if not result:
        return ""
    return result[0][0]  # name


# Del functions


def del_user(user_id):
    """int user_id"""
    make_interferation("UPDATE Users SET status=3 WHERE ID = ?", [user_id])


def del_user_from_group(group_id, user_id):
    """int group_id, int user_id"""
    make_interferation(
        "DELETE FROM Groups_Students WHERE ID_group = ? AND ID_user = ?",
        [group_id, user_id],
    )


def del_task(task_id):
    """int task_id"""
    make_interferation("UPDATE Tasks SET status=3 WHERE ID = ?", [task_id])


def del_message(message_id):
    """int message_id"""
    make_interferation("UPDATE Messages SET status=3 WHERE ID = ?", [message_id])


# Ban functions


def ban_user(user_id):
    """int user_id"""
    make_interferation("UPDATE Users SET status=2 WHERE ID = ?", [user_id])


def ban_task(task_id):
    """int task_id"""
    make_interferation("UPDATE Tasks SET status=2 WHERE ID = ?", [task_id])


def ban_message(message_id):
    """int message_id"""
    make_interferation("UPDATE Messages SET status=2 WHERE ID = ?", [message_id])


def unban_user(user_id):
    """int user_id"""
    if get_status_user(user_id) != 2:
        return False
    make_interferation("UPDATE Users SET status=2 WHERE ID = ?", [user_id])
    return True


def unban_task(task_id):
    """int task_id"""
    if get_status_user(task_id) != 2:
        return False
    make_interferation("UPDATE Tasks SET status=2 WHERE ID = ?", [task_id])
    return True


def unban_message(message_id):
    """int message_id"""
    if get_status_user(message_id) != 2:
        return False
    make_interferation("UPDATE Messages SET status=1 WHERE ID = ?", [message_id])
    return True


# Change functions


def change_user(user_id, data):
    """int user_id, dict (name, surname, patronymic, email, password, telephone, age, country, role (user, user, admin), about, path (path to the photo)"""
    current = [
        data["name"],
        data["surname"],
        data["patronymic"],
        data["email"],
        data["password"],
        data["telephone"],
        data["age"],
        data["country"],
        data["role"],
        data["about"],
        data["path"],
        1,
    ]
    current += [user_id]
    make_interferation(
        "UPDATE Users SET name=?, surname=?, patronymic=?, email=?, password=?, telephone=?, age=?, country=?, role=?, about=?, path=?, status=?  WHERE ID = ?",
        current,
    )


def change_task(task_id, data):
    """int task_id, dict (text, answer, difficulty, num_in_ege, source)"""
    current = [
        data["text"],
        data["answer"],
        data["difficulty"],
        get_id_type(data["num_in_ege"]),
        data["source"],
        time(),
        1,
    ]
    current += [task_id]
    make_interferation(
        "UPDATE Tasks SET text=?, answer=?, difficulty=?, ID_type=?, source=?, date=?, status=? WHERE ID = ?",
        current,
    )


def change_message(message_id, data):
    """dict (name, text, ID_user, date)"""
    current = [data["name"], data["text"], data["ID_user"], data["date"], 1]
    current += [message_id]
    make_interferation(
        "UPDATE Messages SET name=?, text=?, ID_user=?, date=?, status=? WHERE ID = ?",
        current,
    )
