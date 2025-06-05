import sqlite3
from config import config

def get_connection():
    return sqlite3.connect(config.db_path)