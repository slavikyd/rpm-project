import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage

from config.settings import settings
from src.bot import setup_bot, setup_dp
from src.handlers.command.router import router as command_router
from src.storage.redis import setup_redis


async def start_pooling():
    logging.error('Starting polling')
    redis = setup_redis()
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)

    dp.include_router(command_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_pooling())
