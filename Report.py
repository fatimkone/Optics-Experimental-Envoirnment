from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import xlsxwriter
import sqlite3
import smtplib, ssl
from email.mime.text import *
from email.mime.multipart import MIMEMultipart
import os
import csv


def Reported(time):
    db=sqlite3.connect("Account.db")
    cursor=db.cursor()
    MasterCode=time[0]
    accId=time[1]
    sql = "SELECT ClientIP FROM Code WHERE MasterCode=?"
    cursor.execute(sql, (MasterCode,))
    stu = cursor.fetchall()
    stu = list(dict.fromkeys(stu))
    # creates file reports for end of session
    CSV_Report(MasterCode, time[3], time[2])
    # inserts files into database
    sql = " INSERT INTO Files (File,File2, AccountID) VALUES(?,?,?)"
    path = os.path.abspath("{0}.csv".format(MasterCode))
    path2 = os.path.abspath("{0}.xlsx".format(MasterCode))
    insert = (path,path2, accId)
    cursor.execute(sql, insert)
    db.commit()
    sql = "SELECT FilesID FROM Files"
    cursor.execute(sql)
    ids = cursor.fetchall()
    sorting = []
    for i in ids:
        if list(i)[0] is None:
            sorting.append(0)
        else:
            sorting.append(list(i)[0])
    sorting = sorted(sorting)
    last = sorting[-1]
    # sends files to email
    sql = "SELECT Email FROM Account WHERE AccountID=?"
    cursor.execute(sql, (accId,))
    msg = MIMEMultipart()
    MESSAGE_BODY = "Hello \n Find the report for your session on Optics Experimentation Environment attached"
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = "Session File"
    msg['From'] = "christmasshopmail@gmail.com"
    msg['To'] = cursor.fetchall()[0][0]
    # Add body to email
    msg.attach(body_part)
    # Attach the file with filename to the email
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("{0}.csv".format(MasterCode), "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}.csv"'.format(MasterCode))
    msg.attach(part)

    part2 = MIMEBase('application', "octet-stream")
    part2.set_payload(open("{0}.csv".format(MasterCode), "rb").read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', 'attachment; filename="{0}.xlsx"'.format(MasterCode))
    msg.attach(part2)

    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # Login to the server
    smtp_obj.login("christmasshopmail@gmail.com", "testpassword123+")
    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()
    # adds session info into databse
    x = len(stu) - 1
    sql = "INSERT INTO Session(ClassID,Files,Duration,StudentsPresent) VALUES(?,?,?,?)"
    cursor.execute(sql, (MasterCode.partition("-")[0], last, time[0], x))
    db.commit()
    sql = "DELETE FROM Code WHERE MasterCode=?"
    cursor.execute(sql, (MasterCode,))
    db.commit()
##### CSV_Report #######
# Parameters :- code:string, answered:list, question:list
# Purpose :- creates files for session one file that displays a bar chart and another that displays
# a more in depth analysis of each student and identify who may need help or more of a challenge
###########################
def CSV_Report(code, answered, question):
    header = ["StudentID", "Name"]
    f = open("{0}.csv".format(code), 'w')
    data = []
    for qs in question:
        data.append(0)
    for i in answered.values():
        x = 0
        for p in i:
            data[x] = data[x] + int(p)
            x += 1
    for d in range(0, len(data)):
        data[d] = data[d] / len(answered.keys()) * 100
    f.close()
    # creates bar chart for average correct against questions set
    workbook = xlsxwriter.Workbook("{0}.xlsx".format(code))
    worksheet = workbook.add_worksheet()
    chart = workbook.add_chart({'type': 'bar'})
    worksheet.write("A1", "Question Average")
    worksheet.write_column("A2", data)
    chart.add_series({'name': '=Sheet1!$A$1', 'values': '=Sheet1!$A$2:$A${}'.format(len(data) + 1)})
    chart.set_title({'name': 'Class Average Per Question'})
    chart.set_x_axis({'name': 'Percentage(%)'})
    chart.set_y_axis({'name': 'Question No.'})
    chart.set_style(13)
    worksheet.insert_chart('B1', chart, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    f = open("{0}.csv".format(code), 'a')
    writer = csv.writer(f, delimiter=',')
    header = header + question
    writer.writerow(i for i in header)
    ID = answered.keys()
    rankings = {}
    # gets percentage of correct answers for each student
    for student in ID:
        total = 0
        for i in answered[student]:
            total = total + int(i)
        total = total / len(question) * 100
        rankings[student] = total
    # updates students progress for that class in database
    with sqlite3.connect("Account.db") as db:
        cursor = db.cursor()
        classId = code.split("-")[0]
        for student in ID:
            details = []
            sql = "SELECT Firstname, Surname  FROM Students WHERE StudentsID=?"
            cursor.execute(sql, (student,))
            name=cursor.fetchone()
            details.append(student)
            details.append("{} {}".format(name[0], name[1]))
            for i in ("".join(repr(e) for e in answered[student])):
                details.append(i)
            writer.writerow(i for i in details)
            sql = "UPDATE Class SET Progress=? WHERE ClassID=? AND StudentsID=?"
            cursor.execute(sql, (rankings[student], classId, student))

    top = []
    help = []
    for i in ID:
        # identifies those who need more a challenge
        if rankings[i] >= 95:
            top.append(i)
        # identifies those who need help
        elif rankings[i] <= 60:
            help.append(i)
    writer.writerow(i for i in ["StudentID of Those That Need a Challenge"])
    writer.writerow(i for i in top)
    writer.writerow(i for i in ["StudentID of Those That Need Help"])
    writer.writerow(i for i in help)
    f.close()

