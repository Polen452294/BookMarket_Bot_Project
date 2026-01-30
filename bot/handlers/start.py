from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from api import upsert_user
from keyboards import main_menu

router = Router()

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
    # стараемся не спамить: если можем — редактируем текущее сообщение
    try:
        await cb.message.edit_text("Выбери раздел:", reply_markup=main_menu())
    except Exception:
        await cb.message.answer("Выбери раздел:", reply_markup=main_menu())
    await cb.answer()
