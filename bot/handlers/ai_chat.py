from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from ai.service import gemini_service

from database.connection import get_db
from database.models import User

router = Router()

@router.message(F.text.startswith("/chat") | F.text.startswith("/ai") | F.text.startswith("/suhbat"))
async def ai_chat_handler(message: Message):
    query = message.text.replace("/chat", "").replace("/ai", "").replace("/suhbat", "").strip()
    
    if not query:
        return await message.answer(
            "\ud83e\udd16 <b>AI Chat</b>\n\n"
            "Menga kino haqida savol bering yoki tavsiya so'rang!\n\n"
            "<b>Misollar:</b>\n"
            "\u2022 Qanday kino tavsiya qilasiz?\n"
            "\u2022 Titanlar hujumi haqida gapirib bering\n"
            "\u2022 Eng yaxshi anime qaysi?"
        )
    
    await message.answer("\ud83e\udd16 <b>AI javob berishda...</b>")
    
    try:
        prompt = f"""
        Sen professional kino va anime maslahatchisisan. 
        Foydalanuvchi savoli: "{query}"
        
        Javobni o'zbek tilida, qisqa va foydali qil. 
        Agar tavsiya bersang, 3-5 ta variant ber.
        """
        
        response = gemini_service.model.generate_content(prompt)
        await message.answer(response.text)
        
    except Exception as e:
        logger.error(f"AI Chat xatosi: {e}")
        await message.answer("\u26a0\ufe0f Xatolik yuz berdi. Keyinroq urinib ko'ring.")

def setup_handlers(dp):
    dp.include_router(router)
