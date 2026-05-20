from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    SCRAPER_PHONE: str
    DATABASE_URL: str
    REDIS_URL: str
    GEMINI_API_KEY: str
    CHANNELS_TO_MONITOR: str = ""
    TELEGRAM_CHAT_ID: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
