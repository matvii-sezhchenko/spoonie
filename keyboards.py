from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
import config_buttons as btn

def main_menu () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text=btn.BTN_FEEDING)
	builder.button(text=btn.BTN_SLEEP)
	builder.button(text=btn.BTN_DEFECATIONS)
	builder.button(text=btn.BTN_METRIC)
	builder.button(text=btn.BTN_REPORTS)

	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)

def feeding_levels () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	for ml in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]:
		builder.button(text=f"{ml} мл")
	builder.adjust(3)

	cancel_builder = ReplyKeyboardBuilder()
	cancel_builder.button(text=btn.BTN_CANCEL)
	builder.attach(cancel_builder)
	return builder.as_markup(resize_keyboard=True)

def diaper_menu () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text=btn.BTN_PEEPEE)
	builder.button(text=btn.BTN_POOPOO)
	builder.button(text=btn.BTN_ALL_DIAPER)
	builder.button(text=btn.BTN_BURPED)
	builder.button(text=btn.BTN_CANCEL)
	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)

def report_menu() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text=btn.BTN_FROM_THREE_DAYS)
	builder.button(text=btn.BTN_FROM_MONTH)
	builder.button(text=btn.BTN_CANCEL)
	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)

def metric_menu() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text=btn.BTN_WEIGHT)
	builder.button(text=btn.BTN_GROWTH)
	builder.button(text=btn.BTN_CANCEL)
	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)