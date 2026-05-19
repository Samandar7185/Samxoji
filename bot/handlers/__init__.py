from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from ai.service import gemini_service

router = Router()

@router.message(F.text)
def search_handler(message: Message):
    # Vaqtinchalik stub
    return message.answer("🔍 Qidiruv boshlandi... Gemini ishlamoqda!")

def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
    logger.info("✅ Bot handlers sozlandi")
