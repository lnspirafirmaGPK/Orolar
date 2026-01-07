from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database.connection import get_db
from models.user import User, UserRole
from models.transaction import Transaction
from models.api_usage import APIUsage
from services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/admin", tags=["Admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency: Check Admin Role
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = AuthService.get_current_user(db, token)
    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user

@router.get("/stats")
def get_platform_stats(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """ดูสถิติภาพรวมของระบบ"""

    total_users = db.query(User).count()
    total_transactions = db.query(Transaction).count()
    total_revenue = db.query(func.sum(Transaction.amount)).filter(Transaction.amount > 0).scalar() or 0.0
    total_api_calls = db.query(APIUsage).count()

    return {
        "users": total_users,
        "transactions": total_transactions,
        "revenue": total_revenue,
        "api_calls": total_api_calls
    }

@router.get("/users")
def list_users(
    skip: int = 0,
    limit: int = 100,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """รายชื่อ User ทั้งหมด"""
    users = db.query(User).offset(skip).limit(limit).all()
    # Return specific fields to avoid leaking passwords
    return [
        {"id": u.id, "email": u.email, "role": u.role, "balance": u.balance}
        for u in users
    ]
