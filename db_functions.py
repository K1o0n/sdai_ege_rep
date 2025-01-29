import sqlite3
from time import time

# Special  functions:

def get_id_type(num):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id FROM Types WHERE num_in_ege = ?", [num]).fetchall()
    connect.close()
    if not result:
        return -1
    return result[0][0]      # id

def get_status_task(id_message):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT status FROM Messages WHERE ID = ?", [id_message]).fetchall()
    connect.close()
    if not result:
        return -1
    return result[0][0]

def get_status_user(id_message):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT status FROM Messages WHERE ID = ?", [id_message]).fetchall()
    connect.close()
    if not result:
        return -1
    return result[0][0]

def get_status_message(id_message):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT status FROM Messages WHERE ID = ?", [id_message]).fetchall()
    connect.close()
    if not result:
        return -1
    return result[0][0]

# Add functions:

def add_task(data):         # dict: (text, answer, difficulty, num_in_ege, date, source)
    current = [data['text'], data['answer'], data['difficulty'], get_id_type(data['num_in_ege']), data['source'], time(), 1]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Tasks (text, answer, difficulty, source, ID_type, date, status) VALUES (?, ?, ?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_user(data):     # dict (name, surname, patronymic, email, password, telephone, age, country, role (user, user, admin), about, path (path to the photo))
    current = [data['name'], data['surname'], data['patronymic'], data['email'], data['password'], data['telephone'], data['age'], data['country'], data['role'], data['about'], data['path'], time(), 1]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (name, surname, patronymic, email, password, telephone, age, country, role, about, path, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_attempt(data):      # dict: (ID_user, ID_task, is_right, ID_course)
    current = [data['ID_user'], data['ID_task'], data['is_right'], data['answer'], time(), data['ID_result'], data['ID_course']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Attempt (ID_user, ID_task, is_right, time) VALUES (?, ?, ?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_result(data):       # dict: (score, time, ID_user, ID_option)
    current = [data['score'], data['time'], data['ID_user'], data['ID_option'], data['']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Results (score, time, ID_user, ID_option) VALUES (?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_student_into_course(data):     # dict: (ID_user, ID_course)
    current = [data['ID_user'], data['ID_course']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_teacher_into_course(data):     # dict: (ID_user, ID_course)
    current = [data['ID_user'], data['ID_user']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_file(data):     # dict: (ID_task, path, type)
    current = [data['ID_task'], data['path'], data['type']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Files (ID_task, path, type) VALUES (?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_message(data): # dict: (name, text, ID_user, date)
    current = [data['name'], data['text'], data['ID_user'], data['date'], 1]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Messages (name, text, ID_user, date, status) VALUES (?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_teacher_into_group(group_id, teacher_id):
    current = [group_id, teacher_id]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Groups_Teachers (ID_group, ID_teacher) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_student_into_group(group_id, student_id):
    current = [group_id, student_id]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Groups_Students (ID_group, ID_Student) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_group(data, teacher_id): # dict: (name)
    current = [data['name']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Groups VALUES (name) VALUES (?)", current)
    group_id = cursor.execute("SELECT max(ID) FROM Groups WHERE name = ?)", current)
    connect.commit()
    connect.close()
    add_teacher_into_group(group_id, teacher_id)

# Get functions:

def get_all_tasks(status): # (1-active, 2-banned, 3-deleted)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE status = ?", [status]).fetchall()
    connect.close()
    return result       # [(id, text, answer, difficulty, ID_type, source, solution, status(1-active)]

def get_answers():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id, answer FROM Tasks").fetchall()
    connect.close()
    return result       # [(id, answer)...]

def get_courses(status): # (1-active, 2-banned, 3-deleted)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Courses WHERE status = ? ORDER BY date", [status]).fetchall()
    connect.close()
    return result       # [(id, name, about, is_public, date, status)]

def get_course(course_id):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Courses WHERE ID = ?", [course_id]).fetchall()
    connect.close()
    return result       # [(id, name, about, is_public, date, status)]

def get_groups_for_teacher(teacher_id):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT Groups.ID, Groups.name FROM Groups JOIN Groups_Teachers ON Groups.ID = Groups_Teachers.ID_group WHERE ID_user = ?", [teacher_id]).fetchall()
    connect.close()
    return result  # [(id, name)]

def get_groups_for_student(student_id):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT Groups.ID, Groups.name FROM Groups JOIN Groups_Students ON Groups.ID = Groups_Students.ID_group WHERE ID_user = ?", [student_id]).fetchall()
    connect.close()
    return result  # [(id, name)]

def get_options_for_group(id_group):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Options JOIN Groups_Options ON Groups.ID = .ID_group WHERE ID_group = ?",
        [id_group]).fetchall()
    connect.close()
    return result  # [(id, name)]

def get_messages(status): # (1-active, 2-banned, 3-deleted)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Messages WHERE status = ? ORDER BY date", [status]).fetchall()
    connect.close()
    return result  # [(id, name, text, ID_user, status(1-active), date]

def get_user(id_user, status):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Users WHERE id = ? AND status = ?", [id_user, status]).fetchall()
    connect.close()
    return result       # [(name, surname, patronymic, email, password, age, country, role (user, user, admin), about, path (path to the photo)), date, status (1-active, 2-banned, 3-deleted)]

def get_user_id(email, status): # (1-active, 2-banned, 3-deleted)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Users WHERE email = ? AND status = ?", [email, status]).fetchall()
    connect.close()
    if not result:
        return -1
    return result[0][0]     # id

def get_answer(id_task):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT answer FROM Tasks WHERE id = ?", [id_task]).fetchall()
    connect.close()
    if not result:
        return ''
    return result[0][0]       # answer (string)

def get_options():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Options").fetchall()
    connect.close()
    return result  # [(id, name, ID_user)]

def get_tasks_for_option(id_option):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id_task FROM Tasks_Options WHERE ID = ?", [id_option]).fetchall()
    connect.close()
    return result  # [(id_task)]

def get_task(id_task, status):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE ID = ? AND status = ?", [id_task, status]).fetchall()
    connect.close()
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_params(params, status):        # dict: {ID_type:(x1, x2, x3...), difficulty:()):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE ID_type IN ? AND difficulty IN ? AND status = ?", [params['ID_type'], params['difficulty'], status]).fetchall()
    connect.close()
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_type(id_type, status):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE ID_type = ? AND status = ?", [id_type, status]).fetchall()
    connect.close()
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_difficulty(difficulty, status):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE difficulty = ? AND status = ?", [difficulty, status]).fetchall()
    connect.close()
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]
    
def get_tasks_by_source(source, status):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks WHERE source = ? AND status = ?", [source, status]).fetchall()
    connect.close()
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_for_course(id_course):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Course_Tasks JOIN Tasks ON Tasks.ID = Course_Tasks.ID_task WHERE ID_course = ?", [id_course]).fetchall()
    connect.close()
    return result  # [(ID, ID_course, ID_task, is_required, ID, text, answer, difficulty, ID_type, source, solution, status)]

def get_lessons_for_course(id_course):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Lessons_Course JOIN Lessons ON Lessons.ID = Lessons_Courses.ID_task WHERE ID_course = ?", [id_course]).fetchall()
    connect.close()
    return result  # [(ID, ID_course, ID_task, is_required, ID, name)]

def get_blok_for_course(id_course):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Blocks WHERE ID_course = ?", [id_course]).fetchall()
    connect.close()
    return result  # [(id_lesson)]

def get_files_for_lesson(id_lesson):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Information WHERE ID_lesson = ?", [id_lesson]).fetchall()
    connect.close()
    return result  # [(id, path, ID_lesson)]

def get_attempts_of_user_task(id_user, id_task):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Attempts WHERE ID_user = ? AND ID_task = ? ORDER BY date", [id_user, id_task]).fetchall()
    connect.close()
    return result  # [(ID, ID_user, ID_task, answer, is_correct, date, ID_course)]

def get_attempts_by_task_type(id_user):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT Attempts.date, Attempts.is_correct, ID_type, Types.name FROM Attempts JOIN Tasks JOIN Types ON Attempts.ID_task = Tasks.ID AND Tasks.ID_type = Types.ID WHERE Attempts.ID_user = ? ORDER BY Types.name",[id_user]).fetchall()
    connect.close()     # [(date, is_correct, ID_type, Types.name)]
    return result

def get_attempts_of_user(id_user):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Attempts WHERE ID_user = ?", [id_user]).fetchall()
    connect.close()
    return result  # (ID, ID_user, ID_task, is_right, date)

def get_type_name(id_type):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT name FROM Type WHERE ID = ?", [id_type]).fetchall()
    connect.close()
    if not result:
        return ''
    return result[0][0] # name

# Del functions

def del_user(id_user):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET status=3 WHERE ID = ?", [id_user]).fetchall()
    connect.commit()
    connect.close()

def del_task(id_task):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Tasks SET status=3 WHERE ID = ?", [id_task]).fetchall()
    connect.commit()
    connect.close()

def del_message(id_message):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Messages SET status=3 WHERE ID = ?", [id_message]).fetchall()
    connect.commit()
    connect.close()

# Ban functions

def ban_user(id_user):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET status=2 WHERE ID = ?", [id_user]).fetchall()
    connect.commit()
    connect.close()

def ban_task(id_task):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Tasks SET status=2 WHERE ID = ?", [id_task]).fetchall()
    connect.commit()
    connect.close()

def ban_message(id_message):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Messages SET status=2 WHERE ID = ?", [id_message]).fetchall()
    connect.commit()
    connect.close()

def unban_user(id_user):
    if get_status_user(id_user) != 2:
        return False
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET status=2 WHERE ID = ?", [id_user]).fetchall()
    connect.commit()
    connect.close()
    return True

def unban_task(id_task):
    if get_status_user(id_task) != 2:
        return False
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Tasks SET status=2 WHERE ID = ?", [id_task]).fetchall()
    connect.commit()
    connect.close()
    return True

def unban_message(id_message):
    if get_status_user(id_message) != 2:
        return False
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Messages SET status=1 WHERE ID = ?", [id_message]).fetchall()
    connect.commit()
    connect.close()
    return True

# Change functions

def change_user(id_user, data): #list or dict (name, surname, patronymic, email, password, telephone, age, country, role (user, user, admin), about, path (path to the photo))
    current = [data['name'], data['surname'], data['patronymic'], data['email'], data['password'], data['telephone'], data['age'], data['country'], data['role'], data['about'], data['path'], 1]
    current += [id_user]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET name=?, surname=?, patronymic=?, email=?, password=?, telephone=?, age=?, country=?, role=?, about=?, path=?, status=?  WHERE ID = ?", current).fetchall()
    connect.commit()
    connect.close()

def change_task(id_task, data):     #dict: (text, answer, difficulty, num_in_ege, source)
    current = [data['text'], data['answer'], data['difficulty'], get_id_type(data['num_in_ege']), data['source'], time(), 1]
    current += [id_task]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Tasks SET text=?, answer=?, difficulty=?, ID_type=?, source=?, date=?, status=? WHERE ID = ?", current).fetchall()
    connect.commit()
    connect.close()

def change_message(id_message, data):       # dict: (name, text, ID_user, date)
    current = [data['name'], data['text'], data['ID_user'], data['date'], 1]
    current += [id_message]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE Messages SET name=?, text=?, ID_user=?, date=?, status=? WHERE ID = ?", current).fetchall()
    connect.commit()
    connect.close()
