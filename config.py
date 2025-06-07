import os

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, path="data/config.yaml", encoding="utf-8"):
        with open(path, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.bot_token = os.getenv("TOKEN")

        self.chat_id = self.cfg["chat_data"]["chat_id"]
        self.chat_threads_id = self.cfg["chat_data"]["treads_id"]

        self.admin_ids = self.cfg["admins"]

        self.db_path = self.cfg["db_path"]

        self.class_data = self.load_class_list("data/class_list.yaml")
        self.class_presidents_data = self.load_class_presidents_list(
            "data/class_presidents_list.yaml"
        )

    def load_class_list(self, path: str) -> dict:
        """
        Загружает словарь с классами та буквами классов.
        :param path: путь к YAML файлу с классами та буквами
        :return: словарь доступных букв классов
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_class_presidents_list(self, path: str) -> dict:
        """
        Загружает словарь со старостами та их классами.
        :param path: путь к YAML файлу с классами та буквами
        :return: словарь старост классов
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


config = Config()
