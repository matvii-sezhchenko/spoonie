import asyncio
from aiogram import Bot, Dispatcher
from app import config

from app.repository.database_manager import DatabaseManager
from app.repository.feeding_repository import FeedingRepository
from app.controllers.feeding_controller import FeedingController
from app.controllers.mixture_controller import MixtureController

from app.handlers import main_handlers, feeding_handlers, timer_handlers

async def main ():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    db_manager = DatabaseManager()
    feeding_repo = FeedingRepository(db_manager)

    feeding_cntr = FeedingController(repository=feeding_repo)
    mixture_cntr = MixtureController()

    dp.include_router(main_handlers.router)
    dp.include_router(feeding_handlers.router)
    dp.include_router(timer_handlers.router)

    print('Bot is started')
    await dp.start_polling(
        bot,
        feeding_controller=feeding_cntr,
        mixture_controller=mixture_cntr
    )

if __name__ == "__main__":
    asyncio.run(main())