import aio_pika
import msgpack
from config.settings import settings

from aiogram.types import Message

from consumer.schema.form import FormMessage
from consumer.schema.recommendation import RecMessage

from src.storage.rabbit import channel_pool


async def init_user_queue(message: Message, form: dict[str, str]) -> None:
    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange(
            'user_recommendations',
            aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

        queue = await channel.declare_queue(
            settings.USER_RECOMMENDATIONS_QUEUE_TEMPLATE.format(
                user_id=message.from_user.id,
            ),
            durable=True,
        )

        users_queue = await channel.declare_queue(
            'user_messages',
            durable=True,
        )

        await queue.bind(
            exchange,
            settings.USER_RECOMMENDATIONS_QUEUE_TEMPLATE.format(
                user_id=message.from_user.id,
            ),
        )

        await users_queue.bind(
            exchange,
            'user_messages',
        )

        await exchange.publish(
            aio_pika.Message(
                msgpack.packb(
                    FormMessage(
                        event='user_form',
                        action='send_form',
                        user_id=message.from_user.id,
                        **form,
                    ),
                ),
                # TODO: correlation_id
            ),
            'user_messages',
        )
        await exchange.publish(
            aio_pika.Message(
                msgpack.packb(
                    RecMessage(
                        event='user_recommendations',
                        action='get_recommendations',
                        user_id=message.from_user.id,
                    )
                )
            ),
            'user_messages',
        )
