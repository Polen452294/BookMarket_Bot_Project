from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.main import main_menu, products_kb, back_to_menu_kb
from services.api import get_products

from api import upsert_user

from keyboards.main import main_menu
from keyboards.main import products_kb
from services.api import get_products

router = Router()

print("products_kb from:", products_kb.__module__)

HELP_TEXT = (
    "🧭 Помощь\n\n"
    "Доступные действия:\n"
    "• 📝 Оставить заявку — отправить запрос администратору\n"
    "• 🗂 Мои заявки — посмотреть статус заявок\n"
    "• 📦 Каталог — товары/услуги из бекенда\n"
    "• ℹ️ О проекте — что это за система\n\n"
    "Команды:\n"
    "/start — открыть меню\n"
    "/help — помощь\n"
    "/admin — (только админы) список новых заявок"
)

@router.message(F.text.startswith("/start"))
async def start(message: Message):
    source = None
    if message.text and len(message.text.split()) > 1:
        source = message.text.split(maxsplit=1)[1]

    await upsert_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        source=source,
    )

    await message.answer("Привет! 👋\nВыбери раздел:", reply_markup=main_menu())


@router.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(HELP_TEXT, reply_markup=main_menu())


@router.callback_query(F.data == "menu")
async def menu(cb: CallbackQuery):
    try:
        await cb.message.edit_text("Выбери раздел:", reply_markup=main_menu())
    except Exception:
        await cb.message.answer("Выбери раздел:", reply_markup=main_menu())
    await cb.answer()

@router.callback_query(F.data == "catalog")
async def show_catalog(cb: CallbackQuery):
    products = await get_products()

    if not products:
        await cb.message.edit_text("Каталог пока пуст.", reply_markup=back_to_menu_kb())
        await cb.answer()
        return

    await cb.message.edit_text(
        "📦 Каталог:",
        reply_markup=products_kb(products, with_back=True)
    )
    await cb.answer()

@router.callback_query(F.data == "about")
async def about(cb: CallbackQuery):
    text = (
        "ℹ️ <b>О проекте</b>\n\n"
        "Это учебный проект-платформа:\n"
        "• FastAPI + PostgreSQL (бекенд)\n"
        "• aiogram (бот-клиент)\n"
        "• Каталог товаров через API\n\n"
        "Смысл: бот — тонкий клиент, вся логика в бекенде."
    )

    await cb.message.edit_text(text, reply_markup=back_to_menu_kb(), parse_mode="HTML")
    await cb.answer()

@router.callback_query(F.data == "menu")
async def back_to_menu(cb: CallbackQuery):
    await cb.message.edit_text("Главное меню:", reply_markup=main_menu())
    await cb.answer()