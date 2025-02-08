from flask import Flask, render_template, request
import db_functions as db
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def tasks():
    tasks = db.get_all_tasks(1)
    tasks = [(i[0], i[1], i[3], i[4], i[5], i[2]) for i in tasks]
    """
    task = [
        1,         # task id
        "text",    # task statement
        5,         # difficulty
        1,         # number
        'Kompege', # source
        1488       # answer
        ]
    """
    return render_template("task_page.html", tasks=tasks)


@app.route("/submit-task", methods=["POST"])
def submit_answer():
    # TODO: get uid from session
    user_id = 2

    data = request.json
    task_id = data["task_id"]
    answer = data["ans"].strip()
    correct_answer = db.get_task(task_id, 1)[0][2].strip()

    # For now tryin to not change db_functions, so move this later
    conn = sqlite3.connect("MAIN_BD.db")
    conn.cursor().execute(
        """insert into Attempts 
               (ID_task, ID_user, answer, is_correct, date, ID_course)
               values (?, ?, ?, ?, NULL, NULL)""",
        (task_id, user_id, answer, answer == correct_answer),
    ).fetchall()
    conn.commit()
    conn.close()

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
