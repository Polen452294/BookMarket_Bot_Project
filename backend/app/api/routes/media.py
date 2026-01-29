from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_current_admin
from app.core.db import get_db
from app.core.storage import ensure_media_dir, safe_filename, build_public_url
from app.models.product import Product
from app.models.media import Media
from app.schemas.media import MediaOut

router = APIRouter(tags=["media"])


@router.post("/admin/media/upload", response_model=MediaOut, dependencies=[Depends(get_current_admin)])
async def upload_media(
    product_id: int = Form(...),
    type: str = Form(...),  # photo | video
    sort_order: int = Form(0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if type not in ("photo", "video"):
        raise HTTPException(400, "type must be 'photo' or 'video'")

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    media_dir = ensure_media_dir()
    fname = safe_filename(file.filename or "file.bin")
    dst: Path = media_dir / fname

    content = await file.read()
    if not content:
        raise HTTPException(400, "Empty file")

    dst.write_bytes(content)

    rel_url = f"/media/{fname}"
    public_url = build_public_url(rel_url)

    m = Media(product_id=product_id, type=type, url=public_url, sort_order=sort_order)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
