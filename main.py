import asyncio
import logging
import os

#env import
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# Custom modules
import keyboards
import config_buttons as btn

#Classes
from services.base_service import BaseService
from services.weight_service import WeightService
from services.growth_service import GrowthService
from services.feeding_service import FeedingService
from services.sleep_service import SleepService
from services.defecation_service import DefecationService
from services.diaper_service import DiaperService
from states import BabyStats

base_service = BaseService()
weight_service = WeightService()
growth_service = GrowthService()
feeding_service = FeedingService()
sleep_service = SleepService()
defecation_service = DefecationService()
diaper_service = DiaperService()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
	await message.answer(
		f"Вітаю, {message.from_user.first_name}! Оберіть дію:",
		reply_markup=keyboards.main_menu()
	)

@dp.message(F.text == btn.BTN_CANCEL)
async def cancel_action(message: types.Message, state: FSMContext):
	current_state = await state.get_state()

	if current_state is None:
		await message.answer(
			"Дію скасовано ❌",
			reply_markup=keyboards.main_menu()
		)

	await state.clear()
	await message.answer(
		"Дію скасовано ❌",
		reply_markup=keyboards.main_menu()
	)

#****************************FEEDINGS*********************************
@dp.message(F.text == btn.BTN_FEEDING)
async def show_feeding_menu (message: types.Message, state: FSMContext):
	text: str = feeding_service.get_one_day()
	await state.set_state(BabyStats.waiting_for_feeding_ml)
	await message.answer(
		text, 
		reply_markup=keyboards.feeding_levels(),
		parse_mode="Markdown"
	)

@dp.message(BabyStats.waiting_for_feeding_ml)
async def process_feeding(message: types.Message, state: FSMContext):
	success, result_text = feeding_service.add_new_feeding(
		message.from_user.full_name,
		message.text
	)

	if success:
		await close_active_sleep_if_exists(message)

	await message.answer(
		result_text,
		reply_markup=keyboards.main_menu()
	)

	await state.clear()

#********************************************Sleeping**********************************
@dp.message(F.text == btn.BTN_SLEEP)
async def process_sleep(message: types.Message):
	success, text_active_session = sleep_service.get_active_session()
	result_text = None

	if success:
		result_text = sleep_service.close_sleep_session()
	else:
		result_text = sleep_service.reg_sleep(message.from_user.first_name)

	await message.answer(
		result_text,
		reply_markup=keyboards.main_menu()
	)

#********************************************Defecation********************************

@dp.message(F.text == btn.BTN_DEFECATIONS)
async def show_defecation_menu(message: types.Message, state: FSMContext):
	await state.set_state(BabyStats.waiting_for_defecations)
	await message.answer(
		"Що саме зачудив?", 
		reply_markup=keyboards.defecation_menu()
	)

@dp.message(F.text == btn.BTN_PEEPEE, BabyStats.waiting_for_defecations)
async def reg_peepee(message: types.Message, state: FSMContext):
	user = message.from_user.first_name
	success, result_text = defecation_service.fix_peepee(user)
	result_text = result_text + "\n" + "Чи використано підгузок?"

	if success:
		await close_active_sleep_if_exists(message)
	
	await message.answer(
		f"{result_text}",
		reply_markup=keyboards.diaper_menu()
	)

	await state.set_state(BabyStats.waiting_for_diaper_use)

@dp.message(F.text == btn.BTN_POOPOO, BabyStats.waiting_for_defecations)
async def reg_poopoo(message: types.Message, state: FSMContext):
	user = message.from_user.first_name
	success, result_text = defecation_service.fix_poopoo(user)
	result_text = result_text + "\n" + "Чи використано підгузок?"

	if success:
		await close_active_sleep_if_exists(message)
	
	await message.answer(
		f"{result_text}",
		reply_markup=keyboards.diaper_menu()
	)

	await state.set_state(BabyStats.waiting_for_diaper_use)

@dp.message(F.text == btn.BTN_JACKPOT, BabyStats.waiting_for_defecations)
async def reg_jackpot(message: types.Message, state: FSMContext):
	user = message.from_user.first_name
	success_peepee, result_text_peepee = defecation_service.fix_peepee(user)
	success_poopoo, result_text_poopoo = defecation_service.fix_poopoo(user)
	result_text = result_text_peepee + "\n" + result_text_poopoo + "\n" + "Чи використано підгузок?"

	if success_peepee or success_poopoo:
		await close_active_sleep_if_exists(message)
	
	await message.answer(
		f"{result_text}",
		reply_markup=keyboards.diaper_menu()
	)

	await state.set_state(BabyStats.waiting_for_diaper_use)

@dp.message(F.text == btn.BTN_BURPED, BabyStats.waiting_for_defecations)
async def reg_burped(message: types.Message, state: FSMContext):
	user = message.from_user.first_name
	success, result_text = defecation_service.fix_burped(user)

	if success:
		await close_active_sleep_if_exists(message)
	
	await message.answer(
		f"{result_text}",
		reply_markup=keyboards.main_menu()
	)

	await state.clear()

@dp.message(F.text == btn.BTN_YES, BabyStats.waiting_for_diaper_use)
async def reg_use_diaper(message: types.Message, state: FSMContext):
	user = message.from_user.first_name
	success, result_text = diaper_service.fix_diaper(user)
	
	await message.answer(
		f"{result_text}",
		reply_markup=keyboards.main_menu()
	)

	await state.clear()

@dp.message(F.text == btn.BTN_NO, BabyStats.waiting_for_diaper_use)
async def diaper_not_use(message: types.Message, state: FSMContext):	
	await message.answer(
		f"🥲 Підгузок не використаний",
		reply_markup=keyboards.main_menu()
	)

	await state.clear()

# *******************************Metrics******************************
@dp.message(F.text == btn.BTN_METRIC)
async def metric_menu(message: types.Message):
	await message.answer("Що заміряємо:", reply_markup=keyboards.metric_menu())


# *******************************Baby weight******************************
@dp.message(F.text == btn.BTN_WEIGHT)
async def weight_menu(message: types.Message, state: FSMContext):
	response = "Введіть вагу малюка в грамах:"
	await message.answer(
		response,
		parse_mode="Markdown"
	)
	await state.set_state(BabyStats.waiting_for_weight)

@dp.message(BabyStats.waiting_for_weight)
async def handle_weight_input(message: types.Message, state: FSMContext):
	result_text = weight_service.add_new_weight(
		message.from_user.full_name,
		message.text
	)

	await message.answer(
		result_text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)
	await state.clear()

# *******************************Baby growth******************************
@dp.message(F.text == btn.BTN_GROWTH)
async def growth_menu(message: types.Message, state: FSMContext):
	response = "Введіть зріст малюка в сантиметрах:"
	await message.answer(
		response,
		parse_mode="Markdown"
	)
	await state.set_state(BabyStats.waiting_for_growth)

@dp.message(BabyStats.waiting_for_growth)
async def handle_growth_input(message: types.Message, state: FSMContext):
	result_text = growth_service.add_new_growth(
		message.from_user.full_name,
		message.text
	)

	await message.answer(
		result_text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)
	await state.clear()

# **********************************Reports menu*****************************
@dp.message(F.text == btn.BTN_REPORTS)
async def show_report_menu(message: types.Message):
	await message.answer("Оберіть тип звіту:", reply_markup=keyboards.report_menu())

# **********************************Short raport*****************************
@dp.message(F.text == btn.BTN_FROM_THREE_DAYS)
async def standard_report(message: types.Message):
	feeding_text = feeding_service.get_three_days_analytics()
	sleep_text = sleep_service.get_three_days_analytics()
	defecation_text = defecation_service.get_three_days_analytics()
	diaper_text = diaper_service.get_three_days_analytics()

	final_text = (
		f"{feeding_text}" 
		f"{sleep_text}"
		f"{defecation_text}"
		f"{diaper_text}"
	)

	await message.answer(
		final_text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)

# *******************************Monthly raport******************************
@dp.message(F.text == btn.BTN_FROM_MONTH)
async def monthly_report(message: types.Message):
	weight_data = weight_service.get_monthly_analytics()
	growth_data = growth_service.get_monthly_analytics()
	feeding_data = feeding_service.get_monthly_analytics()
	sleep_data = sleep_service.get_monthly_analytics()
	defecation_data = defecation_service.get_monthly_analytics()
	diaper_data = diaper_service.get_month_analytics()

	text = (
		f"📊 **Аналітика за місяць**\n"
		f"{feeding_data}"
		f"{defecation_data}"
		f"{diaper_data}"
		f"{sleep_data}"
		f"{weight_data}"
		f"{growth_data}"
	)

	await message.answer(
		text,
		parse_mode="Markdown",
		reply_markup=keyboards.main_menu()
	)

async def close_active_sleep_if_exists (message: types.Message):
	success, text_result = sleep_service.get_active_session()

	if success:
		await message.answer(
			text_result,
			parse_mode="Markdown"
		)
		
		text_result = sleep_service.close_sleep_session()
		await message.answer(
			text_result,
			parse_mode="Markdown"
		)

async def main():
	base_service.initDB()
	print("Бот запущений")
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())