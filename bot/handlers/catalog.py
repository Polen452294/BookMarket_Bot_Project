from aiogram import Router, F
from aiogram.types import CallbackQuery

from api import get_products
from keyboards import products_kb, product_kb, back_to_menu_kb
from config import API_BASE_URL

router = Router()


@router.callback_query(F.data == "catalog")
async def show_catalog(cb: CallbackQuery):
    products = await get_products()

    if not products:
        # edit_text чтобы не плодить сообщения
        try:
            await cb.message.edit_text("Каталог пока пуст.", reply_markup=back_to_menu_kb())
        except Exception:
            await cb.message.answer("Каталог пока пуст.", reply_markup=back_to_menu_kb())
        await cb.answer()
        return

    try:
        await cb.message.edit_text("📦 Каталог:", reply_markup=products_kb(products))
    except Exception:
        await cb.message.answer("📦 Каталог:", reply_markup=products_kb(products))
    await cb.answer()



@router.callback_query(F.data.startswith("product:"))
async def show_product(cb: CallbackQuery):
    product_id = int(cb.data.split(":")[1])

    products = await get_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    text = f"📦 <b>{product['title']}</b>"
    if product.get("description"):
        text += f"\n\n{product['description']}"

    await cb.message.answer(
        text,
        reply_markup=product_kb(product_id, API_BASE_URL),
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(F.data == "about")
async def about(cb: CallbackQuery):
    text = (
        "ℹ️ О проекте\n\n"
        "Платформа для Telegram-ботов под фриланс:\n"
        "• заявки (FSM) + статусы\n"
        "• каталог товаров\n"
        "• веб-страница товара с медиа\n"
        "• рассылки (через бекенд)\n\n"
        "Идея: бот — интерфейс, логика в FastAPI."
    )
    try:
        await cb.message.edit_text(text, reply_markup=back_to_menu_kb())
    except Exception:
        await cb.message.answer(text, reply_markup=back_to_menu_kb())
    await cb.answer()