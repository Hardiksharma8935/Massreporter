import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.database import init_db
from app.bot_handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize database
    await init_db()

    # Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Include routers
    dp.include_router(router)

    logging.info("Starting Telegram Moderation Assistant...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
  
