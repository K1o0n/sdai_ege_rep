from flask import Flask, render_template, session, request, redirect
import db_functions as db

app = Flask(__name__)

def auth(route):
    def inner(*args, **kwargs):
        if 'email' in session:
            return route(*args, **kwargs)
        else:
            return redirect('/sign-in/')


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign-up.html')
    data = dict(request.form)
    data['country'] = 'Russia! GOYDA!'
    data['about'] = None
    data['path'] = None
    db.add_user(data)
    session['email'] = data['email']
    return "123"


@app.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign-in.html')
    data = dict(request.form)
    uid = db.get_user_id(data['email'])
    user = db.get_user(uid)
    # orms were invented in 1995... People before 1995:
    if user and user[0][4] == data['password']:
        session['email'] = data['email']
        return "123"
    else:
        return render_template('sign-in.html', error='Неверные данные!')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

