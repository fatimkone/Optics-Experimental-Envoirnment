import math
import socket
import threading
import tkinter
import tkinter.scrolledtext
from math import *
import time


##### Server #######
# Parameters :- None
# Purpose :- handles incoming chat messages from clients and allows teacher to broadcast messages to students
# it also calculates the answers to questions set and sets a timer for time to answer question
###########################
class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 55559
        self.clients = []
        self.nicknames = []
        self.answered = {}
        self.answers = 0
        self.question = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.nickname = "Server"
        self.gui_done = False
        self.running = True
        self.timer = 0
        self.asked = False
        self.t0 = 0
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    ##### guestions ######
    # Parameters :- timeset:int, question:string, inputs:list
    # Return Type :- None
    # Purpose :-  sets up the questions on the server and calculate the answer for each question
    # sets the time everyone has to answer the question
    # displays the question to everyone
    ###############################
    def questions(self, timeset, question, inputs):
        if inputs[-1] == "created":
            self.broadcast(("QUESTION:" + question).encode())
            self.asked = True
            self.question.append(question)
            self.answers = inputs[0]
            print(timeset)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "index" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = round(sin(math.radians(inputs[1])) / sin(math.radians(inputs[0])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "critical" in question and len(inputs) == 1:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = round(asin(1 / math.radians(inputs[0])) * 180 / pi,1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "fringes" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = (round((inputs[0] * inputs[2] / inputs[1])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "slits" and "screen" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = (round((inputs[0] * inputs[2] / inputs[1])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "slits" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = (round((inputs[0] * inputs[2] / inputs[1])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "wavelength" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = (round((inputs[0] * inputs[1] / inputs[2])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "order" in question and len(inputs) == 3:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            wavelength = ((inputs[0] * inputs[1]) / inputs[2])
            self.answers = round(asin(math.radians((inputs[3] * wavelength) / inputs[2])) * 180 / pi,1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "refraction" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = round(asin(math.radians(inputs[1]) * sin(math.radians(inputs[0]))) * 180 / pi,1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "incidence" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = round((asin(sin(math.radians(inputs[0]) / math.radians(inputs[1])))),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "order" in question:
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            self.answers = round(asin(math.radians((inputs[0] * inputs[2]) / inputs[1])),1)
            self.timer = int(timeset)
            self.t0 = time.time()
        elif "critcal":
            self.broadcast(("QUESTION:" + question + "\n").encode())
            self.asked = True
            self.question.append(question)
            RI = (sin(math.radians(inputs[0])) / sin(math.radians(inputs[1])))
            self.answers = round(asin(1 / RI) * 180 / pi,1)
            self.timer = int(timeset)
            self.t0 = time.time()
        # return self.asked, self.timer,self.t0,self.answers,self.question

    ##### gui_loop ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- creates the gui for the chatbox
    ###########################
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chatbox")
        self.win.configure(bg="lightgray")
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disable")

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.configure(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    ##### broadcast ######
    # Parameters :- message:string
    # Return Type :- None
    # Purpose :- sends parameter message to everyone connected to the server
    ###########################
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    ##### receive ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- establishes connection between client and receives nickname and student id of client and stores it
    ###########################
    def receive(self):
        while self.running:
            client, address = self.sock.accept()
            if self.gui_done:
                self.text_area.config(state="normal")
                self.text_area.insert("end", f"Connected with{str(address)}!\n")
                self.text_area.yview("end")
                self.text_area.config(state="disable")
            client.send("NICK".encode("utf-8"))
            nickname = client.recv(1024).decode()
            client.send("ID".encode("utf-8"))
            stuID = client.recv(1024).decode()
            self.answered[stuID] = []
            self.nicknames.append([nickname, stuID])
            self.clients.append(client)
            if self.gui_done:
                self.text_area.config(state="normal")
                self.text_area.insert("end", f"Nickname of the client is {nickname}\n")
                self.text_area.yview("end")
                self.text_area.config(state="disable")
            self.broadcast(f"{nickname} joined the chat!\n".encode("utf-8"))
            if self.gui_done:
                self.text_area.config(state="normal")
                self.text_area.insert("end", f"{nickname} joined the chat!\n".encode("utf-8"))
                self.text_area.yview("end")
                self.text_area.config(state="disable")
            client.send("Connected to the server\n".encode("utf-8"))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    ##### stop ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- stops server and returns values needed to create report
    ###########################
    def stop(self):
        self.running = False
        self.broadcast("^^++".encode("utf-8"))
        self.sock.close()
        with open("return.txt", "r") as f:
            t = f.read()
            t = eval(t) + [self.question, self.answered]
        f.close()
        print(t)
        with open("return.txt", "w") as f:
            f.write(str(t))
        f.close()

    ##### handle ######
    # Parameters :- client:object
    # Return Type :- None
    # Purpose :- handles the incoming message
    ###########################
    def handle(self, client):
        while self.running:
            if self.asked:
                current_time = time.time()
                dur = (current_time - self.t0)
                print(dur)
                print(self.timer)
                if dur >= self.timer:
                    self.answers = 0
                    self.timer = 0
                    self.asked = False
                    for key in self.answered:
                        while len(self.answered[key]) != len(self.question):
                            self.answered[key].append(0)

            try:
                message = client.recv(1024)
                if self.asked:
                    if "/answer" in message.decode() or "/Answer" in message.decode():
                        student = self.nicknames[self.clients.index(client)][1]
                        if "/answer" in message.decode():
                            answer = message.decode().partition("/answer ")[2]
                        elif "/Answer" in message.decode():
                            answer = message.decode().partition("/Answer ")[2]
                        print(message.decode())
                        print(self.answers)
                        print(answer)
                        if float(answer) == float(self.answers) and len(self.answered[student]) != len(self.question):
                            self.answered[student].append(1)
                        elif float(answer) != float(self.answers) and len(self.answered[student]) != len(self.question):
                            self.answered[student].append(0)
                    else:
                        print(f"\n{self.nicknames[self.clients.index(client)][0]} says {message}")
                        self.broadcast(message)
                        if self.gui_done:
                            self.text_area.config(state="normal")
                            self.text_area.insert("end", message)
                            self.text_area.yview("end")
                            self.text_area.config(state="disable")

                else:
                    if "/answer" in message.decode() or "/Answer" in message.decode():
                        print("Blocked")
                    else:
                        print(f"{self.nicknames[self.clients.index(client)][0]} says {message}")
                        self.broadcast(message)
                        if self.gui_done:
                            self.text_area.config(state="normal")
                            self.text_area.insert("end", message)
                            self.text_area.yview("end")
                            self.text_area.config(state="disable")
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                break

    ##### write #######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- writes what the server/teacher/host has typed in the chat box
    ###########################
    def write(self):
        message = f"{self.nickname}:{self.input_area.get('1.0', 'end')}"

        if self.gui_done:
            self.text_area.config(state="normal")
            self.text_area.insert("end", message)
            self.text_area.yview("end")
            self.text_area.config(state="disable")
        self.input_area.delete('1.0', 'end')
        self.broadcast(message.encode("utf-8"))

# receive
