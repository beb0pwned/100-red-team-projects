import socket
import subprocess
import argparse

HOST = "127.0.0.1"
PORT = 7334


def send_command(command):
    output = subprocess.check_output([command])
    return output

commands = ['ls', 'get', 'del']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode('utf-8').strip()

            if command not in commands:
                joined = ", ".join(commands)
                conn.send(f"Please select a valid command: {joined}\n".encode('utf-8'))
            elif command == 'ls':
                conn.send(send_command('ls'))
