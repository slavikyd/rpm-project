from consumer.schema.form import FormMessage


async def handle_event_form(message: FormMessage):
    if message['action'] == 'send_form':
        # TODO: отправить данные из сооющения в БД
        print(message)
