from numpy.core.fromnumeric import ptp
from WriteJsonOnDisk.jsonFile import submitToUSB
from geotag.geo import repeatedTarget
import AlphanumericCharacterDetection.AlphaNumeric
from dataTransimission.server_station.UAV_SERVER import UAV_SERVER
import Shape_Detection.darknet as dn
from sendUAV.sender import UAVSOCK
from dataTransimission.server_station.interop import interop_client


dn.load_model()
server = UAV_SERVER()
UAV = UAVSOCK("127.0.0.1", 5500)
mission = {}
detectedCount = 0
terminate = True
print('''                                                                                                     
RRRRRRRRRRRRRRRRR                    BBBBBBBBBBBBBBBBB                                                
R::::::::::::::::R                   B::::::::::::::::B                                               
R::::::RRRRRR:::::R                  B::::::BBBBBB:::::B                                              
RR:::::R     R:::::R                 BB:::::B     B:::::B                                             
  R::::R     R:::::R   ooooooooooo     B::::B     B:::::B    eeeeeeeeeeee    nnnn  nnnnnnnn           
  R::::R     R:::::R oo:::::::::::oo   B::::B     B:::::B  ee::::::::::::ee  n:::nn::::::::nn         
  R::::RRRRRR:::::R o:::::::::::::::o  B::::BBBBBB:::::B  e::::::eeeee:::::een::::::::::::::nn        
  R:::::::::::::RR  o:::::ooooo:::::o  B:::::::::::::BB  e::::::e     e:::::enn:::::::::::::::n       
  R::::RRRRRR:::::R o::::o     o::::o  B::::BBBBBB:::::B e:::::::eeeee::::::e  n:::::nnnn:::::n       
  R::::R     R:::::Ro::::o     o::::o  B::::B     B:::::Be:::::::::::::::::e   n::::n    n::::n       
  R::::R     R:::::Ro::::o     o::::o  B::::B     B:::::Be::::::eeeeeeeeeee    n::::n    n::::n       
  R::::R     R:::::Ro::::o     o::::o  B::::B     B:::::Be:::::::e             n::::n    n::::n       
RR:::::R     R:::::Ro:::::ooooo:::::oBB:::::BBBBBB::::::Be::::::::e            n::::n    n::::n       
R::::::R     R:::::Ro:::::::::::::::oB:::::::::::::::::B  e::::::::eeeeeeee    n::::n    n::::n       
R::::::R     R:::::R oo:::::::::::oo B::::::::::::::::B    ee:::::::::::::e    n::::n    n::::n       
RRRRRRRR     RRRRRRR   ooooooooooo   BBBBBBBBBBBBBBBBB       eeeeeeeeeeeeee    nnnnnn    nnnnnn       
                                                                                                      
                                                                                                      
                                                                                                      
                                                                                                      
                                                                                                      

UUUUUUUU     UUUUUUUU               AAA               VVVVVVVV           VVVVVVVV        CCCCCCCCCCCCC
U::::::U     U::::::U              A:::A              V::::::V           V::::::V     CCC::::::::::::C
U::::::U     U::::::U             A:::::A             V::::::V           V::::::V   CC:::::::::::::::C
UU:::::U     U:::::UU            A:::::::A            V::::::V           V::::::V  C:::::CCCCCCCC::::C
 U:::::U     U:::::U            A:::::::::A            V:::::V           V:::::V  C:::::C       CCCCCC
 U:::::D     D:::::U           A:::::A:::::A            V:::::V         V:::::V  C:::::C              
 U:::::D     D:::::U          A:::::A A:::::A            V:::::V       V:::::V   C:::::C              
 U:::::D     D:::::U         A:::::A   A:::::A            V:::::V     V:::::V    C:::::C              
 U:::::D     D:::::U        A:::::A     A:::::A            V:::::V   V:::::V     C:::::C              
 U:::::D     D:::::U       A:::::AAAAAAAAA:::::A            V:::::V V:::::V      C:::::C              
 U:::::D     D:::::U      A:::::::::::::::::::::A            V:::::V:::::V       C:::::C              
 U::::::U   U::::::U     A:::::AAAAAAAAAAAAA:::::A            V:::::::::V         C:::::C       CCCCCC
 U:::::::UUU:::::::U    A:::::A             A:::::A            V:::::::V           C:::::CCCCCCCC::::C
  UU:::::::::::::UU    A:::::A               A:::::A            V:::::V             CC:::::::::::::::C
    UU:::::::::UU     A:::::A                 A:::::A            V:::V                CCC::::::::::::C
      UUUUUUUUU      AAAAAAA                   AAAAAAA            VVV                    CCCCCCCCCCCCC
''')

while terminate:
    terminate, location, img = server.receiveMissions()
    if not terminate:
        break
    if location == None:
        continue
    mission["latitude"], mission["longitude"], altitude = location
    objType, imageResult, croppedTarget, found = dn.detectShape(img)
    if found and (not repeatedTarget(location)):
        detectedCount = detectedCount + 1
        mission["type"] = objType
        mission["alphanumeric"] = AlphanumericCharacterDetection.AlphaNumeric.getAlphaNumeric(croppedTarget)[0][0]

        imagePath = submitToUSB(mission, imageResult,detectedCount)

        #submitToJudge(mission, imagePath) # DevOps TODO: finish interop wrapping

        if objType == "Friend":
            UAV.sendUAV(location)

print("finished")