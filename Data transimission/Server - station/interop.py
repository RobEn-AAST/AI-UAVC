from client.auvsi_suas.client import client
from client.auvsi_suas.proto import interop_api_pb2
from urllib import request
from re import findall
import functools
from cv2 import imwrite

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
        return interop_client.__responses[response_code]

    @__handle_with(__message)
    def get_teams(self):
        return self.__this_client.get_teams()

    @__handle_with(__message)
    def get_mission(self,mission_id):
        return self.__this_client.get_mission(mission_id)

    @__handle_with(__message)
    def send_standard_object(self,mission,geolocation,orientation,shape,shape_color,letter,letter_color,image):
        object_of_interset = interop_api_pb2.Odlc()
        object_of_interset.type = interop_api_pb2.Odlc.STANDARD
        object_of_interset.latitude = geolocation[0]
        object_of_interset.longitude = geolocation[1]
        object_of_interset.orientation = orientation
        object_of_interset.shape = shape
        object_of_interset.shape_color = shape_color
        object_of_interset.alphanumeric = letter
        object_of_interset.alphanumeric_color = letter_color
        object_of_interset.autonomous = True
        object_of_interset.mission = mission
        object_of_interset = self.__this_client.post_odlc(object_of_interset)
        imwrite(str(mission) + ".jpg", image)
        with open(str(mission) + ".jpg", 'rb') as f:
            image_data = f.read()
            self.__this_client.put_odlc_image(object_of_interset.id, image_data)

    @__handle_with(__message)
    def send_emergant_object(self,mission,latitude,longitude,image_path,description = None):
        object_of_interset = interop_api_pb2.Odlc()
        object_of_interset.mission = mission
        object_of_interset.type = 4
        object_of_interset.latitude = latitude
        object_of_interset.longitude = longitude
        if description != None:
            object_of_interset.description = description
        object_of_interset.autonomous = True
        object_of_interset = self.__this_client.post_odlc(object_of_interset)
        with open(image_path, 'rb') as f:
            image_data = f.read()
            self.__this_client.put_odlc_image(object_of_interset.id, image_data)

    @__handle_with(__message)
    def send_sample(self):
        object_of_interset = interop_api_pb2.Odlc()
        object_of_interset.type = interop_api_pb2.Odlc.STANDARD
        object_of_interset.latitude = 38
        object_of_interset.longitude = -76
        object_of_interset.orientation = interop_api_pb2.Odlc.N
        object_of_interset.shape = interop_api_pb2.Odlc.SQUARE
        object_of_interset.shape_color = interop_api_pb2.Odlc.GREEN
        object_of_interset.alphanumeric = 'A'
        object_of_interset.alphanumeric_color = interop_api_pb2.Odlc.WHITE
        object_of_interset.autonomous = True
        object_of_interset.mission = 1
        object_of_interset = self.__this_client.post_odlc(object_of_interset)        
        with open('1.jpg', 'rb') as f:
            image_data = f.read()
            self.__this_client.put_odlc_image(object_of_interset.id, image_data)
    @staticmethod
    def test(ipadrress,port,username,password):
        my = interop_client(ipadrress,port,username,password)
        my.send_sample()
        my.send_emergant_object(1,38,-76,'1.jpg',description= "iam an emergant object")
if __name__ == '__main__':
    interop_client.test('127.0.0.1','8000','testuser','testpass')