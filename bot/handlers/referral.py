from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from database.connection import get_db
from database.models import User, Referral

router = Router()

@router.message(F.text.startswith("/referral") | F.text.startswith("/taklif"))
async def referral_handler(message: Message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/your_bot?start=ref_{user_id}"
    
    text = (
        "\ud83c\udf81 <b>Referral tizimi</b>\n\n"
        "Do'stlaringizni taklif qiling va bonus oling!\n\n"
        f"\ud83d\udd17 Sizning havolangiz:\n`{ref_link}`\n\n"
        "\ud83d\udcb0 Har bir taklif uchun +50 ball!"
    )
    
    await message.answer(text)

def setup_handlers(dp):
    dp.include_router(router)
