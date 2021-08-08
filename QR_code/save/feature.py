import numpy as np
import cv2
from PIL import Image


img1 = cv2.imread("img5.jpg")
img2 = cv2.imread("final2.jpg")

scale = (640, 360)
print(scale)
img2 = cv2.resize(img2, scale)

orb  = cv2.ORB_create(nfeatures=2000)


kp1 = orb.detect(img1,None)
kp2 = orb.detect(img2,None)


kp1, des1 = orb.compute(img1,kp1)
kp2, des2 = orb.compute(img2,kp2)

#imgkp1 = cv2.drawKeypoints(img1,kp1,None)
#imgkp2 = cv2.drawKeypoints(img2,kp2,None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

print(len(good))
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)


cv2.imshow("img3", img3)
cv2.imshow("img1",img1)
cv2.imshow("img2",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

