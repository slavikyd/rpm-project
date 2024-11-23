import asyncio
from typing import Any

import msgpack
from aio_pika import Queue
from aio_pika.exceptions import QueueEmpty
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F

from config.settings import settings

from .router import router
from ..states.recommend import DateGroup
from ...storage.rabbit import channel_pool


@router.message(F.text == '/find')
async def start_dating(message: Message, state: FSMContext) -> None:
    await message.answer('Началась подборка')
    await state.set_state(DateGroup.dating)

    async with channel_pool.acquire() as channel:
        queue: Queue = await channel.declare_queue(
            settings.USER_RECOMMENDATIONS_QUEUE_TEMPLATE.format(user_id=message.from_user.id),
            durable=True,
        )

        # 'name': recommend.name,
        # 'age': recommend.age,
        # 'description': recommend.description,

        retries = 3
        for _ in range(retries):
            try:
                recommend = await queue.get()
                parsed_recommend: dict[str, Any] = msgpack.unpackb(recommend.body)

                inline_btn_1 = InlineKeyboardButton(text='Следующий человек', callback_data='next_recommend')
                markup = InlineKeyboardMarkup(
                    inline_keyboard=[[inline_btn_1]]
                )

                await message.answer(
                    text=f"{parsed_recommend['name']}\n{parsed_recommend['age']}\n{parsed_recommend['description']}",
                    reply_markup=markup,
                )
                return
            except QueueEmpty:
                await asyncio.sleep(1)

        await message.answer('Нет рекомендаций')
