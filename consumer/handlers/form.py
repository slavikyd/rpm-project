import aio_pika
import msgpack
# import logging
from aio_pika import ExchangeType
from sqlalchemy import select, func, insert

from config.settings import settings
from consumer.model.user import User
from consumer.schema.form import FormMessage
from consumer.storage.db import async_session
from consumer.storage.rabbit import channel_pool
from src.storage.db import * #TODO: убрать импорт всего

async def handle_event_form(message: FormMessage):
    if message['action'] == 'send_form':
        # TODO: отправить данные из сооющения в БД
        async with async_session() as db:
            # TODO: УБРАТЬ ЭТУ ДИЧЬ
            user_data = {
                'user_id': message.user_id,
                'name': message.name,
                'age': message.age,
                'gender': message.gender,
                'description': message.description,
                'filter_by_age': message.filter_by_age,
                'filter_by_gender': message.filter_by_gender,
                'filter_by_description': message.filter_by_description,
            }
            await db.execute(insert(User).values(**user_data))
            print(message)
        # logging.info(message)
