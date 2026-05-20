from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("download"))
async def cmd_download(message: Message):
    await message.answer("Download funksiyasi hozircha cheklangan. Admin bilan bog'laning.")
