from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_({"О проекте", "ℹ️ О проекте", "О проекте ℹ️"}))
async def about(msg: Message):
    await msg.answer(
        "📚 BookMarket Bot\n\n"
        "Бот для просмотра каталога книг и оформления заявок.\n"
        "Backend: FastAPI + PostgreSQL + Docker."
    )
