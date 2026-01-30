from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError

from app.core.config import settings

router = APIRouter(tags=["admin-auth"])

ALGO = "HS256"

class LoginIn(BaseModel):
    username: str
    password: str

class LoginOut(BaseModel):
    token: str
    token_type: str = "bearer"

@router.post("/admin/auth/login", response_model=LoginOut)
def admin_login(payload: LoginIn):
    if payload.username != settings.ADMIN_USERNAME or payload.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ADMIN_JWT_EXPIRES_MINUTES)

    token = jwt.encode(
        {"sub": payload.username, "exp": exp},
        settings.ADMIN_JWT_SECRET,
        algorithm=ALGO,
    )
    return LoginOut(token=token)

def verify_admin_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.ADMIN_JWT_SECRET, algorithms=[ALGO])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
