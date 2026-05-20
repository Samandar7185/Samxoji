from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from loguru import logger

router = Router()

@router.message(F.text.startswith("/buy") | F.text.startswith("/sotib"))
async def buy_premium(message: Message):
    await message.answer_invoice(
        title="Premium obuna",
        description="Cheksiz yuklab olish + AI Chat + Reklamasiz",
        payload="premium_30days",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="30 kun", amount=1500)],
        start_parameter="premium"
    )

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer("✅ <b>To'lov muvaffaqiyatli!</b>\n\nPremium obuna faollashtirildi!")

def setup_handlers(dp):
    dp.include_router(router)
