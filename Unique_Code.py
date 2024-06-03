from datetime import datetime

# creates new code using current time and class id
def uni_code(cID):
    code = ""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    for i in range(7):
        no = int(now[0]) + int(now[1])
        code = code + str(no)
        now = now[2:]
    code = str(cID) + "-" + code
    return code

uni_code(1)