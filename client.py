from random import randint
import socket

class Client:
    def __init__(self):
        self.id = randint(0, 2**64-1)

client = Client()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("127.0.0.1", 8001))

# Send client ID to TTP
conn.sendall(client.id.to_bytes(8, "little"))
# Receive kp from TTP
x = int.from_bytes(conn.recv(1024), "little")
print(x)
