"""
Payment Service
จัดการการเติมเงินและ subscription
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
import stripe

from models.user import User
from models.transaction import Transaction, TransactionType, TransactionStatus
from models.subscription import Subscription, SubscriptionStatus
from config.settings import settings

# Initialize Stripe
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    """
    บริการจัดการ Payment
    """

    @staticmethod
    def create_topup_intent(db: Session, user: User, amount: float) -> Dict[str, Any]:
        """
        สร้าง Payment Intent สำหรับเติมเงิน (Stripe)
        """

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                metadata={
                    "user_id": user.id,
                    "type": "topup"
                }
            )

            return {
                "client_secret": intent.client_secret,
                "amount": amount
            }

        except Exception as e:
            raise Exception(f"Payment intent creation failed: {str(e)}")

    @staticmethod
    def process_topup(db: Session, user: User, amount: float, reference_id: str):
        """
        ประมวลผลการเติมเงิน
        """

        balance_before = user.balance
        user.balance += amount
        balance_after = user.balance

        # บันทึก transaction
        transaction = Transaction(
            user_id=user.id,
            type=TransactionType.TOPUP,
            status=TransactionStatus.COMPLETED,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"Top-up ${amount}",
            reference_id=reference_id
        )

        db.add(transaction)
        db.commit()

        return transaction

    @staticmethod
    def create_subscription(
        db: Session,
        user: User,
        plan_name: str
    ) -> Subscription:
        """
        สร้าง subscription
        """

        # ดึงข้อมูล plan
        plan = settings.SUBSCRIPTION_PLANS.get(plan_name)
        if not plan:
            raise ValueError(f"Invalid plan: {plan_name}")

        # คำนวณวันหมดอายุ (30 วัน)
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30)

        # เติม credits
        user.balance += plan["credits"]
        user.subscription_plan = plan_name
        user.subscription_expires = end_date

        # สร้าง subscription record
        subscription = Subscription(
            user_id=user.id,
            plan_name=plan_name,
            amount=plan["price"],
            credits_granted=plan["credits"],
            status=SubscriptionStatus.ACTIVE,
            start_date=start_date,
            end_date=end_date
        )

        # บันทึก transaction
        transaction = Transaction(
            user_id=user.id,
            type=TransactionType.SUBSCRIPTION,
            status=TransactionStatus.COMPLETED,
            amount=plan["credits"],  # บวก (ได้ credit)
            balance_before=user.balance - plan["credits"],
            balance_after=user.balance,
            description=f"Subscription: {plan['name']}"
        )

        db.add(subscription)
        db.add(transaction)
        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def generate_promptpay_qr(amount: float) -> str:
        """
        สร้าง PromptPay QR Code (จำลอง)
        ในจริงต้องใช้ library promptpay
        """

        # ตัวอย่าง: ใช้ library `promptpay-qr`
        # from promptpay import qrcode
        # qr = qrcode.generate_qr(settings.PROMPTPAY_PHONE, amount)

        return f"promptpay://pay?phone={settings.PROMPTPAY_PHONE}&amount={amount}"
