from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.middlewares.communication_middleware import StudentCheckMiddleware
from utils.message_forward import ChatSender

router = Router()
router.message.middleware(StudentCheckMiddleware())


class Form(StatesGroup):
    text = State()


@router.message(Command("suggest", "ask", "message"))
async def cmd_message(message: Message, state: FSMContext):
    """
    Обработчик команд /suggest, /ask, /message.

    Сохраняет текущую команду в состояние и переводит FSM
    в режим ожидания текста сообщения.
    """
    await state.set_state(Form.text)
    # Сохранение текста команды без "/"
    await state.update_data(command=message.text[1:])
    await message.answer(
        "Будь ласка, введіть текст повідомлення.\nПримітка: введіть текст одним повідомленням."
    )


@router.message(Form.text)
async def message_text_handler(message: Message, state: FSMContext, bot):
    """
    Обработчик текстового сообщения от пользователя, после ввода команды.

    Извлекает команду из состояния, отправляет сообщение в соответствующий форум
    и завершает диалог.
    """

    data = await state.get_data()
    command = data.get("command")

    sender = ChatSender(bot)

    await sender.send_message_to_chat(command, message.from_user, message)

    await message.answer("Повідомлення відправлено. Дякуємо за вашу активність!")

    await state.clear()
