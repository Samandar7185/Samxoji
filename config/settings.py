# ==================== CONFIG ====================
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

import os

class Settings(BaseSettings):
    # Telegram (optional for non-bot services)
    BOT_TOKEN: Optional[str] = None
    API_ID: Optional[int] = None
    API_HASH: Optional[str] = None
    SCRAPER_PHONE: Optional[str] = None

    # Database / infra
    DATABASE_URL: str
    REDIS_URL: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    CHANNELS_TO_MONITOR: str = ""
    TELEGRAM_CHAT_ID: Optional[int] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# Parse CHANNELS_TO_MONITOR into a list of integer IDs (ignore @usernames)
def _parse_channels(value: str) -> List[int]:
    out: List[int] = []
    if not value:
        return out
    for part in value.split(","):
        p = part.strip()
        if not p:
            continue
        # Skip username-like entries (@username)
        if p.startswith("@"):
            continue
        try:
            out.append(int(p))
        except ValueError:
            # not an integer, skip
            continue
    return out

MONITORED_CHANNELS = _parse_channels(settings.CHANNELS_TO_MONITOR)
