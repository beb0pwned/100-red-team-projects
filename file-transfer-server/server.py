#!/usr/bin/python3

import os
import socket

HOST = "127.0.0.1"
PORT = 7334

COMMANDS = ["ls", "get", "del", "quit"]


def safe_filename(name):
    """Reject path traversal — basename must equal the name itself."""
    return bool(name) and os.path.basename(name) == name


def ok(text):
    """Length-prefixed OK response for plain text."""
    body = text.encode()
    return f"OK {len(body)}\n".encode() + body


def err(msg):
    return f"ERR {msg}\n".encode()


def handle_ls():
    entries = sorted(os.listdir("."))
    return ok("\n".join(entries) + "\n" if entries else "(empty)\n")


def handle_get(filename):
    if not safe_filename(filename):
        return err("invalid filename"), None
    if not os.path.isfile(filename):
        return err(f"no such file: {filename}"), None
    with open(filename, "rb") as f:
        data = f.read()
    header = f"FILE {len(data)}\n".encode()
    return header, data


def handle_del(filename):
    if not safe_filename(filename):
        return err("invalid filename")
    if not os.path.isfile(filename):
        return err(f"no such file: {filename}")
    os.remove(filename)
    return ok(f"deleted {filename}\n")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected: {addr}")
            conn.sendall(b"220 Simple File Transfer Server ready.\n")

            rfile = conn.makefile("rb")

            while True:
                line = rfile.readline()
                if not line:
                    break

                parts = line.decode("utf-8", errors="replace").strip().split(None, 1)
                if not parts:
                    continue

                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                print(f"  CMD: {cmd!r}  ARG: {arg!r}")

                if cmd == "quit":
                    conn.sendall(ok("bye\n"))
                    break
                elif cmd == "ls":
                    conn.sendall(handle_ls())
                elif cmd == "get":
                    header, data = handle_get(arg)
                    conn.sendall(header)
                    if data is not None:
                        conn.sendall(data)
                elif cmd == "del":
                    conn.sendall(handle_del(arg))
                else:
                    conn.sendall(err(f"unknown command. Available: {', '.join(COMMANDS)}"))

            print(f"Disconnected: {addr}")
