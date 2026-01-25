from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginIn, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    # MVP: логин/пароль берём из env (потом можно вынести в таблицу)
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=payload.username)
    return TokenOut(access_token=token)
