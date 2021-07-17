import numpy as np
import os
import json


def geo_d(geo):
   path = (os.path.dirname(os.path.abspath(__file__)))
   with open(path+'/geotags.json','r') as f:
      geos = json.load(f)
      print(geos["geos"])
      for i in range(len(geos)):
         if geos["geos"][i] == geo: # calculate distance avbout 20 metetr from the geolocation
            return False
         else:
            with open(path+'/geotags.json','w') as f:
               geos["geos"].append(geo)
               json.dump(geos,f)
               return True




print(geo_d(11))
     


      
    










   
   

