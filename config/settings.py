# ==================== CONFIG ====================
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Union

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    SCRAPER_PHONE: str = ""

    DATABASE_URL: str
    REDIS_URL: str
    GEMINI_API_KEY: str = ""

    CHANNELS_TO_MONITOR: str = ""
    TELEGRAM_CHAT_ID: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Parse CHANNELS_TO_MONITOR into a list of ints or strings.
# Supports values like: "1001234567890,1009876543210" or "@channel_username,12345"
MONITORED_CHANNELS: List[Union[int, str]] = []
raw_channels = (settings.CHANNELS_TO_MONITOR or "").strip()
if raw_channels:
    for part in raw_channels.split(','):
        ch = part.strip()
        if not ch:
            continue
        # numeric id
        if ch.lstrip('-').isdigit():
            try:
                MONITORED_CHANNELS.append(int(ch))
            except ValueError:
                MONITORED_CHANNELS.append(ch)
        else:
            # allow usernames like @channel
            MONITORED_CHANNELS.append(ch)
