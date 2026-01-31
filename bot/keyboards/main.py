from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")],
        ]
    )


def products_kb(products: list[dict], with_back: bool = False) -> InlineKeyboardMarkup:
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=p["title"],
                callback_data=f"product:{p['id']}"
            )
        ])

    if with_back:
        buttons.append([InlineKeyboardButton(text="⬅️ В главное меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_kb(product_id: int, public_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📸 Фото / Видео",
                    url=f"{public_url}/p/{product_id}",
                )
            ]
        ]
    )

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Оставить заявку", callback_data="order_new")],
            [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")],
        ]
    )


def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить контакт", request_contact=True)],
                  [KeyboardButton(text="Пропустить")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def admin_order_kb(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ В работу", callback_data=f"order:in_progress:{order_id}"),
                InlineKeyboardButton(text="✅ Закрыть", callback_data=f"order:closed:{order_id}"),
            ],
            [
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"order:rejected:{order_id}"),
                InlineKeyboardButton(text="💬 Комментарий", callback_data=f"order_comment:{order_id}"),
            ],
        ]
    )

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Оставить заявку", callback_data="order_new")],
            [InlineKeyboardButton(text="🗂 Мои заявки", callback_data="my_orders")],
            [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")],
        ]
    )

def back_to_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
        ]
    )

def reject_reasons_kb(order_id: int):
    reasons = [
        ("Не по теме", "not_topic"),
        ("Нет мест/времени", "no_slots"),
        ("Нужны детали", "need_details"),
        ("Не работаем с таким", "no_service"),
        ("Другое", "other"),
    ]
    rows = []
    for title, code in reasons:
        rows.append([InlineKeyboardButton(text=title, callback_data=f"reject:{order_id}:{code}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"reject_back:{order_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def my_order_kb(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Подробнее", callback_data=f"order_view:{order_id}")],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")],
        ]
    )

def back_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="menu")]
        ]
    )
