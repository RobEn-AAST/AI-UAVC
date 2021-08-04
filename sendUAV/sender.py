import socket

class UAVSOCK() :

    HEADERSIZE = 20

    def __init__(self, ip, port):
        self.PORT = port
        self.IP = ip
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))

    def sendUAV(self, loc):
        loc  = str(loc)[1:-1]
        self.connect()
        data = f"{len(loc):<{self.HEADERSIZE}}" + loc
        codedMsg = bytes(data, "utf-8")
        self.socket.send(codedMsg)
        self.close()
        print("sent")

    def close(self):
        self.socket.close()
    

if __name__ == "__main__":

    client = UAVSOCK("localhost", 5500)
