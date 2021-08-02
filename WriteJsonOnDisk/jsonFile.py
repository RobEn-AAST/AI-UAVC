import json
import cv2


def submitToUSB(submitables, img, c) :

    jsonString = json.dumps(submitables)

    with open(f"submitables/{c}.json", "w") as f:
        f.write(jsonString)

    cv2.imwrite(f"submitables/{c}.png", img)

    return f"submitables/{c}.png"