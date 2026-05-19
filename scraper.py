import asyncio
import logging
from telethon import TelegramClient, events
from config.settings import settings
from database.database import get_db_connection
from ai_search import get_embedding

logger = logging.getLogger(__name__)

# Telethon Clientni yaratish
client = TelegramClient('kino_hub_scraper', settings.API_ID, settings.API_HASH)

@client.on(events.NewMessage(chats=settings.MONITOR_CHANNELS))
async def handle_new_post(event):
    """Kanalga yangi post tashlanganda ishlaydi"""
    if event.message.video:
        video = event.message.video
        caption = event.message.text or ""
        
        # Sarlavhani aniqlash (agar caption bo'lmasa, standart nom)
        title = caption.split("\n")[0] if caption else "Nomsiz Video"
        
        logger.info(f"Yangi video topildi: {title}")
        
        # AI uchun embedding yaratish
        try:
            embedding = await get_embedding(f"{title} {caption}")
            
            # Ma'lumotlar bazasiga saqlash
            conn = await get_db_connection()
            await conn.execute(
                """
                INSERT INTO movies (title, file_id, caption, embedding)
                VALUES ($1, $2, $3, $4::vector)
                """,
                title, video.id, caption, str(embedding)
            )
            await conn.close()
            logger.info(f"Video bazaga muvaffaqiyatli qo'shildi: {title}")
        except Exception as e:
            logger.error(f"Videoni bazaga saqlashda xatolik: {e}")

async def start_scraper():
    logger.info("Scraper ishga tushmoqda...")
    await client.start(phone=settings.SCRAPER_PHONE)
    await client.run_until_disconnected()
