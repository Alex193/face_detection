# Face Detection
Real-time face detection with YOLOv8


## Описание

Этот проект предназначен для детекции лиц человека с использованием модели YOLOv8. Он включает в себя функционал для захвата изображений с веб-камеры и камер Basler, а также для отображения результатов детекции на экране.

## Структура проекта

```
face_detection_test_task/

├── backend/
│   ├── __init__.py
│   ├── config_loader.py
│   ├── image_captor.py
│   ├── object_detection_models.py
├── frontend/
│   ├── __init__.py
│   ├── image_displayer.py
├── resources/
│   ├── config.json
│   ├── config_basler.pfs
│   ├── best.pt
├── venv/
│   ├── ...
├── main.py
├── requirements.txt
└── .idea/
    ├── ...
```

## Установка

1. Клонируйте репозиторий:
   ```sh
   git clone <URL>
   cd face_detection_test_task
   ```

2. Создайте и активируйте виртуальное окружение:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
   ```

3. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```

## Использование

Запустите основной скрипт:
```sh
python main.py
```

## Файлы и Директории

### backend/

- **config_loader.py**:
  - `ConfigLoader`: Класс для загрузки конфигурационных файлов.

- **image_captor.py**:
  - `WebCamImageCaptor`: Класс для захвата изображений с веб-камеры.
  - `BaslerImageCaptor`: Класс для захвата изображений с камер Basler.

- **object_detection_models.py**:
  - `ObjectDetectionModel`: Абстрактный базовый класс для моделей детекции объектов.
  - `YOLOv8Model`: Класс для модели детекции объектов YOLOv8.

### frontend/

- **image_displayer.py**:
  - `ImageDisplayer`: Класс для отображения изображений и отрисовки объектов на экране.

### resources/

- **config.json**: Конфигурационный файл с настройками.
- **config_basler.pfs**: Конфигурационный файл для камер Basler.
- **best.pt**: Веса модели

### main.py

Главный файл для запуска приложения. Включает в себя инициализацию всех необходимых компонентов и запуск основной логики.

## Основные Классы и Методы

### `ObjectDetectionModel`
Абстрактный класс для моделей детекции объектов.
- `load_model(self, path_to_model_weights, yolo_path)`: Загрузка модели.
- `detect_objects(self, frame, model, current_model_conf, image_dislayer, labels_translator=None)`: Детекция объектов.
- `run_model(self, translator, weights, cur_model_conf, captor, displayer, yolo_path=None)`: Запуск модели.

### `YOLOv8Model`
Наследуется от `ObjectDetectionModel`.
- `load_model(self, path_to_model_weights, yolo_path=None)`: Загрузка модели YOLOv8.
- `detect_objects(self, frame, model, current_model_conf, image_dislayer, labels_translator=None)`: Детекция объектов.
- `run_model(self, translator, weights, cur_model_conf, captor, displayer, yolo_path=None, camera_type='usb')`: Запуск модели YOLOv8 в режиме реального времени.

### `WebCamImageCaptor`
Класс для захвата изображений с веб-камеры.
- `get_frame(self)`: Захват одного кадра.
- `release(self)`: Освобождение ресурса видеопотока.

### `BaslerImageCaptor`
Класс для захвата изображений с камер Basler.
- `get_frame(self)`: Захват одного кадра.
- `release(self)`: Освобождение ресурса видеопотока.

### `ImageDisplayer`
Класс для отображения изображений и отрисовки объектов на экране.
- `draw_bbox_on_frame(self, frame, obj, color, descr)`: Отрисовка прямоугольника вокруг объекта.
- `display_frame_with_labels(self, frame)`: Отображение кадра с метками.
- `show_frame_on_monitor(self, frame, monitor_number=1)`: Отображение изображения на выбранном мониторе.

## Зависимости

Список зависимостей находится в файле `requirements.txt`. Убедитесь, что все зависимости установлены перед запуском проекта.
