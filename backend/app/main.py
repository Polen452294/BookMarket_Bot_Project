from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.products import router as products_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app = FastAPI(title="Bot Platform API")

app.include_router(health_router)
app.include_router(auth_router)

app.include_router(products_router)
app.include_router(users_router)
