import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.orders import router as orders_router

from config import API_BASE_URL
print("API_BASE_URL =", API_BASE_URL)

import os
print("BOT CWD =", os.getcwd())

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(orders_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
