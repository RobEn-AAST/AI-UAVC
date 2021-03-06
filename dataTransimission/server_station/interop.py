from os import path
from auvsi_suas.proto import interop_api_pb2
from .interop_library.auvsi_suas.client import client
from .interop_library.auvsi_suas.proto import interop_api_pb2
from urllib import request
from re import findall
import functools
from PIL.ExifTags import TAGS
from PIL import Image
from GPSPhoto import gpsphoto


class interop_client:
    __responses = {
        200 : ("The request was successful","no action needed"),
        400 : ("The request was bad/invalid","Check the contents of the request"),
        401 : ("The request is unauthorized","check the login credentials"),
        403 : ("The request is forbidden","check that you are not sending to admin page"),
        404 : ("The request was made to an invalid URL","check the URL string"),
        405 : ("The request used an invalid method","check whether you are using a get request or a post request"),
        500 : ("The server encountered an internal error","report what happened to the judges")
    }

    def __message(e):
        code_string = findall("\d{3}\s{1}Error",str(e))[0]
        code_string = findall("\d{3}",code_string)[0]
        error_code = int(code_string)
        problem,solution = interop_client.__resolve_responses(error_code)
        print("exception raised !!!")
        print("error code : " + code_string)
        print("problem : " + problem)
        print("solution : " + solution)
        exit()

    def __handle_with(handler):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    return handler(e)
            return wrapper
        return decorator

    @__handle_with(__message)
    def __init__(self,ipaddress,port,userame,password):
        self.ipaddress = ipaddress
        self.port = port
        self.username = userame
        self.password = password
        self.__this_client = client.Client(url='http://' + ipaddress + ':' + port,username=userame,password=password)

    def is_alive(self):
        result = request.urlopen("http://" + self.ipadress + ":" + self.port).getcode()
        return True if result == 200 else False, result

    @staticmethod
    def __resolve_responses(response_code):
        if response_code in interop_client.__responses:
            return interop_client.__responses[response_code]
        else:
            return "Un resolved error"
    @__handle_with(__message)
    def get_teams(self):
        return self.__this_client.get_teams()

    @__handle_with(__message)
    def get_mission(self,mission_id):
        return self.__this_client.get_mission(mission_id)

    @__handle_with(__message)
    def submitToJudge(self, mission, imagePath,id = 1):
        object_of_interset = interop_api_pb2.Odlc()
        object_of_interset.type = interop_api_pb2.Odlc.STANDARD
        object_of_interset.latitude = mission["latitude"]
        object_of_interset.longitude = mission["longitude"]
        object_of_interset.alphanumeric = mission["alphanumeric"]
        object_of_interset.autonomous = True
        object_of_interset.mission = id
        if mission["type"] == "Friend":
            object_of_interset.shape_color = interop_api_pb2.Odlc.RED
        else:
            object_of_interset.shape_color = interop_api_pb2.Odlc.BLUE
        object_of_interset.alphanumeric_color = interop_api_pb2.Odlc.WHITE
        object_of_interset.shape = interop_api_pb2.Odlc.SQUARE
        object_of_interset = self.__this_client.post_odlc(object_of_interset)
        photo = gpsphoto.GPSPhoto(imagePath)
        info = gpsphoto.GPSInfo((mission["latitude"], mission["longitude"]))
        photo.modGPSData(info,  path)
        with open(imagePath, 'rb') as f:
            image_data = f.read()
            self.__this_client.put_odlc_image(object_of_interset.id, image_data)

    @__handle_with(__message)
    def update_location(self, latitude, longitude, altitude, heading):
        telemetry= interop_api_pb2.Telemetry()
        telemetry.latitude = latitude
        telemetry.longitude = longitude
        telemetry.altitude = altitude
        telemetry.heading = heading
        self.__this_client.post_telemetry(telemetry)

if __name__ == '__main__':
    interop_client.test('127.0.0.1','8000','testuser','testpass')
