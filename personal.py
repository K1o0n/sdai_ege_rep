from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

import check_answers

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    kwargs = dict()
    with open("data_base.json") as file:
        data = json.load(file)
    kwargs['name'] = "Регистрация"
    if data[0]['name'] != "":
        kwargs['name'] = "Личный кабинет"
    return render_template("tasks.html", **kwargs)

@app.route("/tasks", methods=['POST', 'GET'])
def tasks():
    N = 6
    kwargs = dict()
    if request.method == 'GET':
        task = []
        for i in range(1, N + 1):
            name = "static/tasks/" + str(i) + "_task.txt"
            file = open(name, mode="r", encoding="UTF-8")
            s = file.read()
            file.close()
            s = s.replace('\n', '<br>')
            task.append([s, name[13:-4], "None"])
        kwargs["tasks"] = task
        return render_template("task_page.html", **kwargs)
    elif request.method == 'POST':
        print(request.form)
        post = check_answers.check(request.form, N)
        task = []
        for i in range(1, N + 1):
            name = "static/tasks/" + str(i) + "_task.txt"
            file = open(name, mode="r", encoding="UTF-8")
            s = file.read()
            file.close()
            s = s.replace('\n', '<br>')
            if post[i - 1]:
                color = "green"
            else:
                color = "red"
            key = str(i) + "_task"
            right_ans = "static/tasks/" + str(i) + "_answer.txt"
            with open(right_ans) as file:
                data = file.read()
                data = data[:-1]
            task.append([s, name[13:-4], color, request.form[key], data])
        print(task)
        if "check_answers" in request.form and request.form["check_answers"] == 'on':
            kwargs["check_answers"] = True
        else:
            kwargs["check_answers"] = False
        kwargs["tasks"] = task
        return render_template("task_page.html", **kwargs)

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")