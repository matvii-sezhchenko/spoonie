from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🍼 Годування"))
    builder.add(KeyboardButton(text="⏳ Таймер суміші"))
    builder.add(KeyboardButton(text="⏱️ Показати таймер"))
    builder.add(KeyboardButton(text="🔄 Скинути таймер"))
    builder.add(KeyboardButton(text="📊 Звіт"))

    builder.adjust(1, 3, 1)

    return builder.as_markup(resize_keyboard=True)

def get_volumes_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    quick_volumes = ["30", "60", "90", "120", "130", "150", "160", "200"]

    for vol in quick_volumes:
        builder.add(KeyboardButton(text=vol))

    builder.add(KeyboardButton(text="❌ Скасувати"))

    builder.adjust(4, 4, 1)

    return builder.as_markup(resize_keyboard=True)

def get_mixture_timer() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="⏱️ 01:00"))
    builder.add(KeyboardButton(text="⏱️ 01:30"))
    builder.add(KeyboardButton(text="⏱️ 01:50"))
    builder.add(KeyboardButton(text="✍️ Власне ..."))

    builder.add(KeyboardButton(text="❌ Скасувати"))

    builder.adjust(3, 1, 1)
    return builder.as_markup(resize_keyboard=True)

def get_last_feeding_inline_keyboard(feeding_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✏️ Змінити об'єм", callback_data=f"feed_edit:{feeding_id}"))
    builder.add(InlineKeyboardButton(text="🗑️ Видалити", callback_data=f"feed_del:{feeding_id}"))
    builder.adjust(2)
    return builder.as_markup()

def get_delete_confirm_inline_keyboard(feeding_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Так, видалити", callback_data=f"feed_del_confirm:{feeding_id}"))
    builder.add(InlineKeyboardButton(text="❌ Скасувати", callback_data=f"feed_del_cancel:{feeding_id}"))
    builder.adjust(2)
    return builder.as_markup()


