import numpy as np
import cv2

qr_cascade = cv2.CascadeClassifier("cascade.xml")


img = cv2.imread("test4.jpg")

gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
qr = qr_cascade.detectMultiScale(gray,1.01,7)
for(x,y,w,h) in qr:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
