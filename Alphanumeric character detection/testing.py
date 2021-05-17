from alphanum_B import OCR_To_results
from Text_Detection import flip_image
from cv2 import cv2



img  = cv2.imread('test.jpg')

rotate = flip_image(image=img)


result,orientation = OCR_To_results(rotate)


print("character >> " + result)
print("orientation >> " + orientation)



