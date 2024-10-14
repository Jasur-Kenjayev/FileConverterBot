from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="♻️ File Convert"),
        ],
        [
            KeyboardButton(text="👤 Kabinet"),
            KeyboardButton(text="🎁 Bonus"),
        ],
        [
            KeyboardButton(text="〽️ Statistika"),
            KeyboardButton(text="✏️ Yordam"),
        ],
    ],
    resize_keyboard=True
)
nazat = ReplyKeyboardMarkup(
    keyboard = [
         [
         KeyboardButton(text="◀️ Orqaga"),
         ],
       ],
       resize_keyboard=True
)

Chek = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Orqaga ➡️")
        ],
    ],
    resize_keyboard=True,
)