from aiogram import types
from loader import dp, bot
from data.config import ADMINS
from keyboards.default.menu import Menu, Chek
from keyboards.inline.balansadd import Tolov
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from states.Cheke import Chekes

@dp.message_handler(text="Orqaga ➡️", state=Chekes)
async def finished(message:
types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🤖Orqaga Muvafaqiyatli qaytdingiz✅</b>", reply_markup=Menu)


@dp.callback_query_handler(text_contains="cheked")
async def chek(call: CallbackQuery):
    await call.message.answer("<b>🖼 Toʻlovingizni chek rasmini yuboring:</b>", reply_markup=Chek)
    await call.message.delete()
    await call.answer(cache_time=60)
    await Chekes.photos.set()

@dp.message_handler(state=Chekes.photos,content_types=types.ContentType.ANY)
async def Photo(message: Message,state: FSMContext):
    id = message.from_user.id
    name = message.from_user.full_name
    await bot.send_message(chat_id=ADMINS[0], text=f"<b>👤 Ismi:</b> {name}\n<b>🆔 ID:</b> <code>{id}</code>\n\n <b>👇 To'lov Cheki 👇</b>")
    await message.send_copy(chat_id=ADMINS[0])
    await state.finish()
    await message.answer("<b>✅ Toʻlov ma‘lumoti qabul qilindi.</b>\n\nToʻlov cheki 15-50 daqiqa ichida tekshiriladi.",reply_markup=Menu)
