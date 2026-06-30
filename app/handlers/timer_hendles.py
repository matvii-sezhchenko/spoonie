from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app import config
from app.handlers.keyboards import get_main_keyboard, get_mixture_timer

from app.controllers.mixture_controller import MixtureController

class TimerHendles(StatesGroup):
    waiting_for_duration = State()

router = Router()

@router.message(StateFilter(TimerHendles.waiting_for_duration), F.text == "Власне ...")
async def start_timer_costum(message: Message, state: FSMContext, mixture_controller: MixtureController):
    await state.set_state(TimerHendles.waiting_for_duration)
    await message.answer(
        "Введіть час у хвилинах",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "Таймер суміши")
async def start_timer(message: Message, state: FSMContext, mixture_controller: MixtureController):
    await state.set_state(TimerHendles.waiting_for_duration)
    await message.answer(
        "Оберіть таймер",
        reply_markup=get_mixture_timer()
    )

@router.message(StateFilter(TimerHendles.waiting_for_duration), )
async def handle_user_input(message: Message, state: FSMContext, mixture_controller: MixtureController):
    user_input = message.text
    duration_minutes = 0

    if user_input == "01:00":
        duration_minutes = config.TIMER_SET_ONE
    elif user_input == "01:30":
        duration_minutes = config.TIMER_SET_ONE_HALF
    elif user_input == "02:00":
        duration_minutes = config.TIMER_SET_FULL
    elif user_input.isdigit():
        duration_minutes = int(user_input)
    else:
        await message.answer("Будь ласка, оберіть час із кнопок або введіть число.")
        return
    
    await state.clear()
    await message.answer(
        f"Таймер запущено на {duration_minutes} хв!",
        reply_markup=get_main_keyboard()
    )