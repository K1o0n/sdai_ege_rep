from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

import check_answers
import database

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    kwargs = dict()
    kwargs['name'] = "Регистрация"
    return render_template("tasks.html", **kwargs)

@app.route("/tasks", methods=['POST', 'GET'])
def tasks():
    kwargs = dict()
    task = []
    tasks = database.getTasks()
    print(tasks)
    print("________________________")
    if request.method == 'GET':

        for item in tasks:
            s = item[0].replace('\n', '<br>')
            task.append([s, item[1], "none", item[2]])
        kwargs["tasks"] = task
        return render_template("task_page.html", **kwargs)

    elif request.method == 'POST':
        print(request.form)
        post = check_answers.check(request.form)

        for i in range(len(tasks)):
            s = tasks[i][0].replace('\n', '<br>')
            if post[0][i] == True:
                color = "green"
            elif post[0][i] == 'none':
                color = "none"
            else:
                color = "red"

            task.append([s, tasks[i][1], color, tasks[i][2], request.form[post[1][i][1]], post[1][i][0]])
        if "check_answers" in request.form:
            kwargs["check_answers"] = True
        else:
            kwargs["check_answers"] = False
        kwargs["tasks"] = task
        return render_template("task_page.html", **kwargs)

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")