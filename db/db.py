import sqlite3

from config import config


def get_connection():
    """
    Подключается к базе данных
    :return: подключение к базе данных
    """
    return sqlite3.connect(config.db_path)
