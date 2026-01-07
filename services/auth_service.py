"""
Authentication Service
JWT-based authentication
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user import User, UserRole
from config.settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

class AuthService:
    """
    บริการจัดการ Authentication
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """ตรวจสอบรหัสผ่าน"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """เข้ารหัสรหัสผ่าน"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """สร้าง JWT token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """ตรวจสอบ JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """ตรวจสอบ email + password"""
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not AuthService.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def register_user(
        db: Session,
        email: str,
        password: str,
        full_name: str
    ) -> User:
        """สร้าง user ใหม่"""

        # ตรวจสอบว่า email ซ้ำหรือไม่
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise ValueError("Email already registered")

        # สร้าง user
        hashed_password = AuthService.get_password_hash(password)

        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            balance=1.0,  # Free tier: $1 credit
            subscription_plan="free"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """ดึง user จาก token"""
        payload = AuthService.verify_token(token)

        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
