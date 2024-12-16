import sqlite3


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
    task = f"""
                INSERT INTO tasks 
                (Statement, Type_id, Class, Answer, Solution, Difficulty)
                VALUES  (?, ?, ?, ?, ?, ?);
                """
    doTask(task, data)

def getTasks():
    connection = sqlite3.connect('EGE.db')
    cursor = connection.cursor()
    response = cursor.execute("""SELECT * FROM tasks""")
    ret = []
    for line in response:
        ret.append([line[1], f"{line[0]}_task", "None"])
    return ret

def getAnswers():
    connection = sqlite3.connect('EGE.db')
    cursor = connection.cursor()
    response = cursor.execute("""SELECT * FROM tasks""")
    ret = []
    for line in response:
        print(line)
        ret.append([line[1], f"{line[4]}_task"])
    return ret

# createUser(('Penkina Alla Evgenievna', '+72347135312', 'penkina@gmail.com', 'pAssWoRd'))

getAnswers()