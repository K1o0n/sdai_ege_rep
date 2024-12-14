from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route("/")
def index():
    kwargs = dict()
    with open("data_base.json") as file:
        data = json.load(file)
    kwargs['name'] = "Регистрация"
    if data[0]['name'] != "":
        kwargs['name'] = "Личный кабинет"
    return render_template("index.html", **kwargs)

@app.route("/sign-in", methods=['POST', 'GET'])
def sign_in():
    if request.method == 'GET':
        return render_template("sign-in.html")
    elif request.method == 'POST':
        print(request.form)
        with open("data_base.json") as file:
            data = json.load(file)
        data[0]['name'] = request.form['name']
        data[0]['color'] = request.form['FavColor']
        data[0]['e-mail'] = request.form['e-mail']
        data[0]['age'] = request.form['age']
        data[0]['password'] = request.form['password']
        data[0]['telephone'] = request.form['telephone']
        #f = request.files['example']
        #f.save('upload')
        print(data)
        with open('data_base.json', 'w') as file:
            file.write(json.dumps(data))
        return redirect("/dashboard")

@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    if request.method == 'GET':
        kwargs = dict()
        with open("data_base.json") as file:
            data = json.load(file)
        kwargs["name"] = data[0]['name']
        kwargs["telephone"] = data[0]['telephone']
        kwargs["email"] = data[0]['e-mail']
        kwargs["color"] = data[0]['color']
        return render_template("dashboard.html", **kwargs)
    elif request.method == 'POST':
        with open("data_base.json") as file:
            data = json.load(file)
        data[0]['name'] = ""
        data[0]['color'] = ""
        data[0]['e-mail'] = ""
        data[0]['age'] = ""
        data[0]['password'] = ""
        data[0]['telephone'] = ""
        print(data)
        with open('data_base.json', 'w') as file:
            file.write(json.dumps(data))
        return redirect("/")

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")