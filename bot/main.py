import asyncio
from aiogram import Bot as AiogramBot
from aiogram import Dispatcher
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
    except Exception as e:
        # aiogram 3.x: catch generic Exception here (TelegramError no longer exported)
        print(f"Bot runtime error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
