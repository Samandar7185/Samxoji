import asyncio
from loguru import logger

async def main():
    logger.success("🔎 Scraper service boshlandi (demo)")
    await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
