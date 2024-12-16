import database

def check(answ):
    checked = []
    right_answers = []
    response = database.getAnswers()
    for line in response:
        right_answers.append(line[0])
    for item in right_answers:
        if answ[item[1]] == item[0]:
            checked.append(True)
        else:
            checked.append(False)
    return(checked)