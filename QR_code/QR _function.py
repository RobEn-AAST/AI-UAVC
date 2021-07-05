import numpy as np
import cv2
from pyzbar.pyzbar import decode





def QR(img):
    qrList = []
    for qrcode in decode(img):
        data = qrcode.data.decode('utf-8')
        qrList.append(data)
    
    if len(qrList)>0:
        return True,qrList
    else:
        return False


img = cv2.imread("test.jpg")
print(QR(img))
