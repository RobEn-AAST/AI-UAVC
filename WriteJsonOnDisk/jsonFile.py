# import module
import json
from PIL import Image
import cv2

img = cv2.imread("/test.pngQR_code")

c=1
submitablesImg = {
    "img": img, "alphanumeric": "A" , "geotag" : "xxx" , "color" : "red"
}
submitablesQR = {
    "QRimg": img, "QRvalue": "xxxxx", "geotag" : "xxxx"
}
def writeFile(submitables,c) :
    if "QRimg" in submitables:
        
        jsonString = json.dumps(submitables)
        jsonFile = open(f"WriteJsonOnDisk/QRcode/{c}.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    
        img = Image.open("QR_code/test.png",'r')
        img.save(f'WriteJsonOnDisk/QRcode/{c}.png', 'PNG')
    
    elif "alphanumeric" in submitables:
        
        jsonString = json.dumps(submitables)
        jsonFile = open(f"WriteJsonOnDisk/Image/{c}.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    
        img = Image.open("QR_code/test.png",'r')
        img.save(f'WriteJsonOnDisk/Image/{c}.png', 'PNG')
while c!=4 :
    writeFile(submitablesImg,c)
    c =  c+1

