import aio_pika
import msgpack
import logging
from consumer.schema.form import FormMessage, RecommendMessage
from consumer.storage.rabbit import channel_pool
from aio_pika import ExchangeType
from config.settings import settings


async def handle_event_form(message: FormMessage):
    if message['action'] == 'send_form':
        # TODO: отправить данные из сооющения в БД
        print(f'USER DATA MESSAGE \n type: {type(message)} \n data: {message}')

async def handle_recommend_query(message: RecommendMessage):
    logging.info('Recommendations query is called!')
    if message['action'] == 'get_recommends':
        # TODO: подключение к chromadb
        # async with async_session() as db:
        # TODO: получение id рекомендованных пользователей 
        recommendations = [
            {
                'name': 'vadim',
                'age': '99',
                'description': 'дедуля',
            },
            {
                'name': 'egor',
                'age': '18',
                'description': 'szheg mersedes',
            },
            {
                'name': 'slavik',
                'age': '18',
                'description': 'seks paren',
            },
        ]
        
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange("user_recommendations", ExchangeType.DIRECT, durable=True)

            for recommendation in recommendations:
                await exchange.publish(
                    aio_pika.Message(
                        msgpack.packb(recommendation),
                    ),
                    routing_key=settings.USER_RECOMMENDATIONS_QUEUE_TEMPLATE.format(user_id=message['user_id']),
                )
