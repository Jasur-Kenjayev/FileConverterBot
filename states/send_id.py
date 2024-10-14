from aiogram.dispatcher.filters.state import StatesGroup, State


class idsendi(StatesGroup):
    idsend = State()
    idmsg = State()
    idConfirm = State()