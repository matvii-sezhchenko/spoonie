from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import TIMER_SET_FULL, TIMER_SET_ONE_HALF, TIMER_SET_HOUR

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="Годування"))
    builder.add(KeyboardButton(text="Таймер суміши"))
    builder.add(KeyboardButton(text="Показати таймер"))
    builder.add(KeyboardButton(text="Скинути таймер придатності"))
    builder.add(KeyboardButton(text="Звіт"))

    builder.adjust(1,3,1)

    return builder.as_markup(resize_keyboard=True)

def get_volumes_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    quick_volumes = ["30", "60", "90", "120", "130", "150", "160", "200"]

    for vol in quick_volumes:
        builder.add(KeyboardButton(text=vol))

    builder.add(KeyboardButton(text="Скасувати"))

    builder.adjust(4, 4, 1)

    return builder.as_markup(resize_keyboard=True)

def get_mixture_timer() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="01:00"))
    builder.add(KeyboardButton(text="01:30"))
    builder.add(KeyboardButton(text="02:00"))
    builder.add(KeyboardButton(text="Власне ..."))

    builder.add(KeyboardButton(text="Скасувати"))

    builder.adjust(3, 1, 1)
    return builder.as_markup(resize_keyboard=True)

