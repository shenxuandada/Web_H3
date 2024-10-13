import os
import socket
from datetime import datetime

if not os.path.exists('request'):
    os.makedirs('request')
if not os.path.exists('images'):
    os.makedirs('images')

HOST = '127.0.0.1'
PORT = 9998

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(60000)
            if not data:
                break

            if b'Content-Type: image' in data:
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                filename = f"images/{timestamp}.jpg"

                with open(filename, 'wb') as f:
                    f.write(data.split(b'\r\n\r\n')[1])

                print(f"Image saved as {filename}")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                filename = f"request/{timestamp}.bin"
                with open(filename, 'wb') as f:
                    f.write(data)
                print(f"Request saved as {filename}")

# curl -X POST -H "Content-Type: image/jpeg" --data-binary @"C:/Users/hp/Desktop/test.jpg" http://127.0.0.1:9998
