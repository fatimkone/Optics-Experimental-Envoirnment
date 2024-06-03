import socket
import threading
from _thread import *
import pickle
import sys

server = socket.gethostbyname(socket.gethostname())
port = 55633
clients = set()
clients_lock = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(1)
print("Waiting for a connection, Server Started")
d = {1: 'dont redraw'}


##### threaded_clients ######
# Parameters :- conn:object, client:set, x:int
# Return Type :- None
# Purpose :- handles incoming data for each client
###########################
def threaded_client(conn, clients, x,server):
    conn.send(pickle.dumps(d))

    while True:
        try:
            data = conn.recv(16384)
        except ConnectionAbortedError:
            break
        if str(data.decode)=="OUT":
            server.close()
            sys.exit()
        else:
            with clients_lock:
                r = open("disconnect.txt", "r")
                dis = r.readlines()
                for line in dis:
                    if line in str(clients):
                        print("Disconnected to:", eval(line))
                        clients.discard(eval(line))
                open('disconnect.txt', 'w').close()
                # checks if the client is the top client
                # then sends its incoming data to every other client
                if x == 1:
                    if data is None:
                        clients.clear()
                        conn.close()
                        break
                    else:
                        if len(clients) > 1:
                            for c in clients:
                                try:
                                    c.sendall(data)
                                except OSError:
                                    break


                else:
                    continue
    print("Disconnected")
    conn.close()


x = 0
while True:
    conn, addr = s.accept()
    f = open("disconnect.txt", "w")
    with clients_lock:
        clients.add(conn)
        print("Connected to:", addr)
        x = x + 1
        # starts new thread for new client that join server
        start_new_thread(threaded_client, (conn, clients, x,server))
