import yaml
import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, path='data/config.yaml', encoding="utf-8"):
        with open(path, 'r') as f:
            self.cfg = yaml.safe_load(f)

        self.bot_token = os.getenv("TOKEN")

        self.chat_id = self.cfg['chat_data']['chat_id']
        self.chat_threads_id = self.cfg['chat_data']['treads_id']

        self.admin_ids = self.cfg['admins']

        self.db_path = self.cfg['db_path']

        self.class_data = self._load_class_list("data/class_list.yaml")

    def _load_class_list(self, path: str) -> dict:
        """
        Загружает словарь с классами та буквами классов.
        :param path: путь к YAML файлу с классами та буквами
        :return: словарь доступных букв классов
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

config = Config()