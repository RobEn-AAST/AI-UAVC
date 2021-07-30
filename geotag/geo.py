import numpy as np
import os
import json


def repeatedTarget(loc):
   path = (os.path.dirname(os.path.abspath(__file__)))
   with open('geotags.json','r') as f:
      geos = json.load(f)
      Location = str(loc)
      Location = Location[1:-1]
      lat, lon = Location.split(',')
      lat = float(lat)
      lon = float(lon)
      if len(geos["geos"]) == 0:
         with open('geotags.json','w') as f:
            geos["geos"].append({"lat":lat, "lon":lon})
            json.dump(geos,f)
         return False
      for i in range(len(geos)):
         result = ((((lat - geos["geos"][i]["lat"] )**2) + ((lon - geos["geos"][i]["lon"])**2) )**0.5)
         if result>=30: # calculate distance avbout 20 metetr from the geolocation
            continue
         else:
            with open('geotags.json','w') as f:
               geos["geos"].append({"lat":lat, "lon":lon})
               print(geos)
               json.dump(geos,f)
               return False
      return True
