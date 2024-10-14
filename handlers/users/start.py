import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu import Menu
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.types import ParseMode


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    id = message.from_user.id
    try:
        balansi = open(f"balans/balans{id}.txt", "r")
        balansi.close()
        await message.answer(f"*👋 Xush kelibsiz,* {message.from_user.full_name}\n\n*🗂 File Converter - barcha turdagi fayllarni bir formatdan boshqa formatga tez va oson o'tqazing*\n\n🤖 Ushbu bot orqali document fayllarni va boshqa turdagi fayllarni 200+ dan ortiq formatga konvertatsiya qilishingiz mumkin!\n\n*⬇️ Marhamat kerakli menyuni tanlang ⬇️*",parse_mode=ParseMode.MARKDOWN,reply_markup=Menu)
    except:
        balans = open(f"balans/balans{id}.txt", "w")
        baci = ('2')
        balans.write(baci)
        balans.close()
        await message.answer(f"*👋 Xush kelibsiz,* {message.from_user.full_name}\n\n*🗂 File Converter - barcha turdagi fayllarni bir formatdan boshqa formatga tez va oson o'tqazing*\n\n🤖 Ushbu bot orqali document fayllarni va boshqa turdagi fayllarni 200+ dan ortiq formatga konvertatsiya qilishingiz mumkin!\n\n*⬇️ Marhamat kerakli menyuni tanlang ⬇️*",parse_mode=ParseMode.MARKDOWN,reply_markup=Menu)
        await message.answer("<b>🎉 Tabriklayman hisobingizga 2 Coin 💎 qo'shildi ✅</b>")

    name = message.from_user.full_name

    try:
        db.add_user(id=message.from_user.id,name=name)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)

    count = db.count_users()[0]
    msg = f"*{message.from_user.full_name} 💡Bazaga Yangi 👤Foydalanuvchi ➕Qo'shildi. Bazada {count} ta Foydalanuvchi Bor✅*"
    await bot.send_message(chat_id=ADMINS[0], text=msg, parse_mode=ParseMode.MARKDOWN)