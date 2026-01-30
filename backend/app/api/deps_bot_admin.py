from fastapi import Header, HTTPException
from app.core.config import settings


def bot_admin_guard(
    x_bot_admin_token: str | None = Header(default=None, alias="X-Bot-Admin-Token")
):
    if not x_bot_admin_token or x_bot_admin_token != settings.bot_admin_token:
        raise HTTPException(status_code=401, detail="Invalid bot admin token")
    return True
