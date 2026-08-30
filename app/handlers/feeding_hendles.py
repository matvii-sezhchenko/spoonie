from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.handlers.keyboards import get_main_keyboard, get_volumes_keyboard
from app.controllers.feeding_controller import FeedingController

class FeedingStates(StatesGroup):
    waiting_for_volume = State()

router = Router()

@router.message(F.text.in_({"🍼 Годування", "Годування"}))
async def start_feeding(message: Message, state: FSMContext, feeding_controller: FeedingController):
    info_text = feeding_controller.get_last_feeding()
    await state.set_state(FeedingStates.waiting_for_volume)
    await message.answer(
        info_text,
        reply_markup=get_volumes_keyboard()
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