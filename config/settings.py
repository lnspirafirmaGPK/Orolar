"""
Configuration Management
ตั้งค่าทั้งหมดของระบบ
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    การตั้งค่าหลัก (อ่านจาก Environment Variables)
    """

    # === Application ===
    APP_NAME: str = "Orolar AI Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str  # สำหรับ JWT

    # === Cosmic Salt (Resonance Engine) ===
    COSMIC_SALT: str  # สำหรับ Harmonic System

    # === Database ===
    DATABASE_URL: str = "sqlite:///./orolar.db"  # เริ่มด้วย SQLite

    # === AI Providers ===
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None

    # === Pricing (per 1M tokens) ===
    PRICING: dict = {
        "claude-sonnet": {"input": 3.00, "output": 15.00},
        "claude-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gemini-flash": {"input": 0.075, "output": 0.30},
        "grok-beta": {"input": 5.00, "output": 15.00},
    }

    # === Revenue Sharing ===
    PLATFORM_FEE_PERCENTAGE: float = 0.0  # 0% markup (ไม่เอาเปรียบ)
    CHARITY_PERCENTAGE: float = 100.0     # 100% กำไรไปบริจาค

    # === Subscription Plans ===
    SUBSCRIPTION_PLANS: dict = {
        "free": {
            "name": "Free Tier",
            "price": 0.0,
            "credits": 1.0,  # $1 credit
            "features": ["BYOK (Bring Your Own Key)"]
        },
        "basic": {
            "name": "Basic",
            "price": 9.99,
            "credits": 15.0,  # $15 credit (50% bonus)
            "features": ["Shared pool", "Priority support"]
        },
        "pro": {
            "name": "Professional",
            "price": 29.99,
            "credits": 50.0,  # $50 credit (67% bonus)
            "features": ["All models", "Advanced analytics", "API access"]
        }
    }

    # === Payment ===
    STRIPE_SECRET_KEY: Optional[str] = None
    PROMPTPAY_PHONE: Optional[str] = None

    # === Rate Limiting ===
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

# Singleton instance
settings = Settings()
