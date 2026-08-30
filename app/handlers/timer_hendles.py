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

@router.message(StateFilter(TimerHendles.waiting_for_duration), F.text.in_({"✍️ Власне ...", "Власне ...", "✍️ Власне..."}))
async def start_timer_costum(message: Message, state: FSMContext, mixture_controller: MixtureController):
    await state.set_state(TimerHendles.waiting_for_duration)
    await message.answer(
        "Введіть час у хвилинах",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.in_({"⏳ Таймер суміші", "Таймер суміші", "⏰ Таймер суміші", "Таймер суміши", "⏳ Таймер суміши"}))
async def start_timer(message: Message, state: FSMContext, mixture_controller: MixtureController):
    await state.set_state(TimerHendles.waiting_for_duration)
    await message.answer(
        "Оберіть таймер",
        reply_markup=get_mixture_timer()
    )

@router.message(StateFilter(TimerHendles.waiting_for_duration))
async def handle_user_input(message: Message, state: FSMContext, mixture_controller: MixtureController):
    user_input = message.text
    duration_minutes = 0

    if user_input in ("01:00", "⏱️ 01:00", "⏱ 01:00"):
        duration_minutes = getattr(config, "TIMER_SET_HOUR", 60)
    elif user_input in ("01:30", "⏱️ 01:30", "⏱ 01:30"):
        duration_minutes = getattr(config, "TIMER_SET_ONE_HALF", 90)
    elif user_input in ("01:50", "⏱️ 01:50", "⏱ 01:50"):
        duration_minutes = getattr(config, "TIMER_SET_FULL", 110)
    elif user_input.isdigit():
        duration_minutes = int(user_input)
    else:
        await message.answer("Будь ласка, оберіть час із кнопок або введіть число.")
        return
    
    text_answer = mixture_controller.start_timer(message.from_user.full_name, duration_minutes=duration_minutes)
    
    await state.clear()
    await message.answer(
        text_answer,
        reply_markup=get_main_keyboard()
    )

@router.message(F.text.in_({"⏱️ Показати таймер", "Показати таймер"}))
async def show_timer(message: Message, mixture_controller: MixtureController):
    response_text = mixture_controller.get_time_left()
    await message.answer(response_text, reply_markup=get_main_keyboard())


@router.message(F.text.in_({"🔄 Скинути таймер", "Скинути таймер"}))
async def reset_timer(message: Message, mixture_controller: MixtureController):
    response_text = mixture_controller.reset_timer()
    await message.answer(response_text, reply_markup=get_main_keyboard())