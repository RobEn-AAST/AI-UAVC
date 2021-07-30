from WriteJsonOnDisk.jsonFile import submitToUSB
from geotag.geo import repeatedTarget
import AlphanumericCharacterDetection.AlphaNumeric
from dataTransimission.server_station.UAV_SERVER import UAV_SERVER


server = UAV_SERVER()
# load model
mission = {}
detectedCount = 0
terminate = True

while terminate:
    terminate, location, img = server.receiveMissions() # TODO: set up location on pi too
    mission["latitude"], mission["longitude"] = location

    objType, imageResult, croppedTarget, found = detectShape(img) # AI returns ("Foe", (lat, long), true) (crops image to bounding rect) TODO: wrap the AI 
        # objType : 'Friend' || 'Foe'
        # found : bool
        # imageResult: image with rectangle drawn

    if found and (not repeatedTarget(location)):
        detectedCount = detectedCount + 1
        mission["type"] = objType
        mission["alphanumeric"] = AlphanumericCharacterDetection.AlphaNumeric.getAlphaNumeric(croppedTarget)

        mission["img"] = croppedTarget
        mission["originalImage"] = imageResult

        mission["imgPath"] = submitToUSB(mission, detectedCount)
        submitToJudge(mission) # DevOps TODO: finish interop wrapping

        # if objType == "Friend": # RR = Red Rectangel
        #     sendUAV(location) # MavLink TODO: see wahdan/salma