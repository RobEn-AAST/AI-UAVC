import json
import cv2


def submitToUSB(submitables, img, c) :

    jsonString = json.dumps(submitables)

    with open("submitables/" + str(c) + ".json", "w") as f:
        f.write(jsonString)

    cv2.imwrite("submitables/" + str(c) + ".png", img)

    return "submitables/" + str(c) + ".png"