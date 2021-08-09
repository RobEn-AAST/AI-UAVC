import cv2
import numpy as np
import os
#path is the folder in which the QR code's are at
path = 'QR_code/save/Classes'
#images is a list that contains all the images in the path file
images = []
#class names is a list that contains the class names
classNames = []
#my list is a list that contains image names with their extensions i.e jpg,png,etc...
myList = os.listdir(path)

#this is the function that returns which class a qr belongs to

def reader(img):
    #img2 is the image which we get from the footage
    img2 = img
    height = int(img2.shape[0]*2.39)
    width = int(img2.shape[1]*2.39)

    #this is the best scale I managed to use bas 3'ayar fy law 3ayez
    scale = (width, height)

    img2 = cv2.resize(img2, scale)
    #this is the step where I get the key points in an image to start comparing it with the class images
    orb  = cv2.ORB_create(nfeatures=2000) # <-- law 3ayez tezawed fel rakam dah aw te2alelo bra7tak bas 5ally balak 3alashan bey2asar 3ala el number of matches
    kp2 = orb.detect(img2,None)
    kp2, des2 = orb.compute(img2,kp2)
    bf = cv2.BFMatcher()


    # print("total classes detected", len(myList))
    #this loop adds the class names which are basically the image names without their extensions
    for c1 in myList:
        imgCur = cv2.imread(f"{path}/{c1}")
        images.append(imgCur)
        classNames.append(os.path.splitext(c1)[0])

    j=0
    max_conf = 0

    #this loop gets the element with the most matches
    for i in myList:
        img1 = cv2.imread(f"{path}/{i}")
        kp1 = orb.detect(img1,None)
        kp1, des1 = orb.compute(img1,kp1)
        matches = bf.knnMatch(des1,des2,k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        if len(good)> max_conf:
            max_conf = len(good)
            j = myList.index(i)
        # print(len(good))
    #here I return a string conatining the class name with the highest matches
    return "5" if max_conf < 15 else classNames[j]
    # return classNames[j]

#here I call the import the image
# img = cv2.imread("test2.jpeg")
# #I print the result of the reader function
# print(f"Class: {reader(img)}")
        
