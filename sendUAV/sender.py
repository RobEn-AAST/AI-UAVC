import socket

class clientSock() :

    HEADERSIZE = 20

    def __init__(self, ip, port):
        self.PORT = port
        self.IP = ip
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))

    def sendMsg(self, loc):
        data = f"{len(loc):<{self.HEADERSIZE}}" + loc
        codedMsg = bytes(data, "utf-8")
        self.socket.send(codedMsg)

    def close(self):
        self.socket.close()

if __name__ == "__main__":

    client = clientSock("localhost", 5000)

    client.connect()
    client.sendMsg("36.67,32.78")

    client.close()
