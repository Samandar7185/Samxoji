from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

import json

from database.connection import get_db
from database.models import User, Video

router = Router()

@router.message(F.text.startswith("/favorites") | F.text.startswith("/sevimlilar"))
async def favorites_handler(message: Message):
    user_id = message.from_user.id
    
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == user_id).first()
    
    if not user or not user.favorites:
        return await message.answer("\ud83d\udcc1 Sevimlilar ro'yxati bo'sh.\n\nVideo topib, "Saqlash" tugmasini bosing!")
    
    text = "\ud83d\udcc1 <b>Sevimlilar:</b>\n\n"
    for i, fav in enumerate(user.favorites[:10], 1):
        text += f"{i}. {fav.get('title', 'Noma\'lum')}\n"
    
    await message.answer(text)

def setup_handlers(dp):
    dp.include_router(router)
