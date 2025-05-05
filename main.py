import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.handlers import routers
from core.logic import UserLogic
from config import ConfigManager


UserLogic.load()

async def main():
    bot = Bot(
        token=ConfigManager.env["TOKEN"],
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)
        
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())