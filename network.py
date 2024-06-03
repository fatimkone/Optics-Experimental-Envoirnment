import socket
import pickle
import select
import time

##### Network #######
# Parameters :- None
# Purpose :- handles data coming and going to server
###########################
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 55633
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    ##### connect ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :-  connects client to server
    ####################
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(16384)
        except socket.error as e:
            print(e)

    ##### rec ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :-  used to handle incoming data
    ####################
    def rec(self):
        timeout = 0.1
        ready_sockets, _, _ = select.select(
        [self.client], [], [], timeout)
        if ready_sockets:
            return self.client.recv(16384).decode("utf-8")
        else:
            return None



    ##### send ######
    # Parameters :- data:byte
    # Return Type :- None
    # Purpose :- sends data to server
    ####################
    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv(16384)
        except socket.error as e:
            print(e)

    ##### disconnect ######
    # Parameters :- None
    # Return Type :- None
    # Purpose :- disconnects client from server
    ####################
    def disconnect(self):
        f = open("disconnect.txt", "a+")
        f.seek(0)
        data = f.read(100)
        if len(data) > 0:
            f.write("\n")
        f.write(str(self.client))
        self.client.close()
    def disconnect2(self):
        self.send("OUT".encode())
