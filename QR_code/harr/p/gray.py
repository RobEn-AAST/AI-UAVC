import cv2

for i in range (151):
    print (i)
    img = cv2.imread(f"img({i}).jpg")
    gray  = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"img({i}).jpg",gray)
