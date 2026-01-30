from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import OrderFlow
from keyboards import phone_kb, main_menu, admin_order_kb
from api import create_order, admin_set_order_status
from config import ADMIN_IDS

router = Router()


@router.callback_query(F.data == "order_new")
async def order_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(OrderFlow.text)
    await cb.message.answer("📝 Опиши, что нужно (одним сообщением):")
    await cb.answer()


@router.message(OrderFlow.text)
async def order_text(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if len(text) < 5:
        await message.answer("Слишком коротко. Опиши чуть подробнее 🙂")
        return
    await state.update_data(text=text)
    await state.set_state(OrderFlow.phone)
    await message.answer("Отправь контакт (или нажми «Пропустить»):", reply_markup=phone_kb())


@router.message(OrderFlow.phone, F.contact)
async def order_phone_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    phone = message.contact.phone_number if message.contact else None
    await finalize_order(message, state, text, phone)


@router.message(OrderFlow.phone, F.text.casefold() == "пропустить")
async def order_phone_skip(message: Message, state: FSMContext):
    data = await state.get_data()
    await finalize_order(message, state, data["text"], None)


async def finalize_order(message: Message, state: FSMContext, text: str, phone: str | None):
    status_code, raw_text, obj = await create_order(message.from_user.id, text, phone)

    if status_code == 409:
        await message.answer("У тебя уже есть активная заявка. Дождись обработки ✅", reply_markup=None)
        await state.clear()
        await message.answer("Выбери раздел:", reply_markup=main_menu())
        return

    if status_code >= 400 or not obj:
        await message.answer(f"Ошибка при создании заявки 😕 (код {status_code})")
        await state.clear()
        await message.answer("Выбери раздел:", reply_markup=main_menu())
        return

    order_id = obj["id"]
    await state.clear()
    await message.answer("✅ Заявка отправлена! Скоро с тобой свяжутся.", reply_markup=None)
    await message.answer("Выбери раздел:", reply_markup=main_menu())

    # уведомляем админов
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                f"🆕 Новая заявка #{order_id}\n"
                f"От: @{message.from_user.username or 'без username'} (id={message.from_user.id})\n\n"
                f"{text}\n\n"
                f"Телефон: {phone or '—'}",
                reply_markup=admin_order_kb(order_id),
            )
        except Exception:
            pass


# --- админские кнопки статусов ---
@router.callback_query(F.data.startswith("order:"))
async def admin_order_action(cb: CallbackQuery):
    try:
        _, status, order_id_s = cb.data.split(":")
        order_id = int(order_id_s)
    except Exception:
        await cb.answer("Некорректная кнопка", show_alert=True)
        return

    if cb.from_user.id not in ADMIN_IDS:
        await cb.answer("Нет прав", show_alert=True)
        return

    try:
        await admin_set_order_status(order_id, status)
        await cb.message.answer(f"✅ Заявка #{order_id} → статус: {status}")
        await cb.answer("Готово")
    except Exception as e:
        await cb.answer("Ошибка обновления", show_alert=True)
        await cb.message.answer(f"Ошибка: {e}")
