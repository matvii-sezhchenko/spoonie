import asyncio
from aiogram import Bot, Dispatcher
from app import config

from app.repository.database_manager import DatabaseManager
from app.repository.feeding_repository import FeedingRepository
from app.controllers.feeding_controller import FeedingController

from app.handlers.feeding_hendles import register_feeding_handlers

async def main ():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    db_manager = DatabaseManager()
    feeding_repo = FeedingRepository(db_manager)

    feeding_cntr = FeedingController(repository=feeding_repo)

    register_feeding_handlers(dp, feeding_cntr)

    print('Bot is started')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())