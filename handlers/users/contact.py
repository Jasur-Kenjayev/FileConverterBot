import requests
from aiogram.dispatcher import FSMContext
from aiogram import types

from data.config import ADMINS
from keyboards.default.pay import contact
from keyboards.default.menu import Menu
from states.contactStet import Contacts
from loader import dp, bot


@dp.message_handler(text="↩️ Orqaga", state=Contacts)
async def cancel_contact(message:
types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>📇 Bosh Menudasiz✅</b>", reply_markup=Menu)

@dp.message_handler(text="✏️ Yordam")
async def contacti(message:
types.Message):
    msg = "<b>✍️ Murojaatingizni kiriting Men uni administratorga yetkazaman.</b>\n\n➡️ Kiritishingiz mumkin:\nOvoz | Audio | Rasm | Text | Fayl"
    await message.answer(msg, reply_markup=contact)
    await Contacts.contact.set()


@dp.message_handler(state=Contacts.contact,content_types=types.ContentType.ANY)
async def msg_contact(message:
types.Message,state: FSMContext):
    id = message.from_user.id
    name = message.from_user.full_name
    await bot.send_message(chat_id=ADMINS[0], text=f"<b>👤 Ismi:</b> {name}\n<b>🆔 ID:</b> <code>{id}</code>\n\n <b>👇 Yuborgan Xabari 👇</b>")
    await message.send_copy(chat_id=ADMINS[0])
    await state.finish()
    await message.reply("<b>✅ Xabar yuborildi...</b>", reply_markup=Menu)