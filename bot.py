import asyncio
from loguru import logger

from aiogram import Bot, Dispatcher

from config import config
from app import admin, communication

bot = Bot(token=config.bot_token)
dp = Dispatcher()


async def main():
    dp.include_routers(communication.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Бота запущено")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бота вимкнуто")