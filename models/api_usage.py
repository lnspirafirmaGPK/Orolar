"""
API Usage Tracking
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base

class APIUsage(Base):
    __tablename__ = "api_usages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Request Info
    model = Column(String, nullable=False)  # claude-sonnet, gpt-4, etc.
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)

    # Cost Calculation
    cost = Column(Float, nullable=False)

    # Metadata
    request_metadata = Column(JSON)  # เก็บ metadata เพิ่มเติม (ไม่เก็บ message content!)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="api_usages")

    def __repr__(self):
        return f"<APIUsage {self.model} ${self.cost:.4f} for User {self.user_id}>"
