from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states import AdminComment, OrderFlow
from api import admin_set_order_comment, create_order, admin_set_order_status, get_my_orders, admin_list_orders, admin_get_notify_info, get_order
from keyboards import my_order_kb, phone_kb, main_menu, admin_order_kb, back_to_menu_kb, reject_reasons_kb
from config import ADMIN_IDS

router = Router()

STATUS_USER_TEXT = {
    "new": "🆕 Заявка создана",
    "in_progress": "🟡 Ваша заявка взята в работу",
    "closed": "✅ Заявка закрыта",
    "rejected": "❌ Заявка отклонена",
}

STATUS_LABEL = {
    "new": "🆕 Новая",
    "in_progress": "🟡 В работе",
    "closed": "✅ Закрыта",
    "rejected": "❌ Отклонена",
}

REJECT_REASON_TEXT = {
    "not_topic": "Запрос не относится к нашей тематике.",
    "no_slots": "Сейчас нет свободного времени на новые заявки.",
    "need_details": "Не хватает деталей для работы. Уточните запрос и отправьте заново.",
    "no_service": "Мы не работаем с таким типом задач.",
    "other": "По внутренним причинам не можем взять заявку.",
}

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


@router.message(OrderFlow.phone, F.text.casefold() == "пропустить")
async def order_phone_skip(message: Message, state: FSMContext):
    await message.answer("Ок, без контакта.", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await finalize_order(message, state, data["text"], None)


@router.message(OrderFlow.phone, F.text.casefold() == "пропустить")
async def order_phone_skip(message: Message, state: FSMContext):
    data = await state.get_data()
    await finalize_order(message, state, data["text"], None)


async def finalize_order(message: Message, state: FSMContext, text: str, phone: str | None):

    await message.answer("⏳ Принял, обрабатываю...", reply_markup=ReplyKeyboardRemove())
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

    if status == "rejected":
            try:
                await cb.message.edit_reply_markup(reply_markup=reject_reasons_kb(order_id))
            except Exception:
                await cb.message.answer("Выбери причину отклонения:", reply_markup=reject_reasons_kb(order_id))
            await cb.answer()
            return

    try:
        await admin_set_order_status(order_id, status)

        info = await admin_get_notify_info(order_id)
        tg_id = int(info["tg_id"])
        new_status = info["status"]

        user_text = STATUS_USER_TEXT.get(new_status, f"Статус изменён: {new_status}")
        try:
            await cb.bot.send_message(
                tg_id,
                f"{user_text}\n\n"
                f"Заявка #{order_id}\n"
                f"Если нужно уточнение — просто ответь на это сообщение.",
            )
        except Exception:
            pass

        admin_label = STATUS_LABEL.get(new_status, new_status)
        await cb.answer("Готово")
        await cb.message.answer(f"✅ Заявка #{order_id} → {admin_label}")

    except Exception as e:
        await cb.answer("Ошибка обновления", show_alert=True)
        await cb.message.answer(f"Ошибка: {e}")

@router.callback_query(F.data == "my_orders")
async def my_orders(cb: CallbackQuery):
    try:
        orders = await get_my_orders(cb.from_user.id)
    except Exception as e:
        try:
            await cb.message.edit_text(
                f"Ошибка загрузки заявок 😕\n{e}",
                reply_markup=back_to_menu_kb(),
            )
        except Exception:
            await cb.message.answer(
                f"Ошибка загрузки заявок 😕\n{e}",
                reply_markup=back_to_menu_kb(),
            )
        await cb.answer()
        return

    if not orders:
        try:
            await cb.message.edit_text(
                "У тебя пока нет заявок.",
                reply_markup=back_to_menu_kb(),
            )
        except Exception:
            await cb.message.answer(
                "У тебя пока нет заявок.",
                reply_markup=back_to_menu_kb(),
            )
        await cb.answer()
        return

    lines = ["🗂 <b>Мои заявки</b>\n"]
    for o in orders[:10]:
        status = STATUS_LABEL.get(o["status"], o["status"])
        text_preview = (o["text"] or "")[:80].replace("\n", " ")
        phone = o.get("phone") or "—"
        lines.append(
            f"#{o['id']} • {status}\n"
            f"📄 {text_preview}\n"
            f"📱 {phone}\n"
        )
        await cb.message.edit_text(
            "\n\n".join(lines),
            reply_markup=my_order_kb(orders[0]["id"]),
            parse_mode="HTML",
        )


    text = "\n".join(lines)

    try:
        await cb.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_menu_kb(),
        )
    except Exception:
        await cb.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=back_to_menu_kb(),
        )
    await cb.answer()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Нет прав.")
        return

    try:
        new_orders = await admin_list_orders(status="new")
        in_progress_orders = await admin_list_orders(status="in_progress")
        orders = (new_orders + in_progress_orders)

    except Exception as e:
        await message.answer(f"Ошибка админ-списка 😕\n{e}")
        return

    if not orders:
        await message.answer("✅ Новых заявок нет.")
        return

    await message.answer(f"🆕 Новые заявки: {len(orders)} (покажу последние 10)")

    for o in orders[:10]:
        await message.answer(
            f"🆕 Заявка #{o['id']}\n"
            f"UserID: {o['user_id']}\n\n"
            f"{o['text']}\n\n"
            f"Телефон: {o.get('phone') or '—'}",
            reply_markup=admin_order_kb(o["id"]),
        )

@router.callback_query(F.data.startswith("reject:"))
async def reject_with_reason(cb: CallbackQuery):
    if cb.from_user.id not in ADMIN_IDS:
        await cb.answer("Нет прав", show_alert=True)
        return

    try:
        _, order_id_s, code = cb.data.split(":")
        order_id = int(order_id_s)
    except Exception:
        await cb.answer("Некорректные данные", show_alert=True)
        return

    reason_text = REJECT_REASON_TEXT.get(code, "По внутренним причинам не можем взять заявку.")

    try:
        await admin_set_order_status(order_id, "rejected")

        info = await admin_get_notify_info(order_id)
        tg_id = int(info["tg_id"])

        try:
            await cb.bot.send_message(
                tg_id,
                "❌ Ваша заявка отклонена.\n\n"
                f"Причина: {reason_text}\n\n"
                f"Заявка #{order_id}\n"
                "Если хотите — отправьте новую заявку с уточнениями.",
            )
        except Exception:
            pass

        try:
            await cb.message.edit_reply_markup(reply_markup=admin_order_kb(order_id))
        except Exception:
            pass

        await cb.answer("Отклонено")
        await cb.message.answer(f"✅ Заявка #{order_id} отклонена. Причина: {reason_text}")

    except Exception as e:
        await cb.answer("Ошибка", show_alert=True)
        await cb.message.answer(f"Ошибка: {e}")

@router.callback_query(F.data.startswith("reject_back:"))
async def reject_back(cb: CallbackQuery):
    if cb.from_user.id not in ADMIN_IDS:
        await cb.answer("Нет прав", show_alert=True)
        return

    try:
        order_id = int(cb.data.split(":")[1])
    except Exception:
        await cb.answer()
        return

    try:
        await cb.message.edit_reply_markup(reply_markup=admin_order_kb(order_id))
    except Exception:
        pass

    await cb.answer()

@router.message(OrderFlow.phone, F.contact)
async def order_phone_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    phone = message.contact.phone_number if message.contact else None
    await finalize_order(message, state, text, phone)

@router.callback_query(F.data.startswith("order_view:"))
async def view_order(cb: CallbackQuery):
    order_id = int(cb.data.split(":")[1])

    order = await get_order(order_id, cb.from_user.id)

    text = (
        f"📝 Заявка #{order['id']}\n\n"
        f"📄 {order['text']}\n\n"
        f"📱 {order.get('phone') or '—'}\n"
        f"📌 Статус: {STATUS_LABEL[order['status']]}\n"
        f"💬 Комментарий: {order.get('comment') or '—'}"
    )

    await cb.message.edit_text(text, reply_markup=back_to_menu_kb())
    await cb.answer()

@router.callback_query(F.data.startswith("order_comment:"))
async def admin_comment_start(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id not in ADMIN_IDS:
        return

    order_id = int(cb.data.split(":")[1])
    await state.set_state(AdminComment.text)
    await state.update_data(order_id=order_id)
    await cb.message.answer("💬 Введи комментарий для пользователя:")
    await cb.answer()

@router.message(AdminComment.text)
async def admin_comment_save(message: Message, state: FSMContext):
    data = await state.get_data()
    order_id = data["order_id"]
    comment = message.text.strip()

    await admin_set_order_comment(order_id, comment)

    info = await admin_get_notify_info(order_id)

    await message.bot.send_message(
        info["tg_id"],
        f"💬 Комментарий по заявке #{order_id}:\n\n{comment}",
    )

    await message.answer("✅ Комментарий отправлен пользователю")
    await state.clear()
