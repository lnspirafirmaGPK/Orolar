"""
User Model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database.connection import Base

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)

    # Balance & Credits
    balance = Column(Float, default=0.0)  # เงินคงเหลือ (USD)

    # Subscription
    subscription_plan = Column(String, default="free")  # free, basic, pro
    subscription_expires = Column(DateTime, nullable=True)

    # Role
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    api_usages = relationship("APIUsage", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
