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

@router.callback_query(F.data == "favorites")
async def favorites_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "❤️ <b>Sevimlilar</b>\n\n"
        "Sizning sevimli videolaringiz:",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "referral")
async def referral_callback(callback: CallbackQuery):
    ref_link = f"https://t.me/your_bot?start=ref_{callback.from_user.id}"
    await callback.message.edit_text(
        f"🎁 <b>Referral tizimi</b>\n\n"
        f"Do'stlaringizni taklif qiling!\n\n"
        f"Sizning havolangiz:\n`{ref_link}`",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "buy_premium")
async def buy_premium_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "💰 <b>Premium obuna</b>\n\n"
        "Cheksiz yuklab olish + AI Chat + Reklamasiz\n\n"
        "Narxi: 1500 Telegram Stars (30 kun)",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data == "stats")
async def stats_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📊 <b>Statistika</b>\n\n"
        "Jami foydalanuvchilar: 1,234\n"
        "Jami videolar: 5,678\n"
        "Jami baholar: 892",
        reply_markup=None
    )
    await callback.answer()

@router.callback_query(F.data.startswith("quality_"))
async def quality_callback(callback: CallbackQuery):
    data = callback.data.split("_")
    quality = data[1]
    video_id = data[2]
    
    await callback.message.edit_text(
        f"⏳ <b>{quality} sifatda yuklanmoqda...</b>\n\n"
        "Iltimos, biroz kuting...",
        reply_markup=None
    )
    
    # TODO: Haqiqiy yuklab olish
    await callback.message.answer(
        f"✅ <b>Yuklab olish tayyor!</b>\n\n"
        f"Sifat: {quality}\n"
        f"Video ID: {video_id}"
    )
    await callback.answer()

def setup_handlers(dp):
    dp.include_router(router)
    logger.success("✅ Tugmali va chiroyli handlerlar ulandi")
