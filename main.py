import asyncio
import database
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=tokenTelegram.API_TOKEN)

db = Dispatcher()

async def main():
	database.init_db()
	await db.start_polling(bot)