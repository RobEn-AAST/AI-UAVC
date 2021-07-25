"""
This is the base plate code for the main file
    - This code can and will change according to the need of each function developed
    - Naming and base logic are subject to change
"""

# import any needed libs like so
from QR_code.QR_function import checkQR
from WriteJsonOnDisk.jsonFile import submitToUSB
from geotag.geo import repeatedTarget
from AlphanumericCharacterDetection.getAlphaNumeric import getAlphaNumeric
from dataTransimission.server_station.UAV_SERVER import UAV_SERVER

server = UAV_SERVER()
mission = {}
detectedCount = 0
terminate = True


while terminate:
    # every {0.5} sec we will =>
    terminate, location, img = server.receiveMissions() # Receive image and geotag(long, lat) from UAV 
    qrPresent, value = checkQR(img) # check if there is a QR code in the image and return value if so
    mission["latitude"], mission["longitude"] = location # osama to get long and lat lowa7dohom

    if qrPresent:
        mission["QRimg"] = img
        mission["type"] = "QR-code"
        mission["value"] = value
    else:
        result, boundRect, found = detectShape(img) # AI returns ("Enemy", (lat, long), true) (crops image to bounding rect)
        if found and (not repeatedTarget(boundRect)):
            detectedCount = detectedCount + 1
            cropedTarget = cropToRect(img)
            mission["type"] = result # enemy or allie (as string)
            mission["alphanumeric"] = getAlphaNumeric(cropedTarget) # alphanumeric detection

            # place values in dict (could be cleaner but leave it for now)
            mission["img"] = cropedTarget
            mission["originalImage"] = img

            jsonLocation = submitToUSB(mission, detectedCount) # Serialization
            submitToJudge(jsonLocation) # DevOps
            # count for the times of running the function , increment the count

            if result == "Friend": # RR = Red Rectangel
                sendUAV(location) # MavLink