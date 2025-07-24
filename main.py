from flask import Flask, render_template, session, request, redirect, url_for, flash
import db_functions
import db_functions as db
from os import urandom
import sqlite3
import time, datetime
import random
import graph_functions
import os, re, ast
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
DATABASE = "forum.db"
app.config["SECRET_KEY"] = urandom(16)
# app.config["secret_key"] = urandom(16)
# print(urandom(16))
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
app.secret_key = os.getenv("secret_key")
print(app.secret_key)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
def auth(route):
    def inner(*args, **kwargs):
        if "email" in session:
            return route(*args, **kwargs)
        else:
            return redirect("/sign-in/")

    return inner


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def not_found(e):
    return render_template("500.html")


@app.route("/")
def index():
    user = "email" in session
    return render_template("main.html", user=user)


@app.route("/sign-up/", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")
    data = dict(request.form)
    if db.get_user_id(data["email"], 1) != -1:
        return render_template(
            "sign-up.html", error="Пользователь с таким email уже существует!"
        )
    data["country"] = "Russia! GOYDA!"
    data["about"] = None
    data["path"] = None
    db.add_user(data)
    session["email"] = data["email"]
    return redirect("/")

@app.route("/sign-in/", methods=["GET", "POST"])
def sign_in():
    print("[sign-in]")
    if request.method == "GET":
        return render_template("sign-in.html")
    data = dict(request.form)
    uid = db.get_user_id(data["email"], 1)
    user = db.get_user(uid, 1)
    
    # orms were invented in 1995... People before 1995:
    if user and user[0][6] == data["password"]:
        session["email"] = data["email"]
        return redirect("/")
    else:
        return render_template("sign-in.html", error="Неверные данные!")


@app.route("/dashboard/")
def dashboard():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")
    data = graph_functions.convert_attempts_by_type(uid)
    labels = data[0]
    correct = data[1]
    incorrect = data[2]
    # orms were invented in 1995... People before 1995:
    [
        _,
        name,
        surname,
        patronymic,
        email,
        age,
        _,
        country,
        _,
        about,
        phone,
        role,
        path,
        *_,
    ] = user[0]
    is_teacher = 0
    if role == "teacher":
        is_teacher = 1
    user_data = {
        "last_name": surname,
        "first_name": name,
        "middle_name": patronymic,
        "email": email,
        "is_teacher": is_teacher,
        "created_at": 0,
        "avatar": path,
    }

    return render_template(
        "profile.html",
        user=user_data,
        labels=labels,
        correct=correct,
        awards = graph_functions.get_awards(uid),
        incorrect=incorrect,
        user_id=uid,
    )


@app.route("/logout/")
def logout():
    if "email" in session:
        del session["email"]
    return redirect("/")


@app.route("/text-lesson/<course_id>")
def text_lesson(course_id):
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")

    html = open(f"Samples_For_Courses/{course_id}.html", "r", encoding="utf8").read()
    return render_template(
        "text-lesson.html",
        course_name=db_functions.get_course(course_id)[0][1],
        materials=html,
        id=course_id,
        user=True,
    )


@app.route("/video-lesson/<course_id>")
def video_lesson(course_id):
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")

    url = open(f"Samples_For_Courses/{course_id}_url.txt", "r", encoding="utf8").read()
    return render_template(
        "video-lesson.html",
        course_name=db_functions.get_course(course_id)[0][1],
        video_url=url,
        id=course_id,
        user=True,
    )


@app.route("/courses")
def courses():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")
    return render_template("courses.html", user=True)


@app.route("/task-lesson/<course_id>/<int:num>")
def task_lesson(course_id, num):
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")

    tasks = db_functions.get_blocks_for_course(course_id)
    print(tasks)
    return render_template(
        "task-lesson.html",
        course_name=db_functions.get_course(course_id)[0][1],
        task=tasks[num - 1],
        id=course_id,
        task_num=num,
        user=True,
    )


def get_max_num(task_id) -> int:  # протестированная функция
    """
    Возвращает максимальный номер файла вида {task_id}\_{num}.ext, чтобы можно было сохранить файл с номером num+1
    :param task_id:  id задания

    :return: максимальный номер файла вида {task_id}\_{num}.ext
    """
    max_num = 0
    pattern = re.compile(rf"{task_id}_(\d+)\.\w+")
    for filename in os.listdir("static/images"):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return max_num


def save_file(file, task_id, form):
    filename = file.filename
    text = form["text"]
    num = get_max_num(task_id) + 1
    filename_ext = os.path.splitext(filename)[1][1:]  # Расширение без точки
    new_filename = f"{task_id}_{num}.{filename_ext}"
    # print(text)
    if filename_ext in ["png", "jpg", "jpeg"]:
        # text = text.replace(f"[{filename_ext}]({filename})", f"""<img src="/static/images/{new_filename}" style="max-width: 100%">""")
        text = text.replace(f"[{filename_ext}]({filename})", f"""<pre class="markdown">![{filename}](/static/images/{new_filename})</pre>""")
        form["text"] = text
    else:
        _temp = f"""<br>
        <a href="/static/other/{new_filename}" class="btn btn-link goida" download>
            <pre class="markdown goida" style="display: inline-block; padding: 0; border: none; background: none;">![...](/static/images/{filename_ext}.png) {form["num_in_ege"]}.{filename_ext}</pre>
        </a>
        """
        text = text.replace(f"[{filename_ext}]({filename})",_temp)
        form["text"] = text
    if filename_ext in ["png", "jpg", "jpeg"]:
        file.save(os.path.join("static/images", new_filename))
    elif filename_ext in ["docx", 'xlsx', 'txt', 'csv']:
        file.save(os.path.join("static/other", new_filename))


@app.route("/add-task", methods=["POST", "GET"])
def add_task():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)

    if not user:
        return redirect("/sign-in/")
    if request.method == "GET":
        return render_template("add-task.html", user=True)
    elif request.method == "POST":
        print(request.form)
        print(request.files)
        temp_form = {
            "text": request.form["text"],
            "answer": request.form["answer"],
            "difficulty": request.form["difficulty"],
            "num_in_ege": db.get_id_type(request.form["num_in_ege"]),
            "source": request.form["source"],
            "time": time.time(),
            "status": 1,
        }
        if "files" in request.files:
            files = request.files.getlist("files")
            for file in files:
                if file:

                    def get_max_absent_task_id() -> int:  # вынести эту функцию в db_functions.py
                        conn = sqlite3.connect("MAIN_BD.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT ID FROM tasks ORDER BY ID")
                        ids = [row[0] for row in cursor.fetchall()]
                        conn.close()
                        if len(ids) == 0:
                            return 1
                        return max(ids) + 1

                    save_file(file, get_max_absent_task_id(), temp_form)
        db_functions.add_task2(temp_form)
        return redirect("/")


@app.route("/tasks/", methods=["GET", "POST"])
def tasks():
    if "email" not in session:
        return redirect("/sign-in/")
    if request.method == "GET":
        # session['email'] = 'k1o0n@yandex.ru'
        uid = db.get_user_id(session["email"], 1)
        user = db.get_user(uid, 1)
        if not user:
            return redirect("/sign-in/")

        tasks = db.get_all_tasks(1)
    else:
        filters = request.form
        diffs = filters.getlist("difficulty") or list(range(1, 11))
        sources = filters.getlist("source")  # ingore >.<
        tps = filters.getlist("task-type") or list(range(1, 28))
        tasks = db.get_tasks_by_params({"ID_type": tps, "difficulty": diffs}, 1)

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
    return render_template("test_task_page.html", tasks=tasks, user=True)


@app.route("/variant/")
def variant():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")

    tasks = db.get_all_tasks(1)
    tasks = [(i[0], i[1], i[3], i[4], i[5], i[2]) for i in tasks]
    random.shuffle(tasks)
    tasks = tasks[:20]
    tasks.sort(key=lambda x: x[3])

    return render_template("variant.html", user=True, tasks=tasks)


@app.route("/variant/<int:id>")
def variant_by_id(id: int):
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if not user:
        return redirect("/sign-in/")

    tasks = db.get_tasks_for_option(id)
    tasks = [(i[0], i[1], i[3], i[4], i[5], i[2]) for i in tasks]
#    random.shuffle(tasks)
#    tasks = tasks[:20]
    tasks.sort(key=lambda x: x[3])

    return render_template("variant.html", user=True, tasks=tasks, variant_id=id)


@app.route("/submit-task", methods=["POST"])
def submit_task():
    # print(session)
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    print(uid, user)
    if not user:
        return redirect("/sign-in/")

    # orms were invented in 1995... People before 1995:
    [user_id, *_] = user[0]
    data = request.json
    task_id = data["task_id"]
    answer = data["ans"].strip()
    correct_answer = db.get_task(task_id, 1)[0][2].strip()

    # For now trying to not change db_functions, so move this later
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


def make_time(x):
    tt = time.localtime(x)
    return datetime.datetime(tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min)


@app.route("/group/<int:group_id>", methods=["POST", "GET"])
def group(group_id):
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    students = db_functions.get_students_for_group(group_id)
    teachers = db_functions.get_teachers_for_group(group_id)
    print(teachers)
    ok = 0
    for teacher in teachers:
        if teacher[0] == uid:
            ok = 1
    for student in students:
        if student[0] == uid:
            ok = 1
    if not ok:
        flash("У вас нет доступа к этой группе")
        return redirect("/groups")
    # TODO: fix kostil
    # ADMIN = db_functions.get_user_role(uid, 1) == "teacher"
    ADMIN = 1
    students.sort(key=lambda x: x[0])
    correct = []
    incorrect = []
    labels = []
    for person in students:
        name = person[1] + " " + person[2]
        labels.append(name)
        all_options_for_person = db_functions.get_results_for_user_in_group(person[0], group_id)
        cor = 0
        if db_functions.get_results_for_user_in_group(person[0], group_id):
            for option in all_options_for_person:
                cor += option[1]
        else:
            cor = 0
        incor = len(all_options_for_person) * 10 - cor

        correct.append(cor)
        incorrect.append(incor)

    try:
        group_name = db.get_group(group_id)[0][
            1
        ]  # Оно теоретически работает, просто в db нет групп еще
    except Exception:
        group_name = "Группа усиленной подготовки по Латеху"
    if ADMIN:
        all_options = db_functions.get_options_for_group(group_id)
        UNDONE_options = [
            {
                "name": i[1],
                "deadline": make_time(i[4]),
                "solved_tasks": 0,
                "total_tasks": 0,
                "id": i[0],
            }
            for i in all_options
        ]
        DONE_options = []
        if len(UNDONE_options) == 0:
            UNDONE_options = [
                {
                    "name": "Пробный вариант",
                    "deadline": make_time(time.time()),
                    "solved_tasks": 0,
                    "total_tasks": 0,
                    "id": 0,
                }
            ]
        token = db.get_group(group_id)[0][3]
        return render_template(
            "group.html",
            teachers=teachers,
            users=students,
            ADMIN=ADMIN,
            group_name=group_name,
            course_id=group_id,
            course_token=token,
            done_options=DONE_options,
            und_options=UNDONE_options,
            user=True,
            labels=labels,
            correct=correct,
            incorrect=incorrect,
        )
    else:
        done_options = db_functions.get_options_for_user_in_group(uid, group_id)
        not_done_options = db_functions.get_options_for_user_in_group_not_done(
            uid, group_id
        )

        def __get(x) -> tuple[int, int]:
            solved: int = db.get_results_for_option_user(uid, x)[1]
            total: int = db.get_task_count_for_option(x)
            return (solved, total)

        done_options = [(i[1], i[4], *__get(i[0])) for i in done_options]
        DONE_options = [
            {
                "name": i[0],
                "deadline": make_time(i[1]),
                "solved_tasks": i[2],
                "total_tasks": i[3],
            }
            for i in done_options
        ]
        UNDONE_options = [
            {
                "name": i[1],
                "deadline": make_time(i[4]),
                "solved_tasks": 0,
                "total_tasks": 0,
            }
            for i in not_done_options
        ]
        token = db.get_group(group_id)[0][3]
        return render_template(
            "group.html",
            teachers=teachers,
            users=students,
            ADMIN=ADMIN,
            group_name=group_name,
            course_id=group_id,
            course_token=token,
            done_options=DONE_options,
            und_options=UNDONE_options,
            user=True,
            labels=labels,
            correct=correct,
            incorrect=incorrect,
        )


@app.route("/groups", methods=["POST", "GET"])
def groups():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    user = db.get_user(uid, 1)
    if request.method == "POST":
        print(request.form)
        # db_functions.add_task(request.form)
        return render_template("groups.html",  user=True, role="teacher")
    if not user:
        return redirect("/sign-in/")
    role = db_functions.get_user_role(uid, 1)
    if role == "teacher":
        groups = db_functions.get_groups_for_teacher(uid)
    else:
        groups = db_functions.get_groups_for_student(uid)
    return render_template("groups.html", groups=groups, user=True, role="teacher")


@app.route("/make_new_group", methods=["POST"])
def make_new_group():
    uid = db.get_user_id(session["email"], 1)
    token = "".join(
        [str(random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"))
                     for i in range(6)])
    db.add_group("Новая группа", uid, token)
    return redirect(url_for("groups"))


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
    if role == "teacher":
        db.add_teacher_into_group(group_id, user_id)
    else:
        db.add_student_into_group(group_id, user_id)
    return redirect(url_for("group", group_id=group_id, section="admin"))


@app.route("/add_option_to_group", methods=["POST"])
def add_option_to_group():
    print(request.form)
    option_id = int(request.form.get("option-id"))
    group_id = int(request.form.get("group_id"))
    db.add_option_into_group(option_id, group_id)
    return redirect(url_for("group", group_id=group_id, section="admin"))


@app.route("/remove_user_from_group", methods=["POST"])
def remove_user_from_group():
    user_id = request.form.get("user_id")
    group_id = request.form.get("group_id")
    db.del_user_from_group(group_id, user_id)
    return redirect(url_for("group", group_id=group_id, section="admin"))


@app.route("/add_to_group", methods=["POST"])
def add_to_group():
    group_code = request.form.get("group_code")
    user_id = db.get_user_id(session["email"], 1)
    role = db_functions.get_user_role(user_id, 1)
    if role == "teacher":
        user_groups = db_functions.get_groups_for_teacher(user_id)
    else:
        user_groups = db_functions.get_groups_for_student(user_id)
    for x in user_groups:
        if x[2] == group_code:
            flash("Вы уже состоите в этой группе")
            return redirect(url_for("groups"))
    print(db.get_group_id(group_code), group_code)
    try:
        group_id = db.get_group_id(group_code)[0][0]
    except Exception:
        flash("Нет такой группы")
        return redirect(url_for("groups"))
    role = db_functions.get_user_role(user_id, 1)
    if role == "teacher":
        db.add_teacher_into_group(group_id, user_id)
    else:
        db.add_student_into_group(group_id, user_id)
    return redirect(url_for("group", group_id=group_id))


@app.route("/make_variant", methods=["POST", "GET"])
def make_variant():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    if request.method == "POST":
        print(request.form['values'], request.form['name'])
        # vals = [int(x) for x in request.form['values']]
        vals = [int(x) for x in ast.literal_eval(request.form['values'])]
        vid = db.add_option({
            'name': request.form['name'],
            'user_id': uid,
            'date': time.time() + 100000})
        for val in vals:
            db.add_task_into_option(vid,val)
        return redirect("/all_variants")
    return render_template("make_variant.html", user=True, role="teacher")


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL  
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            topic_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL, 
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    """
    )
    conn.commit()
    conn.close()


# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Возвращает строки в виде словарей
    return conn


# Главная страница
@app.route("/forum")
def forum():
    conn = get_db_connection()
    # Получаем темы с количеством комментариев
    topics = conn.execute(
        """
            SELECT 
                topics.*, 
                COUNT(comments.id) as comments_count 
            FROM topics 
            LEFT JOIN comments ON topics.id = comments.topic_id 
            GROUP BY topics.id 
            ORDER BY topics.id DESC
        """
    ).fetchall()
    conn.close()
    _user = 0
    if "email" in session:
        _user = 1
    return render_template("forum.html", topics=topics, ADMIN=1, user=_user)


# Страница темы
@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def topic(topic_id):
    conn = get_db_connection()
    if request.method == "POST":
        comment_content = request.form["comment"]
        user_id = (
            1  # Здесь можно добавить логику для получения ID текущего пользователя
        )
        conn.execute(
            "INSERT INTO comments (content, topic_id, user_id) VALUES (?, ?, ?)",
            (comment_content, topic_id, user_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("topic", topic_id=topic_id))

    topic = conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
    comments = conn.execute(
        "SELECT * FROM comments WHERE topic_id = ?", (topic_id,)
    ).fetchall()
    conn.close()
    _user = 0
    if "email" in session:
        _user = 1
    return render_template(
        "topic.html", topic=topic, comments=comments, ADMIN=1, user=_user
    )


# Создание новой темы
@app.route("/forum/create_topic", methods=["GET", "POST"])
def create_topic():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        user_id = 1  # Заглушка - в реальном приложении брать из сессии

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO topics (title, content, user_id) VALUES (?, ?, ?)",
            (title, content, user_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("forum"))
    _user = 0
    if "email" in session:
        _user = 1
    return render_template("create_topic.html", ADMIN=1, user=_user)


# Админская панель
@app.route("/forum/admin")
def admin():
    conn = get_db_connection()

    # Получаем все темы с комментариями
    topics = conn.execute(
        """
        SELECT 
            topics.id as topic_id,
            topics.title as topic_title,
            comments.id as comment_id,
            comments.content as comment_content,
            comments.user_id as comment_user_id
        FROM topics
        LEFT JOIN comments ON topics.id = comments.topic_id
        ORDER BY topics.id DESC, comments.id DESC
    """
    ).fetchall()

    conn.close()

    # Группируем комментарии по темам
    grouped = {}
    for row in topics:
        topic_id = row["topic_id"]
        if topic_id not in grouped:
            grouped[topic_id] = {"title": row["topic_title"], "comments": []}
        if row["comment_id"]:  # Если есть комментарий
            grouped[topic_id]["comments"].append(
                {
                    "id": row["comment_id"],
                    "content": row["comment_content"],
                    "user_id": row["comment_user_id"],
                }
            )
    _user = 0
    if "email" in session:
        _user = 1
    return render_template("admin.html", grouped_topics=grouped, ADMIN=1, user=_user)


# Удаление темы
@app.route("/delete_topic/<int:topic_id>")
def delete_topic(topic_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
    conn.execute("DELETE FROM comments WHERE topic_id = ?", (topic_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


# Удаление комментария
@app.route("/delete_comment/<int:comment_id>")
def delete_comment(comment_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


@app.route("/all_variants")
def all_variants():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)

    variants = db.get_options()
    prepared_variants = [
        {
            "name": i[1],
            "deadline": make_time(i[4]),
            "solved_tasks": 0,
            "total_tasks": 0,
            "id": i[0],
        }
        for i in variants
    ]
    print(prepared_variants)
    return render_template(
        "all_variants.html",
        user=True,
        options=prepared_variants,
        ADMIN=db.get_user_role(uid, 1) == "teacher",
    )


@app.route("/submit-test", methods=["POST"])
def submit_test():
    if "email" not in session:
        return redirect("/sign-in/")
    uid = db.get_user_id(session["email"], 1)
    data = request.json
    data["ID_option"] = data["variant_id"]
    data["ID_user"] = uid
    db.add_result(data)
    return {"status": "ok", "message": "goida!"}

if __name__ == "__main__":
    init_db()  # Инициализация базы данных форума при запуске приложения
    app.run(host="0.0.0.0", port=5000)
