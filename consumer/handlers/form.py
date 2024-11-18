import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy import select, func

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

            not_fetched = await db.execute(select(User).order_by(func.random()))
            tuple_rows = not_fetched.all()
            users = [row for row, in tuple_rows]

            async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
                exchange = await channel.declare_exchange("users", ExchangeType.TOPIC, durable=True)

                for user in users:
                    await exchange.publish(
                        aio_pika.Message(
                            msgpack.packb({
                                'name': user.name,
                                'age': user.age,
                                'gender': user.gender,
                                'description': user.description,
                                'filter_by_age': user.filter_by_age,
                                'filter_by_gender': user.filter_by_gender,
                                'filter_by_description': user.filter_by_description,
                            }),
                        ),
                        routing_key=settings.USER_RECOMMENDATIONS_QUEUE_TEMPLATE.format(user_id=message['user_id']),
                    )
        print(message)
