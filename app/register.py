from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.send_message import SendMessage

from app.middlewares import AdminCheckMiddleware
from config import config
from db.crud import *

class RegisterStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_class_number = State()
    waiting_for_class_letter = State()

router = Router()

@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    """
    Обработчик команды register. Регистрация ученика в базе данных для дальнейшей верификации старостой класса.
    :param message:
    :param state:
    :return:
    """
    if is_student_in_db(message.chat.id):
        await message.answer("Ваш акаунт вже зареєстрований. У випадку, якщо ви не проходили реєстрацію, зверніться до старости класу.")
        return

    await state.set_state(RegisterStates.waiting_for_name)
    await message.answer("Будь ласка, введіть ваше ім'я")

@router.message(RegisterStates.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip()) # strip - удаляет лишние символы из строки (по типу пробелов)
    await state.set_state(RegisterStates.waiting_for_surname)
    await message.answer("Будь ласка, введіть ваше прізвище")

@router.message(RegisterStates.waiting_for_surname)
async def get_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await state.set_state(RegisterStates.waiting_for_class_number)
    await message.answer("Будь ласка, введіть номер вашого класу")

@router.message(RegisterStates.waiting_for_class_number)
async def get_class_number(message: Message, state: FSMContext):
    class_number = message.text.strip()

    await state.set_state(RegisterStates.waiting_for_class_letter)

    letters = config.class_data.get(int(class_number))

    if not class_number:
        await message.answer("Некоректний номер класу. Спробуйте ще раз.")
        return

    await state.update_data(class_number=class_number)

    buttons = [
        [InlineKeyboardButton(text=letter, callback_data=f"letter:{letter}")]
        for letter in letters
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await state.set_state(RegisterStates.waiting_for_class_letter)
    await message.answer("Оберіть літеру вашого класу", reply_markup=markup)

@router.callback_query(RegisterStates.waiting_for_class_letter, F.data.startswith("letter:"))
async def get_class_letter(callback: CallbackQuery, state: FSMContext):
    letter = callback.data.split(":")[1]
    data = await state.get_data()

    add_students(
        tg_id=callback.from_user.id,
        first_name=data['name'],
        last_name=data['surname'],
        class_number=data['class_number'],
        class_letter=letter,
        is_registered=False
    )

    await callback.message.edit_text("Ваша заявка відправлена старості.")
    await state.clear()