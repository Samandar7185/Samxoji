from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from loguru import logger

from bot.keyboards import main_menu_keyboard, quality_keyboard

from config.settings import settings
from ai.service import gemini_service

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "✅ <b>Kino Hub</b> ga xush kelibsiz!\n\n"
        "🎬 Eng yaxshi kino va anime bot!",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "search")
async def search_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔍 <b>Qidirish</b>\n\n"
        "Kino yoki anime nomini yozing:",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "ai_chat")
async def ai_chat_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🤖 <b>AI Chat</b>\n\n"
        "Menga savol bering yoki tavsiya so'rang!\n\n"
        "Misol: <code>Qanday kino tavsiya qilasiz?</code>",
        reply_markup=None
    )
    await callback.answer()

def setup_handlers(dp):
    dp.include_router(router)
    logger.success("✅ Tugmali va chiroyli handlerlar ulandi")
