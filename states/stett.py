from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonalData(StatesGroup):
	adss = State()