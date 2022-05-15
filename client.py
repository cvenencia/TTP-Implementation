from random import randint
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

class Client:
    def __init__(self):
        self.id = randint(0, 2**128-1)

def registration_process(X):
    # Connect to TTP on port 8000 to start registration
    conn_register = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_register.connect(("127.0.0.1", 8000))

    # Send client ID to TTP
    conn_register.sendall(X.id.to_bytes(16, "little"))
    # Receive kp and km from TTP
    X.k, X.km = [int(i) for i in conn_register.recv(2048).decode('utf-8').split('\n')]

def communication_process(X):
    # Connect to TTP on port 8001 to start communication
    conn_comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_comm.connect(("127.0.0.1", 8001))

    # Generate nonce
    X.r = get_random_bytes(12)
    
    # Send ID and nonce to TTP
    conn_comm.sendall(str.encode("\n".join([str(X.id), str(int.from_bytes(X.r, "little"))])))
    
    # Receive the information back from TTP
    cx, tx, idy, ry, n = [int(i) for i in conn_comm.recv(2048).decode('utf-8').split('\n')]

    if n == 0:
        # If user is P

        cp = cx.to_bytes(32, "little")
        tp = tx.to_bytes(16, "little")
        idq = idy.to_bytes(16, "little")
        rq = ry.to_bytes(12, "little")
        
        # 5.a. Verify Tx is a valid MAC on the message
        cobj = CMAC.new(X.km.to_bytes(16, "little"), ciphermod=AES)
        cobj.update(bytearray(idq+rq+X.r+cp))
        try:
            cobj.verify(tp)
            print ("The key  with partner %s wasn't altered "%str(idq)[1:] )

            # 5.b. Decrypt key
            cipher = AES.new(X.k.to_bytes(32, "little"), AES.MODE_GCM, nonce=X.r)
            k= cipher.decrypt(cp)
            print ("Key: "+str(k))
        except ValueError:
            print ("The message or the key is wrong")

    elif n == 1:
        # If user is Q

        cq = cx.to_bytes(32, "little")
        tq = tx.to_bytes(16, "little")
        idp = idy.to_bytes(16, "little")
        rp = ry.to_bytes(12, "little")

        # 5.a. Verify Tx is a valid MAC on the message
        cobj = CMAC.new(X.km.to_bytes(16, "little"), ciphermod=AES)
        cobj.update(bytearray(idp+X.r+rp+cq))
        try:
            cobj.verify(tq)
            print ("The key  with partner %s wasn't altered "%str(idp)[1:] )

            # 5.b. Decrypt key
            cipher = AES.new(X.k.to_bytes(32, "little"), AES.MODE_GCM, nonce=rp)
            k= cipher.decrypt(cq)
            print ("Key: "+str(k))
        except ValueError:
            print ("The message or the key is wrong")

def main():
    X = Client()

    registration_process(X)
    communication_process(X)

main()
