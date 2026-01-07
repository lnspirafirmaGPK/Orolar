from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database.connection import get_db
from services.auth_service import AuthService
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    balance: float
    role: str

@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(
            db=db,
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_role": user.role.value
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
    db: Session = Depends(get_db)
):
    user = AuthService.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
