from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP,error
import numpy as np
from cv2 import cv2
from interop import interop_client
import struct
import pickle
from threading import Timer
"""
UAV Server for exchanging data between raspberry PI and the ground station using socket programming

Theory of operation :-
----------------------
A - initiating the connection : A 3 way TCP hand-shake is established between the PI and the server

B - exchange image token : The token generated by the PI is received by the server
and then the server repeats it for 2 reason :
    1 - Test the connection in terms of reliability
    2 - use as an identification for images in the mission dictionary object

C - Mission Sending : 
        Objective : 
        -----------
            receiving of a generic dictionary object from the PI and start proccessing it
        Methodology :
        -------------
            I - An signal is received from the PI
                    if signal == "END" : 
                        - respond with ACK signal
                        - exit the function
                    else :
                        - The mission dictionary is loaded from the sent json string using loads() function
            II - check the mission object for image tokens
                    if no images are found :
                        start a thread for handling the mission object and wait for the next object
                    else :
                        send IMG_SYN signal requesting for the images
            III  - Wait for a IMG_ACK response from the PI Acknowledged the request and waiting for the image key
            IV   - send the image key to the PI and wait for the response
                    if the response is IMG_ACK : 
                        1 - Respond with IMG_C requesting the image control data and wait for the response
                        2 - The PI will send the control data of the image requested 
                        3 - Send IMG_B requesting the image bytes and wait for response
                        4 - Receive all the segments and concatenate them in one byte stream
                        5 - decode that bytes stream and store it as value to its key in the mission dictionary
                        6 - if another image is needed : send an IMG_SYN/ACK signal
                            else : send an IMG_FIN signal
                        7 - wait for the PI response
                        8 - if response is IMG_FIN : the PI acknowledged that the all image have been sent successfully
                            if response is IMG_ACK : send the next image key to the PI to start receiving
            V - start a thread for handling the mission object and wait for the next object
            VI - send to the PI saying that the mission was received successfully
D - Error handling :
----------------
If the connection is reset for any reason their are a sequence of actions taken :
    A - Close the socket
    B - ReInitialize the connection and exchange the image token again like described in section A and B in the Theory of operation section
    C - check if the last object have been received or not
    D - If not sent we must drop it
"""

class UAV_SERVER(socket):
    """
    UAV Server class that handles data exchange with the PI client 
    ...
    Attributes
    ----------
    PORT : int, optional
        communication port (default is 5000)
    Initialized : Boolean
        Boolean to whether the Client is connected to the server or not
    imgToken : str
        token for image exchange and received from the client
    Methods
    -------
    receiveMissions()
        Receives mission object from the client and Handles it acccording to the object content

    missionHandling(conn, Mission)
        Static function used for handling Mission objects
    """
    def __init__(self, PORT = 5000):
        """
        Parameters
        ----------
        PORT : int, optional
            Communication port (default is 5000)
        """
        super().__init__(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.bind(("", PORT))
        self.listen()
        print("UAV SERVER is in listening mode...")
        try:
            self.conn, self.FROM = self.accept() # accept 3 way hand shake for session establishment
            self.conn.settimeout(2.0)
            self.FROM = self.FROM[0]
            self.initialized = True
            print("3-way TCP Hand shake established with PI (" + self.FROM +") on port : " + str(PORT))    
        except Exception as e:
            print("3-way TCP Hand shake failed due to  : " + str(e))
            self.initialized = False
        return
        

    def receiveMissions(self):
        image  = None
        payload_size = struct.calcsize(">L")
        try:
            string = b""
            while len(string) < payload_size:
                bits = self.conn.recv(4096)
                string += bits
            packed_msg_size = string[:payload_size]
            data = string[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                bits = self.conn.recv(4096)
                data += bits
            frame_data = data[:msg_size]
            data = data[msg_size:]
            mission = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            if mission["finished"]:
                return False,None,None
            image=cv2.resize(cv2.imdecode(mission["image"], cv2.IMREAD_COLOR),(250,250))
            geolocation = list(map(float, mission["geo"].split(',')))
            self.conn.sendall(b"success")
            return True,geolocation, image
        except Exception as exception:
            self.initialized = False
            self.close()
            print("Mission receiving failed due to : " + str(exception))
            print("RE-establishing connection")
            self.__init__()
            print("Connection regained")
            return True,None,None

#driver code to test the program
if __name__ == '__main__':
    myserver = UAV_SERVER()
    terminate = True
    #INTEROP = interop_client('127.0.0.1','8000','testuser','testpass')
    counter = 0
    while terminate:
        terminate, geolocation, image = myserver.receiveMissions()
        if image is None:
            continue
        else:
            counter += 1
            cv2.imwrite(str(counter) + ".jpg", image)
            #INTEROP.send_standard_object(1,geolocation,interop_api_pb2.Odlc.N,interop_api_pb2.Odlc.SQUARE,interop_api_pb2.Odlc.GREEN,'A',interop_api_pb2.Odlc.WHITE,image)
    """
    
    
    mission handling code 


    """
    print("finished")
    cv2.destroyAllWindows()
