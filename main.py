from flask import Flask, render_template, session, request, redirect, url_for
import db_functions
import db_functions as db
from os import urandom
import sqlite3
import time, datetime

app = Flask(__name__)
DATABASE = 'forum.db'
app.config['SECRET_KEY'] = urandom(16)

def auth(route):
    def inner(*args, **kwargs):
        if 'email' in session:
            return route(*args, **kwargs)
        else:
            return redirect('/sign-in/')
    return inner


@app.route('/')
def index():
    user = 'email' in session
    return render_template('main.html', user=user)



@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign-up.html')
    data = dict(request.form)
    if db.get_user_id(data['email'], 1) != -1:
        return render_template('sign-up.html', error='Пользователь с таким email уже существует!')
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
    if not user:
        return redirect('/sign-in/')

    labels = [str(i) for i in range(1, 28)]
    correct = [i for i in range(10, 38)]
    incorrect = [c for c in correct]
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
                           telephone=phone,
                           labels=labels,
                           correct=correct,
                           incorrect=incorrect,
                           user=True
                           )



@app.route('/logout/')
def logout():
    if 'email' in session:
        del session['email']
    return redirect('/')


@app.route('/text-lesson/<course_id>')
def text_lesson(course_id):
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect('/sign-in/')

    html = open(f'Samples_For_Courses/{course_id}.html', 'r', encoding='utf8').read()
    return render_template(
        'text-lesson.html', 
        course_name=db_functions.get_course(course_id)[0][1],
        materials=html,
        id = course_id,
        user=True)

@app.route('/video-lesson/<course_id>')
def video_lesson(course_id):
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect('/sign-in/')

    url = open(f'Samples_For_Courses/{course_id}_url.txt', 'r', encoding='utf8').read()
    return render_template(
        'video-lesson.html',
        course_name=db_functions.get_course(course_id)[0][1],
        video_url=url,
        id = course_id,
        user=True)

@app.route('/courses')
def courses():
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect('/sign-in/')
    return render_template('courses.html', user=True)

@app.route('/task-lesson/<course_id>/<int:num>')
def task_lesson(course_id, num):
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect('/sign-in/')

    tasks = db_functions.get_tasks_for_course(course_id)
    print(tasks)
    return render_template(
        'task-lesson.html',
        course_name=db_functions.get_course(course_id)[0][1],
        task=tasks[num - 1],
        id=course_id,
        task_num=num,
        user=True)

@app.route("/add-task", methods=['POST', 'GET'])
def add_task():
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)

    if not user:
        return redirect('/sign-in/')
    if request.method == 'GET':
        return render_template("add-task.html", user=True)
    elif request.method == 'POST':
        print(request.form)
        db_functions.add_task(request.form)
        return redirect("/")


@app.route('/tasks/')
def tasks():
    if 'email' not in session:
        return redirect('/sign-in/')
    # session['email'] = 'k1o0n@yandex.ru'
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect('/sign-in/')

    tasks = db.get_all_tasks(1)
    tasks = [(i[0], i[1], i[3], i[4], i[5], i[2]) for i in tasks]
    '''
    task = [
        1,         # task id
        "text",    # task statement
        5,         # difficulty
        1,         # number
        'Kompege', # source
        1488       # answer
        ]
    '''
    return render_template('test_task_page.html', tasks=tasks, user=True)


@app.route('/submit-task', methods=["POST"])
def submit_task(): 
    # print(session)
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)
    print(uid, user)
    if not user:
        return redirect('/sign-in/')
    
    # orms were invented in 1995... People before 1995:
    [user_id, *_] = user[0]
    data = request.json
    task_id = data['task_id']
    answer  = data['ans'].strip()
    correct_answer = db.get_task(task_id, 1)[0][2].strip()

    # For now trying to not change db_functions, so move this later
    conn = sqlite3.connect("MAIN_BD.db")
    conn.cursor().execute(
            '''insert into Attempts 
               (ID_task, ID_user, answer, is_correct, date, ID_course)
               values (?, ?, ?, ?, NULL, NULL)''',
            (task_id, user_id, answer, answer == correct_answer)).fetchall()
    conn.commit()
    conn.close()

    return data
def make_time(x):
    tt = time.localtime(x)
    return datetime.datetime(tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min)
@app.route("/group/<int:group_id>", methods=["POST", "GET"])
def group(group_id):
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    students = db_functions.get_students_for_group(group_id)
    teachers = db_functions.get_teachers_for_group(group_id)
    ADMIN = db_functions.get_user_role(uid, 1) == 'teacher'
    ADMIN = 1
    students.sort(key = lambda x: x[0])
    try:
        group_name = db.get_group(group_id)[0][1] #Оно теоретически работает, просто в db нет групп еще
    except Exception:
        group_name = "Группа усиленной подготовки по Латеху"
    if ADMIN:
        all_options = db_functions.get_options_for_group(group_id)
        UNDONE_options = [{"name": i[1], "deadline": make_time(i[4]), "solved_tasks": 0, "total_tasks": 0} for i in all_options]
        DONE_options = []
        return render_template('group.html', teachers=teachers, users=students, ADMIN=ADMIN,
                           group_name=group_name, course_id=group_id,
                           done_options=DONE_options, und_options=UNDONE_options, user = True)
    else:
        done_options = db_functions.get_options_for_user_in_group(uid, group_id)
        not_done_options= db_functions.get_options_for_user_in_group_not_done(uid, group_id)
        def __get(x) -> tuple[int, int]:
            solved: int = db.get_results_for_option_user(uid, x)[1]
            total : int = db.get_task_count_for_option(x)
            return (solved, total)
        done_options = [(i[1], i[4], *__get(i[0])) for i in done_options]
        DONE_options = [{"name": i[0], "deadline": make_time(i[1]), "solved_tasks": i[2], "total_tasks": i[3]} for i in done_options]
        UNDONE_options = [{"name": i[1], "deadline": make_time(i[4]), "solved_tasks": 0, "total_tasks": 0} for i in not_done_options]
        return render_template('group.html', teachers=teachers, users=students, ADMIN=ADMIN,
                            group_name=group_name, course_id=group_id,
                            done_options=DONE_options, und_options=UNDONE_options, user = True)
# @app.route("/add_option", methods=["POST", "GET"])
# def add_option():
#     if 'email' not in session:
#         return redirect('/sign-in/')
#     uid = db.get_user_id(session['email'], 1)
#     name = request.form["name"]
#     arr = [int(x) for x in request.form["tasks"]]
#     if request.method == "POST":
#         __to_add = [(name, uid, time.time())]
#         __id = db.add_option(__to_add) # теперь существует какой-то новый вариант
#         for __x in arr:
#             db.add_task_into_option(__id, __x)
#         return redirect("/")
#     else:
#         return render_template("add_variant.html", user = True)
@app.route("/add_user_to_group", methods=["POST"])
def add_user_to_group():
    print(request.form)
    user_id = request.form.get("user-id")
    role = request.form.get("role")
    group_id = request.form.get("group_id")
    # Add logic to add the user to the group with the specified role
    # Example: db_functions.add_user_to_group(user_id, group_id, role)
    return redirect(url_for("group", group_id=group_id, section="admin"))

@app.route("/add_option_to_group", methods=["POST"])
def add_option_to_group():
    print(request.form)
    option_id = request.form.get("option-id")
    group_id = request.form.get("group_id")
    # Add logic to add the option to the group
    # Example: db_functions.add_option_to_group(option_id, group_id)
    return redirect(url_for("group", group_id=group_id, section="admin"))
@app.route("/remove_user_from_group", methods=["POST"])
def remove_user_from_group():
    print(request.form)
    user_id = request.form.get("user-id")
    group_id = request.form.get("group_id")
    # Add logic to remove the user from the group
    # Example: db_functions.remove_user_from_group(user_id, group_id)
    return redirect(url_for("group", group_id=group_id, section="admin"))
@app.route("/my-groups", methods=['POST', 'GET'])
def my_groups():
    if 'email' not in session:
        return redirect('/sign-in/')
    uid = db.get_user_id(session['email'], 1)
    user = db.get_user(uid, 1)

    if not user:
        return redirect('/sign-in/')
    if request.method == 'GET':
        groups = [[[1,1],[2,3],[4,6],[1,6],["-",1]],[[1,1],[2,3],[4,6],[1,6],["-",1]],[[1,1],[2,3],[4,6],[1,6],["-",1]]]
        return render_template("groups.html", groups = groups, user=True)
    elif request.method == 'POST':
        print(request.form)
        db_functions.add_task(request.form)
        return redirect("/")


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL  
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL, 
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    ''')
    conn.commit()
    conn.close()

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Возвращает строки в виде словарей
    return conn

# Главная страница
@app.route('/forum')
def forum():
    conn = get_db_connection()
    # Получаем темы с количеством комментариев
    topics = conn.execute('''
            SELECT 
                topics.*, 
                COUNT(comments.id) as comments_count 
            FROM topics 
            LEFT JOIN comments ON topics.id = comments.topic_id 
            GROUP BY topics.id 
            ORDER BY topics.id DESC
        ''').fetchall()
    conn.close()
    return render_template('forum.html', topics=topics, ADMIN = 1)

# Страница темы
@app.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    conn = get_db_connection()
    if request.method == 'POST':
        comment_content = request.form['comment']
        user_id = 1  # Здесь можно добавить логику для получения ID текущего пользователя
        conn.execute('INSERT INTO comments (content, topic_id, user_id) VALUES (?, ?, ?)',
                     (comment_content, topic_id, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('topic', topic_id=topic_id))

    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE topic_id = ?', (topic_id,)).fetchall()
    conn.close()
    return render_template('topic.html', topic=topic, comments=comments, ADMIN = 1)

# Создание новой темы
@app.route('/forum/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = 1  # Заглушка - в реальном приложении брать из сессии

        conn = get_db_connection()
        conn.execute('INSERT INTO topics (title, content, user_id) VALUES (?, ?, ?)',
                     (title, content, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('forum'))
    return render_template('create_topic.html', ADMIN = 1)

# Админская панель
@app.route('/forum/admin')
def admin():
    conn = get_db_connection()

    # Получаем все темы с комментариями
    topics = conn.execute('''
        SELECT 
            topics.id as topic_id,
            topics.title as topic_title,
            comments.id as comment_id,
            comments.content as comment_content,
            comments.user_id as comment_user_id
        FROM topics
        LEFT JOIN comments ON topics.id = comments.topic_id
        ORDER BY topics.id DESC, comments.id DESC
    ''').fetchall()

    conn.close()

    # Группируем комментарии по темам
    grouped = {}
    for row in topics:
        topic_id = row['topic_id']
        if topic_id not in grouped:
            grouped[topic_id] = {
                'title': row['topic_title'],
                'comments': []
            }
        if row['comment_id']:  # Если есть комментарий
            grouped[topic_id]['comments'].append({
                'id': row['comment_id'],
                'content': row['comment_content'],
                'user_id': row['comment_user_id']
            })

    return render_template('admin.html', grouped_topics=grouped, ADMIN = 1)

# Удаление темы
@app.route('/delete_topic/<int:topic_id>')
def delete_topic(topic_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM topics WHERE id = ?', (topic_id,))
    conn.execute('DELETE FROM comments WHERE topic_id = ?', (topic_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Удаление комментария
@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


if __name__ == "__main__":
    init_db()  # Инициализация базы данных форума при запуске приложения
    app.run(host='0.0.0.0', port=8080)
