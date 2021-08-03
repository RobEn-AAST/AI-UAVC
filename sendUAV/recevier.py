import socket


class ServerSock():
    HEADERSIZE = 20

    def __init__(self, IP, PORT):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((IP, PORT))
        self.serverSocket.listen(10)
        print("Listening on " + str(IP) + ":" + str(PORT))
        
    def accept(self):
        clientSocket, address = self.serverSocket.accept() # blocking code
        print(f"connection from : {address}")
        return clientSocket

    def getMessage(self, connect):
        fullMsg = ''
        newMsg = True

        while True:

            msg = connect.recv(self.HEADERSIZE+5)

            # if msg start then get it's len from the header
            if newMsg:
                decodedMsg = msg[:self.HEADERSIZE].decode("utf-8")
                msgLen = int(decodedMsg)
                newMsg = False

            fullMsg += msg.decode("utf-8")

            if len(fullMsg)-self.HEADERSIZE == msgLen:
                newMsg = True
                break
            
        return fullMsg[self.HEADERSIZE:] 

if __name__ == "__main__":

    server = ServerSock("localhost", 5000)

    connect = server.accept() 

    print(server.getMessage(connect))


    

