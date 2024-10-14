from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "<b>🤖 Ushbu Bot 200+ dan ortiq fayllarni qo'llab-quvvatlaydi:</b>\n\n<i>📇 Bot orqali document fayllarni va boshqa turdagi fayllarni 200+ dan ortiq formatga konvertatsiya qilishingiz mumkin!</i>\n\n<b>🔄 Konvertatsiya qulish uchun yuborishingiz mumkin bo'lga fayllar formati ⬇️</b>\n<i>pdf, docx, pptx, xlsx, xls, doc, dwg, epub, mobi, ai, ico, csv, html, svg, tiff, tiff-fax, ocr, txt, rasterize, repair, rotate, split, squeeze, numbers, bmp, dotx, log, pages, potx, vsd +++</i>\n\n<b>✅ @fileconverteribot</b>"
    await message.answer(text)