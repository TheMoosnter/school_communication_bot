import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.middlewares.admin_middleware import AdminCheckMiddleware
from db.crud import StudentsDB
from utils.safe_send import SafeSender

router = Router()
router.message.middleware(AdminCheckMiddleware())
stud_db = StudentsDB()

class GetFullName(StatesGroup):
    waiting_for_full_name = State()


@router.message(F.reply_to_message, ~F.text.startswith("/"))
async def get_mes_data(message: Message, bot):
    if not message.reply_to_message:
        await message.answer("Ви не відповідаєте на повідомлення. Спробуйте ще раз.")

    original = message.reply_to_message.text

    author_id_str = re.search(r"\[user_id:(\d+)\]", original or "")
    message_id_str = re.search(r"\[message_id:(\d+)\]", original or "")
    if not author_id_str:
        await message.answer("Невідомий ID автора повідомлення.")
        return
    if not message_id_str:
        await message.answer("Невідомий ID повідомлення повідомлення.")
        return

    author_id = int(author_id_str.group(1))
    message_id = int(message_id_str.group(1))
    sf = SafeSender(bot)
    await sf.send_message_with_reply(
        message=message,
        send_to=author_id,
        text=f"Відповідь від адміністрації:\n\n{message.text}",
        reply_to_message_id=message_id
    )


@router.message(Command("get_info"))
async def cmd_get_info(message: Message, bot, state: FSMContext):
    """
    Обработчик команды /get_info.

    Переводит FSM в режим ожидания полного имени ученика.
    """
    await state.set_state(GetFullName.waiting_for_full_name)
    await message.answer("Введіть повне ім'я учня")

@router.message(GetFullName.waiting_for_full_name)
async def cmd_get_info_get_surname(message: Message, bot, state: FSMContext):
    """
    Получает имя и фамилию ученика и с помощью айди телеграмм аккаунта выводит
    информацию об ученике.
    """
    data = message.text

    try:
        name, surname = data.split()
    except ValueError:
        await message.answer("Ви ввели некоректне значення.")
        return

    stud_id = stud_db.get_id_by_full_name(name, surname)
    if not stud_id:
        await message.answer("Такого учня не існує в базі даних.")
    else:
        text = f"Інформація про учня {name} {surname}:"
        for i in range(len(stud_id)):
            text += f"\nКласс: {stud_db.get_class_number(stud_id[i][0])}-{stud_db.get_class_letter(stud_id[i][0])}\nНік в телеграм: @{stud_db.get_username(stud_id[i][0])}\n"
        await message.answer(text)

    await state.clear()
