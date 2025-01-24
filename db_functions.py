import sqlite3
from time import time

# Special  functions:

def get_id_type(num):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id FROM Types WHERE num_in_ege").fetchall()[0]
    connect.close()
    return result       # id

# Add functions:

def add_task(data):         #list or dict: (text, answer, difficulty, num_in_ege, source)
    current = [data['text'], data['answer'], data['difficulty'], get_id_type(data['num_in_ege']), data['source']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (text, answer, difficulty, source, ID_tupe) VALUES (?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_user(data):     #list or dict (name, surname, patronymic, email, password, telephone, age, country, role (student, teacher, admin), about, path (path to the photo))
    current = [data['name'], data['surname'], data['patronymic'], data['email'], data['password'], data['telephone'], data['age'], data['country'], data['role'], data['about'], data['path']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Users (name, surname, patronymic, email, password, telephone, age, country, role, about, path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_attempt(data):      #list or dict: (ID_student, ID_task, is_right)
    current = [data['ID_student'], data['ID_task'], data['is_right']]
    data.append(time())
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Attempt (ID_student, ID_task, is_right, time) VALUES (?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_result(data):       #list or dict: (score, time, ID_student, ID_option)
    current = [data['score'], data['time'], data['ID_student'], data['ID_option']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Results (score, time, ID_student, ID_option) VALUES (?, ?, ?, ?)", current)
    connect.commit()
    connect.close()

def add_student_into_course(data):     #list or dict: (ID_student, ID_course)
    current = [data['ID_student'], data['ID_course']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_teachers VALUES (ID_student, ID_course) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_teacher_into_course(data):     #list or dict: (ID_teacher, ID_course)
    current = [data['ID_teacher'], data['ID_student']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Course_Students VALUES (ID_teacher, ID_course) VALUES (?, ?)", current)
    connect.commit()
    connect.close()

def add_file(data):     #list or dict: (ID_task, path, type)
    current = [data['ID_task'], data['path'], data['type']]
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Files VALUES (ID_task, path, type) VALUES (?, ?, ?)", current)
    connect.commit()
    connect.close()

# Get functions:

def get_all_tasks():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Tasks").fetchall()
    connect.close()
    return result       # [(id, text, answer, difficulty, ID_type, source, solution)]

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
    result = cursor.execute("SELECT answer FROM Tasks WHERE id = ?", [id_task]).fetchall()[0]
    connect.close()
    return result       # answer (string)

def get_options():
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Options").fetchall()
    connect.close()
    return result  # [(id, name, ID_teacher)]

def get_tasks_id(id_option):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id_task FROM Tasks_Options WHERE ID = ?", [id_option]).fetchall()
    connect.close()
    return result  # [(id_task)]

def get_lessons_for_course(id_course):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT id_lesson FROM Course_Lessons WHERE ID_course = ?", [id_course]).fetchall()
    connect.close()
    return result  # [(id_lesson)]

def get_files_for_lesson(id_lesson):
    connect = sqlite3.connect("MAIN_BD.db")
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM Information WHERE ID_lesson = ?", [id_lesson]).fetchall()
    connect.close()
    return result  # [(id, path, ID_lesson)]