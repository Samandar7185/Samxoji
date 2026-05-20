from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from bot.keyboards import main_menu_keyboard

router = Router()

@router.callback_query(F.data == "settings")
async def settings_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌍 Tilni o'zgartirish", callback_data="change_language"),
            InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="notifications")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_menu")
        ]
    ])
    
    await callback.message.edit_text(
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Til: O'zbekcha\n"
        "Bildirishnomalar: Yoqilgan",
        reply_markup=keyboard
    )
    await callback.answer()

@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):
    await callback.message.edit_text(
        "🌍 <b>Tilni tanlang:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Ruscha", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 Inglizcha", callback_data="lang_en")]
        ])
    )
    await callback.answer()

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    lang_names = {"uz": "O'zbekcha", "ru": "Ruscha", "en": "Inglizcha"}
    
    await callback.message.edit_text(
        f"✅ Til {lang_names[lang]} ga o'zgartirildi!",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

def setup_handlers(dp):
    dp.include_router(router)
