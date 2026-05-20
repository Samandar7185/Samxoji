from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument
from loguru import logger
import asyncio

from config.settings import settings

client = TelegramClient(
    'kino_scraper',
    settings.API_ID,
    settings.API_HASH
).start(phone=settings.SCRAPER_PHONE)

@client.on(events.NewMessage(chats=settings.CHANNELS_TO_MONITOR.split(',')))
async def new_video_handler(event):
    if event.message.media and isinstance(event.message.media, MessageMediaDocument):
        doc = event.message.media.document
        logger.info(f"📹 Yangi video: {event.message.message or 'Noma\'lum video'}")
        # TODO: Database ga yozish + embedding + bildirishnoma

async def main():
    logger.success("🔎 Scraper ishga tushdi...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
