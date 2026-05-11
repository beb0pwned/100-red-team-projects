import socket

HOST = "127.0.0.1"
PORT = 7334

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        command = input("# ")
        if not command:
            break
        s.sendall(command.encode('utf-8'))
        response = s.recv(1024)
        if not response:
            break
        print(response.decode('utf-8'))