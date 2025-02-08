import db_functions as db
import time

from db_functions import get_attempts_by_task_type


def convert_time(current_time):
    result = (time.localtime(current_time).tm_year, time.localtime(current_time).tm_mon)
    return result


def convert_attempts_by_months(user_id):
    all_attempts = db.get_attempts_of_user(user_id)
    for i in range(len(all_attempts)):
        all_attempts[i][5] = convert_time(all_attempts[i][5])
    cur_index = 0
    result = {}
    correct = 0
    wrong = 0
    while cur_index < len(all_attempts):
        if (
            cur_index == 0
            or all_attempts[cur_index][5] == all_attempts[cur_index - 1][5]
        ):
            result[all_attempts[cur_index][5]] = (correct, wrong)
            correct = 0
            wrong = 0
        else:
            if all_attempts[cur_index][4]:
                correct += 1
            else:
                wrong += 1
    return result


def convert_attempts_by_type(user_id):
    all_attempts = get_attempts_by_task_type(user_id)
    cur_index = 0
    result1 = [i for i in range(1, 28)]
    result2 = [0] * 27
    result3 = [0] * 27
    while cur_index < len(all_attempts):
        if all_attempts[cur_index][1]:
            result2[all_attempts[cur_index][2]] += 1
        else:
            result3[all_attempts[cur_index][2]] += 1
        cur_index += 1
    return result1, result2, result3


def get_step(num, step):
    r = -1
    while num >= 1:
        num //= step
        r += 1
    return r


def get_awards(id_user):
    """
    params: id_user: int
    return: List: if student: [List:[int
    """
    role = db.get_user_role(id_user, 1)
    result = []
    if role == "student":
        tasks = db.get_cnt_tasks_for_user(id_user, 1)
        if len(tasks) == 0:
            c1 = 0
        else:
            c1 = len(tasks)
        n1 = get_step(c1, 5)
        types = db.get_cnt_types_for_user(id_user)
        if len(types) == 0:
            c2 = 0
        else:
            c2 = len(types)
        n2 = get_step(c2, 5)
        groups = db.get_groups_for_student(id_user)
        if len(groups) == 0:
            c3 = 0
        else:
            c3 = len(groups)
        n3 = get_step(c3, 2)
        result = [
            [c1, n1, 3 ** (n1 + 1)],
            [c2, n2, 5 ** (n2 + 1)],
            [c3, n3, 2 ** (n3 + 1)],
        ]
    elif role == "teacher":
        options = db.get_cnt_options_for_teacher(id_user)
        if len(options) == 0:
            c1 = 0
        else:
            c1 = len(options)
        n1 = get_step(c1, 5)
        groups = db.get_cnt_groups_for_teacher(id_user)
        if len(groups) == 0:
            c2 = 0
        else:
            c2 = len(groups)
        n2 = get_step(c2, 2)
        all_groups = db.get_groups_for_student(id_user)
        if len(all_groups) == 0:
            c3 = 0
        else:
            c3 = len(all_groups)
        n3 = get_step(c3, 2)
        result = [[c1, n1, 2 ** (n1 + 1)]]
        result.append([c2, n2, 3 ** (n2 + 1)])
        result.append([c3, n3, 5 ** (n3 + 1)])
    return result


print(get_awards(1))
