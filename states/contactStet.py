from aiogram.dispatcher.filters.state import StatesGroup, State


class Contacts(StatesGroup):
    contact = State()