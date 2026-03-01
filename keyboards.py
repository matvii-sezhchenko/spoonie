from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def main_menu () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text="🍼 Годування")
	builder.button(text="😴 Сон")
	builder.button(text="🧷 Випорожнення")
	builder.button(text="📊 Звіт")

	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)

def feeding_levels () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for ml in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 180, 210]:
		builder.button(text=f"{ml} мл")

	builder.button(text=f"Відмінити")
		
	builder.adjust(3)
	return builder.as_markup(resize_keyboard=True)

def diaper_menu () -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	builder.button(text="💦 По-малому")
	builder.button(text="💩 По-великому")
	builder.button(text="🤮 Зригнув")
	builder.button(text="🌟 Все разом")
	builder.button(text="Відмінити")

	builder.adjust(2)
	return builder.as_markup(resize_keyboard=True)

def report_menu() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.button(text="📋 Стандартний (3 дні)")
	builder.button(text="📅 Місячний звіт (30 днів)")
	builder.button(text="Відмінити")
	builder.adjust(1)
	return builder.as_markup(resize_keyboard=True)