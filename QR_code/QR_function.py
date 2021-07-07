import numpy as np
import cv2
from pyzbar.pyzbar import decode




#this is the function that detects QR codes and returns their value
def checkQR(img):
    #qrList is the list that holds the values of the QR codes in case there are multiple QR codes in the same image
    qrList = []
    for qrcode in decode(img):
        data = qrcode.data.decode('utf-8')
        qrList.append(data)
    
    if len(qrList)>0:
        return True,qrList
    else:
        return False,qrList

#here I load the image
img = cv2.imread("test_desert5.jpg")

# Here I added a sharpenening effect to better detect the qr code
kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, 0]], np.float32) 
kernel = 1/2 * kernel
sharp = cv2.filter2D(img, -1, kernel)
#here I just check the results
print(checkQR(sharp))
