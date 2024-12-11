from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from io import BytesIO
from tempfile import NamedTemporaryFile


from src.handlers.buttons import SKIP_BUTTON_CALLBACK_MSG, SKIP_BUTTON_MSG
from src.handlers.states.auth import AuthForm, AuthGroup
from src.handlers.command.router import router

from src.utils import validators

from src.utils.recommendations import init_user_queue
from src.services.minio_service import upload_photo  

@router.callback_query(F.data == '/auth', AuthGroup.no_authorized)
async def auth(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AuthForm.photo)
    await callback.message.answer('*Загрузите фотографию для вашего профиля:')

@router.message(F.content_type == 'photo', AuthForm.photo)
async def process_photo(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    file_name = f"user_{message.from_user.username}.jpg"

    bot = message.bot

    
    try:
        file_info = await bot.get_file(photo.file_id)

        file_bytes = await bot.download_file(file_info.file_path)

        await upload_photo('main', file_name, file_bytes.getvalue())

        await state.update_data(photo=file_name)
        await state.set_state(AuthForm.name)
        await message.answer("Фото загружено. Введите имя.")
    except Exception as e:
        await message.answer(f"Ошибка загрузки фотографии: {e}")
        return


@router.message(AuthForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    valid_msg = validators.valid_username(message.text)
    if valid_msg:
        await message.answer(valid_msg)
        return

    await state.update_data(username=message)
    await state.set_state(AuthForm.age)
    await message.answer('Введите возраст')


@router.message(AuthForm.age)
async def process_age(message: Message, state: FSMContext) -> None:
    valid_msg = validators.valid_age(message.text)
    if valid_msg:
        await message.answer(valid_msg)
        return

    await state.update_data(age=message)
    await state.set_state(AuthForm.gender)
    masculine_button = InlineKeyboardButton(
        text='мужчина',
        callback_data='masculine',
    )
    feminine_button = InlineKeyboardButton(
        text='женщина',
        callback_data='feminine',
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[masculine_button, feminine_button]],
    )
    await message.answer(
        'Выберите ваш пол',
        reply_markup=markup,
    )


@router.callback_query(F.data.in_({'feminine', 'masculine'}), AuthForm.gender)
async def process_gender(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(gender=callback.data)
    await state.set_state(AuthForm.description)

    # TODO: поправить повторения кнопки 'skip'
    skip = InlineKeyboardButton(
        text=SKIP_BUTTON_MSG,
        callback_data=SKIP_BUTTON_CALLBACK_MSG,
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[skip]]
    )

    await callback.message.answer(
        '*Введите описание о себе',
        reply_markup=markup,
    )
    


@router.callback_query(F.data == SKIP_BUTTON_CALLBACK_MSG, AuthForm.description)
async def process_description_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await process_description(callback.message, state, isCallbackEvent=True)


@router.message(AuthForm.description)
async def process_description(message: Message, state: FSMContext, isCallbackEvent=False) -> None:
    if isCallbackEvent:
        await state.update_data(description=None)
    else:
        valid_msg = validators.valid_description(message.text)
        if valid_msg:
            await message.answer(valid_msg)
            return

        await state.update_data(description=message)

    await state.set_state(AuthForm.filter_by_age)

    skip = InlineKeyboardButton(
        text=SKIP_BUTTON_MSG,
        callback_data=SKIP_BUTTON_CALLBACK_MSG,
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[skip]])

    await message.answer(
        '*Укажите фильтр по возрасту (в формате: 18-36)',
        reply_markup=markup,
    )


@router.callback_query(F.data == SKIP_BUTTON_CALLBACK_MSG, AuthForm.filter_by_age)
async def process_filter_by_age_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await process_filter_by_age(callback.message, state, isCallbackEvent=True)


@router.message(AuthForm.filter_by_age)
async def process_filter_by_age(message: Message, state: FSMContext, isCallbackEvent=False) -> None:
    if isCallbackEvent:
        await state.update_data(filter_by_age=None)
    else:
        valid_msg = validators.valid_filter_by_age(message.text)
        if valid_msg:
            await message.answer(valid_msg)
            return

        await state.update_data(filter_by_age=message.text)

    await state.set_state(AuthForm.filter_by_gender)
    masculine_button = InlineKeyboardButton(
        text='мужчина',
        callback_data='masculine',
    )
    feminine_button = InlineKeyboardButton(
        text='женщина',
        callback_data='feminine',
    )
    no_preferences_button = InlineKeyboardButton(
        text='все',
        callback_data='all',
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[masculine_button, feminine_button, no_preferences_button]],
    )
    await message.answer(
        '*Выберите пол того, кого вы ищете',
        reply_markup=markup,
    )


@router.callback_query(
    F.data.in_({'feminine', 'masculine', 'all'}),
    AuthForm.filter_by_gender,
)
async def process_filter_by_gender(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(filter_by_gender=callback.data)
    await state.set_state(AuthForm.filter_by_description)

    skip = InlineKeyboardButton(
        text=SKIP_BUTTON_MSG,
        callback_data=SKIP_BUTTON_CALLBACK_MSG,
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[skip]])

    await callback.message.answer(
        'Укажите описание, кого вы хотите найти',
        reply_markup=markup
    )


@router.callback_query(F.data == SKIP_BUTTON_CALLBACK_MSG, AuthForm.filter_by_description)
async def process_filter_by_description_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await process_filter_by_description(callback.message, state, isCallbackEvent=True)


@router.message(AuthForm.filter_by_description)
async def process_filter_by_description(message: Message, state: FSMContext, isCallbackEvent=False) -> None:
    if isCallbackEvent:
        form = await state.update_data(filter_by_description=None)
    else:
        valid_msg = validators.valid_filter_by_age(message.text)
        if valid_msg:
            await message.answer(valid_msg)
            return

        form = await state.update_data(filter_by_description=message.text)

    form = {
        field: field_data.text
        if isinstance(field_data, Message) else field_data
        for field, field_data in form.items()
    }
    form['age'] = int(form['age'])

    await state.set_state(AuthGroup.authorized)

    # TODO: исправить имя функции и расположения файла (recommendations.py)
    await init_user_queue(message, form)
    await message.answer('Теперь вы авторизованы')
