# AI-UAVC
The Egypt unmanned arial vehicle challange


### Goal program
This is a simple blackbox representation of the abstraction level we want to achieve
```python
mission = {}
detectedCount = 0

while True:
    # every {0.5} sec we will =>
    img, geotag = recieveMission() # Recieve image and geotag(long, lat) from UAV 
    qrPresent, value = checkQR(img) # check if there is a QR code in the image and return value if so

    if qrPresent:
        mission["QRimg"] = img
        mission["type"] = "QR-code"
        mission["longitude"], mission["latitude"] = geotag
        mission["value"] = value
    else:
        result, location, found = detectShape(img) # AI
        if found and (not repeatedTarget(geotag)):
            detectedCount = detectedCount + 1
            alphanumeric = getAlphaNumeric(img) # alphanumeric detection

            # place values in dict (could be cleaner but leave it for now)
            mission["img"] = img
            mission["geotag"] = geotag
            mission["alphanumeric"] = alphanumeric

            jsonLocation = submitToUSB(mission, detectedCount) # Serialization
            submitToJudge(jsonLocation) # DevOps
            # count for the times of running the function , increment the count

            if result == "RR": # RR = Red Rectangel
                sendUAV(geotag) # MavLink
```


## Missions

### Shape detection using AI model
 - Samir
 - mariam, safty, mohamed ali

### Shape detection using OpenCV
 - doha

### QR codes (Testing)
 - emad

### Alphanumeric (Testing)
split the model into 2 functions that load the model at first and predict when needed
 - kohel
 - essam
 - nourhan
 - omar

### serialize submitable data into json on disk
return string of locations
 - doha
 - omar tamer

### serialize and send data to interop
 - safty
 - wahdan
 - osama

### GeoCheck
check if the new given geotag is in radius of a previus detected object to prevent re-submission of same object
 - osama

### capturing video data for training ❌
 - osama
