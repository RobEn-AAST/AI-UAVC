# import module
import json
from PIL import Image
import cv2

# img = cv2.imread("/test.pngQR_code")

# c=1
# submitablesImg = {
#     "img": img, "alphanumeric": "A" , "geotag" : "xxx" , "color" : "red"
# }
# submitablesQR = {
#     "QRimg": img, "QRvalue": "xxxxx", "geotag" : "xxxx"
# }

# TODO
#   - change path to relative depending on this file locatoins
#   - return the path of each deliverable made with it's name
#

def submitToUSB(submitables,c) :

    jsonString = json.dumps(submitables)
    jsonFile = open(f"WriteJsonOnDisk/Image/{c}.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    img = Image.open("QR_code/test.png",'r')
    img.save(f'WriteJsonOnDisk/Image/{c}.png', 'PNG')

