"""
Database Connection & Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    """
    Dependency ให้ FastAPI ใช้สำหรับแต่ละ request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """
    สร้างตารางทั้งหมด (สำหรับ development)
    Production ควรใช้ Alembic migrations
    """
    from models.user import User
    from models.subscription import Subscription
    from models.transaction import Transaction
    from models.api_usage import APIUsage

    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")
