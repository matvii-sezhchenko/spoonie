from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.handlers.keyboards import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привіт! Я твій бот-трекер. Оберіть дію на клавіатурі нижче:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text.in_({"❌ Скасувати", "Скасувати"}))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Дію скасовано.",
        reply_markup=get_main_keyboard()
    )