import numpy as np
import cv2
from pyzbar.pyzbar import decode





def checkQR(img):
    qrList = []
    for qrcode in decode(img):
        data = qrcode.data.decode('utf-8')
        qrList.append(data)
    
    if len(qrList)>0:
        return True,qrList
    else:
        return False,qrList


img = cv2.imread("re4.jpg")

# Here I added a sharpenening effect to better detect the qr code
kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, 0]], np.float32) 
kernel = 1/2 * kernel
sharp = cv2.filter2D(img, -1, kernel)


print(checkQR(img))



