import asyncio
from aiogram import Bot as AiogramBot
from aiogram import Dispatcher
from aiogram.exceptions import TelegramError
from config.settings import settings

async def main():
    bot = AiogramBot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    from bot.handlers import start, search, download
    dp.include_router(start.router)
    dp.include_router(search.router)
    dp.include_router(download.router)

    print("🤖 Bot starting...")
    try:
        await dp.start_polling(bot)
    except TelegramError as e:
        print(f"Telegram error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
