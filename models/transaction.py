"""
Transaction Model (Payment & Usage)
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database.connection import Base

class TransactionType(enum.Enum):
    TOPUP = "topup"           # เติมเงิน
    SUBSCRIPTION = "subscription"  # ซื้อ subscription
    AI_USAGE = "ai_usage"     # ใช้งาน AI (หักเงิน)
    REFUND = "refund"         # คืนเงิน

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)

    amount = Column(Float, nullable=False)  # ยอดเงิน (+ = เติม, - = ใช้)
    balance_before = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)

    # Metadata
    description = Column(String)
    reference_id = Column(String)  # Payment gateway reference

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.type.value} ${self.amount} for User {self.user_id}>"
