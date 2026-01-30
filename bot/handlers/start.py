from aiogram import Router, F
from aiogram.types import Message
from api import upsert_user
from keyboards import main_menu

router = Router()


@router.message(F.text == "/start")
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

    await message.answer(
        "Привет! 👋\nВыбери раздел:",
        reply_markup=main_menu(),
    )
