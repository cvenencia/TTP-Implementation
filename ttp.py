import socket
import json
from multiprocessing import Process, Manager
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

users = []

def get_key(id):
    id = int.from_bytes(id, "little")
    update_users()
    for u in users:
        if u["id"] == id:
            return (u["key"]).to_bytes(32, "little")

def get_keym(id):
    id = int.from_bytes(id, "little")
    update_users()
    for u in users:
        if u["id"] == id:
            return (u["keym"]).to_bytes(16, "little")

def register_user(s):
    conn, _ = s.accept()
    with conn:
        try:
            id = conn.recv(1024)
            key = get_random_bytes(32)
            keym = get_random_bytes(16)
            add_user({
                "id": int.from_bytes(id, 'little'),
                "key": int.from_bytes(key, 'little'),
                "keym": int.from_bytes(keym, 'little')
            })
            # print(f"User with ID {int.from_bytes(id, 'little')} registered with key {int.from_bytes(key, 'little')}")
            conn.sendall(str.encode("\n".join([
                str(int.from_bytes(key, "little")),
                str(int.from_bytes(keym, "little")),
            ])))
        except KeyboardInterrupt:
            if conn:
                conn.close()

def register_requests_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8000))
        s.listen()
        print("Open port waiting for register requests...")
        while True:
            register_user(s)

def asdf(conn, user, return_dict):
    try:
        idx, rx = [int(i) for i in conn.recv(2048).decode('utf-8').split('\n')]
        if user == 0:
            return_dict["idp"] = (idx).to_bytes(16, "little")
            return_dict["rp"] = (rx).to_bytes(12, "little")
            print("P ended")
        else:
            return_dict["idq"] = (idx).to_bytes(16, "little")
            return_dict["rq"] = (rx).to_bytes(12, "little")
            print("Q ended")
    except KeyboardInterrupt:
        if conn:
            conn.close()

def asdf_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8001))
        s.listen()
        print("Open port waiting for communication requests...")
        users_connected = 0
        
        # while True:
        processes = []
        conns = []
        manager = Manager()
        data = manager.dict()
        while users_connected < 2:
            conn, _ = s.accept()
            conns.append(conn)
            p = Process(target=asdf, args=(conn, users_connected, data))
            processes.append(p)
            p.start()
            users_connected += 1
        
        for p in processes:
            p.join()

        skey = get_random_bytes(32)
        print ("Key: "+str(skey))

        cipher = AES.new(get_key(data["idp"]), AES.MODE_GCM, nonce=data["rp"])
        cipher.update(data["idp"])
        Cp,s = cipher.encrypt_and_digest(skey)

        cipher = AES.new(get_key(data["idq"]), AES.MODE_GCM, nonce=data["rp"])
        cipher.update(data["idq"])
        Cq,s = cipher.encrypt_and_digest(skey)

        #proceso de MAC
        cobj = CMAC.new(get_keym(data["idp"]), ciphermod=AES)
        cobj.update(bytearray(data["idq"]+data["rq"]+data["rp"]+Cp))
        Tp=cobj.digest()

        cobj = CMAC.new(get_keym(data["idq"]), ciphermod=AES)
        cobj.update(bytearray(data["idp"]+data["rq"]+data["rp"]+Cq))
        Tq=cobj.digest()

        conns[0].sendall(str.encode("\n".join([
                str(int.from_bytes(Cp, "little")),
                str(int.from_bytes(Tp, "little")),
                str(int.from_bytes(data["idq"], "little")),
                str(int.from_bytes(data["rq"], "little")),
                str(0)
        ])))
        conns[1].sendall(str.encode("\n".join([
                str(int.from_bytes(Cq, "little")),
                str(int.from_bytes(Tq, "little")),
                str(int.from_bytes(data["idp"], "little")),
                str(int.from_bytes(data["rp"], "little")),
                str(1)
        ])))
       

def add_user(pair):
    global users
    with open("./users.json") as users_file:
        users = json.load(users_file)
    users.append(pair)
    with open("./users.json", "w") as users_file:
        users_file.write(json.dumps(users))

def update_users():
    global users
    with open("./users.json") as users_file:
        users = json.load(users_file)

def main():
    with open("./users.json") as users_file:
        global users
        users = json.load(users_file)
    register_thread = Process(target=register_requests_handler)
    register_thread.start()

    asdf_thread = Process(target=asdf_handler)
    asdf_thread.start()

main()
    