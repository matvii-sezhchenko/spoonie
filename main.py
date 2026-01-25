import asyncio
import logging
import os

import matplotlib.pyplot as plt
import io

import matplotlib
matplotlib.use('Agg')

from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Custom modules
import tokenTelegram
import database
import keyboards

logging.basicConfig(level=logging.INFO)


bot = Bot(token=tokenTelegram.API_TOKEN_BABY_TRACKER)

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
	await message.answer(
		f"Вітаю, {message.from_user.first_name}! Оберіть дію:",
		reply_markup=keyboards.main_menu()
	)

@dp.message(F.text == "🍼 Годування")
async def show_feeding_menu (message: types.Message):
	last_feed = database.get_last_feeding()
	
	if last_feed:
		volume, timestamp = last_feed
		time_only = timestamp.split()[1] 
		text = f"Останнє годування: **{time_only}** ({volume} мл).\n\nСкільки малюк з'їв зараз?"
	else:
		text = "Даних про годування ще немає. Скільки малюк з'їв?"

	await message.answer(
		text, 
		reply_markup=keyboards.feeding_levels(),
		parse_mode="Markdown"
	)

@dp.message(F.text == "🧷 Підгузок")
async def show_diaper_menu(message: types.Message):
	await message.answer("Що саме зачудив?", reply_markup=keyboards.diaper_menu())

@dp.message(F.text.in_(["💦 По-малому", "💩 По-великому", "🌟 Все разом", "🤮 Зригнув"]))
async def process_diaper(message: types.Message):
	user = message.from_user.first_name
	diaper_type = message.text
	
	database.add_diaper(user, diaper_type)
	
	await message.answer(
		f"✅ Записано: {diaper_type} ({user})",
		reply_markup=keyboards.main_menu()
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
			await message.answer(sleep_info)

		await message.answer(
			f"✅ Записано: {volume} мл ({user})",
			reply_markup=keyboards.main_menu()
		)
	except Exception as e:
		logging.error(f"Помилка при записі годування {e}")
		await message.answer("Ой, щось пішло не за планом")

@dp.message(F.text == "Відмінити")
async def cancel_action(message: types.Message):
	await message.answer(
		"Дію скасовано, повернення в основне меню.",
		reply_markup=keyboards.main_menu()
	)

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
async def show_report_menu(message: types.Message):
	await message.answer("Оберіть тип звіту:", reply_markup=keyboards.report_menu())

@dp.message(F.text == "📋 Стандартний (3 дні)")
async def standard_report(message: types.Message):
	feeds, diapers, sleep, all_times = database.get_full_report_data(days=3)
	
	intervals = []
	fmt = "%d.%m %H:%M"
	for i in range(len(all_times)-1):
		t1, t2 = datetime.strptime(all_times[i], fmt), datetime.strptime(all_times[i+1], fmt)
		diff = abs((t1 - t2).total_seconds() / 60)
		if diff < 600: intervals.append(diff)
	
	avg_int_total = sum(intervals)/len(intervals) if intervals else 0
	avg_h, avg_m = int(avg_int_total // 60), int(avg_int_total % 60)

	avg_diapers = sum(diapers.values()) / len(diapers) if diapers else 0
	
	avg_sleep = sum(sleep.values()) / len(sleep) if sleep else 0

	lines = [
		f"⏱ Середній інтервал годування: **{avg_h:02d}:{avg_m:02d}**",
		f"🧷 Середня зміна підгузків на добу: **{int(avg_diapers)}**",
		f"😴 Загальна кількість сну: **{int(avg_sleep)} годин**\n"
	]

	all_dates = sorted(set(list(feeds.keys()) + list(diapers.keys()) + list(sleep.keys())), reverse=True)[:3]
	current_year = datetime.now().year

	for date in all_dates:
		f_count, f_vol = feeds.get(date, (0, 0))
		d_count = diapers.get(date, 0)
		s_hours = int(sleep.get(date, 0))
		
		lines.append(f"🗓 **{date}.{current_year}:**")
		lines.append(f"Кількість прийомів їжі: {f_count}, спожитий об'єм {f_vol} мл")
		lines.append(f"Витрата підгузків: {d_count} шт")
		lines.append(f"Сон: {s_hours} годин\n")

	await message.answer("\n".join(lines), parse_mode="Markdown")


async def main():
	database.init_db()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())