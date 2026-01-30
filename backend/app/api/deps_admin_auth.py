from fastapi import Header, HTTPException
from app.api.routes.auth import verify_admin_jwt

def require_admin_jwt(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = parts[1]
    return verify_admin_jwt(token)
