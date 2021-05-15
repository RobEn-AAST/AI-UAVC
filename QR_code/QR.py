import numpy as np
import cv2
from pyzbar.pyzbar import decode





def QR(img):
    
    for qrcode in decode(img):
        data = qrcode.data.decode('utf-8')
        position = qrcode.rect
        print(f"the value of the QR code is : '{data}'\n it's position is: {position}")

img = cv2.imread("test_desert2.jpg")
QR(img)
