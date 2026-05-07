import socket

HOST = "127.0.0.1"
PORT = 7334

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        username = conn.recv(1024).decode('utf-8')
        print(f"{username} joined")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            tagged = f"'{username}': {message}"
            conn.sendall(tagged.encode('utf-8'))