from screeninfo import get_monitors
import cv2
import numpy as np
from backend.config_loader import ConfigLoader


class ImageDisplayer:
    """
    Класс для отображения изображений и отрисовки объектов на экране.

    Этот класс предоставляет методы для управления отображением изображений на нескольких мониторах, 
    отрисовки прямоугольников (bbox) вокруг задетектированных объектов.
    """
    def __init__(self):
        """
        Инициализирует ImageDisplayer, определяя доступные мониторы.
        """
        self.monitors = get_monitors()
        self.config = ConfigLoader().get_config
        self.frame_size = (1920, 1080)  # Стандартные размеры экрана монитора

    def get_monitors_positions(self):
        """Возвращает список с координатами (x, y) верхнего левого угла каждого монитора."""
        return [(monitor.x, monitor.y) for monitor in self.monitors]
    
    def one_object_display(self, array: np.ndarray, cur_obj: np.ndarray, des: str) -> None:
        """
        Отрисовка прямоугольника задетектированного объекта
        :param array: полотно для вывода
        :param cur_obj: координаты задетектированного объекта
        :param des: название задетектированного объекта
        :return: None
        """
        cv2.rectangle(array, (int(cur_obj[0]), int(cur_obj[1])),
                        (int(cur_obj[2]), int(cur_obj[3])), (255, 255, 0), 2)
        cv2.putText(array, des, (int(cur_obj[0]), int(cur_obj[1])),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        return None

    def show_frame_on_monitor(self, frame: np.ndarray, monitor_number: int = 1) -> None:
        """
        Отображает изображение на выбранном мониторе.
        :param frame: Кадр для отрисовки на мониторе
        :param monitor_number: Индекс монитора
        :return: None
        """
        if monitor_number >= len(self.monitors) or monitor_number < 0:
            print(f"Монитор с номером {monitor_number} не найден.")
            return

        if frame is None:
            print("Передано пустое изображение")
            return

        frame = np.array(frame)
        x, y = self.get_monitors_positions()[monitor_number]
        window_name = f"Monitor {monitor_number}"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
