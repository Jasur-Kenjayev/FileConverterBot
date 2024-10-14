from aiogram.dispatcher.filters.state import StatesGroup, State


class Balans(StatesGroup):
    balanstet = State()
    obalans = State()
    baConfirm = State()