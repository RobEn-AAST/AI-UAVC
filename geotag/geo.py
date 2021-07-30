import numpy as np
import os
import json


def repeatedTarget(loc):
   path = (os.path.dirname(os.path.abspath(__file__)))
   with open(path+'/geotags.json','r') as f:
      Location = str(loc)
      lat, lon = Location.split(',')
      lat = float(lat)
      lon = float(lon)
      geos = json.load(f)
      print(geos["geos"])
      for i in range(len(geos)):
         result= ((((loc[lat] - geos["geos"][i]["lat"] )**2) + ((loc[lon]-geos[i]["lon"])**2) )**0.5)
         print(result)
         if result>=30: # calculate distance avbout 20 metetr from the geolocation
            return True
         else:
            with open(path+'/geotags.json','w') as f:
               geos["geos"].append(loc)
               json.dump(geos,f)
               return False

location =(1.2,2.3)
repeatedTarget(location)
