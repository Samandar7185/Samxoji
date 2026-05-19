from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database.connection import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    english_title = Column(String, nullable=True)
    uzbek_title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    channel_id = Column(String, index=True)
    message_id = Column(Integer)
    quality = Column(String)  # 480p, 720p, 1080p
    language = Column(String)
    duration = Column(Integer)
    size = Column(Float)
    embedding = Column(Text)  # JSON string of embedding vector
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    language = Column(String, default="uz")
    favorites = Column(Text, default="[]")  # JSON list
    created_at = Column(DateTime(timezone=True), server_default=func.now())
