from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from database.connection import get_db
from database.models import User, Video, Rating

router = Router()

@router.message(F.text.startswith("/stats") | F.text.startswith("/statistika"))
async def stats_handler(message: Message):
    db = next(get_db())
    
    total_users = db.query(User).count()
    total_videos = db.query(Video).count()
    total_ratings = db.query(Rating).count()
    
    text = (
        "📊 <b>STATISTIKA</b>\n\n"
        f"👥 Jami foydalanuvchilar: {total_users}\n"
        f"📹 Jami videolar: {total_videos}\n"
        f"⭐ Jami baholar: {total_ratings}\n\n"
        "🏆 Eng mashhur videolar (tez orada!)"
    )
    
    await message.answer(text)

def setup_handlers(dp):
    dp.include_router(router)
