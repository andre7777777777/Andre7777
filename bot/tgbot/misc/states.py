from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    mailing_message = State()
