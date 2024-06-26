import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


class Client:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 55559
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        self.stuId = simpledialog.askstring("StudentID", "Enter your student id", parent=msg)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    # creates the gui for the chatbox
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

    def write(self):
        message = f"{self.nickname + self.stuId}:{self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode())
        self.input_area.delete('1.0', 'end')
    #disconnects client from server and returns values needed to create report
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
    #sends nickname and student id of client to server
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode()
                if message == "NICK":
                    self.sock.send(self.nickname.encode("utf-8"))
                elif message == "ID":
                    self.sock.send(self.stuId.encode("utf-8"))
                elif message=="^^++":
                    self.stop()
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", message)
                        self.text_area.yview("end")
                        self.text_area.config(state="disable")


            except:
                self.sock.close()
                break

