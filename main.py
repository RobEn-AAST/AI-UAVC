import cv2
from numpy.core.fromnumeric import ptp
from WriteJsonOnDisk.jsonFile import submitToUSB
from geotag.geo import repeatedTarget
import AlphanumericCharacterDetection.AlphaNumeric
from dataTransimission.server_station.UAV_SERVER import UAV_SERVER
import Shape_Detection.darknet as dn
from sendUAV.sender import UAVSOCK
dn.load_model()
server = UAV_SERVER()
UAV = UAVSOCK("localhost", 5500)
mission = {}
detectedCount = 0
terminate = True

while terminate:
    terminate, location, img = server.receiveMissions()
    if not terminate:
        break
    if location == None:
        continue
    mission["latitude"], mission["longitude"] = location
<<<<<<< HEAD

    objType, imageResult, croppedTarget, found = dn.detectShape(img)
    if found and (not repeatedTarget(location)):
        detectedCount += 1
=======
    objType, imageResult, croppedTarget, found, lat, lon = dn.detectShape(img)
    location = lat + location[0], lon + location[1]
    # cv2.imwrite("results.jpg",imageResult)
    if found and (not repeatedTarget(location)):
        detectedCount = detectedCount + 1
        print(detectedCount)
>>>>>>> a5b69235e81459192ed488577aa84bbb10f798f2
        mission["type"] = objType
        mission["alphanumeric"] = AlphanumericCharacterDetection.AlphaNumeric.getAlphaNumeric(croppedTarget)[0][0]

        imagePath = submitToUSB(mission, imageResult,detectedCount)

        #submitToJudge(mission, imagePath) # DevOps TODO: finish interop wrapping

        if objType == "Friend":
            UAV.sendUAV(location)
print("finished")

# TODO 
# nefok repeatedTarget and make it clear
# get exact timeout for sleep from UAV team
# talk about interop with UAV
# make sure connection string on PI is set correctly
# talk about sockets in sendUAV with emad
# ask emad which image to save (cropped or original) = original