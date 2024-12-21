import database

def check(answ):
    checked = []
    right_answers = []
    response = database.getAnswers()
    for line in response:
        right_answers.append([line[1], line[2]])
    for item in right_answers:
        if answ[item[1]] == item[0]:
            checked.append(True)
        elif answ[item[1]] == '':
            checked.append('none')
        else:
            checked.append(False)
    return([checked, right_answers])