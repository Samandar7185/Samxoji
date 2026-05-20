from aiogram import Router, F
from aiogram.types import CallbackQuery
from loguru import logger

router = Router()

@router.callback_query(F.data.startswith("download_"))
async def download_callback(callback: CallbackQuery):
    file_id = callback.data.split("_")[1]
    await callback.answer("📥 Yuklab olish boshlandi...")
    await callback.message.answer("✅ Fayl yuborildi! (demo)")

def setup_handlers(dp):
    dp.include_router(router)
    logger.success("✅ Download handler ulandi")
