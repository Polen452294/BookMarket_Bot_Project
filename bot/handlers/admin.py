from aiogram import Router
from aiogram.types import Message
from config import ADMIN_IDS
from api import admin_stats, admin_cleanup

router = Router()

@router.message(lambda m: m.text == "/stats")
async def stats_cmd(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    data = await admin_stats()

    o = data["orders"]
    u = data["users"]

    await message.answer(
        "📊 Статистика\n\n"
        f"👥 Пользователи: {u['total']}\n\n"
        f"📝 Заявки всего: {o['total']}\n"
        f"🆕 Новые: {o['new']}\n"
        f"🟡 В работе: {o['in_progress']}\n"
        f"✅ Закрытые: {o['closed']}\n"
        f"❌ Отклонённые: {o['rejected']}"
    )

@router.message(lambda m: m.text and m.text.startswith("/cleanup"))
async def cleanup_cmd(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer(
            "⚠️ Использование:\n"
            "/cleanup closed\n"
            "/cleanup rejected\n"
            "/cleanup 30d"
        )
        return

    arg = parts[1]

    if arg.endswith("d") and arg[:-1].isdigit():
        days = int(arg[:-1])
        res = await admin_cleanup(days=days)
        await message.answer(f"🧹 Удалено заявок старше {days} дней: {res['deleted']}")
        return

    if arg in ("closed", "rejected"):
        res = await admin_cleanup(status=arg)
        await message.answer(f"🧹 Удалено заявок со статусом '{arg}': {res['deleted']}")
        return

    await message.answer("❌ Неверный аргумент. Используй: closed / rejected / 30d")

