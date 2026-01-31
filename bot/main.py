import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.types import Message

from config import BOT_TOKEN
from handlers.admin import router as admin_router
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.orders import router as orders_router
from handlers.about import router as about_router
from handlers import catalog

from utils.commands import setup_commands
from config import ADMIN_IDS

from config import API_BASE_URL
print("API_BASE_URL =", API_BASE_URL)

import os
print("BOT CWD =", os.getcwd())

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(orders_router)
    dp.include_router(about_router)

    await setup_commands(bot, ADMIN_IDS)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())