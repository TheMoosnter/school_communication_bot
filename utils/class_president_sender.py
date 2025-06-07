from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup

from config import config

class ClassPresidentSender:
    def __init__(self, bot):
        self.bot = bot
        self.classes_data = config.class_presidents_data

    async def send_reg_request_to_class_president(self, tg_id: int, tg_full_name: str, name: str, surname: str,
                                                  class_number: int, class_letter: str):
        """
        Отправляет заявку о регистрации ученика старосте класса, выбранного учеником
        :param tg_id: айди телеграмм-аккаунта
        :param tg_full_name: полное имя телеграмм-аккаунта
        :param name: имя ученика
        :param surname: фамилия ученика
        :param class_number: номер класса
        :param class_letter: буква класса
        """
        classes = self.classes_data[int(class_number)]
        class_president_id = classes.get(class_letter)

        request_author_text = f'<a href="tg://user?id={tg_id}">{tg_full_name}</a>'
        message_text = f"Користувач {request_author_text} хоче зареєструватися як {name} {surname}."

        buttons = [
            [InlineKeyboardButton(text='✅ Підтвердити', callback_data=f'approve:{tg_id}')],
            [InlineKeyboardButton(text='❌ Відхилити', callback_data=f'reject:{tg_id}')]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await self.bot.send_message(class_president_id, message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
