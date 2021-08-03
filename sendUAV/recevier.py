import socket


class ServerSock():
    def __init__(self, IP, PORT):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.serverSocket.bind((IP, PORT))
        self.serverSocket.listen()
        print("Listening on " + str(IP) + ":" + str(PORT))
        
    def accept(self):
        clientSocket, address = self.serverSocket.accept() # blocking code
        print(f"connection from : {address}")
        return clientSocket

    def getMessage(self, connect):
        fullMsg = ''
        msg = connect.recv(1024)
        # if msg start then get it's len from the header
        fullMsg += msg.decode("utf-8")
        connect.sendall(b"success")
        return fullMsg

if __name__ == "__main__":

    server = ServerSock("localhost", 5000)

    connect = server.accept() 
    
    print(server.getMessage(connect))

    

