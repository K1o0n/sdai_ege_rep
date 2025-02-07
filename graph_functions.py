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
        if cur_index == 0 or all_attempts[cur_index][5] == all_attempts[cur_index - 1][5]:
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

def get_awards(id_user):
    """
    params: id_user: int
    return: List
    """
    role = db.get_user_role(id_user, 1)
    result = []
    if role != 'teacher':
      tasks = db.get_cnt_tasks_for_user(id_user, 1)
      types = db.get_cnt_types_for_user(id_user)
