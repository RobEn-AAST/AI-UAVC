#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from cv2 import cv2
from time import sleep
import pickle
import struct
from threading import Thread, Lock
import numpy as np
from pymavlink.mavutil import mavlink_connection
import logging
from datetime import datetime

ConnectionThreadLock = Lock()
class ConnectionThread(Thread):
    def __init__(self,socket : socket):
        Thread.__init__(self)
        self.socket = socket
    
    def run(self):
        ConnectionThreadLock.acquire()
        self.socket.__init__(ADDRESS = self.socket.ADDRESS)
        logging.warning("Connection regained")
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
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
            logging.warning("Failed to establish connection due to : " + str(e))
            self.initialized = False

    def sendMission(self, geolocation = None, image = None, Finished= False):
        try:
            if not (geolocation == None and image == None):
                _, frame = cv2.imencode('.jpg', image)
                mission = {
                    "geo" : geolocation,
                    "image" : frame,
                    "finished" : Finished
                }
                self.Queue.append(mission)
            if len(self.Queue) == 0:
                return True
            out = self.Queue.pop(0)
            if not self.initialized:
                if not (geolocation == None and image == None):
                    self.Queue.append(mission)
                return True
            Segments = pickle.dumps(out, 0)
            SegmentsNumber = len(Segments)
            self.sendall(struct.pack(">L", SegmentsNumber) + Segments)
            response = self.recv(1024)
            if response == b'success':
                return out["finished"]
        except Exception as exception:
            self.Queue.append(out)
            self.close()
            self.initialized = False
            logging.warning("Connection failed due to : " + str(exception))
            logging.info("RE-establishing connection")
            new_connection = ConnectionThread(self)
            new_connection.start()
        return out["finished"]
                
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
    logging.basicConfig(filename= 'AIclient.log', filemode= 'w',format='%(asctime)s-%(levelname)s-%(message)s')
    connection_string ='/dev/ttyACM0'
    logging.info("Connecting to PIX-HAWK on internal port= " + connection_string + " with baud= 57600")
    vehicle = mavlink_connection(device= connection_string, baud= 57600)
    logging.info("The PIX-HAWK has been connected successfully")
    logging.info("Connecting to the ground station on ADDRESS=192.168.1.56 and PORT= 5000")
    mysocket = UAV_CLIENT(ADDRESS = "192.168.1.56")
    logging.info("The ground station has been connected successfully")
    cap = cv2.VideoCapture('home/pi/MAH00145.MP4')
    logging.info("Camera stream has been captured")
    # Get default camera window size
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("Stream ended")
            break
        coordinates = vehicle.location()
        geolocation = coordinates.split(",")
        geolocation = map(lambda x : float(x[4:]), coordinates)
        coordinates = list(coordinates)
        mysocket.sendMission(coordinates, frame)
        logging.info("Frame with location= { " + coordinates + " } has been sent to the ground station")
        sleep(0.1)
    cap.release()
    logging.info("Camera stream has been released")
    logging.info("Ending the mission")
    mysocket.endMission()
    logging.info("Program exited with no errors")
