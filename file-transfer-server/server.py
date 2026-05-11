import socket
import os

HOST = "127.0.0.1"
PORT = 7334

commands = ['ls', 'get', 'rm']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        while True:
            command = conn.recv(1024).decode('utf-8')
            if not command:
                break
            if command not in commands:
                print(f"Please select a valid command: {", ".join(commands)}")
            elif command == 'ls':
                os.system('ls')