import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.connection import init_db
from api.routes import auth, chat, subscription, admin
from api.middleware.rate_limiter import rate_limit_middleware
from config.settings import settings

# --- ส่วนการตั้งค่าตำแหน่งไฟล์ ---
# หาตำแหน่งปัจจุบันของไฟล์ main.py
BASE_DIR = Path(__file__).resolve().parent
# ระบุตำแหน่งโฟลเดอร์ frontend ให้แม่นยำ
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware
app.middleware("http")(rate_limit_middleware)

# Routes
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(subscription.router)
app.include_router(admin.router)

# --- แก้ไขตรงนี้: เชื่อมต่อ Frontend ---
# ตรวจสอบก่อนว่าโฟลเดอร์มีอยู่จริงไหมเพื่อป้องกัน Error
if os.path.exists(FRONTEND_PATH):
    app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="static")
else:
    print(f" Warning: ไม่พบโฟลเดอร์ frontend ที่ตำแหน่ง {FRONTEND_PATH}")

@app.on_event("startup")
def on_startup():
    init_db()