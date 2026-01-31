from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from services.api import get_products, get_product
from services.api import api_get_json
from keyboards.catalog import (
    CatCb, ProdCb, BackToProductsCb,
    kb_categories, kb_products, products_kb, product_details_kb, kb_back_to_products,
    render_product_text
)
from keyboards.main import main_menu


router = Router()


@router.callback_query(F.data == "catalog")
async def show_catalog(cb: CallbackQuery):
    products = await get_products()
    await cb.message.edit_text("📚 Каталог:", reply_markup=products_kb(products))
    await cb.answer()


@router.callback_query(F.data.startswith("product:"))
async def show_product(cb: CallbackQuery):
    _, raw_id = cb.data.split(":", 1)
    product_id = int(raw_id)

    product = await get_product(product_id)

    text = (
        f"📘 <b>{product.get('title', '—')}</b>\n"
        f"✍️ <b>Автор:</b> {product.get('author') or '—'}\n"
        f"💰 <b>Цена:</b> {product.get('price') or '—'} ₽\n\n"
        f"{product.get('description') or ''}"
    )

    await cb.message.edit_text(
        text,
        reply_markup=product_details_kb(product_id),
        parse_mode="HTML"
    )
    await cb.answer()


@router.callback_query(ProdCb.filter())
async def show_product(cb: CallbackQuery, callback_data: ProdCb):
    product_id = callback_data.id
    cat_id = callback_data.cat_id

    p = await api_get_json(f"/products/{product_id}")

    cat_name = None
    try:
        cat = await api_get_json(f"/categories/{cat_id}")
        cat_name = cat.get("name")
    except Exception:
        pass

    text = render_product_text(p, category_name=cat_name)

    await cb.message.edit_text(
        text,
        reply_markup=kb_back_to_products(cat_id),
        parse_mode="HTML"
    )
    await cb.answer()


@router.callback_query(BackToProductsCb.filter())
async def back_to_products(cb: CallbackQuery, callback_data: BackToProductsCb):
    cat_id = callback_data.cat_id
    products = await api_get_json("/products", params={"category_id": cat_id})
    await cb.message.edit_text("📚 Книги в категории:", reply_markup=kb_products(cat_id, products))
    await cb.answer()


@router.callback_query(F.data == "catalog_root")
async def back_to_categories(cb: CallbackQuery):
    cats = await api_get_json("/categories")
    await cb.message.edit_text("Выбери категорию:", reply_markup=kb_categories(cats))
    await cb.answer()

@router.callback_query(F.data.startswith("product:"))
async def show_product(cb: CallbackQuery):
    _, raw_id = cb.data.split(":", 1)
    product_id = int(raw_id)

    product = await get_product(product_id)
    if not product:
        await cb.message.edit_text("❌ Книга не найдена", reply_markup=main_menu())
        await cb.answer()
        return

    text = (
        f"📘 <b>{product.get('title', '—')}</b>\n\n"
        f"✍️ <b>Автор:</b> {product.get('author') or '—'}\n"
        f"🏢 <b>Издательство:</b> {product.get('publisher') or '—'}\n"
        f"📅 <b>Год:</b> {product.get('year') or '—'}\n"
        f"📄 <b>Страниц:</b> {product.get('pages') or '—'}\n"
        f"🌍 <b>Язык:</b> {product.get('language') or '—'}\n\n"
        f"💰 <b>Цена:</b> {product.get('price') or '—'} ₽\n"
        f"🔥 <s>{product.get('old_price') or '—'} ₽</s>\n\n"
        f"⭐ <b>Рейтинг:</b> {product.get('rating') or '—'} "
        f"({product.get('reviews_count') or 0} отзывов)\n\n"
        f"{product.get('description') or ''}"
    )

    await cb.message.edit_text(
        text,
        reply_markup=product_details_kb(product.get("id", product_id)),
        parse_mode="HTML"
    )
    await cb.answer()


@router.callback_query(F.data == "menu")
async def back_to_menu(cb: CallbackQuery):
    await cb.message.edit_text("Главное меню:", reply_markup=main_menu())
    await cb.answer()