import asyncio
import os
import time
import hashlib
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import convertapi
from states.Convers import PersonalData2
from keyboards.default.menu import nazat, Menu
from keyboards.inline.keyboards import SUPPORTED_CONVERSIONS
from loader import dp, bot
from handlers.users.api import api_keys

CONVERTAPI_SECRET = api_keys()
convertapi.api_secret = CONVERTAPI_SECRET


def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()[:16]


file_mapping = {}


@dp.message_handler(text="◀️ Orqaga", state=PersonalData2)
async def state_fini(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("🏠", reply_markup=Menu)


@dp.message_handler(text="♻️ File Convert")
async def runi(message: Message):
    id = message.from_user.id
    user_stat_path = f"user_stat/user{id}.txt"
    balans_path = f"balans/balans{id}.txt"

    if not os.path.exists(user_stat_path):
        with open(user_stat_path, "w") as user:
            user.write('0')

    with open(balans_path, "r") as balans:
        hisobi = int(balans.read())

    if hisobi >= 1:
        await message.answer("<b>📥 Konvertatsiya qilish uchun botga fayl yuboring 👇</b>", reply_markup=nazat)
        await PersonalData2.conv.set()
    else:
        await message.answer("<b>👤 Hisobingizda Coin 💎 yetarli emas iltimos hisobingizni to'ldiring ✅</b>")


@dp.message_handler(content_types=['document'], state=PersonalData2.conv)
async def handle_document(message: Message):
    try:
        document = message.document
        file_id = document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        filename = document.file_name
        extension = filename.split('.')[-1]
        total_size = document.file_size

        progress_message = await message.answer("📥 Downloading in progress\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 0%")

        downloaded_file = await bot.download_file(file_path)

        downloaded_size = 0
        chunk_size = 4096
        prev_progress = -1  # Initialize with a value that is not a valid progress percentage

        with open(filename, "wb") as f:
            while True:
                chunk = downloaded_file.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded_size += len(chunk)
                progress = int((downloaded_size / total_size) * 10)
                progress_message_text = f"📥 Downloading in progress\n" + "🟩" * progress + "⬜" * (
                            10 - progress) + f" {progress * 10}%"
                # Update the message only if the progress changes
                if progress != prev_progress:
                    await progress_message.edit_text(progress_message_text)
                    prev_progress = progress

        file_hash = generate_hash(file_id)
        file_mapping[file_hash] = filename

        supported_formats = SUPPORTED_CONVERSIONS.get(extension, [])
        keyboard = InlineKeyboardMarkup(row_width=3)
        for fmt in supported_formats:
            if fmt != extension:
                callback_data = f'{file_hash}_{fmt}'
                keyboard.insert(InlineKeyboardButton(fmt.upper(), callback_data=callback_data))

        if supported_formats:
            await progress_message.edit_text(f"<b>🔄 Faylni qaysi formatga konvertatsiya qilishni xohlaysiz ❔</b>",
                                             reply_markup=keyboard)
            await PersonalData2.cone.set()
        else:
            await progress_message.edit_text("<b>📂 Ushbu fayl uchun qo'llab-quvvatlanadigan formatlar topilmadi ❗️</b>")
    except Exception as e:
        await message.answer(f"<b>📙 fayl hajmi judda katta iltimos kichikroq fayl yuboring !!!</b>")
        print(f"Error: {e}")


async def update_conversion_progress(conversion_message, start_time, duration=10):
    while True:
        elapsed_time = time.time() - start_time
        progress = min(int((elapsed_time / duration) * 10), 10)
        progress_message_text = "<i>🔄 Konvertatsiya qilinmoqda. iltimos kuting...</i>\n" + "🟩" * progress + "⬜" * (
                    10 - progress) + f" {progress * 10}%"
        try:
            await conversion_message.edit_text(
                f"<b>🔰 Status: Conversion\n⏳ Elapsed time: {elapsed_time:.2f} seconds</b>\n\n{progress_message_text}")
        except Exception as e:
            print(f"Failed to update message: {e}")
            break
        await asyncio.sleep(1)
        if progress == 10:
            break


@dp.callback_query_handler(lambda c: len(c.data.split('_')) == 2, state=PersonalData2.cone)
async def process_callback_convert(callback_query: CallbackQuery, state: FSMContext):
    file_hash, fmt = callback_query.data.split('_')
    filename = file_mapping.get(file_hash)
    if not filename:
        await callback_query.answer("Fayl topilmadi!")
        return

    start_time = time.time()
    conversion_message = await bot.send_message(
        callback_query.from_user.id,
        f"🔄 Conversion in progress\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%\nElapsed time: 0.00 seconds"
    )
    update_task = asyncio.create_task(update_conversion_progress(conversion_message, start_time))

    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, convertapi.convert, fmt, {'File': filename})
        converted_file_name = f"{callback_query.from_user.id}.{fmt}"
        await loop.run_in_executor(None, result.file.save, converted_file_name)
        converted_file = InputFile(converted_file_name)

        await bot.send_document(callback_query.from_user.id, converted_file, caption="✅ @fileconverteribot",
                                reply_markup=Menu)

        # Update balance and user stats
        await update_user_stats(callback_query.from_user.id)

        # Temporary files cleanup
        os.remove(filename)
        os.remove(converted_file_name)
        del file_mapping[file_hash]

    except convertapi.exceptions.ApiError:
        await bot.send_message(callback_query.from_user.id,
                               f"<b>🛠 Ushbu xizmatda texnik ishlar olib borilmoqda iltimos keyinroq urinib ko'ring!!!</b>",
                               reply_markup=Menu)

    finally:
        update_task.cancel()

    conversion_time = time.time() - start_time
    await conversion_message.edit_text(f"<i>✅ Conversion complete\nTime taken: {conversion_time:.2f} seconds...</i>")
    await state.finish()


async def update_user_stats(user_id):
    # Update balance
    balans_path = f"balans/balans{user_id}.txt"
    with open(balans_path, "r") as balans:
        hisobi = int(balans.read())
    hisobi -= 1
    with open(balans_path, "w") as balans:
        balans.write(str(hisobi))

    # Update user stats
    user_stat_path = f"user_stat/user{user_id}.txt"
    with open(user_stat_path, "r") as user:
        user_count = int(user.read())
    user_count += 1
    with open(user_stat_path, "w") as user:
        user.write(str(user_count))

    # Update conversion stats
    con_stats_path = "conversions_stats/convert_stats.txt"
    with open(con_stats_path, "r") as con_stats:
        con_count = int(con_stats.read())
    con_count += 1
    with open(con_stats_path, "w") as con_stats:
        con_stats.write(str(con_count))

@dp.message_handler(
    content_types=['text', 'photo', 'video', 'audio', 'sticker', 'voice', 'story', 'contact', 'game', 'poll',
                   'location'], state=PersonalData2.conv)
async def handle_non_document(message: Message, state: FSMContext):
    await message.reply("<b>🚫 botga faqat fayl yuborish mumkin to'liq ma'lumot /help ✅</b>", reply_markup=Menu)
    await state.finish()
