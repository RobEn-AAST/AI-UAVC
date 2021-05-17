import cv2
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression
import os

layerNames = [ "feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3" ]
net = cv2.dnn.readNet("east_detection_model.pb")
orientation = {
	"N" : 1,
	"NE" : 2,
	"E" : 3,
	"SE" : 4,
	"S" : 5,
	"SW" : 6,
	"W" : 7,
	"NW" : 8
}


def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

def flip_image(counter,image):
	if np.shape(image) == () or image.size == 0:
		return None
	height, width, _ = image.shape
	all_images = []
	for x in range(0,315,45):
		M = cv2.getRotationMatrix2D((width//2, height//2), x, 1.0)
		rotated = cv2.warpAffine(image, M, (width, height))
		all_images.append(rotated)
	os.mkdir("results\\Object " + str(counter))
	namer = 0
	for x in all_images:
		cv2.imwrite("results\\Object " + str(counter) + "\\image " + str(namer) + ".jpg",x)
		namer += 1	
	return

def detect_text(frame, size = (320,320)) :
	layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
	frame = imutils.resize(frame, width=1000)
	blob = cv2.dnn.blobFromImage(frame, 1.0, size,(123.68, 116.78, 103.94), swapRB=True, crop=False)
	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)
	(rects, confidences) = decode_predictions(scores, geometry)
	boxes = non_max_suppression(np.array(rects), probs=confidences)
	return boxes,confidences

def decode_predictions(scores, geometry):
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []
	for y in range(0, numRows):
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]
		for x in range(0, numCols):
			if scoresData[x] < 0.5:
				continue
			(offsetX, offsetY) = (x * 4.0, y * 4.0)
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])
	return (rects, confidences)

def detect(COUNTER,frame,size = (320,320)):
	orig = frame.copy()
	(H, W) = frame.shape[:2]
	rW = W / float(size[0])
	rH = H / float(size[1])
	boxes,confidences = detect_text(frame.copy())
	boxes_out = []
	for (startX, startY, endX, endY) in boxes:
		startX = int(startX * rW)
		startY = int(startY * rH)
		endX = int(endX * rW)
		endY = int(endY * rH)
		boxes_out.append((startX, startY, endX, endY))

	out = len(boxes) > 0

	if out :
		flip_image(COUNTER,orig)
	return boxes_out,out