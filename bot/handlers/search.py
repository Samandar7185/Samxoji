from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("search"))
async def cmd_search(message: Message):
    # Simple parser: /search query
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, qidiruv so'rovini kiriting: /search <so'rov>")
        return
    query = args[1]
    # Placeholder response
    await message.answer(f"Qidiruv: {query}\nNatijalar tayyorlanmoqda...")
