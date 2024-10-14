from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Pays = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga")
        ],
    ],
    resize_keyboard=True,
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="↩️ Orqaga")
        ],
    ],
    resize_keyboard=True,
)