import sqlite3
import os
import hashlib
import pickle
from tkinter import *
from tkinter import ttk
import smtplib, ssl
from email.mime.text import *
from email.mime.multipart import MIMEMultipart
import os
import re
import Unique_Code
import subprocess
import socket
import urllib.request
import csv
import Report
##### Create_SQL #######
# Parameters :- None
# Purpose :- This class holds methods for frequently used sql queries
###########################
class Create_SQL:
    def __init__(self):
        self.dbname = "Account.db"
        self.db=sqlite3.connect(self.dbname)
        self.cursor = self.db.cursor()

    ##### Create_ClassStu #######
    # Parameters :- classid:int, studentid:int, accid:int
    # Return Type :- None
    # Purpose :- adds student into a particular class
    #######################
    def Create_ClassStu(self,classid,studentid,accid):
        sql = "INSERT INTO Class(ClassID, StudentsID, AccountID) VALUES(?,?,?)"
        self.cursor.execute(sql, (classid, studentid, accid))
        self.db.commit()

    ##### Create_Accounts #######
    # Parameters :- Title:string, Firstname:string, Surname:string, School:string, Email:string, userID:int
    # Return Type :- None
    # Purpose :- creates an account for teachers
    #######################
    def Create_Accounts(self, Title, Firstname, Surname, School, Email, userID):
            values = (Title, Firstname, Surname, School, Email,userID)
            sql = "insert into Account(Title,Firstname,Surname,School,Email,UsersID) values (?,?,?,?,?,?)"
            self.cursor.execute(sql, values)
            self.db.commit()

    ##### Session #######
    # Parameters :- FileID:int, ClassID:int, Date:string, Duration:float, StudentsPresent:int
    # Return Type :- None
    # Purpose :- creates session entity for recently complete session
    #######################
    def Session(self, FileID, ClassID, Date, Duration, StudentsPresent):
            values = (FileID, ClassID, Date, Duration, StudentsPresent)
            sql = "insert into Session(FileID,ClassID, Date,Duration,StudentsPresent) values (?,?,?,?,?)"
            self.cursor.execute(sql, values)
            self.db.commit()

    ##### Create_Users #######
    # Parameters :- Username:string, Password:string
    # Return Type :- None
    # Purpose :- adds account login requirements to seperate table
    #######################
    def Create_Users(self, Username, Password):
        values = (Username,Password)
        sql = "insert into Users(Username, Password) values (?,?)"
        self.cursor.execute(sql, values)
        self.db.commit()
        sql = "SELECT UsersID FROM Users"
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        sorting = []
        for i in ids:
            if list(i)[0] == None:
                sorting.append(0)
            else:
                sorting.append(list(i)[0])
        sorting = sorted(sorting)
        return sorting[-1]

    ##### Create_Class #######
    # Parameters :- StudentID:int, AccountID:int
    # Return Type :- None
    # Purpose :- creates a new class
    #######################
    def Create_Class(self, StudentID, AccountID):
            values = (StudentID,AccountID)
            sql = "insert into Class(StudentsID, AccountID) values (?,?)"
            self.cursor.execute(sql, values)
            self.db.commit()

    ##### Create_Students #######
    # Parameters :- Firstname:string, Surname:string, Email:string
    # Return Type :- None
    # Purpose :- creates new student
    #######################
    def Create_Students(self,Firstname,Surname,Email):
            values = (Firstname, Surname, Email)
            sql = "insert into Students(Firstname,Surname,Email) values (?,?,?)"
            self.cursor.execute(sql, values)
            self.db.commit()

    ##### Edit #######
    # Parameters :- Table:string, ID:int, Field:string, Editted:string
    # Return Type :- None
    # Purpose :- edits a specific field in a specific table
    #######################
    def Edit(self, Table, ID, Field, Editted):
            sql = "update {0} set {1}=? where {0}ID=?".format(Table, Field)
            self.cursor.execute(sql, (Editted, ID))
            self.db.commit()

    ##### Delete #######
    # Parameters :- Table:string, ID:int
    # Return Type :- None
    # Purpose :- deletes any entity in any table
    #######################
    def Delete(self, Table, ID):
            sql = "delete from {0} where {0}ID=?".format(Table)
            self.cursor.execute(sql, ID)
            self.db.commit()

##### Account #######
# Parameters :- ID:int, username:string, accID:int
# Return Type :- None
# Purpose :- class for main account window and the windows it branches out to
#######################
class Account:
    def __init__(self, ID, username, accID):
        self.ID = ID
        self.username = username
        self.main = Tk()
        self.main.geometry("150x205")
        self.accId = accID[0]
        self.create = Create_SQL()
        self.hostIP =socket.gethostbyname(socket.gethostname())
        self.start()
        self.db=sqlite3.connect("Account.db")
        self.cursor = self.db.cursor()

    ##### back_reg #######
    # Parameters :- win:object
    # Return Type :- None
    # Purpose :- allows users to go back to first window
    #######################
    def back_reg(self, win):
        win.destroy()
        n.Main()

    ##### start #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- generates main menu within the account
    #######################
    def start(self):
        btn = Button(self.main, text="Edit Account", width=20,
                     command=lambda: self.edit_account())
        btn.pack()
        btn1 = Button(self.main, text="Add Class", width=20,
                      command=lambda: self.add_class())
        btn1.pack()
        btn2 = Button(self.main, text="Edit Class", width=20,
                      command=lambda: self.edit_class())
        btn2.pack()
        btn3 = Button(self.main, text="New Session", width=20,
                      command=lambda: self.code(self.main))
        btn3.pack()
        btn4 = Button(self.main, text="View Class", width=20,
                      command=lambda: self.view_class1())
        btn4.pack()
        btn5 = Button(self.main, text="Offline Mode", width=20,
                      command=lambda: self.offline(self.main))
        btn5.pack()
        btn6 = Button(self.main, text="LogOut", width=20,
                      command=self.log_out)
        btn6.pack()

    ##### offline #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- runs the envoirnment without connecting it to a network
    #######################
    def offline(self,win):
        win.destroy()
        off = subprocess.call(('python OSD.py'))
        n.Main()

    ##### code #######
    # Parameters :- win:object
    # Return Type :- None
    # Purpose :- window asks for the class id of the class you want to run the session with
    #######################
    def code(self, win):
        stu = Toplevel(win)
        classId = Label(stu, text="ClassID")
        classId.grid(row=1, column=1)

        c_id_text = StringVar()
        e1 = Entry(stu, textvariable=c_id_text)
        e1.grid(row=1, column=2)

        btn = Button(stu, text="Confirm", width=20,
                     command=lambda: self.teach_class(e1.get(), stu))
        btn.grid(row=9, column=2)


    ##### teach_class #######
    # Parameters :- cID:int ,win:object
    # Return Type :- None
    # Purpose :- sends email to everyone in class with code, loads the envoirnment, and intitialieses the report making process
    #######################
    def teach_class(self, cID, win):
            sql = "SELECT StudentsID,Email FROM Students INNER JOIN Class USING(StudentsID) WHERE ClassID=? AND AccountID=?"
            self.cursor.execute(sql, (int(cID), int(self.accId[0])))
            stu=self.cursor.fetchall()
            if len(stu):
                MasterCode = Unique_Code.uni_code(cID)
                for i in stu:
                    sql = "SELECT Email FROM Account WHERE AccountID=?"
                    self.cursor.execute(sql, (self.accId[0],))
                    context = ssl.create_default_context()
                    msg = MIMEMultipart()
                    MESSAGE_BODY = "Hello \n A session on the Optics Experimentation Environment has started with a class you are in the Code is:{0}".format(
                        MasterCode)
                    body_part = MIMEText(MESSAGE_BODY, 'plain')
                    msg['Subject'] = "Session Starting"
                    msg['From'] = "christmasshopmail@gmail.com"
                    msg['To'] = i[1]
                    # Add body to email
                    msg.attach(body_part)
                    # Create SMTP object
                    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
                    # Login to the server
                    smtp_obj.login("christmasshopmail@gmail.com", "testpassword123+")
                    # Convert the message to a string and send it
                    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
                    smtp_obj.quit()
                sql = "INSERT INTO Code(MasterCode,HostIP,ClassID) VALUES(?,?,?)"
                self.cursor.execute(sql, (MasterCode, self.hostIP, cID))
                self.db.commit()
                print("before")
                with open("return.txt", "w") as f:
                    f.write(str([MasterCode,self.accId[0]]))
                f.close()
                self.osd(self.main,win)
                n.Main()
            else:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Class Error")
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()
    def osd(self,main,win):
        win.destroy()
        main.destroy()
        subprocess.call(('python OSD.py'))
        n.Main()

    ##### log_out #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- logs the users out and brings them back to first window
    #######################
    def log_out(self):
        self.main.destroy()
        n.Main()

    ##### edit_account #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- allows you to edit a certain area of your account
    #######################
    def edit_account(self):
        editor = Toplevel(self.main)
        editor.wm_title("Choose")
        label = Label(editor, text="Which Element Do You  Want To Edit")
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(editor, text="Firstname", command=lambda: self.edit_sql("Account", "Firstname", editor))
        B1.pack()
        B5 = Button(editor, text="Lastname", command=lambda: self.edit_sql("Account", "Surname", editor))
        B5.pack()
        B2 = Button(editor, text="Password", command=lambda: self.edit_sql("Users", "Password", editor))
        B2.pack()
        B3 = Button(editor, text="Email", command=lambda: self.edit_sql("Account", "Email", editor))
        B3.pack()
        B4 = Button(editor, text="School", command=lambda: self.edit_sql("Account", "School", editor))
        B4.pack()
        B6 = Button(editor, text="Okay", command=editor.destroy)
        B6.pack()


    ##### edit_sql #######
    # Parameters :- table:string, element:string, win:object
    # Return Type :- None
    # Purpose :- updates any field and any table of database
    #######################
    def edit_sql(self, table, element, win):
        win.destroy()
        edit = Tk()
        label = Label(edit, text="New:")
        label.grid(row=1, column=1)
        label = Label(edit, text="Confirm New:")
        label.grid(row=2, column=1)
        new_text = StringVar()
        e1 = Entry(edit, textvariable=new_text)
        e1.grid(row=1, column=2)
        connew_text = StringVar()
        e2 = Entry(edit, textvariable=connew_text)
        e2.grid(row=2, column=2)
        B1 = Button(edit, text="Okay", command=lambda:self.edit_sql2(str(e1.get()),str(e2.get()),edit,table,element))
        B1.grid(row=3, column=2)

    ##### edit_sql2 #######
    # Parameters :- new:string,con_new:string,win:object,table:string,element:string
    # Return Type :- None
    # Purpose :- verifies that inputs are the same and adds to database
    #######################
    def edit_sql2(self,new,con_new,win,table,element):
        if new == con_new:
            win.destroy()
            sql = "update {0} set {1}=? where {0}ID=?".format(table, element)
            self.cursor.execute(sql, (new, self.ID))
            self.db.commit()
            self.edit_account()
        else:
            popup = Toplevel(win)
            popup.wm_title("Error!")
            label = Label(popup, text="Inputs Don't Match")
            label.pack(side="top", fill="x", pady=10)
            B1 = Button(popup, text="Okay", command=popup.destroy)
            B1.pack()

    ##### add_class #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- adds a new class to database
    #######################
    def add_class(self):
        addclass = Tk()
        addclass.geometry = "400x250"
        sql = "SELECT ClassID FROM Class"
        self.cursor.execute(sql)
        ids=self.cursor.fetchall()
        sorting=[]
        for i in ids:
            if list(i)[0]==None:
                sorting.append(0)
            else:
                sorting.append(list(i)[0])
        sorting=sorted(sorting)
        q=1+sorting[-1]
        self.db.commit()
        btn = Button(addclass, text="Add New Student",
                     command=lambda: self.add_student_new(addclass, q))
        btn.pack()
        btn1 = Button(addclass, text="Add Existing Student",
                      command=lambda: self.add_student_existing(q, addclass))
        btn1.pack()

    ##### add_student_new #######
    # Parameters :-  win:object, classid:int
    # Return Type :- None
    # Purpose :- ask for information to create a student
    #######################
    def add_student_new(self, win, classid):
        add = Toplevel(win)
        fname = Label(add, text="New ClassID:{0}".format(classid))
        fname.grid(row=1, column=1)
        fname = Label(add, text="Student Firstname")
        fname.grid(row=2, column=1)
        sname = Label(add, text="Student Surname")
        sname.grid(row=3, column=1)
        email = Label(add, text="Student Email")
        email.grid(row=4, column=1)
        fname_text = StringVar()
        e1 = Entry(add, textvariable=fname_text)
        e1.grid(row=2, column=2)
        sname_text = StringVar()
        e2 = Entry(add, textvariable=sname_text)
        e2.grid(row=3, column=2)
        email_text = StringVar()
        e3 = Entry(add, textvariable=email_text)
        e3.grid(row=4, column=2)
        btn= Button(add, text="Done",
                      command= lambda: self.student_add(str(e1.get()), str(e2.get()), str(e3.get()),add,classid))
        btn.grid(row=5,column=2)

    ##### student_add #######
    # Parameters :- first:string,surname:string,email:string,win:object,classid:int
    # Return Type :- None
    # Purpose :-verifies that inputs where correctly inputted and adds student to database
    # and adds them to class specified
    #######################
    def student_add(self,first,surname,email,win,classid):
        if first!="" and surname!="" and email!="":
            self.create.Create_Students(first, surname, email)
            sql = "SELECT StudentsID FROM Students"
            self.cursor.execute(sql)
            ids = self.cursor.fetchall()
            sorting = []
            for i in ids:
                if list(i)[0] == None:
                    sorting.append(0)
                else:
                    sorting.append(list(i)[0])
            sorting = sorted(sorting)
            self.create.Create_ClassStu(classid, sorting[-1], self.ID)
            win.destroy()
        else:
            popup = Toplevel(win)
            popup.wm_title("Error!")
            label = Label(popup, text="Parameters not filled completely")
            label.pack()
            B1 = Button(popup, text="Okay", command=popup.destroy)
            B1.pack()


    ##### add_student_exisiting #######
    # Parameters :-  win:object, classid:int
    # Return Type :- None
    # Purpose :- asks for exisiting students id so that it can add it to the database
    #######################
    def add_student_existing(self, classid, win):
        edit = Toplevel(win)
        label = Label(edit, text="StudentID:")
        label.grid(row=1, column=1)
        ID_text = StringVar()
        e1 = Entry(edit, textvariable=ID_text)
        e1.grid(row=1, column=2)
        B1 = Button(edit, text="Okay", command=lambda: self.existing_student(classid, edit,e1.get()))
        B1.grid(row=2, column=2)


    ##### existing_student #######
    # Parameters :-  win:object, classid:int, st_id:int
    # Return Type :- None
    # Purpose :- adds existing students to class
    #######################
    def existing_student(self, classid, win,st_id):
            self.cursor.execute("SELECT ClassID,StudentsID FROM Class WHERE ClassID=? AND StudentsID=?",
                           (classid, st_id))
            exist = self.cursor.fetchone()
            if exist is not None:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Student Already in Class")
                label.pack()
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()
            else:
                self.cursor.execute("SELECT StudentsID FROM Students WHERE StudentsID=?",
                                    (st_id,))
                exist = self.cursor.fetchone()
                if exist:
                    self.create.Create_ClassStu(classid,st_id, self.ID)
                    self.db.commit()
                    win.destroy()
                else:
                    popup = Toplevel(win)
                    popup.wm_title("Error!")
                    label = Label(popup, text="Invalid ID")
                    label.pack()
                    B1 = Button(popup, text="Okay", command=popup.destroy)
                    B1.pack()

    ##### edit_class #######
    # Parameters :-  None
    # Return Type :- None
    # Purpose :- presents the option to delete class or deletes student from class
    #######################
    def edit_class(self):
        edit = Toplevel(self.main)
        B1 = Button(edit, text="Delete Class", command=lambda: self.del_class(edit))
        B1.pack()
        B2 = Button(edit, text="Delete Student", command=lambda: self.del_student(edit))
        B2.pack()


    ##### del_class #######
    # Parameters :-  win:object
    # Return Type :- None
    # Purpose :- asks for class id of class that needs to be deleted
    #######################
    def del_class(self, win):
        edit = Toplevel(win)
        label = Label(edit, text="ClassID:")
        label.grid(row=1, column=1)
        ID_text = StringVar()
        e1 = Entry(edit, textvariable=ID_text)
        e1.grid(row=1, column=2)
        B1 = Button(edit, text="Okay", command=lambda: self.del_class2(edit, str(e1.get())))
        B1.grid(row=2, column=2)


    ##### del_class2 #######
    # Parameters :-  edit:object, classid:int
    # Return Type :- None
    # Purpose :- deletes seleected class from database
    #######################
    def del_class2(self, edit, classid):
            self.cursor.execute("SELECT ClassID FROM Class WHERE ClassID=? AND AccountID=?", (classid, self.ID))
            exist = self.cursor.fetchone()
            if len(exist) > 0:
                self.cursor.execute("DELETE FROM Class WHERE ClassID=?", (classid,))
                self.db.commit()
                edit.destroy()
            else:
                popup = Toplevel(edit)
                popup.wm_title("Error!")
                label = Label(popup, text="ID Incorrect")
                label.pack()
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()

    ##### del_student #######
    # Parameters :-  win:object
    # Return Type :- None
    # Purpose :- asks for student id of student that is being deleted
    #######################
    def del_student(self, win):
        edit = Toplevel(win)
        label = Label(edit, text="StudentID:")
        label.grid(row=1, column=1)
        ID_text = StringVar()
        e1 = Entry(edit, textvariable=ID_text)
        e1.grid(row=1, column=2)
        label1 = Label(edit, text="ClassID:")
        label1.grid(row=2, column=1)
        classid_text = StringVar()
        e2 = Entry(edit, textvariable=classid_text)
        e2.grid(row=2, column=2)
        B1 = Button(edit, text="Okay", command=lambda: self.del_student2(edit, str(e1.get()), str(e2.get())))
        B1.grid(row=3,column=2)


    ##### del_student2 #######
    # Parameters :-  edit:object, studentid:int, classid:int
    # Return Type :- None
    # Purpose :- deletes student from that class in the class table
    #######################
    def del_student2(self, edit, studentid, classid):
            self.cursor.execute("SELECT StudentsID FROM Class WHERE StudentsID=? AND ClassID=? AND AccountID=?",
                           (studentid, classid, self.ID))
            exist = self.cursor.fetchone()
            if exist is not None:
                self.cursor.execute("DELETE FROM Class WHERE StudentsID=? AND ClassID=?", (studentid, classid))
                self.db.commit()
                edit.destroy()
            else:
                popup = Toplevel(edit)
                popup.wm_title("Error!")
                label = Label(popup, text="ID Incorrect")
                label.pack()
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()

    ##### edit_student #######
    # Parameters :-  None
    # Return Type :- None
    # Purpose :- edits students information
    #######################
    def edit_student(self):
        editor = Toplevel(self.main)
        editor.wm_title("Choose")
        label = Label(editor, text="Which Element Do You  Want To Edit")
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(editor, text="Firstname", command=lambda: self.edit_sql("Students", "Firstname", editor))
        B1.pack()
        B5 = Button(editor, text="Lastname", command=lambda: self.edit_sql("Students", "Surname", editor))
        B5.pack()
        B3 = Button(editor, text="Email", command=lambda: self.edit_sql("Students", "Email", editor))
        B3.pack()
        B6 = Button(editor, text="Okay", command=editor.destroy)
        B6.pack()


    ##### view_class1 #######
    # Parameters :-  None
    # Return Type :- None
    # Purpose :- asks which class that wants to be viewed
    #######################
    def view_class1(self):
        edit = Tk()
        label = Label(edit, text="ClassID:")
        label.grid(row=1, column=1)
        ID_text = StringVar()
        e1 = Entry(edit, textvariable=ID_text)
        e1.grid(row=1, column=2)
        B1 = Button(edit, text="Okay", command=lambda: self.view_class(edit, str(e1.get())))
        B1.grid(row=2, column=2)


    ##### view_class #######
    # Parameters :- topwin:object, id:int
    # Return Type :- None
    # Purpose :- creates a window displaying the details of every member of the class and there progress in that class
    #######################
    def view_class(self, topwin, id):
            win = Toplevel(topwin)
            self.cursor.execute("SELECT StudentsID, Firstname, Surname,Progress,Email FROM "
                            "Students INNER JOIN Class USING(StudentsID)  WHERE ClassID=?", (id,))
            info = self.cursor.fetchall()
            if len(info) > 0:
                style = ttk.Style()
                style.theme_use('clam')
                tree = ttk.Treeview(win, column=("StudentID", "Firstname", "Surname", "Progress", "Email"),
                                    show='headings', height=5)
                tree.column("# 1", anchor=CENTER)
                tree.heading("# 1", text="StudentID")
                tree.column("# 2", anchor=CENTER)
                tree.heading("# 2", text="Firstname")
                tree.column("# 3", anchor=CENTER)
                tree.heading("# 3", text="Surname")
                tree.column("# 4", anchor=CENTER)
                tree.heading("# 4", text="Progress")
                tree.column("# 5", anchor=CENTER)
                tree.heading("# 5", text="Email")
                # Insert the data in Treeview widget
                for i in info:
                    tree.insert('', 'end', text="1", values=i)
                tree.pack()
                btn = Button(win, text="Back", command=lambda: win.destroy())
                btn.pack()
            else:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="ID Incorrect")
                label.pack()
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()


##### First_Window #######
# Parameters :- None
# Return Type :- None
# Purpose :- class holds the windows and option given when not logged in yet
#######################
class First_Window:
    def __init__(self):
        self.db=sqlite3.connect("Account.db")
        self.cursor = self.db.cursor()
        self.create=Create_SQL()
        self.hostIP = socket.gethostname()

    ##### verify #######
    # Parameters :- username:string, password:string, win:object
    # Return Type :- None
    # Purpose :- verifies the users login and logins them into the main page
    #######################
    def verify(self, username, passw, win):
            password = self.encrypt(passw)
            self.cursor.execute("select UsersID,Username from Users where Password=?", (password,))
            possible = self.cursor.fetchall()
            l1 = []
            print(possible)
            for user in possible:
                if user[1] == str(username):
                    l1.append(user[0])
                    l1.append(user[1])

                else:
                    pass
            if len(l1) > 0:
                print(l1)
                win.destroy()
                print(l1[0])
                self.cursor.execute("SELECT AccountID FROM Account WHERE UsersID=?", (l1[0],))
                t = self.cursor.fetchall()
                print(t)
                Logged = Account(l1[0], l1[1], t)
            else:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Username or Password Incorrect")
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()

    ##### Create_Users #######
    # Parameters :- username:string, password:string, passcon:string, title:string, firstname:string,
    # lastname:string, school:string, email:string, win:object
    # Return Type :- None
    # Purpose :- creates users who sign up and add to database, checks that username is unique
    #######################
    def Create_Users(self, username, password, passcon, title, firstname, lastname, school, email, win):
            self.cursor.execute("SELECT Username FROM Users WHERE Username =?", (str(username),))
            # checks if username already exist within the Accounts database
            existence = self.cursor.fetchone()
            if existence:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Username Already Being Used")
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()
            elif password != passcon:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Password Don't Match")
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()


            elif password == passcon:
                # hashes the password
                encryptpass=self.encrypt(password)
                cur=self.create.Create_Users(username, encryptpass)
                self.create.Create_Accounts(title, firstname, lastname, school, email, cur)
                self.db.commit()
                win.destroy()
                n.Main()

    ##### encrypt #######
    # Parameters :- password:string
    # Return Type :- string
    # Purpose :- using vernier cipher encrypts passwords
    #######################
    def encrypt(self, password):
        key = []
        key[:0] = "KONE"
        if len(password) != len(key):
            x = 0
            for i in range(len(password) - len(key)):
                if i == 4:
                    x = 0
                    key.append(key[x])
                else:
                    key.append(key[x])
                    x += 1
        encrypt_pass = []
        for i in range(len(password)):
            x = (ord(password[i]) + ord(key[i])) % 26
            x += ord('A')
            encrypt_pass.append(chr(x))
        return "".join(encrypt_pass)

    ##### login #######
    # Parameters :- window:object
    # Return Type :- None
    # Purpose :- creates login window
    #######################
    def login(self, window):
        window.destroy()
        login_window = Tk()
        login_window.geometry = "300x150"
        user = Label(login_window, text="Username")
        user.grid(row=1, column=1)
        password = Label(login_window, text="Password")
        password.grid(row=2, column=1)
        user_text = StringVar()
        e1 = Entry(login_window, textvariable=user_text)
        e1.grid(row=1, column=2)

        pass_text = StringVar()
        e2 = Entry(login_window, textvariable=pass_text)
        e2.config(show="*")
        e2.grid(row=2, column=2)

        btn = Button(login_window, text="Confirm", width=20,
                     command=lambda: self.verify(e1.get(), e2.get(), login_window))
        btn.grid(row=3, column=2)
        btn2 = Button(login_window, text="Back", width=20,
                      command=lambda: self.back_reg(login_window))
        btn2.grid(row=3, column=1)

    ##### sign_up #######
    # Parameters :- window:object
    # Return Type :- None
    # Purpose :- creates the window for the sign up
    #######################
    def sign_up(self, window):
        window.destroy()
        signup_window = Tk()
        signup_window.geometry = "400x250"
        user = Label(signup_window, text="Username")
        user.grid(row=1, column=1)
        password = Label(signup_window, text="Password")
        password.grid(row=2, column=1)
        confirm_pass = Label(signup_window, text="Confirm Password")
        confirm_pass.grid(row=3, column=1)
        title = Label(signup_window, text="Title")
        title.grid(row=4, column=1)
        firstname = Label(signup_window, text="Firstname")
        firstname.grid(row=5, column=1)
        lastname = Label(signup_window, text="Lastname")
        lastname.grid(row=6, column=1)
        email = Label(signup_window, text="Email")
        email.grid(row=7, column=1)
        school = Label(signup_window, text="School")
        school.grid(row=8, column=1)

        user_text = StringVar()
        e1 = Entry(signup_window, textvariable=user_text)
        e1.grid(row=1, column=2)

        pass_text = StringVar()
        e2 = Entry(signup_window, textvariable=pass_text)
        e2.grid(row=2, column=2)
        e2.config(show="*")
        passcon_text = StringVar()
        e3 = Entry(signup_window, textvariable=passcon_text)
        e3.grid(row=3, column=2)
        e3.config(show="*")

        title_text = StringVar()
        e4 = Entry(signup_window, textvariable=title_text)
        e4.grid(row=4, column=2)

        firstname_text = StringVar()
        e5 = Entry(signup_window, textvariable=firstname_text)
        e5.grid(row=5, column=2)

        lastname_text = StringVar()
        e6 = Entry(signup_window, textvariable=lastname_text)
        e6.grid(row=6, column=2)

        email_text = StringVar()
        e7 = Entry(signup_window, textvariable=email_text)
        e7.grid(row=7, column=2)

        school_text = StringVar()
        e8 = Entry(signup_window, textvariable=school_text)
        e8.grid(row=8, column=2)

        btn = Button(signup_window, text="Confirm", width=20,
                     command=lambda: self.Create_Users(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e8.get(),
                                                  e7.get(), signup_window))
        btn.grid(row=9, column=2)

        btn2 = Button(signup_window, text="Back", width=20,
                      command=lambda: self.back_reg(signup_window))
        btn2.grid(row=9, column=1)

    ##### back_reg #######
    # Parameters :- win:object
    # Return Type :- None
    # Purpose :- allows users to go back to first window
    #######################
    def back_reg(self, win):
        win.destroy()
        n.Main()

    def offline(self,win):
        win.destroy()
        off = subprocess.call(('python OSD.py'))
        n.Main()

    ##### student_access #######
    # Parameters :- window:object
    # Return Type :- None
    # Purpose :- allows student to enter a code to enter an envoirnment and allows students to access offline mode
    #######################
    def student_access(self, window):
        window.destroy()
        access_window = Tk()
        access_window.geometry = "400x250"
        student = Label(access_window, text="StudentID")
        student.grid(row=1, column=1)
        code = Label(access_window, text="Code")
        code.grid(row=2, column=1)

        s_id_text = StringVar()
        e1 = Entry(access_window, textvariable=s_id_text)
        e1.grid(row=1, column=2)

        code_text = StringVar()
        e2 = Entry(access_window, textvariable=code_text)
        e2.grid(row=2, column=2)
        btn = Button(access_window, text="Offline Access", width=20,
                     command=lambda:self.offline(access_window) )
        btn.grid(row=9, column=3)

        btn = Button(access_window, text="Confirm", width=20,
                     command=lambda: self.studentaccess(e1.get(), e2.get(),access_window))
        btn.grid(row=9, column=2)

        btn2 = Button(access_window, text="Back", width=20,
                      command=lambda: self.back_reg(access_window))
        btn2.grid(row=9, column=1)

    ##### studentaccess #######
    # Parameters :- win:object, code:string, stu_id:int
    # Return Type :- None
    # Purpose :- verifies that code entered is valid and that they are in the class in which
    # the session is being hosted for
    #######################
    def studentaccess(self, stu_id, code,win):
        classID = code.partition("-")[0]
        sql = "SELECT * FROM Class WHERE StudentsID=? AND ClassID=? "
        self.cursor.execute(sql, (stu_id, classID))
        if len(self.cursor.fetchall()) !=0:
            self.cursor.execute("SELECT MasterCode FROM Code WHERE ClassID={0}".format(str(classID)))
            co=self.cursor.fetchone()
            print(classID)
            truecode=co+("%",)
            if len(truecode) != 0:
                if truecode[0]==code:
                    clientip = socket.gethostbyname(socket.gethostname())
                    sql = "SELECT MasterCode,HostIP,ClientIP FROM Code WHERE MasterCode=? AND HostIP=? AND ClientIP=?"
                    self.cursor.execute(sql, (code, self.hostIP, clientip))
                    print(self.cursor.fetchall())
                    if not len(self.cursor.fetchall()):
                        sql = "INSERT INTO Code(MasterCode,HostIP,ClientIP,ClassID) VALUES(?,?,?,?)"
                        self.cursor.execute(sql, (code, self.hostIP,clientip,classID))
                        self.db.commit()
                    else:
                        pass
                    subprocess.call(('python Client-Student.py'))
            else:
                popup = Toplevel(win)
                popup.wm_title("Error!")
                label = Label(popup, text="Code Incorrect")
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Okay", command=popup.destroy)
                B1.pack()

        else:
            popup = Toplevel(win)
            popup.wm_title("Error!")
            label = Label(popup, text="Not In Class")
            label.pack(side="top", fill="x", pady=10)
            B1 = Button(popup, text="Okay", command=popup.destroy)
            B1.pack()

    ##### Main #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- first window to pop up when you run the program
    #######################
    def Main(self):
        window = Tk()
        window.geometry("360x144")

        op = Label(window, text="Choose an Option")
        op.grid(row=1, column=2, columnspan=2)

        log_btn = Button(window, text="Login", width=50, height=2, command=lambda: self.login(window))
        log_btn.grid(row=3, column=2)

        reg_btn = Button(window, text="Sign Up", width=50, height=2, command=lambda: self.sign_up(window))
        reg_btn.grid(row=5, column=2)

        stu_btn = Button(window, text="Student Access", width=50, height=2, command=lambda: self.student_access(window))
        stu_btn.grid(row=7, column=2)
        window.mainloop()







