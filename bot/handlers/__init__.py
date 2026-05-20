from aiogram import Router
from loguru import logger

def setup_handlers(dp):
    from bot.handlers.start import setup_handlers as start_setup
    from bot.handlers.search import setup_handlers as search_setup
    from bot.handlers.download import setup_handlers as download_setup
    from bot.handlers.ai_chat import setup_handlers as ai_chat_setup
    from bot.handlers.favorites import setup_handlers as favorites_setup
    from bot.handlers.referral import setup_handlers as referral_setup
    
    start_setup(dp)
    search_setup(dp)
    download_setup(dp)
    ai_chat_setup(dp)
    favorites_setup(dp)
    referral_setup(dp)
    
    logger.success("✅ Barcha handlerlar (AI Chat, Favorites, Referral) ulandi")
