import numpy as np
import cv2
from backend.image_captor import BaslerImageCaptor, WebCamImageCaptor
from backend.config_loader import ConfigLoader
from frontend.image_displayer import ImageDisplayer
from backend.object_detection_models import YOLOv8Model
import time

# загрузка json файла конфигурацией
path_to_config_json = 'resources/config.json'
config_loader = ConfigLoader(path_to_config_json)
config = config_loader.get_config

displayer = ImageDisplayer()
imgsz = int(config['face_detection']['yolo_imgsize'])
captor = WebCamImageCaptor(config["video_source_main_camera"], config['stream_from_camera_width'], config['stream_from_camera_height'])
translator = config['face_detection']["names"]
cur_model_conf = config['face_detection']['model_conf']
weights = config['face_detection']['model_path']
yolo_v8_class_obj = YOLOv8Model()
yolo_v8_class_obj.run_model(translator, weights, cur_model_conf, captor, displayer, imgsz)