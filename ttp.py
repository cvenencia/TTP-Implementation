import socket
import json
import threading
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

def register_user(s):
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        id = conn.recv(1024)
        keyp = get_random_bytes(32)
        conn.sendall(id)
    
def register_requests_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 8000))
        s.listen()
        while True:
            register_user(s)

def main():
    with open("./users.json") as users_file:
        users = json.load(users_file)
    
    with open("./users.json", "w") as users_file:
        users_file.write(json.dumps(users))

main()
    