from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from loguru import logger

router = Router()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    from bot.keyboards import main_menu_keyboard
    await callback.message.edit_text(
        "✅ <b>Kino Hub</b> ga xush kelibsiz!",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

def setup_handlers(dp):
    dp.include_router(router)
