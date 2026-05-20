from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from loguru import logger

from bot.keyboards import main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "✅ <b>Kino Hub</b> ga xush kelibsiz!\n\n"
        "🎬 Eng yaxshi kino va anime bot!",
        reply_markup=main_menu_keyboard()
    )

def setup_handlers(dp):
    dp.include_router(router)
    logger.success("✅ Start handler ulandi")
