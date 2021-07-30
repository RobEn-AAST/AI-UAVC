from WriteJsonOnDisk.jsonFile import submitToUSB
from geotag.geo import repeatedTarget
import AlphanumericCharacterDetection.AlphaNumeric
from dataTransimission.server_station.UAV_SERVER import UAV_SERVER

server = UAV_SERVER()
mission = {}
detectedCount = 0
terminate = True

while terminate:
    terminate, location, img = server.receiveMissions()
    mission["latitude"], mission["longitude"] = location # osama to get long and lat lowa7dohom TODO: get lat and long alone

    result, boundRect, found = detectShape(img) # AI returns ("Foe", (lat, long), true) (crops image to bounding rect) TODO: wrap the AI 

    if found and (not repeatedTarget(location)): # TODO: finish repeated target if found a repeated location tag
        detectedCount = detectedCount + 1
        croppedTarget = cropToRect(img) # TODO: crop to rect or get it cropped from detect shape 
        mission["type"] = result
        mission["alphanumeric"] = AlphanumericCharacterDetection.AlphaNumeric.getAlphaNumeric(croppedTarget)

        mission["img"] = croppedTarget
        mission["originalImage"] = img

        jsonLocation = submitToUSB(mission, detectedCount)
        submitToJudge(jsonLocation) # DevOps TODO: finish interop wrapping

        if result == "Friend": # RR = Red Rectangel
            sendUAV(location) # MavLink TODO: see Emad/salma/abbas about this unholy function