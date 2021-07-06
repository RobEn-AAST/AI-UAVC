# AI-UAVC
The Egypt unmanned arial vehicle challange


### Goal program
This is a simple blackbox representation of the abstraction level we want to achieve
```python
 submitables = {}

 while True:
  # every 0.5 sec we will =>
  img, geotag = recieve() # DevOps
  qrPresent, value = checkQR(img) # QRCode
  if qrPresent:
   submitables["img"] = img
   submitables["geotag"] = geotag
   submitables["QRValue"] = value
  else:
   result, location, found = detectShape(img) # AI
   if found:
    alphanumeric = detectnumeric(img) # alphanumeric detection
    submitables["img"] = img
    submitables["alphanumeric"] = alphanumeric

    submitablesToJudge(submitables) # DevOps
    submitablesToUSB(submitables,count) # Serialization
    # count for the times of running the function , increment the count
    count = count + 1

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

