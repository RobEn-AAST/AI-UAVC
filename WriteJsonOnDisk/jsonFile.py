# import module
import json
from PIL import Image
import cv2

img = cv2.imread("/test.pngQR_code")


submitablesImg = {
    "img": img, "alphanumeric": "A" , "geotag" : "xxx" , "color" : "red"
}
submitablesQR = {
    "QRimg": img, "QRvalue": "xxxxx", "geotag" : "xxxx"
}
def writeFile(submitables) :
    if "QRimg" in submitables:
        
        jsonString = json.dumps(submitables)
        jsonFile = open("/WriteJsonOnDisk/QRcode/data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    
        img = Image.open("QR_code/test.png",'r')
        img.save('data.png', 'PNG')
