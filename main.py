from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.connection import init_db
from api.routes import auth, chat, subscription, admin
from api.middleware.rate_limiter import rate_limit_middleware
from config.settings import settings

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

# Static Files (Frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.on_event("startup")
def on_startup():
    init_db()
