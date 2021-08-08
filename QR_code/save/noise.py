import numpy as np
import random
import cv2

def sp_noise(image,prob):

    output = image
    thresh = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            #dyh 3alashan teawed white noise
            #elif rdn >prob:
             #   output[i][j] = 255
            else:
                output[i][j] = image[i][j]

    return output

img = cv2.imread('test_t.jpg',0)
noise_img = sp_noise(img,0.005)  #<-------- zawed fel rakam el hena 3alashan tezawed el noise
blur  = cv2.blur(noise_img,(4,3))
cv2.imshow('noise.jpg', noise_img)
cv2.imshow("blur",blur)
cv2.waitKey(0)
cv2.destroyAllWindows()

