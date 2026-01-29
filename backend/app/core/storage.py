from __future__ import annotations

import os
import secrets
from pathlib import Path

from app.core.config import settings


def ensure_media_dir() -> Path:
    p = Path(settings.media_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_filename(original: str) -> str:
    # очень простой вариант: убираем директории и добавляем случайный префикс
    base = os.path.basename(original).replace(" ", "_")
    prefix = secrets.token_hex(8)
    return f"{prefix}_{base}"


def build_public_url(rel_path: str) -> str:
    # rel_path например: /media/xxx.mp4
    return settings.public_base_url.rstrip("/") + rel_path
