# import module
import json
from PIL import Image

submitables = {
    "test":"yes", "test":"no"
}
def writeFile(submitables) :

    jsonString = json.dumps(submitables)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    
    img = Image.open("QR_code/test.png",'r')
    img.save('data.png', 'PNG')
