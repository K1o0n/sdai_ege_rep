import sqlite3
from  datetime import datetime

from flask import request


def doTask(task, data):
    connection = sqlite3.connect('EGE.db')
    cursor = connection.cursor()
    cursor.execute(task, data)
    connection.commit()


def createUser(data):
    task = f"""
            INSERT INTO users (FCs, Tel, Email, Password)
            VALUES  (?, ?, ?, ?);
            """
    doTask(task, data)

def addTask(data):
    new_data = []

    for key in data:
        new_data.append(data[key])
    task = f"""
                INSERT INTO tasks 
                (Type_id, Source, Statement, Answer, Difficulty)
                VALUES  (?, ?, ?, ?, ?);
                """
    doTask(task, new_data)

def getTasks():
    connection = sqlite3.connect('EGE.db')
    cursor = connection.cursor()
    response = cursor.execute("""SELECT * FROM tasks""")
    ret = []

    for line in response:
        ret.append([line[1], f"{line[0]}_task",line[2], line[6], line[7]])
    print(ret)
    return ret

def getAnswers():
    connection = sqlite3.connect('EGE.db')
    cursor = connection.cursor()
    response = cursor.execute("""SELECT * FROM tasks""")
    ret = []
    for line in response:
        print(line)
        ret.append([line[1], line[4], f"{line[0]}_task"])
    return ret

def submitted_data(data):
    for line in data:
        if data[line] != '':
            task = f"""
                    INSERT INTO Submits 
                    (Task_id, User_id, Submit, Time)
                    VALUES  (?, ?, ?, ?);
                    """
            doTask(task, [line, 1, data[line], datetime.today()])
# createUser(('Penkina Alla Evgenievna', '+72347135312', 'penkina@gmail.com', 'pAssWoRd'))

