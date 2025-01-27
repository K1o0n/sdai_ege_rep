from flask import Flask, render_template, session, request, redirect

import db_functions
import db_functions as db
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(16)

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
    return redirect('/dashboard/')


@app.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign-in.html')
    data = dict(request.form)
    uid = db.get_user_id(data['email'], 1)
    user = db.get_user(uid, 1)
    # orms were invented in 1995... People before 1995:
    if user and user[0][6] == data['password']:
        session['email'] = data['email']
        return redirect('/dashboard/')
    else:
        return render_template('sign-in.html', error='Неверные данные!')

@app.route('/dashboard/')
def dashboard():
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    print(uid, user)
    if not user:
        return redirect('/sign-in/')
    
    # orms were invented in 1995... People before 1995:
    [_, name, surname, patronymic, email, 
     age, _, country, _, about, phone, path, *_] = user[0]
    return render_template('dashboard.html', 
                           name=f'{surname} {name} {patronymic}', 
                           email=email, 
                           age=age,
                           country=country,
                           image_path=path,
                           color='Цвета в нашем сервисе пока не поддерживаются, приносим свои извнинения. За Россию!',
                           telephone=phone
                           )


@app.route('/logout/')
def logout():
    if 'email' in session:
        del session['email']
    return redirect('/')


@app.route('/text-lesson/<course_id>')
def text_lesson(course_id):
    html = open(f'Samples_For_Courses/{course_id}.html', 'r', encoding='utf8').read()
    return render_template(
        'text-lesson.html', 
        course_name=db_functions.get_courses(course_id),
        materials=html,
        id = course_id)

@app.route('/video-lesson/<course_id>')
def video_lesson(course_id):
    url = open(f'Samples_For_Courses/{course_id}_url.txt', 'r', encoding='utf8').read()
    return render_template(
        'video-lesson.html',
        course_name=db_functions.get_courses(course_id),
        video_url=url,
        id = course_id)

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/task-lesson/<course_id>/<num>')
def task_lesson(course_id, num):
    tasks = db_functions.get_tasks_for_course(num)
    tasks.append(tasks[0])
    print(tasks)
    return render_template(
        'task-lesson.html',
        course_name=db_functions.get_courses(course_id),
        task= tasks[num],
        id = course_id,
        task_num = num)

@app.route("/add-task", methods=['POST', 'GET'])
def add_task():
    if request.method == 'GET':
        return render_template("add-task.html")
    elif request.method == 'POST':
        print(request.form)
        db_functions.add_task(request.form)
        return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

