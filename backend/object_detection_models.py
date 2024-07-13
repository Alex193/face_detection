from ultralytics import YOLO
from backend.config_loader import ConfigLoader
import torch.cuda
import cv2
from abc import ABC, abstractmethod
import numpy as np
import time


class ObjectDetectionModel(ABC):
    """
    Абстрактный базовый класс для моделей детекции объектов (в данном примере у нас единственная модель детекции, но в будущем можно 
    расширить до произвольного числа подключаемых моделей).

    Этот класс определяет интерфейс для моделей детекции объектов с тремя абстрактными методами, которые
    реализованы в подклассах: load_model, detect_objects и run_model. Также предоставляется метод one_object_display
    для отрисовки прямоугольника вокруг задетектированного объекта.

    Методы:
    --------
    load_model(self, path_to_model_weights, yolo_path):
        Абстрактный метод для загрузки модели детекции объектов.
        
        :param path_to_model_weights: Путь к файлу с весами модели.
        :param yolo_path: Путь к конфигурационным файлам YOLO.

    detect_objects(self, frame, model, current_model_conf, image_dislayer, labels_translator=None):
        Абстрактный метод для детекции объектов на переданном кадре.
        
        :param frame: Кадр изображения для детекции объектов.
        :param model: Модель для детекции объектов.
        :param current_model_conf: Порог уверенности текущей модели.
        :param image_dislayer: Отрисовка видео.
        :param labels_translator: (опционально) Переводчик меток.

    run_model(self, translator, weights, cur_model_conf, captor, displayer, yolo_path=None):
        Абстрактный метод для запуска модели детекции объектов.
        
        :param translator: Переводчик меток объектов.
        :param weights: Веса модели.
        :param cur_model_conf: Порог уверенности текущей модели.
        :param captor: Захват кадров с видеопотока.
        :param displayer: Отрисовка видео.
        :param yolo_path: (опционально) Путь к конфигурационным файлам YOLO.

    one_object_display(array: np.ndarray, cur_obj: np.ndarray, des: str) -> None:
        Отрисовка прямоугольника задетектированного объекта.
        
        :param array: Полотно для вывода кадра на экран.
        :param cur_obj: Координаты задетектированного объекта.
        :param des: Название задетектированного объекта.
        :return: None.
    """
    @abstractmethod
    def load_model(self, path_to_model_weights, yolo_path):
        pass

    @abstractmethod
    def detect_objects(self, frame, model, current_model_conf, image_dislayer, labels_translator=None):
        pass

    @abstractmethod
    def run_model(self, translator, weights, cur_model_conf, captor, displayer, yolo_path=None):
        pass

    def one_object_display(array: np.ndarray, cur_obj: np.ndarray, des: str) -> None:
        cv2.rectangle(array, (int(cur_obj[0]), int(cur_obj[1])),
                      (int(cur_obj[2]), int(cur_obj[3])), (255, 255, 0), 2)
        cv2.putText(array, des, (int(cur_obj[0]), int(cur_obj[1])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        return None

class YOLOv8Model(ObjectDetectionModel):
    """
    Класс для модели детекции объектов YOLOv8, наследующий от ObjectDetectionModel.

    Этот класс предоставляет реализацию для загрузки модели YOLOv8, детекции объектов на кадре и запуска модели в режиме реального времени.

    Методы:
    --------
    __init__(self):
        Инициализация объекта YOLOv8Model.

    load_model(self, path_to_model_weights, yolo_path=None):
        Загружает модель YOLOv8 с заданными весами.

        :param path_to_model_weights: Путь к файлу с весами модели.
        :param yolo_path: (актуально только для v5 версии YOLO) Путь к конфигурационным файлам YOLO.
        :return: Загруженная модель YOLOv8.

    detect_objects(self, frame, model, current_model_conf, image_dislayer, labels_translator=None):
        Выполняет детекцию объектов на переданном кадре.

        :param frame: Кадр изображения для детекции объектов.
        :param model: Модель для детекции объектов.
        :param current_model_conf: Порог уверенности текущей модели.
        :param image_dislayer: Объект для отображения изображения.
        :param labels_translator: (необязательно) Переводчик меток.

    run_model(self, translator, weights, cur_model_conf, captor, displayer, yolo_path=None, camera_type='usb'):
        Запускает модель YOLOv8 в режиме реального времени для детекции объектов.

        :param translator: Переводчик меток объектов.
        :param weights: Веса модели.
        :param cur_model_conf: Порог уверенности текущей модели.
        :param captor: Объект для захвата изображений или видео.
        :param displayer: Объект для отображения изображений или видео.
        :param yolo_path: (актуально только для v5 версии YOLO) Путь к конфигурационным файлам YOLO.
        :param camera_type: Тип камеры ('usb' или 'basler').
    """
    def __init__(self):
        pass

    def load_model(self, path_to_model_weights, yolo_path=None):
        # Check for CUDA device and set it
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {device}')
        current_model = YOLO(path_to_model_weights).to(device=device)
        return current_model

    def detect_objects(self, frame, model, current_model_conf, image_dislayer, imgsz, labels_translator=None):
        print(type(imgsz))
        details_nn_results = model.predict(frame, imgsz=imgsz)
        for item in details_nn_results:
            boxes = item.boxes.cpu().numpy()  # get boxes on cpu in numpy
            for obj in boxes.data:
                if obj[4] > current_model_conf:
                    translate = labels_translator
                    if str(int(obj[5])) in translate:
                        descr = translate[str(int(obj[5]))]
                        image_dislayer.one_object_display(frame, obj, str(descr + ' ' + str(round(obj[4], 2))))

    def run_model(self, translator, weights, cur_model_conf, captor, displayer, imgsz, yolo_path=None, camera_type='usb'):
        yolo_v8_class_obj = YOLOv8Model()
        model = yolo_v8_class_obj.load_model(weights)
        while True:
            time_1 = time.time()
            if camera_type == 'basler':
                frame = captor.capture_from_basler()
            elif camera_type == 'usb':
                ret, frame = captor.get_frame()
            else:
                ret, frame = None, None
            yolo_v8_class_obj.detect_objects(frame=frame,
                                            model=model,
                                            current_model_conf=cur_model_conf,
                                            image_dislayer=displayer,
                                            imgsz=imgsz,
                                            labels_translator=translator)
            # displayer.display_frame_with_labels(frame)
            displayer.show_frame_on_monitor(frame)
            elapsed_time = time.time() - time_1
            fps = 1 / elapsed_time
            print("FPS", fps)
            pressed_key = cv2.waitKey(1)
            if pressed_key & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break