from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import get_db
from services.payment_service import PaymentService
from api.routes.chat import get_current_user
from models.user import User

router = APIRouter(prefix="/subscription", tags=["Subscription"])

class SubscribeRequest(BaseModel):
    plan_name: str # basic, pro

@router.post("/upgrade")
def upgrade_plan(
    request: SubscribeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # ในระบบจริงต้องเช็ค Payment Gateway ก่อน
        # อันนี้จำลองว่าจ่ายเงินแล้ว หรือใช้ Balance ซื้อ
        sub = PaymentService.create_subscription(db, user, request.plan_name)
        return {"status": "success", "plan": sub.plan_name, "credits_granted": sub.credits_granted}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/topup/intent")
def create_topup(
    amount: float,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # สร้าง Stripe Intent
    try:
        intent = PaymentService.create_topup_intent(db, user, amount)
        return intent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
