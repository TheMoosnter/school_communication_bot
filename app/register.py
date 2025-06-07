from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import config
from db.crud import *
from utils.class_president_sender import ClassPresidentSender

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
    if is_user_in_db(message.chat.id):
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
    """
    Получает номер класса и отправляет сообщение с inline-клавиатурой с доступными
    буквами класса
    :param message:
    :param state:
    """
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
async def get_class_letter(callback: CallbackQuery, state: FSMContext, bot):
    """
    Получает выбранную букву из callback сообщения формата letter:А,
    добавляет аккаунт в базу данных, вызывает функцию отправки запроса о регистрации
    старосте выбранного класса
    :param callback:
    :param state:
    :param bot:
    """
    letter = callback.data.split(":")[1]
    data = await state.get_data()

    add_students(
        tg_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=data['name'],
        last_name=data['surname'],
        class_number=data['class_number'],
        class_letter=letter,
        is_registered=False
    )

    sender = ClassPresidentSender(bot)

    await sender.send_reg_request_to_class_president(
        tg_id=callback.from_user.id,
        tg_full_name=callback.from_user.full_name,
        name=data['name'],
        surname=data['surname'],
        class_number=data['class_number'],
        class_letter=letter
    )

    await callback.message.edit_text("Ваша заявка відправлена старості.")
    await state.clear()

@router.callback_query(F.data.startswith("approve:"))
async def approve_student(callback: CallbackQuery, bot: Bot):
    """
    Получает айди телеграмм-аккаунта, который прошёл верификацию старостой и завершает
    процесс регистрации.
    :param callback:
    :param bot:
    :return:
    """
    student_id = int(callback.data.split(":")[1])
    student_name = get_student_name(student_id) + " " + get_student_surname(student_id)

    register_student(tg_id=student_id)

    student_link = f'<a href="tg://user?id={student_id}">{student_name}</a>'
    await callback.message.edit_text(f"Заявка учня {student_link} була прийнята.", parse_mode=ParseMode.HTML)
    await bot.send_message(student_id, "Ви були зареєстровані.\nВведіть команду /start для отримання інформації щодо функціоналу боту.")

@router.callback_query(F.data.startswith("reject:"))
async def reject_student(callback: CallbackQuery, bot: Bot):
    """
    Получает айди телеграмм-аккаунта, который не прошёл верификацию старостой и
    удаляет его из базы данных.
    :param callback:
    :param bot:
    :return:
    """
    student_id = int(callback.data.split(":")[1])
    student_name = get_student_name(student_id) + " " + get_student_surname(student_id)

    remove_student(student_id)

    student_link = f'<a href="tg://user?id={student_id}">{student_name}</a>'
    await callback.message.edit_text(f"Заявка учня {student_link} була відхилена.", parse_mode=ParseMode.HTML)
    await bot.send_message(student_id, "Ваша заявка на реєстрацію була відхилена.")