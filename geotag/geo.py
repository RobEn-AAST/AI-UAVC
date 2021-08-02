import json

def repeatedTarget(loc):
   
   lat, lon = loc

   with open('geotags.json','r') as f:
      geos = json.load(f)
   for geo in geos["geos"]:
      result = ((((lat - geo["lat"] )**2) + ((lon - geo["lon"])**2) )**0.5)

      if result < 20:
         return True

   with open('geotags.json','w') as f:
      geos["geos"].append({"lat":lat, "lon":lon})
      json.dump(geos, f)

   return False