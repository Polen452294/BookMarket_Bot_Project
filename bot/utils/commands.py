from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def setup_commands(bot: Bot, admin_ids: list[int]):
    # --- команды для всех пользователей ---
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Открыть меню"),
            BotCommand(command="help", description="Помощь"),
        ],
        scope=BotCommandScopeDefault(),
    )

    # --- команды только для админов ---
    admin_commands = [
        BotCommand(command="admin", description="Админ-панель (заявки)"),
        BotCommand(command="stats", description="Статистика"),
        BotCommand(command="cleanup", description="Очистка заявок"),
        BotCommand(command="help", description="Помощь"),
    ]

    for admin_id in admin_ids:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(chat_id=admin_id),
        )
