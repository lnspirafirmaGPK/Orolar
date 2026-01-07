from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from config.settings import settings

# Simple in-memory rate limiter (For Production use Redis)
request_counts = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware จำกัดการใช้งานตาม IP
    """
    # ข้าม rate limit สำหรับ static files
    if request.url.path.startswith("/static") or request.method == "OPTIONS":
        return await call_next(request)

    client_ip = request.client.host
    now = time.time()

    # ล้างประวัติที่เก่าเกิน 1 นาที
    request_counts[client_ip] = [
        t for t in request_counts[client_ip]
        if now - t < 60
    ]

    # ตรวจสอบจำนวน request
    if len(request_counts[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )

    request_counts[client_ip].append(now)
    response = await call_next(request)
    return response
