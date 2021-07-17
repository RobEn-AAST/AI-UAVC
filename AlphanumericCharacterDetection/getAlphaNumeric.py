import cv2
import numpy as  np
from alphanum_B import alphanum_B


def getAlphaNumeric(imagefile):
	
	# crop image
	cropped_image = crop_image(imagefile)

	# image = cv2.imread(imagefile)
	lower_white = np.array([0,0,0], dtype=np.uint8)
	upper_white = np.array([200,100,255], dtype=np.uint8)

	mask = cv2.inRange(cropped_image,lower_white,upper_white)


	
	cv2.imshow("crop",cropped_image)
	cv2.imshow("mask",mask)
	
	cv2.waitKey(0)
	return alphanum_B(mask, 1)

def crop_image(imagefile):
	height =imagefile.shape[0]
	width =imagefile.shape[1]
	height_to_crop = int(height * (20/100))
	width_to_crop = int(width * (20/100))
	x_border = height -(height_to_crop*2)
	y_border = width -( width_to_crop*2)
	return  imagefile[ height_to_crop : height_to_crop+ (x_border),
	                          width_to_crop: width_to_crop+ ( y_border) ]

    	