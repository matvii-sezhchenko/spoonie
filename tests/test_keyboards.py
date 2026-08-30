import unittest
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from app.handlers.keyboards import (
    get_main_keyboard,
    get_volumes_keyboard,
    get_mixture_timer,
    get_last_feeding_inline_keyboard,
    get_delete_confirm_inline_keyboard
)

class TestKeyboards(unittest.TestCase):
    def test_main_keyboard(self):
        kb = get_main_keyboard()
        self.assertIsInstance(kb, ReplyKeyboardMarkup)
        
        # Flatten all buttons from keyboard rows
        button_texts = [btn.text for row in kb.keyboard for btn in row]
        expected_buttons = [
            "🍼 Годування",
            "⏳ Таймер суміші",
            "⏱️ Показати таймер",
            "🔄 Скинути таймер",
            "📊 Звіт"
        ]
        for expected in expected_buttons:
            self.assertIn(expected, button_texts)
        self.assertEqual(len(button_texts), 5)

    def test_volumes_keyboard(self):
        kb = get_volumes_keyboard()
        self.assertIsInstance(kb, ReplyKeyboardMarkup)

        button_texts = [btn.text for row in kb.keyboard for btn in row]
        expected_volumes = ["30", "60", "90", "120", "130", "150", "160", "200"]
        for vol in expected_volumes:
            self.assertIn(vol, button_texts)
        self.assertIn("❌ Скасувати", button_texts)
        self.assertEqual(len(button_texts), 9)

    def test_mixture_timer_keyboard(self):
        kb = get_mixture_timer()
        self.assertIsInstance(kb, ReplyKeyboardMarkup)

        button_texts = [btn.text for row in kb.keyboard for btn in row]
        expected_buttons = [
            "⏱️ 01:00",
            "⏱️ 01:30",
            "⏱️ 01:50",
            "✍️ Власне ...",
            "❌ Скасувати"
        ]
        for btn in expected_buttons:
            self.assertIn(btn, button_texts)
        self.assertEqual(len(button_texts), 5)

    def test_last_feeding_inline_keyboard(self):
        kb = get_last_feeding_inline_keyboard(123)
        self.assertIsInstance(kb, InlineKeyboardMarkup)

        buttons = [btn for row in kb.inline_keyboard for btn in row]
        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0].text, "✏️ Змінити об'єм")
        self.assertEqual(buttons[0].callback_data, "feed_edit:123")
        self.assertEqual(buttons[1].text, "🗑️ Видалити")
        self.assertEqual(buttons[1].callback_data, "feed_del:123")

    def test_delete_confirm_inline_keyboard(self):
        kb = get_delete_confirm_inline_keyboard(123)
        self.assertIsInstance(kb, InlineKeyboardMarkup)

        buttons = [btn for row in kb.inline_keyboard for btn in row]
        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0].text, "✅ Так, видалити")
        self.assertEqual(buttons[0].callback_data, "feed_del_confirm:123")
        self.assertEqual(buttons[1].text, "❌ Скасувати")
        self.assertEqual(buttons[1].callback_data, "feed_del_cancel:123")

if __name__ == "__main__":
    unittest.main()

