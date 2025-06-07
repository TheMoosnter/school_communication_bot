from aiogram import BaseMiddleware
from aiogram.types.message import Message
from typing import Callable, Dict, Any, Awaitable

from db.crud import is_user_in_db, is_student_in_db


class StudentCheckMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:

        if not is_user_in_db(event.from_user.id): # Если пользователя нет в базе данных, он не регистрировался
            await event.answer("Ви не зареєструвалися в боті.\nВикористайте команду /register для проходження реєстрації.")
            return
        elif not is_student_in_db(event.from_user.id): # Пользователь регистрировался, но заявка не подтверждена
            await event.answer("Ваша заявка не підтверджена.\nУ випадку довготривалого очікування проходження верифікації, зверніться до старости вашого класу.")
            return
        result = await handler(event, data)
        return result