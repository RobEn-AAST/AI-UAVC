# import module
import json
from PIL import Image

submitables = {
    "test":"yes", "test":"no"
}

jsonString = json.dumps(submitables)
print(jsonString)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
img = Image.open("QR_code/test.png",'r')
img.save('data.png', 'PNG')
