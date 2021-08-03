import json
from math import radians, cos, sin, asin, sqrt

def repeatedTarget(loc):
   
   lat, lon = loc
  
   with open('geotags.json','r') as f:
      geos = json.load(f)

   for geo in geos["geos"]:
      #result = ((((lat - geo["lat"] )**2) + ((lon - geo["lon"])**2) )**0.5)
      dlon = lon - geo["lon"] 
      dlat = lat - geo["lat"]
      a = sin(dlat/2)**2 + cos(geo["lat"]) * cos(lat) * sin(dlon/2)**2
      c = 2 * asin(sqrt(a))
      r = 6371 # Radius of earth in kilometers. Use 3956 for miles 
      d =c * r
      
      if d < 0.3 :
         print(f"geotag distance = {d} from past location so it is repeated")
         return True

   with open('geotags.json','w') as f:
      geos["geos"].append({"lat":lat, "lon":lon})
      json.dump(geos, f)

   return False