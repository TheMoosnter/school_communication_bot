from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types.message import Message

from config import config


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id not in config.admin_ids:
            await event.answer("У вас немає дозволу використовувати цю команду.")
            return
        result = await handler(event, data)
        return result
