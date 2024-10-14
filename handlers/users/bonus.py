import os
import json
from datetime import datetime, timedelta

from loader import dp, bot
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from aiogram import types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Define the inline button
inlinebutton = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="🎁 Bonus olish", callback_data="receive_bonus")
)

BONUS_INTERVAL = timedelta(hours=24)
USER_DATA_FILE = 'user_data.json'

# Ensure the balance directory exists
os.makedirs('balans', exist_ok=True)


# Helper functions to handle balance and user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)


def get_user_balance(user_id):
    balance_file = f'balans/balans{user_id}.txt'
    if os.path.exists(balance_file):
        with open(balance_file, 'r') as file:
            return int(file.read())
    return 0


def update_user_balance(user_id, amount):
    balance_file = f'balans/balans{user_id}.txt'
    balance = get_user_balance(user_id) + amount
    with open(balance_file, 'w') as file:
        file.write(str(balance))


@dp.message_handler(text="🎁 Bonus")
async def bonus(message: types.Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data()

    now = datetime.now()
    last_bonus_time = datetime.fromtimestamp(user_data.get(user_id, 0))

    if now - last_bonus_time >= BONUS_INTERVAL:
        await message.answer("<b>🎁 Bonus olish uchun pastdagi tugmani bosing 👇</b>", reply_markup=inlinebutton)
    else:
        remaining_time = BONUS_INTERVAL - (now - last_bonus_time)
        remaining_hours, remaining_minutes = divmod(remaining_time.seconds, 3600)
        remaining_minutes //= 60

        await message.answer(
            f"<b>⏳ Siz bonusni 24 soatda bir marta olishingiz mumkin. Yangi bonus olishga qolgan vaqt: {remaining_hours} soat {remaining_minutes} daqiqa.</b>"
        )


@dp.callback_query_handler(lambda c: c.data == "receive_bonus")
async def process_bonus(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    user_data = load_user_data()

    now = datetime.now()
    last_bonus_time = datetime.fromtimestamp(user_data.get(user_id, 0))

    if now - last_bonus_time >= BONUS_INTERVAL:
        # Update user's last bonus time
        user_data[user_id] = now.timestamp()
        save_user_data(user_data)

        # Update user balance
        update_user_balance(user_id, 2)

        # Delete the original message
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        # Send a new message informing the user of the bonus
        await bot.send_message(callback_query.message.chat.id, "<b>🎉 Sizga 2 Coin 💎 bonus berildi ✅</b>")
    else:
        remaining_time = BONUS_INTERVAL - (now - last_bonus_time)
        remaining_hours, remaining_minutes = divmod(remaining_time.seconds, 3600)
        remaining_minutes //= 60

        # Send a new message informing the user of the remaining time
        await bot.send_message(
            callback_query.message.chat.id,
            f"<b>⏳ Siz bonusni 24 soatda bir marta olishingiz mumkin. Yangi bonus olishga qolgan vaqt: {remaining_hours} soat {remaining_minutes} daqiqa.</b>"
        )

    # Acknowledge the callback
    await callback_query.answer()
