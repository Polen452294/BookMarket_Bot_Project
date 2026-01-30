from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")],
        ]
    )


def products_kb(products: list[dict]):
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=p["title"],
                callback_data=f"product:{p['id']}",
            )
        ])
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
            ],
        ]
    )