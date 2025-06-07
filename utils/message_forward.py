from aiogram import Bot
from config import config


class ChatSender:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.chat_id = config.chat_id

    async def send_message_to_chat(self, forum_type: str, user, mes):
        """
        Отправляет сообщения в администраторский чат в ветку, которая была передана.

        :param forum_type: Тип ветки, куда сообщение пересылается
        :param user: Информация об авторе сообщения
        :param mes: Информация о сообщении
        """
        thread_id = config.chat_threads_id.get(f"{forum_type}_thread_id")

        hidden_author_id = f"[user_id:{user.id}]"
        hidden_message_id = f"[message_id:{mes.message_id}]"
        user_link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
        message = f"Повідомлення від учня {user_link}: \n\n{mes.text}\n\n{hidden_author_id}\n{hidden_message_id}"
        await self.bot.send_message(
            text=message,
            chat_id=self.chat_id,
            message_thread_id=thread_id,
            parse_mode="HTML",
        )
