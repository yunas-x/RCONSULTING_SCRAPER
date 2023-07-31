import json
from typing import List
import os
from datetime import datetime

from settings.settings import settings

class Utils():
    """Вспомогательный класс
    """
    
    @staticmethod
    def log_error(content: str):
        """Сохраняет логи в файл, указанную в настройках

        Args:
            content (str): лог
        """
        
        with open(Utils.get_path(settings.ERROR), 'a+', encoding="utf-8") as f:
            f.write(content + "\n")

    @staticmethod
    def load_settings():
        """Устанавливает настройки из файла settings.json
        """
        
        with open('settings.json') as json_file:
            data = json.load(json_file)
            settings.EXCEL_FILE_NAME = data["EXCEL_FILE_NAME"]
            settings.URL = data["URL"]
            settings.ERROR = data["ERROR"]
            Utils.check_directory()
    
    @staticmethod
    def check_directory():
        """Подготавливает директорию для работы
        Если создать невозможно, то создает стандартную, используя системное время
        """

        settings.DIRECTORY = f"{os.getcwd()}\{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        os.makedirs(settings.DIRECTORY)
        
    @staticmethod
    def get_errors() -> List[str]:
        """Возвращает список строк из файла с ошибками

        Returns:
            List[str]: строки из файла с ошибками
        """
        
        links: List[str] = []
        try:
            with open(Utils.get_path(settings.ERROR), 'r', encoding="utf-8") as f:
                links = f.readlines()
        except:
            print("no file")
        return links

    @staticmethod
    def get_path(filename: str) -> str:
        """Конкатенирует имя файла со стандартной директорией из настроек

        Args:
            filename (str): название файла (с расширением)

        Returns:
            str: полный путь до файла
        """
        
        return f"{settings.DIRECTORY}/{filename}"