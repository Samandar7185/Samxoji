from sqlalchemy import Column, Integer, String, Text, DateTime, Float, BigInteger, JSON
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
    quality = Column(String)
    language = Column(String)
    duration = Column(Integer)
    size = Column(Float)
    embedding = Column(Text)  # JSON string of vector
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    language = Column(String, default="uz")
    favorites = Column(JSON, default=[])
    watch_history = Column(JSON, default=[])
    preferences = Column(JSON, default={})
    embedding = Column(Text)  # User preference vector
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    video_id = Column(String, index=True)
    rating = Column(Integer)  # 1-5
    review = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    referrer_id = Column(BigInteger, index=True)
    referred_id = Column(BigInteger, unique=True)
    bonus_given = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
