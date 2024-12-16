from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.handlers.command.router import router as command_router
from src.handlers.message.router import router as message_router

from config.settings import settings

dp = Dispatcher()
default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=settings.BOT_TOKEN, default=default)

dp.include_router(command_router)
dp.include_router(message_router)
