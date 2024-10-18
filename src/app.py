import asyncio
import uvicorn

from fastapi import FastAPI
from logger import logger


def create_app() -> FastAPI:
    app = FastAPI()
    return app


async def start_pooling() -> None:
    logger.info('Starting pooling..')
    await asyncio.sleep(100)


if __name__ == '__main__':
    # uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    asyncio.run(start_pooling())
