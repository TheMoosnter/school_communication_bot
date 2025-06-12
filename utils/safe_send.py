from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError


class SafeSender:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(self, message, send_to: int, text: str, **kwargs):
        try:
            await self.bot.send_message(send_to, text, **kwargs)
        except TelegramForbiddenError:
            await message.answer("Не вдалося відправити повідомлення користувачу: користувач заблокував бота")
        except Exception as e:
            await message.answer(f"Не вдалося відправити повідомлення.\n{e}")

    async def send_message_with_reply(self, message, send_to: int, text: str, **kwargs):
        try:
            await self.bot.send_message(send_to, text, **kwargs)
            await message.answer("Повідомлення було відправлено.")
        except TelegramForbiddenError:
            await message.answer("Не вдалося відправити повідомлення.")
        except TelegramBadRequest as e:
            # message to be replied not found
            if "message to be replied not found" in str(e):
                filtered_kwargs = kwargs.copy()
                filtered_kwargs.pop("reply_to_message_id")
                await self.send_message(
                    message=message,
                    send_to=send_to,
                    text=text,
                    **filtered_kwargs
                )
            else:
                await message.answer(f"Не вдалося відправити повідомлення.\n{e}")