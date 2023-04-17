import socket
from threading import Thread
from datetime import datetime

SERVER_HOST, SERVER_PORT = "127.0.0.1", 9090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print(f"[+] Connected.")

name = input("Enter your name: ")

sep_token = "<SEP>"

def msg_receive():
    while True:
        msg = s.recv(1024).decode()
        print("\n" + msg)

t = Thread(target=msg_receive)
t.daemon = True
t.start()

while True:
    msg_to_send = input()

    if msg_to_send.lower() == "exit":
        break

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg_to_send = f"[{date_now}] {name}{sep_token}{msg_to_send}"
    s.send(msg_to_send.encode())

s.close()
