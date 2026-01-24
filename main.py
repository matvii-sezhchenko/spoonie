import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Custom modules
import tokenTelegram
import database
import keyboards

logging.basicConfig(level=logging.INFO)

bot = Bot(token=tokenTelegram.API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
	await message.answer(
		f"Вітаю, {message.from_user.first_name}! Оберіть дію:",
		reply_markup=keyboards.main_menu()
	)

@dp.message(F.text == "🍼 Годування")
async def show_feeding_options (message: types.Message):
	await message.answer(
		"Скількі мл спожито?",
		reply_markup=keyboards.feeding_levels()
	)

@dp.message(F.text.endswith("мл"))
async def process_feeding(message: types.Message):
	user = message.from_user.first_name

	try:
		volume  = int (message.text.split()[0])
		database.add_feeding(user, volume)

		await message.answer(
			f"✅ Записано: {volume} мл ({user})",
			reply_markup=keyboards.main_menu()
		)
	except Exception as e:
		logging.error(f"Помилка при записі годування {e}")
		await message.answer("Ой, щось пішло не за планом")

async def main():
	database.init_db()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())