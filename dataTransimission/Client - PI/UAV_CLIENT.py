#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
from cv2 import cv2
from time import sleep
import pickle
import struct
from threading import Thread, Lock
import numpy as np
ConnectionThreadLock = Lock()
class ConnectionThread(Thread): #A thread for maintaning a redundant connection
    def __init__(self,socket : socket):
        Thread.__init__(self)
        self.socket = socket
    
    def run(self):
        ConnectionThreadLock.acquire()
        self.socket.__init__(ADDRESS = self.socket.ADDRESS)
        ConnectionThreadLock.release()


class UAV_CLIENT(socket):
    def __init__(self, ADDRESS: str = '127.0.0.1', PORT: int = 5000):
        """
        Parameters
        ----------
        ADDRESS : str, optional
            IP address of the server (default is '127.0.0.1')
        
        PORT : int, optional
            Communication port (default is 5000)
        """
        self.Queue = []
        super().__init__(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        try:
            while True:
                try:
                    self.connect((ADDRESS, PORT)) # attempt 3 way hand shake for session establishment
                    break
                except:
                    sleep(0.1)
                    continue
            self.initialized = True
            self.ADDRESS = ADDRESS
            self.PORT = PORT
            self.settimeout(2.0)
        except ConnectionRefusedError as e:
            print("failed to establish connection due to : " + str(e))
            self.initialized = False

    def sendMission(self, geolocation = None, image = None, islast= False):
        out = None
        try:
            if islast:
                img = np.zeros([512,512,1],dtype=np.uint8)
                mission = {
                    "geo" : "",
                    "image" : img,
                    "finished": True 
                }
            elif geolocation == None and image == None:
                if len(self.Queue) == 0:
                    return self.initialized
                else:
                    mission = self.Queue.pop(0)
            else:
                _, frame = cv2.imencode('.jpg', image)
                mission = {
                    "geo" : geolocation,
                    "image" : frame,
                    "finished" : islast
                }
            if not self.initialized:
                self.Queue.append(mission)
                return True
            if len(self.Queue) == 0:
                #images sending as segements of 1KB length
                Segments = pickle.dumps(mission, 0)
            else:
                self.Queue.append(mission)
                out = self.Queue.pop(0)
                Segments = pickle.dumps(out, 0)
            SegmentsNumber = len(Segments)
            self.sendall(struct.pack(">L", SegmentsNumber) + Segments)
            response = self.recv(1024)
            if response == b'success':
                print("success")
            else:
                raise Exception
        except Exception as exception:
            if out is None:
                self.Queue.append(mission)
            else:
                self.Queue.append(out)
            self.close()
            self.initialized = False
            print("Connection failed due to : " + str(exception))
            print("RE-establishing connection")
            new_connection = ConnectionThread(self)
            new_connection.start()
        return True
    
    def endMission(self):
        self.sendMission(geolocation= None, image=None, islast=True)
        self.clearQueue()
        self.initialized = False
    def clearQueue(self):
        end = True
        while end:
            end = self.sendMission()

    def __del__(self):
        self.close()

    
#Driver code to test the program
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    mysocket = UAV_CLIENT()
    # Get default camera window size
    while True:
        ret, frame = cap.read()
        if not ret:
            print("no feed")
            break
        string = "62.888,-45.82"
        mysocket.sendMission(string, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #sleep(2)
    cap.release()
    mysocket.endMission()