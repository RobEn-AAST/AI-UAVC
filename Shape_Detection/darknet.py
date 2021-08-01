#!/usr/bin/env python3

"""
Python 3 wrapper for identifying objects in images

Running the script requires opencv-python to be installed (`pip install opencv-python`)
Directly viewing or returning bounding-boxed images requires scikit-image to be installed (`pip install scikit-image`)
Use pip3 instead of pip on some systems to be sure to install modules for python3
"""

from ctypes import *
import math
import random
import os
import cv2
import time


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int),
                ("embeddings", POINTER(c_float)),
                ("embedding_size", c_int),
                ("sim", c_float),
                ("track_id", c_int)]

class DETNUMPAIR(Structure):
    _fields_ = [("num", c_int),
                ("dets", POINTER(DETECTION))]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


def network_width(net):
    return lib.network_width(net)


def network_height(net):
    return lib.network_height(net)


def bbox2points(bbox):
    """
    From bounding box yolo format
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


# def class_colors(names):
#     """
#     Create a dict with one random BGR color for each
#     class name
#     """
#     return {name: (
#         random.randint(0, 255),
#         random.randint(0, 255),
#         random.randint(0, 255)) for name in names}


def load_network(config_file, data_file, weights, batch_size=1):
    """
    load model description and weights from config files
    args:
        config_file (str): path to .cfg model file
        data_file (str): path to .data model file
        weights (str): path to weights
    returns:
        network: trained model
        class_names
        class_colors
    """
    network = load_net_custom(
        config_file.encode("ascii"),
        weights.encode("ascii"), 0, batch_size)
    metadata = load_meta(data_file.encode("ascii"))
    class_names = [metadata.names[i].decode("ascii") for i in range(metadata.classes)]
    # colors = class_colors(class_names)
    colors = class_colors_v
    return network, class_names, colors


def print_detections(detections, coordinates=False):
    print("\nObjects:")
    for label, confidence, bbox in detections:
        x, y, w, h = bbox
        if coordinates:
            print("{}: {}%    (left_x: {:.0f}   top_y:  {:.0f}   width:   {:.0f}   height:  {:.0f})".format(label, confidence, x, y, w, h))
        else:
            print("{}: {}%".format(label, confidence))


def draw_boxes(detections, image, colors):
    import cv2
    for label, confidence, bbox in detections:
        left, top, right, bottom = bbox2points(bbox)
        cv2.rectangle(image, (left, top), (right, bottom), colors[label], 1)
        cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                    (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    colors[label], 2)
    return image


def decode_detection(detections):
    decoded = []
    for label, confidence, bbox in detections:
        confidence = str(round(confidence * 100, 2))
        decoded.append((str(label), confidence, bbox))
    return decoded


def remove_negatives(detections, class_names, num):
    """
    Remove all classes with 0% confidence within the detection
    """
    predictions = []
    for j in range(num):
        for idx, name in enumerate(class_names):
            if detections[j].prob[idx] > 0:
                bbox = detections[j].bbox
                bbox = (bbox.x, bbox.y, bbox.w, bbox.h)
                predictions.append((name, detections[j].prob[idx], (bbox)))
    return predictions

empty = cv2.imread('empty.jpg')

def detect_image(network, class_names, image, thresh=.5, hier_thresh=.5, nms=.45):
    """
        Returns a list with highest confidence class and their bbox
    """
    pnum = pointer(c_int(0))
    predict_image(network, image)
    detections = get_network_boxes(network, image.w, image.h,
                                   thresh, hier_thresh, None, 0, pnum, 0)
    num = pnum[0]
    if nms:
        do_nms_sort(detections, num, len(class_names), nms)
    predictions = remove_negatives(detections, class_names, num)
    predictions = decode_detection(predictions)
    free_detections(detections, num)
    return sorted(predictions, key=lambda x: x[1])


if os.name == "posix":
    cwd = "/media/raven/raven/yolo/darknet4a"
    lib = CDLL(cwd + "/libdarknet.so", RTLD_GLOBAL)
elif os.name == "nt":
    cwd = os.path.dirname(__file__)
    os.environ['PATH'] = cwd + ';' + os.environ['PATH']
    lib = CDLL("darknet.dll", RTLD_GLOBAL)
else:
    print("Unsupported OS")
    exit

lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE,c_char_p]

predict = lib.network_predict_ptr
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
init_cpu = lib.init_cpu

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_batch_detections = lib.free_batch_detections
free_batch_detections.argtypes = [POINTER(DETNUMPAIR), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict_ptr
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

free_network_ptr = lib.free_network_ptr
free_network_ptr.argtypes = [c_void_p]
free_network_ptr.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

predict_image_letterbox = lib.network_predict_image_letterbox
predict_image_letterbox.argtypes = [c_void_p, IMAGE]
predict_image_letterbox.restype = POINTER(c_float)

network_predict_batch = lib.network_predict_batch
network_predict_batch.argtypes = [c_void_p, IMAGE, c_int, c_int, c_int,
                                   c_float, c_float, POINTER(c_int), c_int, c_int]
network_predict_batch.restype = POINTER(DETNUMPAIR)


# ax = load_network('cfg/yolov4-tiny-3l-test.cfg', 'data/obj.data', 'backup/yolov4-tiny-3l_last.weights')
# detect_image(ax, ['BR', 'RR'], "new/a.jpg".encode('utf-8'))

network, class_names, class_colors_v = 0, 0, {'Friend':(0,0,255), 'Foe':(255,0,0)}
width, height, darknet_image = 0, 0, 0

def load_model():
    global network, class_names, class_colors_v, darknet_image, width, height
    network, class_names, class_colors_v = load_network('cfg/yolov4-tiny-3l-test.cfg', 'data/obj.data', 'backup/yolov4-tiny-3l_last.weights')

    width = network_width(network)
    height = network_height(network)
    darknet_image = make_image(width, height, 3)

def predict_rText(image):
    global network, class_names, class_colors_v, darknet_image, width, height
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    copy_image_from_bytes(darknet_image, image.tobytes())
    detections = detect_image(network, class_names, darknet_image, thresh=0.4)
    return detections

def predict_rFullImage(image):
    global network, class_names, class_colors_v, darknet_image, width, height
    # image = cv2.imread(image)
    if image is None:
        return None, None
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    copy_image_from_bytes(darknet_image, image.tobytes())
    detections = detect_image(network, class_names, darknet_image, thresh=0.7, hier_thresh=0.7, nms=1)
    image = draw_boxes(detections, image, class_colors_v)
    return image, detections

# def predict_rdividedImage(image):
#     s1 = image[:736, :736]
#     s2 = image[:736, 704:]
#     s3 = image[334:, :736]
#     s4 = image[334:, 704:]
#     a, a1 = predict_rFullImage(s1)
#     b, b1 = predict_rFullImage(s2)
#     c, c1 = predict_rFullImage(s3)
#     d, d1 = predict_rFullImage(s4)
#     a1 = a1 + b1 + c1 + d1 
#     image[:736, :736] = a
#     image[:736, 704:] = b
#     image[344:, :736] = c
#     image[344:, 704:] = d
#     return image, a1


def free_model():
    free_image(darknet_image)


def get_cropped_image(image, detections):
    count = 1
    if len(detections) > 0:
        label, confidence, bbox = detections
        xmin, ymin, xmax, ymax = bbox2points(bbox)
        cropped_image = image[ymin:ymax, xmin:xmax]

    # image_arr = [0 for i in range(5)]
    # for i in detections:
    #     label, confidence, bbox = i
    #     xmin, ymin, xmax, ymax = bbox2points(bbox)
    #     image_arr[count] = image[ymin:ymax, xmin:xmax]
    #     count+=1


    return cropped_image, count


def one_detection_to_points(detections):
        label, confidence, bbox = detections
        xmin, ymin, xmax, ymax = bbox2points(bbox)
            
        return xmin, ymin, xmax, ymax


def detectShape(frame):
    image, detection = predict_rFullImage(frame)
    
    if detection.__len__()>0:
        detection = detection[0]
    else:
        return "", frame, empty, False

    label = detection[0]
    # confidence = detection[0][1]
    # bbox = detection[0][2]
    # print(objType)
    Found = False
    if label is not None:
        Found = True
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    crop, count = get_cropped_image(image, detection)

    return label, image, crop, Found


if __name__ == "__main__":
    start = time.process_time()
    load_model()
    print(time.process_time() - start)


    
    # vid = cv2.VideoCapture('testvideos/MAH00145.MP4')
    vid = cv2.VideoCapture('testvideos/MAH00155.MP4')
    ret = True
    while(True):
        ret, frame = vid.read()
        if not ret: break
        
        start = time.process_time()
        # image, detection = predict_rdividedImage(frame)
        image, detection = predict_rFullImage(frame)
        print(detection)
        print(time.process_time() - start)
        
        
        label, image, cropped, Found = detectShape(frame)

        cv2.imshow('frame', image)
        try:
            cv2.imshow('frame2', cropped)
        except Exception:
            pass
        print(label, Found)

        # crop, count = get_cropped_images_array(image, detection)
        # print(count)
        # if (count>1):
        #     input()

        # for i in range(count):
        #     try:
        #         cv2.imshow('frame'+str(i), cv2.cvtColor(crop[i], cv2.COLOR_RGB2BGR))
        #     except Exception as e:
        #         print(e)
        #         continue
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

    free_model()
