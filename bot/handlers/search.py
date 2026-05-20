from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from loguru import logger

from config.settings import settings
from ai.service import gemini_service

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("✅ <b>Kino Hub</b> ga xush kelibsiz!\n\n🔍 Kino yoki anime nomini yozing\n📹 Sifatni tanlang (480p/720p/1080p)\n📰 Kanal monitoringi avtomatik\n\n<b>Misol:</b> <code>titanlar hujumi</code> yoki <code>one piece</code>")

@router.message(F.text & ~F.command)
async def search_handler(message: Message):
    query = message.text.strip()
    if len(query) < 2:
        return await message.answer("⚠️ Kamida 2 ta belgi yozing!")
    
    await message.answer("🔍 <b>Qidiruv boshlandi...</b> Gemini tahlil qilmoqda...")
    
    result = await gemini_service.correct_and_enrich_query(query)
    
    text = f"✅ <b>To'g'rilangan:</b> {result.get('corrected_query')}\n🇬🇧 {result.get('english_title')}\n🇺🇿 {result.get('uzbek_title')}\n\n📌 Keyingi qadam: sifatni tanlang"
    await message.answer(text)

def setup_handlers(dp):
    dp.include_router(router)
    logger.success("✅ Bot handlers to'liq sozlandi")
