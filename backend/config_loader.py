import json

class ConfigLoader:
    """Данный класс реализован с использованием паттерна Singleton"""
    _instance = None
    _is_loaded = False

    def __new__(cls, file_path=None):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance.file_path = file_path
        return cls._instance

    def load_config(self):
        """
        Загружает конфигурацию из JSON файла, если она еще не была загружена.
        Вызывается лениво при первом обращении к конфигурации.
        """
        if not self._is_loaded and self.file_path:
            try:
                with open(self.file_path, 'r', encoding="UTF-8") as file:
                    self.config = json.load(file)
                    self.validate_config()  # Валидация конфигурации после загрузки
                self._is_loaded = True
            except FileNotFoundError:
                raise Exception(f"Конфигурационный файл {self.file_path} не найден.")
            except json.JSONDecodeError:
                raise Exception(f"Ошибка при разборе JSON из файла {self.file_path}.")

    def validate_config(self):
        """
        Проверяет, что конфигурация содержит все необходимые ключи.
        Можно расширить валидацию по необходимости.
        """
        if not isinstance(self.config, dict):
            raise ValueError("Конфигурация должна быть словарем.")

    @property
    def get_config(self):
        """
        Возвращает загруженную конфигурацию. Выполняет ленивую загрузку при необходимости.
        """
        if not self._is_loaded:
            self.load_config()
        return self.config
