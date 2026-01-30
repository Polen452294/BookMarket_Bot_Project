import os
from pathlib import Path
from dotenv import load_dotenv

# Абсолютный путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем .env из корня
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").strip().rstrip("/")

BOT_ADMIN_TOKEN = os.getenv("BOT_ADMIN_TOKEN", "dev-bot-admin-token").strip()
ADMIN_IDS = [int(x.strip()) for x in (os.getenv("ADMIN_IDS", "") or "").split(",") if x.strip()]

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
