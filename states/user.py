from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateLead(StatesGroup):
    enter_age = State()
    enter_days = State()
    enter_time = State()
    enter_days_count = State()