# import module
import json
submitables = {
    "a":"yes", "b":"no"
}

# while True:
# # every 0.5 sec we will =>
#     img, geotag = recieve() # DevOps
#     qrPresent, value = checkQR(img) # QRCode
#     if qrPresent:
#         submitables["img"] = img
#         submitables["geotag"] = geotag
#         submitables["QRValue"] = value
#     else:
#         result, location, found = detectShape(img) # AI
#     if found:
#         alphanumeric = detectnumeric(img) # alphanumeric detection
#         submitables["img"] = img
#         submitables["alphanumeric"] = alphanumeric

#     submitablesToJudge(submitables) # DevOps
#     submitablesToUSB(submitables) # Serialization

#     if result == "RR": # RR = Red Rectangel
#         sendUAV(geotag) # MavLink
#     # Data to be written

  
# Serializing json and 
# Writing json file

jsonString = json.dumps(submitables)
print(jsonString)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
