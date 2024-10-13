import os
import socket
from datetime import datetime

if not os.path.exists('request'):
    os.makedirs('request')

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                break

            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            filename = f"request/{timestamp}.bin"

            with open(filename, 'wb') as f:
                f.write(data)

            print(f"Request saved as {filename}")

            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nRequest received"
            conn.sendall(response)
