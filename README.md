# AI-UAVC
The Egypt unmanned arial vehicle challange


### Goal program
This is a simple blackbox representation of the abstraction level we want to achieve
```python
from QR_code.QR_function import checkQR
from WriteJsonOnDisk.jsonFile import submitablesToUSB

submitables = {}
detectedCount = 0

while True:
    # every {0.5} sec we will =>
    img, geotag = recieveMission() # Recieve image and geotag from UAV
    qrPresent, value = checkQR(img) # check if there is a QR code in the image and return value if so

    if qrPresent:
        # place values in dict (could be cleaner but leave it for now)
        submitables["QRimg"] = img
        submitables["geotag"] = geotag
        submitables["QRValue"] = value
    else:
        result, location, found = detectShape(img) # AI
        if found:
            detectedCount = detectedCount + 1
            alphanumeric = getAlphaNumeric(img) # alphanumeric detection

            # place values in dict (could be cleaner but leave it for now)
            submitables["img"] = img
            submitables["geotag"] = geotag
            submitables["alphanumeric"] = alphanumeric

            submitablesToJudge(submitables, detectedCount) # DevOps
            submitablesToUSB(submitables, detectedCount) # Serialization
            # count for the times of running the function , increment the count

            if result == "RR": # RR = Red Rectangel
                sendUAV(geotag) # MavLink
```



### Shape detection using AI model
 - Samir
 - mariam, safty, mohamed ali

### Shape detection using OpenCV
 - doha

### QR codes
 - emad

### Alphanumeric 
 - Peter
 - essam

### serialize submitable data into json on disk (usb)
 - nourhan
 - omar tamer

### serialize and send data to interop
 - safty
 - wahdan
 - osama

### capturing video data
 - osama
 - doha 

