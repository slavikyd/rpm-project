import asyncio
import uvicorn
from aiogram import Dispatcher, Bot
from fastapi import FastAPI
from src.api.tg.router import router as tg_router
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from src.bot import BotManager
from config.settings import settings

background_tasks = set()


async def lifespan(app: FastAPI):
    dp = Dispatcher()
    bot = Bot(token=settings.BOT_TOKEN)
    bot_manager = BotManager()
    bot_manager.setup_bot(bot)
    bot_manager.setup_dispatcher(dp)

    webhook_data = await bot.get_webhook_info()
    await bot.set_webhook(webhook_data.url)

    yield

    while background_tasks:
        await asyncio.sleep(0)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/docs', lifespan=lifespan)
    app.include_router(tg_router, prefix='/tg', tags=['tg'])

    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app


if __name__ == '__main__':
    uvicorn.run(
        'src.app:create_app',
        factory=True,
        host='0.0.0.0',
        port=5783,
        workers=1,
        reload=True
    )
