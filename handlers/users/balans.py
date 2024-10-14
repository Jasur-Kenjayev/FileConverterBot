from aiogram import types
from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.default.adminKeyboard import cancel, panel
from states.balans import Balans
from data.config import ADMINS
from keyboards.inline.idsendb import confirmation_keyboard, post_callback
from keyboards.inline.balansadd import Balansadd, Tolov
from keyboards.default.pay import Pays
from aiogram.types import ParseMode
from states.paystate import Payess
from keyboards.default.menu import Menu


@dp.message_handler(text="👤 Kabinet")
async def kabinet(message: Message):
    try:
        id = message.from_user.id
        balans = open(f"balans/balans{id}.txt", "r")
        user = open(f"user_stat/user{id}.txt", "r")
        await message.answer(
            f"🎉 Kabinetingizga xush kelibsiz!\n\n*👤 Ismingiz:* {message.from_user.full_name}\n*🔑 ID raqamingiz:* {id}\n*💳 Hisobingiz:* {balans.read()} Coin 💎\n*1️⃣ Ta konvertatsiya =* 1 Coin 💎\n\n*🔄 Konvertatsiyalaringiz:* {user.read()} ta",parse_mode=ParseMode.MARKDOWN,reply_markup=Balansadd)
        user.close()
        balans.close()

    except:
        users = open(f"user_stat/user{id}.txt", "w")
        count = ('0')
        users.write(count)
        users.close()

        balans = open(f"balans/balans{id}.txt", "r")
        user = open(f"user_stat/user{id}.txt", "r")
        await message.answer(
            f"🎉 Kabinetingizga xush kelibsiz!\n\n*👤 Ismingiz:* {message.from_user.full_name}\n*🔑 ID raqamingiz:* {id}\n*💳 Hisobingiz:* {balans.read()} Coin 💎\n*1️⃣ Ta konvertatsiya =* 1 Coin 💎\n\n*🔄 Konvertatsiyalaringiz:* {user.read()} ta",parse_mode=ParseMode.MARKDOWN,reply_markup=Balansadd)
        user.close()
        balans.close()



@dp.message_handler(text="Orqaga ▶️", state=Balans, user_id=ADMINS)
async def camcel(message:
types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🤖Orqaga Muvafaqiyatli qaytdingiz✅</b>", reply_markup=panel)


# send message user
@dp.message_handler(text="💸 ADD MONEY", user_id=ADMINS)
async def create_balans(message: Message):
    await message.answer("<b>👤 foydalanuvchi id ni kiriting👇</b>", reply_markup=cancel)
    await Balans.balanstet.set()


@dp.message_handler(state=Balans.balanstet)
async def enter_ball(message: Message, state: FSMContext):
    balansi = message.text
    await state.update_data(
        {"balansi": balansi}
    )
    balansu = open(f"balans/balans{balansi}.txt", "r")
    await message.answer(
        f"<b>👤 foydalanuvchi balansi {balansu.read()} Coin 💎\n\n✏️ Yubormoqchi bo'lgan miqdorni kiriting👇</b>",
        reply_markup=cancel)
    balansu.close()
    await Balans.next()


@dp.message_handler(state=Balans.obalans)
async def obalans(message: types.Message, state: FSMContext):
    oball = message.text
    await state.update_data(
        {"oball": oball}
    )
    data = await state.get_data()
    oball = data.get("oball")
    msg = f"<b>👤 foydalanuvchi balansiga {oball} Coin 💎 qo'shilsinmi?</b>"
    await Balans.next()
    await message.answer(msg, reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="post"), state=Balans.baConfirm)
async def confirm_postidb(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        balansi = data.get("balansi")
        oball = data.get("oball")
        balans = open(f"balans/balans{balansi}.txt", "w")
        balans.write(oball)
        balans.close()
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>💸Hisob To'ldirildi✅</b>", reply_markup=panel)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=Balans.baConfirm)
async def cancel_postidb(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("<b>Malumotlaringiz rad etildi 🛑</b>", reply_markup=panel)


@dp.message_handler(state=Balans.baConfirm)
async def enter_finshitidb(message: Message, state: FSMContext):
    await message.answer(
        "<b>👆👆👆Quyidagi Kiritgan Malumotlaringizni\n✅Tasdiqlang Yoki ❌Rad eting Bo'lmasa Botagi boshqa tugmalar ishlamaydi🔐</b>")

@dp.message_handler(text="⬅️ Orqaga",state=Payess)
async def state_end(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("🏠", reply_markup=Menu)

@dp.callback_query_handler(text_contains="hisobtoldrish")
async def payments(call: CallbackQuery):
    await call.message.answer("<b>🛍 Qancha Coin 💎 Sotib Olmoqchisiz? Miqdorini Sonda Kiriting 👇</b>",reply_markup=Pays)
    await call.message.delete()
    await call.answer(cache_time=60)
    await Payess.pay.set()

@dp.message_handler(state=Payess.pay)
async def paymetod(message: Message,state: FSMContext):
    id = message.from_user.id
    try:
        msg = message.text
        if int(msg) >= 10:
            await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
            result = int(msg) * 700
            await message.answer(f"<b>✅ {msg} Coin 💎 = {result} UZS</b>", reply_markup=Menu)
            await message.answer(f"<b>💸 To'lov summasi:</b> <code>{result}</code> UZS\n\n<b>💳 Xamyon:</b> <code>9860160131012595</code>\n<b>💬 Izoh:</b> <code>{id}</code>\n\n<b>🔰 Hisobni toʻldirish uchun quyidagilarni ketmaket bajaring.</b>\n\n1) To'lov summasini tepadagi 💳 Xamyon ga tashlang;\n2) «✅ Toʻlov qildim» tugmasini bosing;\n3) Toʻlov haqidagi suratni botga yuboring;\n4) Operator tomonidan to'lov tasdiqlanishini kuting.\n\n<b>⚠️ Toʻlovingiz 15-50 daqiqa ichida koʻrib chiqiladi</b>",reply_markup=Tolov)
            await state.finish()


        else:
            await message.answer(f"<b>🔼 Minlima 10 Coin 💎\n🔽 Maksimal ♾ Coin 💎</b>")
    except:
        await message.answer("<b>ℹ️ Butun son kiriting!!!</b>")