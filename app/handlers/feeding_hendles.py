from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.handlers.keyboards import (
    get_main_keyboard,
    get_volumes_keyboard,
    get_last_feeding_inline_keyboard,
    get_delete_confirm_inline_keyboard
)
from app.controllers.feeding_controller import FeedingController

class FeedingStates(StatesGroup):
    waiting_for_volume = State()
    waiting_for_edit_volume = State()

router = Router()

@router.message(F.text.in_({"🍼 Годування", "Годування"}))
async def start_feeding(message: Message, state: FSMContext, feeding_controller: FeedingController):
    info_text, last_id = feeding_controller.get_last_feeding_info()
    await state.set_state(FeedingStates.waiting_for_volume)

    if last_id is not None:
        await message.answer(
            info_text,
            reply_markup=get_last_feeding_inline_keyboard(last_id)
        )
        await message.answer(
            "Оберіть або введіть об'єм годування (мл):",
            reply_markup=get_volumes_keyboard()
        )
    else:
        await message.answer(
            info_text,
            reply_markup=get_volumes_keyboard()
        )

@router.callback_query(F.data.startswith("feed_del:"))
async def on_feed_delete_request(callback: CallbackQuery):
    feeding_id = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=get_delete_confirm_inline_keyboard(feeding_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("feed_del_confirm:"))
async def on_feed_delete_confirm(callback: CallbackQuery, state: FSMContext, feeding_controller: FeedingController):
    feeding_id = int(callback.data.split(":")[1])
    success, msg = feeding_controller.delete_feeding(feeding_id)
    await state.clear()
    if success:
        await callback.message.edit_text(f"====================================\n{msg}\n====================================")
    else:
        await callback.message.edit_text(msg)
    await callback.answer("Запис видалено" if success else "Помилка")

@router.callback_query(F.data.startswith("feed_del_cancel:"))
async def on_feed_delete_cancel(callback: CallbackQuery):
    feeding_id = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=get_last_feeding_inline_keyboard(feeding_id)
    )
    await callback.answer("Видалення скасовано")

@router.callback_query(F.data.startswith("feed_edit:"))
async def on_feed_edit_request(callback: CallbackQuery, state: FSMContext):
    feeding_id = int(callback.data.split(":")[1])
    await state.update_data(edit_feeding_id=feeding_id)
    await state.set_state(FeedingStates.waiting_for_edit_volume)
    await callback.message.answer(
        "✏️ Оберіть або введіть новий об'єм (мл):",
        reply_markup=get_volumes_keyboard()
    )
    await callback.answer()

@router.message(StateFilter(FeedingStates.waiting_for_edit_volume))
async def handle_edit_user_input(message: Message, state: FSMContext, feeding_controller: FeedingController):
    user_input = message.text
    if not user_input.isdigit():
        await message.answer("Введіть число, будь ласка.")
        return

    data = await state.get_data()
    feeding_id = data.get("edit_feeding_id")
    valid_number = int(user_input)

    if feeding_id:
        is_success, response_text = feeding_controller.update_feeding_volume(feeding_id, valid_number)
    else:
        is_success, response_text = False, "Не знайдено запис для редагування."

    await state.clear()
    await message.answer(
        text=response_text,
        reply_markup=get_main_keyboard()
    )

@router.message(StateFilter(FeedingStates.waiting_for_volume))
async def handle_user_input(message: Message, state: FSMContext, feeding_controller: FeedingController):
    user_input = message.text
    user_name = message.from_user.full_name
    
    if not user_input.isdigit():
        await message.answer(
            "Введіть число, введіть число",
        )
        return

    valid_number = int(user_input)
    is_success, response_text = feeding_controller.add_feeding(user_name, valid_number)

    await state.clear()

    await message.answer(
        text=response_text,
        reply_markup=get_main_keyboard()
    )

@router.message(F.text.in_({"📊 Звіт", "Звіт"}))
async def show_daily_report(message: Message, feeding_controller: FeedingController):
    response_text = feeding_controller.get_daily_report()
    await message.answer(response_text, reply_markup=get_main_keyboard())