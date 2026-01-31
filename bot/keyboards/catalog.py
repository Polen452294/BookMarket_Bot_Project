from typing import Any, Dict, List, Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class CatCb(CallbackData, prefix="cat"):
    id: int


class ProdCb(CallbackData, prefix="prod"):
    id: int
    cat_id: int


class BackToProductsCb(CallbackData, prefix="back_products"):
    cat_id: int


def kb_categories(categories: List[Dict[str, Any]]):
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.button(text=c["name"], callback_data=CatCb(id=c["id"]).pack())
    kb.adjust(1)
    return kb.as_markup()


def kb_products(cat_id: int, products: List[Dict[str, Any]]):
    kb = InlineKeyboardBuilder()
    for p in products:
        title = p.get("title") or p.get("name") or "Без названия"
        kb.button(text=title, callback_data=ProdCb(id=p["id"], cat_id=cat_id).pack())
    kb.button(text="⬅️ Назад", callback_data="catalog_root")  # назад к категориям
    kb.adjust(1)
    return kb.as_markup()


def kb_back_to_products(cat_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data=BackToProductsCb(cat_id=cat_id).pack())
    kb.adjust(1)
    return kb.as_markup()


def render_product_text(p: Dict[str, Any], category_name: Optional[str] = None) -> str:
    title = p.get("title") or p.get("name") or "Без названия"
    author = p.get("author")
    desc = p.get("description") or "—"
    price = p.get("price")
    price_str = f"{price} ₽" if price is not None else "—"

    lines = [f"📘 <b>{title}</b>"]
    if author:
        lines.append(f"✍️ {author}")
    if category_name:
        lines.append(f"🏷 {category_name}")
    lines.append(f"💳 Цена: <b>{price_str}</b>")
    lines.append("")
    lines.append(desc)
    return "\n".join(lines)

def products_kb(products: list[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=p.get("title", "Без названия"),
                callback_data=f"product:{p['id']}"
            )
        ])

    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_details_kb(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")],
        ]
    )