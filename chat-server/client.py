import socket

HOST = "127.0.0.1"
PORT = 7334

def select_username():
    while True:
        username = input("Please select a username: ")
        if len(username) > 0:
            return username.encode('utf-8')
        print("Username must be SOMETHING.")
    

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(select_username())
    while True:
        message = input("# ")
        if not message:
            break
        s.sendall(message.encode('utf-8'))
        response = s.recv(1024)
        if not response:
            break
        print(response.decode('utf-8'))