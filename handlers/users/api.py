import asyncio
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import Menu
from aiogram import types
from keyboards.default.adminKeyboard import panel, conapi, conapiqaytish
from keyboards.inline.idsendb import confirmation_keyboard, post_callback
from data.config import ADMINS
from loader import dp, db, bot
import datetime
import pytz
from aiogram.types import ParseMode, Message
import requests
from states.apistet import ApiStet
from aiogram.types import Message, CallbackQuery


def api_keys():
    key_api = open(f"api/api_key.txt", "r")
    keys = str(key_api.read())
    return keys

@dp.message_handler(text= "◀️ PANEL",user_id=ADMINS)
async def panel_api(message:
	types.Message):
	await message.answer("<b>🔰bosh panelda siz ✅</b>",reply_markup=panel)

@dp.message_handler(text= "🔌 Convertapi",user_id=ADMINS)
async def api(message:
	types.Message):
	await message.answer("<b>🔰api bo'limidasiz ✅</b>",reply_markup=conapi)

@dp.message_handler(text= "ℹ️ API INFO",user_id=ADMINS)
async def api_info(message:
	types.Message):
    url = f'https://v2.convertapi.com/user?Secret={api_keys()}'
    r = requests.get(url).json()
    holat = (r['Active'])
    limit = (r['ConversionsTotal'])
    sarflangan = (r['ConversionsConsumed'])
    qoldi = limit - sarflangan
    if holat:
        await message.answer(f"<b>ℹ️ API HAQIDA MALUMOT\n\n🔰 api holati - ✅ \n🔋 limit - {limit} ta\n🪫 sarflandi - {sarflangan} ta\n✳️ qoldi - {qoldi} ta\n\n✅ @fileconverteribot</b>")
    else:
        await message.answer(f"<b>ℹ️ API HAQIDA MALUMOT\n\n🔰 api holati - 🚫 \n🔋 limit - {limit} ta\n🪫 sarflandi - {sarflangan} ta\n✳️ qoldi - {qoldi} ta\n\n✅ @fileconverteribot</b>")

@dp.message_handler(text="QAYTISH ➡️", state=ApiStet, user_id=ADMINS)
async def API_CANCEL(message:
types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🤖Orqaga Muvafaqiyatli qaytdingiz✅</b>", reply_markup=conapi)


# send message user
@dp.message_handler(text="➕ ADD API", user_id=ADMINS)
async def add_api(message: Message):
    await message.answer("<b>🔌 Yangi api ni kiriting 👇</b>", reply_markup=conapiqaytish)
    await ApiStet.apis1.set()


@dp.message_handler(state=ApiStet.apis1)
async def add_api2(message: types.Message, state: FSMContext):
    msgapi = message.text
    await state.update_data(
        {"msgapi": msgapi}
    )
    data = await state.get_data()
    msgapi = data.get("msgapi")
    await ApiStet.next()
    await message.answer(msgapi, reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="post"), state=ApiStet.apis2)
async def api_result(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msgapi = data.get("msgapi")
        result = str(msgapi)
        response = open(f"api/api_key.txt", "w")
        response.write(result)
        response.close()
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>🔌 API o'zgartirildi ✅</b>", reply_markup=conapi)

@dp.callback_query_handler(post_callback.filter(action="cancel"), state=ApiStet.apis2)
async def posts(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>Malumotlaringiz rad etildi 🛑</b>", reply_markup=conapi)

@dp.message_handler(state=ApiStet.apis2)
async def finishe(message: Message, state: FSMContext):
    await message.answer(
        "<b>👆👆👆Quyidagi Kiritgan Malumotlaringizni\n✅Tasdiqlang Yoki ❌Rad eting Bo'lmasa Botagi boshqa tugmalar ishlamaydi🔐</b>")