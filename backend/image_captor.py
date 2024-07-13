from pypylon import pylon
import cv2


class BaslerImageCaptor:
    """
    Класс для захвата изображений с камер Basler.

    Этот класс предоставляет методы для инициализации камеры Basler, захвата кадров и освобождения ресурса камеры.

    Методы:
    --------
    __init__(self, camera_index, path_to_basler_pfs_config_file):
        Инициализирует объект BaslerImageCaptor, открывая видеопоток с указанной камеры Basler.

        :param camera_index: Индекс камеры (0 для первой камеры, 1 для второй камеры).
        :param path_to_basler_pfs_config_file: Путь к файлу конфигурации камеры Basler.

    get_frame(self):
        Захватывает один кадр из видеопотока.

        :return: Кортеж (ret, frame), где ret - успешность захвата кадра (True/False),
                 frame - захваченный кадр (None, если кадр не был захвачен).

    release(self):
        Освобождает ресурс видеопотока, если он был открыт.

    __enter__(self):
        Возвращает self при использовании объекта в контексте менеджера (with statement).

    __exit__(self, exc_type, exc_val, exc_tb):
        Освобождает ресурс камеры при выходе из контекста менеджера.

    __del__(self):
        Освобождает ресурс видеопотока при удалении объекта.
    """
    def __init__(self, camera_index, path_to_basler_pfs_config_file):
        # Инициализация камеры (0 - единственная камера, 1 - вторая камера)
        # Получаем экземпляр фабрики для создания устройств
        self.tl_factory = pylon.TlFactory.GetInstance()
        # Получаем список всех подключенных устройств (камер)
        self.devices = self.tl_factory.EnumerateDevices()
        if (len(self.devices) == 1 or len(self.devices) == 2) and camera_index == 0:
            self.camera = pylon.InstantCamera(self.tl_factory.CreateDevice(self.devices[0]))
            self.camera.Open()
            try:
                # Попытка загрузить конфигурационный файл
                pylon.FeaturePersistence.Load(path_to_basler_pfs_config_file, self.camera.GetNodeMap(), True)
                print("Конфигурация камеры Basler 0 успешно загружена.")
            except Exception as e:
                # Обработка ошибки при загрузке конфигурации
                print(f"Ошибка при загрузке конфигурации: {e}")
                raise ValueError(f"Не удалось загрузить конфигурацию камеры Basler 0 из файла {path_to_basler_pfs_config_file}")
        elif len(self.devices) == 2 and camera_index == 1:
            self.camera = pylon.InstantCamera(self.tl_factory.CreateDevice(self.devices[1]))
            self.camera.Open()
            try:
                # Попытка загрузить конфигурационный файл
                pylon.FeaturePersistence.Load(path_to_basler_pfs_config_file, self.camera.GetNodeMap(), True)
                print("Конфигурация камеры Basler 1 успешно загружена.")
            except Exception as e:
                # Обработка ошибки при загрузке конфигурации
                print(f"Ошибка при загрузке конфигурации: {e}")
                raise ValueError(
                    f"Не удалось загрузить конфигурацию камеры Basler 1 из файла {path_to_basler_pfs_config_file}")
        else:
            raise ValueError(
                "Число подключенных камер Basler должно быть равно 1 или 2 (camera_index принимает значения 0 или 1)")
        # Настройка конвертера изображений
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        # Начало захвата изображений
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def get_frame(self):
        # Захват одного кадра
        if self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                grabResult.Release()
                return True, cv2.flip(img, 1)
            else:
                grabResult.Release()
                return False, None
        else:
            return False, None

    def release(self):
        # Остановка захвата и закрытие камеры
        if self.camera.IsGrabbing():
            self.camera.StopGrabbing()
        if self.camera.IsOpen():
            self.camera.Close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()


class WebCamImageCaptor:
    """
    Класс для захвата изображений с веб-камеры.

    Этот класс предоставляет методы для инициализации веб-камеры, захвата кадров и освобождения ресурса камеры.

    Методы:
    --------
    __init__(self, video_source, width, height):
        Инициализирует объект WebCamImageCaptor, открывая видеопоток с заданного источника.

        :param video_source: Источник видеопотока (например, индекс камеры или путь к видеофайлу).
        :param width: Ширина кадра.
        :param height: Высота кадра.

    __enter__(self):
        Возвращает self при использовании объекта в контексте менеджера (with statement).

    __exit__(self, exc_type, exc_val, exc_tb):
        Освобождает ресурс камеры при выходе из контекста менеджера.

    get_frame(self):
        Захватывает один кадр из видеопотока.

        :return: Кортеж (ret, frame), где ret - успешность захвата кадра (True/False), 
                 frame - захваченный кадр (None, если кадр не был захвачен).

    release(self):
        Освобождает ресурс видеопотока, если он был открыт.

    __del__(self):
        Освобождает ресурс видеопотока при удалении объекта.
    """

    def __init__(self, video_source, width, height):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise Exception(f"Unable to open video source: {video_source}")

        # Параметры камеры можно настраивать при создании объекта
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # self.vid.set(cv2.CAP_PROP_FPS, fps)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, frame
            else:
                return ret, None
        else:
            return False, None

    def release(self):
        if self.vid.isOpened():
            self.vid.release()

    def __del__(self):
        self.release()
