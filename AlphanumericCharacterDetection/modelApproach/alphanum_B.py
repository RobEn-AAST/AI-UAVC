'''
objective :-
------------
detect and classify shapes and their location in an image with low latency and high accuracy.
it must account for false positives and empty images.

modules used :-
---------------
1 - open cv for image processing tasks.
2 - easyocr for text-recognition tasks.
3 - threading for running text-recognition tasks on a separate thread to reduce latency.
4 - atexit to join all threads on program termination.
5 - Text_Detection which is a manually designed module for text-detection using east detection algorithm.

Inputs :-
---------
1 - captured frame from the camera video stream.

Outputs :-
----------
1 - whether text has been detected or not.
2 - coordinates of text if detected.
3 - an array containing the objects detected and what is the character that this object represents.

Algorithm :-
------------
1 - apply east text-detection on th input frame
2 -	if a new character has been detected
		a - capture the coordinates of the detected character
		b - add a new thread that will be assigned the duty of handling the text-recognition using easy ocr.
		c - create an array which contains many copies of the input frame but rotated in different angles.
		d - start the thread which will run text-recogntion using the array provided in the previous step.
		e - return that text has been detected and return its coordinates
	else
		return the input frame and that no text has been detected
4 - wait for all threads to finish and join them with the main thread
5 - return an array containing the objects detected and what is the character that this object represents.

'''
from cv2 import cv2
from recogniser import Recognize
from os import remove
import time
import numpy as np
from PIL import Image
# from getAlphaNumeric import getAlphaNumeric

WHITE_LIST = ['A','B','C','c','D','E','F','G','H','I','J','K','k','L','l','M','m','N','O','o','P','p','Q','R','S','s','T','U','u','V','v','W','w','X','x','Y','y','Z','z','0','1','2','3','4','5','6','7','8','9']

def alphanum_B(image, id):
	cv2.imwrite("results/" + str(id) + ".jpg", image)
	out_character = ""
	out_confidence = 0
	out_character = Recognize("results/")
	if out_character is None or out_character == '' :
		return None,None,None
	else:
		pass
	remove("results/" + str(id)  + ".jpg")
	return out_character


def getAlphaNumeric(imagefile):
	
	# crop image
	height =imagefile.shape[0]
	width =imagefile.shape[1]
	height_to_crop = int(height * (20/100))
	width_to_crop = int(width * (20/100))
	x_border = height -(height_to_crop*2)
	y_border = width -( width_to_crop*2)
	cropped_image = imagefile[ height_to_crop : height_to_crop+ (x_border),
	                          width_to_crop: width_to_crop+ ( y_border) ]


	
	lower_white = np.array([0,0,0], dtype=np.uint8)
	upper_white = np.array([200,100,255], dtype=np.uint8)

	mask = cv2.inRange(cropped_image,lower_white,upper_white)


	cv2.imshow("Hey",image)
	cv2.imshow("crop",cropped_image)
	cv2.imshow("mask",mask)
	
	cv2.waitKey(0)
	return alphanum_B(mask, 1)

if __name__ == '__main__':
	image  = cv2.imread("Sample4.jpg")
	
	
	timer = time.perf_counter()
	character = getAlphaNumeric(image)
	print(time.perf_counter()-timer)
	print(character)