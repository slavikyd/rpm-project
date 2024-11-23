import msgpack
from consumer.handlers.form import handle_event_form, handle_recommend_query
from consumer.schema.form import FormMessage, RecommendMessage
from consumer.storage.rabbit import channel_pool


async def main() -> None:
    queue_name = 'user_messages'
    async with channel_pool.acquire() as channel:
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    # TODO: сделать python switch case
                    body: FormMessage = msgpack.unpackb(message.body)
                    if body['event'] == 'user_form':
                        await handle_event_form(body)
                    if body['event'] == 'recommendations':
                        await handle_recommend_query(body)