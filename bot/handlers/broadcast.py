from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from database.connection import get_db
from database.models import User

router = Router()

@router.message(F.text.startswith("/broadcast") | F.text.startswith("/xabar"))
async def broadcast_handler(message: Message):
    ADMIN_IDS = [123456789]
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ Ruxsat yo'q!")
    
    text = message.text.replace("/broadcast", "").replace("/xabar", "").strip()
    if not text:
        return await message.answer("⚠️ /broadcast <matn> formatida yozing")
    
    db = next(get_db())
    users = db.query(User).all()
    
    sent = 0
    for user in users:
        try:
            await message.bot.send_message(user.telegram_id, text)
            sent += 1
        except:
            pass
    
    await message.answer(f"✅ {sent} ta foydalanuvchiga yuborildi!")

def setup_handlers(dp):
    dp.include_router(router)
