from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, SO_REUSEADDR, SOL_SOCKET
from time import sleep
import pickle
import struct

class UAVSOCK(socket) :


    def __init__(self, ip, port):
        super().__init__(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.PORT = port
        self.IP = ip
        while True:
            try:
                print("connecting")
                self.connect((self.IP, self.PORT)) # attempt 3 way hand shake for session establishment
                print("connection accepted")
                self.settimeout(5)
                break
            except Exception as exception:
                print(exception)
                sleep(0.1)
                continue

    def sendUAV(self, loc):
        loc = loc[1:-1]
        while True:
            try:
                Segments = pickle.dumps(loc, 0)
                SegmentsNumber = len(Segments)
                self.sendall(struct.pack(">L", SegmentsNumber) + Segments)
                return
            except:
                self = UAVSOCK(ip=self.IP, port=self.PORT)
                continue

    def close(self):
        self.close()
    

if __name__ == "__main__":

    client = UAVSOCK("localhost", 5500)
    while True:
        client.sendUAV("(my location)")
