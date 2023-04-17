import socket
from threading import Thread

SERVER_HOST, SERVER_PORT = "0.0.0.0", 9090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_sockets = []
sep_token = "<SEP>"

def msg_handler(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as ex:
            print(f"[!] Error: {ex}")
        else:
            msg = msg.replace(sep_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())
        
while True:
    conn, addr = s.accept()
    print(f"[*] {addr} connected")
    client_sockets.append(conn)

    t = Thread(target=msg_handler, args=(conn,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()

s.close()
