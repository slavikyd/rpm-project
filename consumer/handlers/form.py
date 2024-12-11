from sqlalchemy import insert

from postgres_db.model.user import User
from consumer.schema.form import FormMessage
from postgres_db.db import async_session


async def handle_event_form(message: FormMessage):
    if message['action'] == 'send_form':
        async with async_session() as db:
            # TODO: придумать более умную распаковку
            user_data = {
                'id': message['user_id'],
                'username': message['username'],
                'age': message['age'],
                'gender': message['gender'],
                'description': message['description'],
                'photo': message['photo'],
                'filter_by_age': message['filter_by_age'],
                'filter_by_gender': message['filter_by_gender'],
                'filter_by_description': message['filter_by_description'],
            }
            await db.execute(insert(User).values(**user_data))
            await db.commit()
