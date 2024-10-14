from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

panel = ReplyKeyboardMarkup(
    keyboard = [
         [
         KeyboardButton(text="💸 ADD MONEY")
         ],
         [
         KeyboardButton(text="📨 SEND MSG"),
         KeyboardButton(text="👤 ALL USERS"),
         KeyboardButton(text="✏️ SEND MSG ID"),
         ],
         [
         KeyboardButton(text="〽️ Statistika"),
         KeyboardButton(text="🔌 Convertapi")
         ],
         [
         	KeyboardButton(text="🔚MENU🔜"),
         ],
       ],
       resize_keyboard=True
)

bekor = ReplyKeyboardMarkup(
    keyboard = [
        [
        	KeyboardButton(text="Orqaga🔜"),
        ],
     ],
     resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Orqaga ▶️"),
        ],
    ],
    resize_keyboard=True
)

bekorid = ReplyKeyboardMarkup(
    keyboard = [
        [
        	KeyboardButton(text="Orqaga❎"),
        ],
     ],
     resize_keyboard=True
)

conapi = ReplyKeyboardMarkup(
    keyboard = [
        [
        	KeyboardButton(text="ℹ️ API INFO"),
        	KeyboardButton(text="➕ ADD API"),
        ],
        [
            KeyboardButton(text="◀️ PANEL"),
        ]
     ],
     resize_keyboard=True
)

conapiqaytish = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="QAYTISH ➡️"),
        ]
     ],
     resize_keyboard=True
)