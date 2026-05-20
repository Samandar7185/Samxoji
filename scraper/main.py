import asyncio
import logging
from scraper.channels import ChannelMonitor

logger = logging.getLogger(__name__)

async def main():
    monitor = ChannelMonitor()
    logger.info("🔍 Scraper starting...")

    while True:
        try:
            await monitor.check_channels()
            await asyncio.sleep(300)  # 5 minutes
        except Exception as e:
            logger.exception(f"Scraper error: {e}")
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
