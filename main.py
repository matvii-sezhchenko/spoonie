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


@dp.message(F.text == "📊 Звіт")
async def show_report(message: types.Message):
    feed_data = database.get_feeding_report_by_days(days=3)
    sleep_data = dict(database.get_sleep_report_by_days(days=3))
    
    report_lines = ["📊 **Звіт за останні дні**\n"]
    
    all_dates = sorted(set([d for d, _ in feed_data] + list(sleep_data.keys())), reverse=True)[:3]

    for date in all_dates:
        volume = next((v for d, v in feed_data if d == date), 0)
        
        total_min = sleep_data.get(date, 0)
        h = int(total_min // 60)
        m = int(total_min % 60)
        
        report_lines.append(f"🗓 **{date}**")
        report_lines.append(f"🍼 Їжа: {volume} мл")
        report_lines.append(f"😴 Сон: {h} год {m} хв")
        report_lines.append("---")

    await message.answer("\n".join(report_lines), parse_mode="Markdown")

async def main():
	database.init_db()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())