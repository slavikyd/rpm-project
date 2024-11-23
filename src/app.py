import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage

from config.settings import settings
from src.bot import setup_bot, setup_dp
from src.handlers.command.router import router as command_router
from src.handlers.message.router import router as message_router
from src.storage.redis import setup_redis


async def start_pooling():
    dp = Dispatcher()
    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)

    dp.include_router(command_router)
    dp.include_router(message_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_pooling())
