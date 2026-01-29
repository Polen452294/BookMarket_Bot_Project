from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.templates import templates
from app.models.product import Product
from app.models.media import Media

router = APIRouter(tags=["public"])


@router.get("/p/{product_id}")
def product_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    media = db.scalars(
        select(Media).where(Media.product_id == product_id).order_by(Media.sort_order.asc(), Media.id.asc())
    ).all()

    return templates.TemplateResponse(
        "product_page.html",
        {"request": request, "product": product, "media": media},
    )
