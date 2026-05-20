from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from config.settings import settings

from database.connection import get_db
from database.models import User, Video, Rating

router = Router()

ADMIN_IDS = [123456789]  # O'zingizning Telegram ID ingizni qo'ying

@router.message(F.text.startswith("/admin") | F.text.startswith("/panel"))
async def admin_panel(message: Message):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        return await message.answer("⛔ Sizda admin huquqi yo'q!")
    
    db = next(get_db())
    total_users = db.query(User).count()
    total_videos = db.query(Video).count()
    total_ratings = db.query(Rating).count()
    
    text = (
        "📊 <b>ADMIN PANEL</b>\n\n"
        f"👥 Foydalanuvchilar: {total_users}\n"
        f"📹 Videolar: {total_videos}\n"
        f"⭐ Baholar: {total_ratings}\n\n"
        "Buyruqlar:\n"
        "/stats - Batafsil statistika\n"
        "/broadcast <matn> - Hammaga xabar yuborish"
    )
    
    await message.answer(text)

def setup_handlers(dp):
    dp.include_router(router)
