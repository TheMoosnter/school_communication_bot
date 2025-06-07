import re

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message

from app.middlewares.admin_middleware import AdminCheckMiddleware

router = Router()
router.message.middleware(AdminCheckMiddleware())


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

    try:
        await bot.send_message(
            author_id,
            f"Відповідь від адміністрації:\n\n{message.text}",
            reply_to_message_id=message_id,
        )
        await message.answer("Повідомлення було відправлено.")

    except TelegramForbiddenError:
        await message.answer("Не вдалося відправити повідомлення.")

    except TelegramBadRequest as e:
        # message to be replied not found
        if "message to be replied not found" in str(e):
            try:
                await bot.send_message(
                    author_id, f"Відповідь від адміністрації:\n\n{message.text}"
                )
                await message.answer("Повідомлення було відправлено.")
            except TelegramForbiddenError:
                await message.answer("Не вдалося відправити повідомлення.")
        else:
            await message.answer("Не вдалося відправити повідомлення.")
