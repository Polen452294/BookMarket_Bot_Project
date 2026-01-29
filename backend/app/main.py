from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.storage import ensure_media_dir

from app.api.routes.health import router as health_router
from app.api.routes.products import router as products_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

from app.api.routes.media import router as media_router
from app.api.routes.public_pages import router as public_pages_router
from app.api.routes.bots import router as bots_router
from app.api.routes.broadcasts import router as broadcasts_router

app = FastAPI(title="Bot Platform API")

# Media static
ensure_media_dir()
app.mount("/media", StaticFiles(directory="storage"), name="media")

# Routes
app.include_router(health_router)
app.include_router(auth_router)

app.include_router(products_router)
app.include_router(users_router)

app.include_router(media_router)
app.include_router(public_pages_router)

app.include_router(bots_router)
app.include_router(broadcasts_router)
