import asyncio
import logging
from config.settings import settings
from bot.main import start_bot  # Bot papkangiz ichidagi asosiy start funksiyasi
from scraper import start_scraper

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Kino Hub loyihasi ishga tushmoqda...")
    
    # Bot va Scraperni parallel ravishda ishga tushirish
    try:
        await asyncio.gather(
            start_bot(),
            start_scraper()
        )
    except Exception as e:
        logger.error(f"Loyihani ishga tushirishda xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(main())
