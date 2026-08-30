import unittest
from unittest.mock import AsyncMock, MagicMock
from aiogram.fsm.context import FSMContext

from app.handlers import main_hendles, feeding_hendles, timer_hendles
from app.handlers.feeding_hendles import FeedingStates
from app.handlers.timer_hendles import TimerHendles

class TestMainHandles(unittest.IsolatedAsyncioTestCase):
    async def test_cmd_start(self):
        message = AsyncMock()
        state = AsyncMock(spec=FSMContext)

        await main_hendles.cmd_start(message, state)

        state.clear.assert_awaited_once()
        message.answer.assert_awaited_once()
        self.assertIn("Привіт!", message.answer.call_args[0][0])

    async def test_cancel(self):
        message = AsyncMock()
        state = AsyncMock(spec=FSMContext)

        await main_hendles.cancel(message, state)

        state.clear.assert_awaited_once()
        message.answer.assert_awaited_once()
        self.assertIn("Дію скасовано", message.answer.call_args[0][0])


class TestFeedingHandles(unittest.IsolatedAsyncioTestCase):
    async def test_start_feeding(self):
        message = AsyncMock()
        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()
        controller.get_last_feeding.return_value = "Останнє годування: в 10:00"

        await feeding_hendles.start_feeding(message, state, controller)

        controller.get_last_feeding.assert_called_once()
        state.set_state.assert_awaited_once_with(FeedingStates.waiting_for_volume)
        message.answer.assert_awaited_once()
        self.assertIn("Останнє годування", message.answer.call_args[0][0])

    async def test_handle_user_input_valid(self):
        message = AsyncMock()
        message.text = "120"
        message.from_user.full_name = "Тато"

        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()
        controller.add_feeding.return_value = (True, "Запис успішно додано")

        await feeding_hendles.handle_user_input(message, state, controller)

        controller.add_feeding.assert_called_once_with("Тато", 120)
        state.clear.assert_awaited_once()
        message.answer.assert_awaited_once()
        self.assertEqual(message.answer.call_args[1]["text"], "Запис успішно додано")

    async def test_handle_user_input_invalid_non_digit(self):
        message = AsyncMock()
        message.text = "багато"
        message.from_user.full_name = "Тато"

        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()

        await feeding_hendles.handle_user_input(message, state, controller)

        controller.add_feeding.assert_not_called()
        state.clear.assert_not_awaited()
        message.answer.assert_awaited_once()
        self.assertIn("Введіть число", message.answer.call_args[0][0])

    async def test_show_daily_report(self):
        message = AsyncMock()
        controller = MagicMock()
        controller.get_daily_report.return_value = "Звіт за сьогодні"

        await feeding_hendles.show_daily_report(message, controller)

        controller.get_daily_report.assert_called_once()
        message.answer.assert_awaited_once()
        self.assertEqual(message.answer.call_args[0][0], "Звіт за сьогодні")


class TestTimerHandles(unittest.IsolatedAsyncioTestCase):
    async def test_start_timer(self):
        message = AsyncMock()
        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()

        await timer_hendles.start_timer(message, state, controller)

        state.set_state.assert_awaited_once_with(TimerHendles.waiting_for_duration)
        message.answer.assert_awaited_once()
        self.assertIn("Оберіть таймер", message.answer.call_args[0][0])

    async def test_start_timer_costum(self):
        message = AsyncMock()
        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()

        await timer_hendles.start_timer_costum(message, state, controller)

        state.set_state.assert_awaited_once_with(TimerHendles.waiting_for_duration)
        message.answer.assert_awaited_once()
        self.assertIn("Введіть час у хвилинах", message.answer.call_args[0][0])

    async def test_handle_user_input_presets(self):
        presets = [
            ("⏱️ 01:00", 60),
            ("01:00", 60),
            ("⏱️ 01:30", 90),
            ("01:30", 90),
            ("⏱️ 01:50", 110),
            ("01:50", 110),
            ("45", 45),
        ]

        for text_input, expected_minutes in presets:
            with self.subTest(text_input=text_input):
                message = AsyncMock()
                message.text = text_input
                message.from_user.full_name = "Тато"

                state = AsyncMock(spec=FSMContext)
                controller = MagicMock()
                controller.start_timer.return_value = f"Таймер успішно запущено на {expected_minutes} хв!"

                await timer_hendles.handle_user_input(message, state, controller)

                controller.start_timer.assert_called_once_with("Тато", duration_minutes=expected_minutes)
                state.clear.assert_awaited_once()
                message.answer.assert_awaited_once()

    async def test_handle_user_input_invalid(self):
        message = AsyncMock()
        message.text = "пів години"
        message.from_user.full_name = "Тато"

        state = AsyncMock(spec=FSMContext)
        controller = MagicMock()

        await timer_hendles.handle_user_input(message, state, controller)

        controller.start_timer.assert_not_called()
        state.clear.assert_not_awaited()
        message.answer.assert_awaited_once()
        self.assertIn("Будь ласка, оберіть час", message.answer.call_args[0][0])

    async def test_show_timer(self):
        message = AsyncMock()
        controller = MagicMock()
        controller.get_time_left.return_value = "Суміш придатна"

        await timer_hendles.show_timer(message, controller)

        controller.get_time_left.assert_called_once()
        message.answer.assert_awaited_once()

    async def test_reset_timer(self):
        message = AsyncMock()
        controller = MagicMock()
        controller.reset_timer.return_value = "Таймер скинуто"

        await timer_hendles.reset_timer(message, controller)

        controller.reset_timer.assert_called_once()
        message.answer.assert_awaited_once()

if __name__ == "__main__":
    unittest.main()

