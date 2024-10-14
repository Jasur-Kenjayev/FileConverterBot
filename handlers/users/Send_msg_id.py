from loader import dp, bot
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from aiogram import types
from states.send_id import idsendi
from keyboards.inline.idsendb import confirmation_keyboard, post_callback
from keyboards.default.adminKeyboard import panel, bekorid
from aiogram.types import Message, CallbackQuery


@dp.message_handler(text="Orqaga❎", state=idsendi, user_id=ADMINS)
async def enterid(message:
types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🤖Orqaga Muvafaqiyatli qaytdingiz✅</b>", reply_markup=panel)


# send message user
@dp.message_handler(text="✏️ SEND MSG ID", user_id=ADMINS)
async def create_postid(message: Message):
    await message.answer("<b>👤 foydalanuvchi id ni kiriting👇</b>", reply_markup=bekorid)
    await idsendi.idsend.set()


@dp.message_handler(state=idsendi.idsend)
async def enter_messageid(message: Message, state: FSMContext):
    idsend = message.text
    await state.update_data(
        {"idsend": idsend}
    )
    await message.answer("<b>✏️ Yubormoqchi bo'lgan habaringizni kiriting!</b>", reply_markup=bekorid)
    await idsendi.next()


@dp.message_handler(state=idsendi.idmsg)
async def idmsgi(message: types.Message, state: FSMContext):
    idmsg = message.text
    await state.update_data(
        {"idmsg": idmsg}
    )
    data = await state.get_data()
    idmsg = data.get("idmsg")
    msg = f"<b>{idmsg}</b>"
    await idsendi.next()
    await message.answer(msg, reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="post"), state=idsendi.idConfirm)
async def confirm_postid(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        idsend = data.get("idsend")
        idmsg = data.get("idmsg")
        msgi = f"<b>{idmsg}</b>"
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>Xabaringiz yuborildi✅</b>", reply_markup=panel)
    await bot.send_message(idsend, msgi, parse_mode="HTML")


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=idsendi.idConfirm)
async def cancel_postid(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>Malumotlaringiz rad etildi 🛑</b>", reply_markup=panel)
@dp.message_handler(state=idsendi.idConfirm)
async def enter_finshitid(message: Message, state: FSMContext):
    await message.answer(
        "<b>👆👆👆Quyidagi Kiritgan Malumotlaringizni\n✅Tasdiqlang Yoki ❌Rad eting Bo'lmasa Botagi boshqa tugmalar ishlamaydi🔐</b>")