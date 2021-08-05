from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
import struct
import pickle

class ServerSock(socket):
    HEADERSIZE = 20

    def __init__(self, IP, PORT):
        super().__init__(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.bind(("", PORT))
        self.listen()
        print("Listening on " + str(IP) + ":" + str(PORT))
        
    def getMessage(self):
        payload_size = struct.calcsize(">L")
        conn, _ = self.accept()
        conn.settimeout(5)
        while True:
            try:
                string = b""
                while len(string) < payload_size:
                    bits = conn.recv(4096)
                    string += bits
                packed_msg_size = string[:payload_size]
                data = string[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
                while len(data) < msg_size:
                    bits = conn.recv(4096)
                    data += bits
                frame_data = data[:msg_size]
                data = data[msg_size:]
                msg = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                # if msg start then get it's len from the header
                return msg
            except Exception:
                conn.close()
                return self.getMessage()
         

if __name__ == "__main__":

    server = ServerSock("localhost", 5500)
    while True:
        print(server.getMessage())


    

