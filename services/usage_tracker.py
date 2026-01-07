"""
Usage Tracker Service
แยก Logic การบันทึกสถิติออกมาเพื่อความสะอาด
"""
from sqlalchemy.orm import Session
from models.api_usage import APIUsage
from models.transaction import Transaction, TransactionType, TransactionStatus
from models.user import User

class UsageTracker:
    @staticmethod
    def record_usage(
        db: Session,
        user: User,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float
    ):
        """บันทึกการใช้งาน API และหักเงิน"""

        # 1. Update User Balance
        balance_before = user.balance
        user.balance -= cost
        balance_after = user.balance

        # 2. Create Transaction Record
        transaction = Transaction(
            user_id=user.id,
            type=TransactionType.AI_USAGE,
            status=TransactionStatus.COMPLETED,
            amount=-cost,
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"AI Request: {model}"
        )

        # 3. Create Usage Stat Record
        usage = APIUsage(
            user_id=user.id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost
        )

        db.add(transaction)
        db.add(usage)
        db.commit()
