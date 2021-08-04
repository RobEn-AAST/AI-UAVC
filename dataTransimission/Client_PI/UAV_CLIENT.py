#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
from cv2 import cv2
from time import sleep
import pickle
import struct
from threading import Thread, Lock
import numpy as np
from dronekit import connect
import pymavlink
from pymavlink import mavutil

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
            self.settimeout(2)
        except ConnectionRefusedError as e:
            print("failed to establish connection due to : " + str(e))
            self.initialized = False

    def sendMission(self, geolocation = None, image = None, Finished= False):
        out = None
        try:
            if not (geolocation == None and image == None):
                _, frame = cv2.imencode('.jpg', image)
                mission = {
                    "geo" : geolocation,
                    "image" : frame,
                    "finished" : Finished
                }
                self.Queue.append(mission)
            try:
                out = self.Queue.pop(0)
            except:
                return True
            if not self.initialized:
                if not (geolocation == None and image == None):
                    self.Queue.append(mission)
                return True
            Segments = pickle.dumps(out, 0)
            SegmentsNumber = len(Segments)
            self.sendall(struct.pack(">L", SegmentsNumber) + Segments)
            response = self.recv(1024)
            if response == b'success':
                print("success")
                return out["finished"]
        except Exception as exception:
            print(exception)
            self.Queue.append(out)
            self.close()
            self.initialized = False
            print("Connection failed due to : " + str(exception))
            print("RE-establishing connection")
            new_connection = ConnectionThread(self)
            new_connection.start()
        return True
                
    def endMission(self):
        self.sendMission(geolocation = (0,0), image = np.zeros([512,512,1],dtype=np.uint8), Finished=True)
        self.clearQueue()
        self.initialized = False
    def clearQueue(self):
        end = True
        while end:
            end = not self.sendMission()

    def __del__(self):
        self.close()

    
#Driver code to test the program
if __name__ == '__main__':
    connection_string ='/dev/ttyACM0'
    vehicle = mavutil.mavlink_connection(device=connection_string, baud=57600)
    cap = cv2.VideoCapture('home/pi/MAH00145.MP4')
    mysocket = UAV_CLIENT(ADDRESS = "192.168.1.56")
    # Get default camera window size
    while True:
        ret, frame = cap.read()
        if not ret:
            print("no feed")
            break
        coordinates = tuple(map(float, str(vehicle.location().split(","))))
        mysocket.sendMission(coordinates, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        sleep(0.1)
    cap.release()
    mysocket.endMission()
