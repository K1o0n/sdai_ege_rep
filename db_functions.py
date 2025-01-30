import sqlite3
from time import time

# Special  functions:

def make_request(request, params = []):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute(request, params).fetchall()
    connect.close()
    return result

def make_interferation(request, params):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute(request, params)
    connect.commit()
    connect.close()
    
def get_id_type(num):
    result = make_request("SELECT id FROM Types WHERE num_in_ege = ?", [num])
    if not result:
        return -1
    return result[0][0]      # id

def get_status_task(id_message):
    result = make_request("SELECT status FROM Tasks WHERE ID = ?", [id_message])
    if not result:
        return -1
    return result[0][0]

def get_status_user(id_message):
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

def add_task(data):         # dict: (text, answer, difficulty, num_in_ege, date, source)
    current = [data['text'], data['answer'], data['difficulty'], get_id_type(data['num_in_ege']), data['source'], time(), 1]
    make_interferation("INSERT INTO Tasks (text, answer, difficulty, source, ID_type, date, status) VALUES (?, ?, ?, ?, ?, ?, ?)", current)

def add_user(data):     # dict (name, surname, patronymic, email, password, telephone, age, country, role (user, user, admin), about, path (path to the photo))
    current = [data['name'], data['surname'], data['patronymic'], data['email'], data['password'], data['telephone'], data['age'], data['country'], data['role'], data['about'], data['path'], time(), 1]
    make_interferation("INSERT INTO Users (name, surname, patronymic, email, password, telephone, age, country, role, about, path, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", current)

def add_attempt(data):      # dict: (ID_user, ID_task, is_right, ID_course)
    current = [data['ID_user'], data['ID_task'], data['is_right'], data['answer'], time(), data['ID_result'], data['ID_course']]
    make_interferation("INSERT INTO Attempt (ID_user, ID_task, is_right, time) VALUES (?, ?, ?, ?, ?, ?, ?)", current)

def add_result(data):       # dict: (score, time, ID_user, ID_option)
    current = [data['score'], data['time'], data['ID_user'], data['ID_option'], data['']]
    make_interferation("INSERT INTO Results (score, time, ID_user, ID_option) VALUES (?, ?, ?, ?)", current)

def add_student_into_course(data):     # dict: (ID_user, ID_course)
    current = [data['ID_user'], data['ID_course']]
    make_interferation("INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current)

def add_teacher_into_course(data):     # dict: (ID_user, ID_course)
    current = [data['ID_user'], data['ID_user']]
    make_interferation("INSERT INTO Course_users (ID_user, ID_course) VALUES (?, ?)", current)

def add_file(data):     # dict: (ID_task, path, type)
    current = [data['ID_task'], data['path'], data['type']]
    make_interferation("INSERT INTO Files (ID_task, path, type) VALUES (?, ?, ?)", current)

def add_message(data): # dict: (name, text, ID_user, date)
    current = [data['name'], data['text'], data['ID_user'], data['date'], 1]
    make_interferation("INSERT INTO Messages (name, text, ID_user, date, status) VALUES (?, ?, ?, ?, ?)", current)

def add_teacher_into_group(group_id, teacher_id):
    current = [group_id, teacher_id]
    make_interferation("INSERT INTO Groups_Teachers (ID_group, ID_teacher) VALUES (?, ?)", current)

def add_student_into_group(group_id, student_id):
    current = [group_id, student_id]
    make_interferation("INSERT INTO Groups_Students (ID_group, ID_Student) VALUES (?, ?)", current)

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
    result = make_request("SELECT * FROM Tasks WHERE status = ?", [status])
    return result       # [(id, text, answer, difficulty, ID_type, source, solution, status(1-active)]

def get_answers(status):
    result = make_request("SELECT id, answer FROM Tasks WHERE ", [status])
    return result       # [(id, answer)...]

def get_courses(status): # (1-active, 2-banned, 3-deleted)
    result = make_request("SELECT * FROM Courses WHERE status = ? ORDER BY date", [status])
    return result       # [(id, name, about, is_public, date, status)]

def get_course(course_id):
    result = make_request("SELECT * FROM Courses WHERE ID = ?", [course_id])
    return result       # [(id, name, about, is_public, date, status)]

def get_groups_for_teacher(teacher_id):
    result = make_request("SELECT Groups.ID, Groups.name FROM Groups JOIN Groups_Teachers ON Groups.ID = Groups_Teachers.ID_group WHERE ID_user = ?", [teacher_id])
    return result  # [(id, name)]

def get_groups_for_student(student_id):
    result = make_request("SELECT Groups.ID, Groups.name FROM Groups JOIN Groups_Students ON Groups.ID = Groups_Students.ID_group WHERE ID_user = ?", [student_id])
    return result  # [(id, name)]

def get_options_for_group(id_group):
    result = make_request("SELECT Oprions.ID, Options.name, Options.ID_user FROM Options JOIN Groups_Options ON Groups_Options.ID_option = Option.ID WHERE ID_group = ?",[id_group])
    return result  # [(id, name, id_of_creator)]

def get_messages(status): # (1-active, 2-banned, 3-deleted)
    result = make_request("SELECT * FROM Messages WHERE status = ? ORDER BY date", [status])
    return result  # [(id, name, text, ID_user, status(1-active), date]

def get_user(id_user, status):
    result = make_request("SELECT * FROM Users WHERE id = ? AND status = ?", [id_user, status])
    return result       # [(name, surname, patronymic, email, password, age, country, role (user, user, admin), about, path (path to the photo)), date, status (1-active, 2-banned, 3-deleted)]

def get_user_id(email, status): # (1-active, 2-banned, 3-deleted)
    result = make_request("SELECT * FROM Users WHERE email = ? AND status = ?", [email, status])
    if not result:
        return -1
    return result[0][0]     # id

def get_answer(id_task):
    result = make_request("SELECT answer FROM Tasks WHERE id = ?", [id_task])
    if not result:
        return ''
    return result[0][0]       # answer (string)

def get_options():
    result = make_request("SELECT * FROM Options")
    return result  # [(id, name, ID_user)]

def get_tasks_for_option(id_option):
    result = make_request("SELECT id_task FROM Tasks_Options WHERE ID = ?", [id_option])
    return result  # [(id_task)]

def get_task(id_task, status):
    result = make_request("SELECT * FROM Tasks WHERE ID = ? AND status = ?", [id_task, status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_params(params, status):        # dict: {ID_type:(x1, x2, x3...), difficulty:()):
    result = make_request("SELECT * FROM Tasks WHERE ID_type IN ? AND difficulty IN ? AND status = ?", [params['ID_type'], params['difficulty'], status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_type(id_type, status):
    result = make_request("SELECT * FROM Tasks WHERE ID_type = ? AND status = ?", [id_type, status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_by_difficulty(difficulty, status):
    result = make_request("SELECT * FROM Tasks WHERE difficulty = ? AND status = ?", [difficulty, status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]
    
def get_tasks_by_source(source, status):
    result = make_request("SELECT * FROM Tasks WHERE source = ? AND status = ?", [source, status])
    return result  # [(id, text, answer, difficulty, ID_type, source, solution, status)]

def get_tasks_for_course(id_course):
    result = make_request("SELECT * FROM Course_Tasks JOIN Tasks ON Tasks.ID = Course_Tasks.ID_task WHERE ID_course = ?", [id_course])
    return result  # [(ID, ID_course, ID_task, is_required, ID, text, answer, difficulty, ID_type, source, solution, status)]

def get_lessons_for_course(id_course):
    result = make_request("SELECT * FROM Lessons_Course JOIN Lessons ON Lessons.ID = Lessons_Courses.ID_task WHERE ID_course = ?", [id_course])
    return result  # [(ID, ID_course, ID_task, is_required, ID, name)]

def get_blok_for_course(id_course):
    result = make_request("SELECT * FROM Blocks WHERE ID_course = ?", [id_course])
    return result  # [(id_lesson)]

def get_files_for_lesson(id_lesson):
    result = make_request("SELECT * FROM Information WHERE ID_lesson = ?", [id_lesson])
    return result  # [(id, path, ID_lesson)]

def get_attempts_of_user_task(id_user, id_task):
    result = make_request("SELECT * FROM Attempts WHERE ID_user = ? AND ID_task = ? ORDER BY date", [id_user, id_task])
    return result  # [(ID, ID_user, ID_task, answer, is_correct, date, ID_course)]

def get_attempts_by_task_type(id_user):
    result = make_request("SELECT Attempts.date, Attempts.is_correct, ID_type, Types.name FROM Attempts JOIN Tasks JOIN Types ON Attempts.ID_task = Tasks.ID AND Tasks.ID_type = Types.ID WHERE Attempts.ID_user = ? ORDER BY Types.name", [id_user])
    return result       # [(date, is_correct, ID_type, Types.name)]

def get_students_for_group(group_id):
    current = [group_id]
    result = make_request("", [group_id])
    return result

def get_attempts_of_user(id_user):
    result = make_request("SELECT * FROM Attempts WHERE ID_user = ?", [id_user])
    return result  # (ID, ID_user, ID_task, is_right, date)

def get_type_name(id_type):
    result = make_request("SELECT name FROM Type WHERE ID = ?", [id_type])
    if not result:
        return ''
    return result[0][0] # name

# Del functions

def del_user(id_user):
    make_interferation("UPDATE Users SET status=3 WHERE ID = ?", [id_user])

def del_task(id_task):
    make_interferation("UPDATE Tasks SET status=3 WHERE ID = ?", [id_task])

def del_message(id_message):
    make_interferation("UPDATE Messages SET status=3 WHERE ID = ?", [id_message])

# Ban functions

def ban_user(id_user):
    make_interferation("UPDATE Users SET status=2 WHERE ID = ?", [id_user])

def ban_task(id_task):
    make_interferation("UPDATE Tasks SET status=2 WHERE ID = ?", [id_task])

def ban_message(id_message):
    make_interferation("UPDATE Messages SET status=2 WHERE ID = ?", [id_message])

def unban_user(id_user):
    if get_status_user(id_user) != 2:
        return False
    make_interferation("UPDATE Users SET status=2 WHERE ID = ?", [id_user])
    return True

def unban_task(id_task):
    if get_status_user(id_task) != 2:
        return False
    make_interferation("UPDATE Tasks SET status=2 WHERE ID = ?", [id_task])
    return True

def unban_message(id_message):
    if get_status_user(id_message) != 2:
        return False
    make_interferation("UPDATE Messages SET status=1 WHERE ID = ?", [id_message])
    return True

# Change functions

def change_user(id_user, data): #list or dict (name, surname, patronymic, email, password, telephone, age, country, role (user, user, admin), about, path (path to the photo))
    current = [data['name'], data['surname'], data['patronymic'], data['email'], data['password'], data['telephone'], data['age'], data['country'], data['role'], data['about'], data['path'], 1]
    current += [id_user]
    make_interferation("UPDATE Users SET name=?, surname=?, patronymic=?, email=?, password=?, telephone=?, age=?, country=?, role=?, about=?, path=?, status=?  WHERE ID = ?", current)

def change_task(id_task, data):     #dict: (text, answer, difficulty, num_in_ege, source)
    current = [data['text'], data['answer'], data['difficulty'], get_id_type(data['num_in_ege']), data['source'], time(), 1]
    current += [id_task]
    make_interferation("UPDATE Tasks SET text=?, answer=?, difficulty=?, ID_type=?, source=?, date=?, status=? WHERE ID = ?", current)

def change_message(id_message, data):       # dict: (name, text, ID_user, date)
    current = [data['name'], data['text'], data['ID_user'], data['date'], 1]
    current += [id_message]
    make_interferation("UPDATE Messages SET name=?, text=?, ID_user=?, date=?, status=? WHERE ID = ?", current)


#@app.route("/group/<int:group_id>")
#def group(group_id):
#    if 'email' not in session:
#        return redirect('/sign-in/')
#    uid = db.get_user_id(session['email'], 1)
#    students = db_functions.get_student
