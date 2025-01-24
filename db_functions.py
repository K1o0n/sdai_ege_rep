import sqlite3
from time import time

# Special  functions:

def transform_into_list(data):
    result = []
    for key in data.keys():
        result.append(data[key])
    return result

def get_id_type(num):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id FROM Types WHERE num_in_ege").fetchall()[0]
    connect.close()
    return result       # id

# Add functions:

def add_task(data):         #list or dict: (text, answer, difficulty, num_in_ege, source)
    if isinstance(data, dict):
        data = transform_into_list(data)
    data[3] = get_id_type(data[3])
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (text, answer, difficulty, source, ID_tupe) VALUES (?, ?, ?, ?, ?)", data)
    connect.commit()
    connect.close()

def add_user(data):     #list or dict (name, surname, patronymic, email, password, telephone, age, country, role (student, teacher, admin), about, path (path to the photo))
    if type(data) != 'list':
        data = transform_into_list(data)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (name, surname, patronymic, email, password, telephone, age, country, role, about, path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    connect.commit()
    connect.close()

def add_attempt(data):      #list or dict: (ID_student, ID_task, is_right)
    if type(data) != 'list':
        data = transform_into_list(data)
    data.append(time())
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Attempt (ID_student, ID_task, is_right, time) VALUES (?, ?, ?, ?)", data)
    connect.commit()
    connect.close()

def add_result(data):       #list or dict: (score, time, ID_student, ID_option)
    if type(data) != 'list':
        data = transform_into_list(data)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Results (score, time, ID_student, ID_option) VALUES (?, ?, ?, ?)", data)
    connect.commit()
    connect.close()

def add_student_into_course(data):     #list or dict: (ID_student, ID_course)
    if type(data) != 'list':
        data = transform_into_list(data)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_teachers VALUES (ID_student, ID_course) VALUES (?, ?)", data)
    connect.commit()
    connect.close()

def add_teacher_into_course(data):     #list or dict: (ID_teacher, ID_course)
    if type(data) != 'list':
        data = transform_into_list(data)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_Students VALUES (ID_teacher, ID_course) VALUES (?, ?)", data)
    connect.commit()
    connect.close()

def add_file(data):     #list or dict: (ID_task, path, type)
    if type(data) != 'list':
        data = transform_into_list(data)
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Files VALUES (ID_task, path, type) VALUES (?, ?, ?)", data)
    connect.commit()
    connect.close()

# Get functions:

def get_all_tasks():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks").fetchall()
    connect.close()
    return result       # [(id, text, answer, difficulty, ID_type, source)]

def get_answers():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id, answer FROM Tasks").fetchall()
    connect.close()
    return result       # [(id, answer)...]

def get_courses():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Courses").fetchall()
    connect.close()
    return result       # [(id, name, ID_teacher, about, is_public)]

def get_user(id_user):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Users WHERE id = ?", id_user).fetchall()
    connect.close()
    return result       # [(name, surname, patronymic, email, password, telephone, age, country, role (student, teacher, admin), about, path (path to the photo))]

def get_user_id(email):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Users WHERE email = ?", email).fetchall()
    connect.close()
    return result       # id

def get_answer(id_task):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT answer FROM Tasks WHERE id = ?", id_task).fetchall()[0]
    connect.close()
    return result       # answer (string)

