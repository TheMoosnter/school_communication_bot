from aiogram import Bot
from config import config

class ChatSender:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.chat_id = config.chat_id
        self.chat_id = config.chat_id

    async def send_message_to_chat(self, forum_type: str, user, text: str):
        """
        Отправляет сообщения в администраторский чат в ветку, которая была передана.

        :param forum_type: Тип ветки, куда сообщение пересылается
        :param user: Информация об авторе сообщения
        :param text: Текст сообщения
        """
        thread_id = config.chat_threads_id.get(f"{forum_type}_thread_id")

        hidden_id = f"[user_id:{user.id}]"
        user_link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
        message = f'Повідомлення від учня {user_link}: \n\n{text}\n\n{hidden_id}'
        await self.bot.send_message(text=message, chat_id=self.chat_id, message_thread_id=thread_id, parse_mode="HTML")