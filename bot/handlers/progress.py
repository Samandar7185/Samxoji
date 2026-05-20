from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
import asyncio

from bot.keyboards import main_menu_keyboard

router = Router()

@router.callback_query(F.data == "progress")
async def progress_demo(callback: CallbackQuery):
    msg = await callback.message.edit_text(
        "⏳ <b>Yuklanmoqda...</b>\n\n"
        "[██████████] 100%"
    )
    await asyncio.sleep(1)
    await msg.edit_text(
        "✅ <b>Yuklab olish tugadi!</b>\n\n"
        "Fayl tayyor.",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

def setup_handlers(dp):
    dp.include_router(router)
