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
import threading
import Text_Detection
import atexit
from recogniser import Recognize

OBJECT_COUNTER = 0
class Text_recognition_thread (threading.Thread):
	def __init__(self,threadID, name,frames = None,WHITE_LIST = None):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.frames = frames
		self.WHITE_LIST = WHITE_LIST
	def run(self):
		global OBJECT_COUNTER
		print ("Starting " + self.name)
		threadLock.acquire()
		Text_Recognition(OBJECT_COUNTER )
		OBJECT_COUNTER += 1
		threadLock.release()


IS_ACTIVE = False
RESULT = []
WHITE_LIST = ['A','B','C','c','D','E','F','G','H','I','J','K','k','L','l','M','m','N','O','o','P','p','Q','R','S','s','T','U','u','V','v','W','w','X','x','Y','y','Z','z','0','1','2','3','4','5','6','7','8','9']
CURRENT_RECTNAGLES = []
CURRENT_TEXT = None
CURRENT_COORDINATES = None
WILL_BE_PROCESSED = 0
threads = []
threadLock = threading.Lock()

def alphanum_B(frame,size = (320,320)):
	global IS_ACTIVE
	global WILL_BE_PROCESSED
	global OBJECT_COUNTER
	global threads
	global WHITE_LIST
	global CURRENT_TEXT
	global CURRENT_RECTNAGLES
	global CURRENT_COORDINATES
	CURRENT_RECTNAGLES,result = Text_Detection.detect(frame,size)
	if  result : # the video just finised detecting an object
		print("Text recognition will begin now....")
		Text_Detection.flip_image(OBJECT_COUNTER,frame)
		Text_Recognition(OBJECT_COUNTER)
		OBJECT_COUNTER += 1
	cv2.putText(frame,CURRENT_TEXT,(0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
	for (startX, startY, endX, endY) in CURRENT_RECTNAGLES:
		cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
		cv2.putText(frame,boxes_tostring((startX, startY, endX, endY)),(startX,startY) ,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
	return frame

def OCR_To_results(COUNTER):
	orientation_arr = [ "N","NW","W","SW","S","SE","E","NE"]
	orientation = None
	counter = 0
	out_character = ""
	out_confidence = 0
	result = Recognize("results\\Object " + str(COUNTER))
	for character,confidence in result:
		if character in WHITE_LIST and confidence > out_confidence: 
			out_character = character
			out_confidence = confidence
			if orientation == None:
				orientation = orientation_arr[counter]
			counter += 1
	return ((out_character,orientation,out_confidence * 100) if out_character != None else ("","N/A",-1))

def Text_Recognition(OBJECT_COUNTER):
	RESULT.append((OCR_To_results(OBJECT_COUNTER),OBJECT_COUNTER))


def boxes_tostring(boxes):
    	return ' : '.join(map(str,boxes))

def exit_handler():
	global threads
	for object_recogintion_thread in threads:
		object_recogintion_thread.join()
	print("Program terminated successfully")

atexit.register(exit_handler)

if __name__ == '__main__':
	images = []
	for x in range(1,7):
		images.append(cv2.imread("demo_image\\test" + str(x) +".jpg"))
	for image in images:
		alphanum_B(image)
	for (letter,orientation,confidence),z in RESULT:
		print("object number : " + str(z) + " , character : " + str(letter) + " , orientation : " + str(orientation) + " , confidence : " + str(confidence))