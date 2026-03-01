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

#Classes
from services.weight_service import WeightService

weight_service = WeightService()

logging.basicConfig(level=logging.INFO)

DB_TIME_FORMAT = "%Y-%m-%d %H:%M"


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

@dp.message(F.text == "🧷 Випорожнення")
async def show_diaper_menu(message: types.Message):
	await message.answer("Що саме зачудив?", reply_markup=keyboards.diaper_menu())

@dp.message(F.text.in_(["💦 По-малому", "💩 По-великому", "🌟 Все разом", "🤮 Зригнув"]))
async def process_diaper(message: types.Message):
	user = message.from_user.first_name
	diaper_type = message.text
	await close_active_sleep_if_exists(message)
	
	database.add_diaper(user, diaper_type)
	
	await message.answer(
		f"✅ Записано: {diaper_type} ({user})",
		reply_markup=keyboards.main_menu()
	)

async def close_active_sleep_if_exists (message: types.Message):
	active_sleep = database.get_active_sleep()

	if active_sleep:
		database.finish_sleep_by_action()

		start_id, start_time, start_user = active_sleep
		text = (
			f"ℹ️ **Автоматично закрито сон**\n"
			f"Малюк заснув о {start_time} (відмітив {start_user}).\n")
		await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.endswith("мл"))
async def process_feeding(message: types.Message):
	user = message.from_user.first_name

	try:
		volume = int (message.text.split()[0])
		database.add_feeding(user, volume)

		await close_active_sleep_if_exists(message)
		
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
		"Повернено в головне меню",
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

def calculate_average_interval(all_times, DB_TIME_FORMAT):
	intervals = []
	for i in range(len(all_times)-1):
		try:
			t1 = datetime.strptime(all_times[i], DB_TIME_FORMAT)
			t2 = datetime.strptime(all_times[i+1], DB_TIME_FORMAT)
			diff = abs((t1 - t2).total_seconds() / 60)

			if 30 < diff < 600:
				intervals.append(diff)
		except (ValueError, TypeError):
			continue

	if not intervals:
		return 0
	return sum(intervals) / len(intervals)

# **********************************Short raport*****************************
@dp.message(F.text == "📋 Стандартний (3 дні)")
async def standard_report(message: types.Message):
	feeds, diapers, sleep, all_times = database.get_full_report_data(days=2)
	avg_int_total = calculate_average_interval(all_times, DB_TIME_FORMAT)
	avg_h, avg_m = int(avg_int_total // 60), int(avg_int_total % 60)
	lines = [f"⏱ Середній інтервал годування: **{avg_h:02d}:{avg_m:02d}**\n"]


	all_dates = sorted(set(list(feeds.keys()) + list(diapers.keys()) + list(sleep.keys())), reverse=True)

	if not all_dates:
		await message.answer("Статистика поки порожня. Додайте перші дані!", reply_markup=keyboards.main_menu())
		return

	for date_str in all_dates:
		f_count, f_vol = feeds.get(date_str, (0, 0))
		d_count = diapers.get(date_str, 0)
		s_hours = sleep.get(date_str, 0)

		try:
			display_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m")
		except ValueError:
			display_date = date_str

		lines.append(f"🗓 **{display_date}:**")
		lines.append(f"🍼 Годувань: {f_count} (всього {f_vol} мл)")
		lines.append(f"🧷 Підгузків: {d_count} шт")
		lines.append(f"😴 Сон: {s_hours:.1f} годин\n")

	await message.answer("\n".join(lines), parse_mode="Markdown", reply_markup=keyboards.main_menu())

# *******************************Monthly raport******************************
@dp.message(F.text == "📅 Місячний звіт (30 днів)")
async def monthly_report(message: types.Message):
	sum_ml, count_diapers, avg_sleep = database.get_monthly_report_data(30)
	weight_data = weight_service.get_monthly_analytics()
	text = (
		f"📊 **Аналітика за місяць**\n"
		f"━━━━━━━━━━━━━━━\n"
		f"🍼 Спожито суміші: **{sum_ml} л**\n"
		f"🧷 Використано підгузків: **{count_diapers} шт**\n"
		f"😴 Сон (сер. за добу): **{avg_sleep} год**\n"
		f"━━━━━━━━━━━━━━━\n"
		f"{weight_data}"
	)

	await message.answer(
		text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)

# *******************************Weight******************************
@dp.message(F.text == "⚖️ Вага")
async def weight_menu(message: types.Message):
	response = "Введіть вагу малюка в грамах:"
	await message.answer(
		response,
		parse_mode="Markdown"
	)

@dp.message(lambda m: m.text.isdigit())
async def handle_weight_input(message: types.Message):
	result_text = weight_service.add_new_weight(
		message.from_user.full_name,
		message.text
	)

	await message.answer(
		result_text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)


async def main():
	database.init_db()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())