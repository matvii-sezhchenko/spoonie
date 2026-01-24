from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def main_menu () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text="🍼 Годування")
	builder.button(text="😴 Сон")
    builder.button(text="📊 Звіт")

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def feeding_levels () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for ml in [30, 60, 90, 120, 150, 180, 210]:
		builder.button(text=f"{ml} мл")
		
	builder.adjust(3)
	return builder.as_markup(resize_keyboard=True)