import asyncio
import logging
from datetime import datetime

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

		active_sleep = database.get_active_sleep()
		sleep_info = ""

		if active_sleep:
			database.finish_sleep_auto(minutes_ago=10)
			sleep_info = f"\n\nℹ️ Автоматично закрито сон (10 хв тому)."

		await message.answer(
			f"✅ Записано: {volume} мл ({user})",
			reply_markup=keyboards.main_menu()
		)
	except Exception as e:
		logging.error(f"Помилка при записі годування {e}")
		await message.answer("Ой, щось пішло не за планом")


@dp.message(F.text.endswith("😴 Сон"))
async def process_sleep(message: types.Message):
	user = message.from_user.first_name
	active_sleep = database.get_active_sleep()

	if not active_sleep:
		database.start_sleep(user)
		await message.answer(f"💤 {user} відмітив, що малюк заснув.")
	else:
		start_id, start_time, start_user = active_sleep
		database.finish_sleep()
		await message.answer(
			f"☀️ Малюк прокинувся!\n\n"
			f"Заснув о: {start_time} (відмітив {start_user})\n"
			f"Прокинувся о: {datetime.now().strftime('%H:%M')} (відмітив {user})"
		)


@dp.message(F.text.endswith("📊 Звіт"))
async def show_report(message: types.Message):
	total_volume = database.get_feeding_report(days=3)
	daily_sleep_data = database.get_sleep_report_by_days(days=3)

	sleep_text = ""

	if daily_sleep_data:
		for day, total_min in daily_sleep_data:
			h = int(total_min // 60)
			m = int(total_min % 60)
			sleep_text += f"🔹 {day} — **{h} год. {m} хв.**\n"
	else:
		sleep_text = "Даних про сон ще немає."

	if total_volume > 0:
		response_text = (
			f"📊 **Звіт за останні 3 дні**\n\n"
			f"Загальна кількість суміші: **{total_volume} мл**\n"
			f"Це приблизно {round(total_volume / 1000, 2)} \n\n"
			f"😴 **Сон по днях:**\n"
			f"{sleep_text}"
		)
	else:
		response_text = "За останні 3s дні записів про годування не знайдено"

	await message.answer(response_text, parse_mode="Markdown")

async def main():
	database.init_db()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())