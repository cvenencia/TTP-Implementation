import socket
import json
from multiprocessing import Process
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

def register_user(s):
    conn, _ = s.accept()
    with conn:
        try:
            id = conn.recv(1024)
            key = get_random_bytes(32)
            add_user({
                "id": int.from_bytes(id, 'little'),
                "key": int.from_bytes(key, 'little')
            })
            print(f"User with ID {int.from_bytes(id, 'little')} registered with key {int.from_bytes(key, 'little')}")
            conn.sendall(key)
        except KeyboardInterrupt:
            if conn:
                conn.close()
    
def register_requests_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8001))
        s.listen()
        print("Open port waiting for register requests...")
        while True:
            register_user(s)

def add_user(pair):
    with open("./users.json") as users_file:
        users = json.load(users_file)
    users.append(pair)
    with open("./users.json", "w") as users_file:
        users_file.write(json.dumps(users))

def main():
    register_thread = Process(target=register_requests_handler)
    register_thread.start()

main()
    