#!/usr/bin/python3

import os
import socket

HOST = "127.0.0.1"
PORT = 7334


def recv_exact(rfile, n):
    buf = b""
    while len(buf) < n:
        chunk = rfile.read(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed mid-transfer")
        buf += chunk
    return buf


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    rfile = s.makefile("rb")

    # Server banner (plain line, not length-prefixed)
    print(rfile.readline().decode().strip())

    while True:
        try:
            line = input("beb0p> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            line = "quit"

        if not line:
            continue

        parts = line.split(None, 1)
        cmd = parts[0].lower()

        s.sendall((line + "\n").encode())

        header = rfile.readline().decode("utf-8", errors="replace").strip()

        if header.startswith("OK "):
            size = int(header.split()[1])
            body = recv_exact(rfile, size).decode("utf-8", errors="replace")
            print(body, end="")

        elif header.startswith("FILE "):
            size = int(header.split()[1])
            filename = os.path.basename(parts[1]) if len(parts) > 1 else "download"
            data = recv_exact(rfile, size)
            with open(filename, "wb") as f:
                f.write(data)
            print(f"Saved '{filename}' ({size} bytes)")

        elif header.startswith("ERR "):
            print(f"Error: {header[4:]}")

        else:
            print(header)

        if cmd == "quit":
            break
