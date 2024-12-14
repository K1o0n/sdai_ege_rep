def check(answ, N):
    checked = []
    for i in range(1, N + 1):
        key = str(i) + "_task"
        right_ans = "static/tasks/" + str(i) + "_answer.txt"
        with open(right_ans) as file:
            data = file.read()
            data = data[:-1]
            if answ[key] == data:
                checked.append(True)
            else:
                checked.append(False)
    return(checked)