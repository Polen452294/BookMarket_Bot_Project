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
    base = os.path.basename(original).replace(" ", "_")
    prefix = secrets.token_hex(8)
    return f"{prefix}_{base}"


def build_public_url(rel_path: str) -> str:
    return settings.public_base_url.rstrip("/") + rel_path
