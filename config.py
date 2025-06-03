import yaml
import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, path='data/config.yaml'):
        with open(path, 'r') as f:
            self.cfg = yaml.safe_load(f)

        self.bot_token = os.getenv("TOKEN")

        self.chat_id = self.cfg['chat_data']['chat_id']
        self.chat_threads_id = self.cfg['chat_data']['treads_id']

        self.admin_ids = self.cfg['admins']

config = Config()