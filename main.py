from flask import Flask, render_template, session, request
import db_functions as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/sign-up/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('sign-in.html')
    data = dict(request.form)
    data['country'] = 'Russia! GOYDA!'
    data['about'] = None
    data['path'] = None
    db.add_user(data)
    return "123"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

