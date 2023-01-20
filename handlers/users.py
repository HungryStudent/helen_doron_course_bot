from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from config import doc_id
from handlers import texts
from create_bot import dp
import keyboards.user as user_kb
from utils import db, crm
from states import user as states


@dp.message_handler(content_types="document")
async def func(message: Message):
    await message.answer(message.document.file_id)


@dp.message_handler(commands='start')
async def start_message(message: Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        phone = message.get_args()
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, phone)
    await message.answer(texts.hello_text)
    await message.answer(texts.enter_age)
    await states.CreateLead.enter_age.set()


@dp.message_handler(state=states.CreateLead.enter_age)
async def enter_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Введите реальный возраст!")
        return

    await state.update_data(age=age)
    days_data = [0] * 7
    await state.update_data(days_data=days_data)
    await message.answer(texts.enter_days, reply_markup=user_kb.days)
    await states.CreateLead.next()


@dp.callback_query_handler(user_kb.days_data.filter(), state=states.CreateLead.enter_days)
async def enter_days(call: CallbackQuery, state: FSMContext, callback_data: dict):
    weekday = int(callback_data["weekday"])
    is_include = int(callback_data["is_include"])
    async with state.proxy() as data:
        data["days_data"][weekday] = abs(is_include - 1)
        await call.message.edit_reply_markup(user_kb.get_days(data["days_data"]))


@dp.callback_query_handler(text="days_finish", state=states.CreateLead.enter_days)
async def days_finish(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 1 not in user_data["days_data"]:
        await call.answer("Выберите как минимум один день")
        return
    await call.message.answer(texts.enter_time)
    await states.CreateLead.next()
    await call.answer()


@dp.message_handler(state=states.CreateLead.enter_time)
async def enter_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)

    await message.answer(texts.enter_days_count, reply_markup=user_kb.days_count)
    await states.CreateLead.next()


@dp.callback_query_handler(state=states.CreateLead.enter_days_count)
async def enter_days_count(call: CallbackQuery, state: FSMContext):
    await state.update_data(days_count=call.data.split(":")[1])
    await call.answer()
    await call.message.answer(texts.finish)

    user_data = await state.get_data()
    await state.finish()
    user_data["phone"] = db.get_user(call.from_user.id)["phone"]
    await crm.create_lead(user_data)
    await call.message.answer_document(doc_id)
