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

_controller: FeedingController = None

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привіт! Я твій бот-трекер. Оберіть дію на клавіатурі нижче:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "Годування")
async def start_feeding(message: Message, state: FSMContext):
    await state.set_state(FeedingStates.waiting_for_volume)
    await message.answer(
        "Оберіть стандартний об'єм або введіть свій вручну (цифрою):",
        reply_markup=get_volumes_keyboard()
    )

@router.message(StateFilter(FeedingStates.waiting_for_volume), F.text == "Скасувати")
async def cancel_feeding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Введення скасовано.",
        reply_markup=get_main_keyboard()
    )

@router.message(StateFilter(FeedingStates.waiting_for_volume))
async def handle_user_input(message: Message, state: FSMContext):
    user_input = message.text
    user_name = message.from_user.full_name
    
    if not user_input.isdigit():
        await message.answer(
            "Введіть число, введіть число",
        )
        return

    valid_number = int(user_input)
    is_success, response_text = _controller.add_feeding(user_name, valid_number)

    await state.clear()

    await message.answer(
        text=response_text,
        reply_markup=get_main_keyboard()
    )

def register_feeding_handlers(dp, controller: FeedingController):
    global _controller
    _controller = controller
    dp.include_router(router)