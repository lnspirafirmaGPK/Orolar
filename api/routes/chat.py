from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database.connection import get_db
from services.auth_service import AuthService
from core.harmonic_kernel import kernel # เรียกใช้ Kernel
from models.user import User
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/chat", tags=["AI Chat"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class ChatRequest(BaseModel):
    message: str
    model: str = "claude"  # claude, gpt, gemini

class ChatResponse(BaseModel):
    text: str
    cost: float
    model: str
    balance_remaining: float

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = AuthService.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

@router.post("/generate", response_model=ChatResponse)
async def chat_generate(
    request: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # เรียกผ่าน Harmonic Kernel แทนการเรียก Router โดยตรง
        result = await kernel.execute_ai_request(
            db=db,
            user=user,
            message=request.message,
            model=request.model
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
