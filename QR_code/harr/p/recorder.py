import cv2
counter = 0
shot = 1

cap = cv2.VideoCapture("test2.mp4")


while True:
    success,img = cap.read()
    shot+=1
    if shot == 5:
        try:
            cv2.imwrite(f"img({counter}).jpg",img)
        except:
            break
        counter+=1
        shot = 1
print("done")
