import unittest
from unittest.mock import MagicMock
from pathlib import Path
import tempfile
import json
import os
from datetime import datetime, timedelta

from app.models.feeding import Feeding
from app.controllers.feeding_controller import FeedingController
from app.controllers.mixture_controller import MixtureController
from app import config

class TestFeedingController(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.controller = FeedingController(self.mock_repo)

    def test_add_feeding_success(self):
        self.mock_repo.save.return_value = (True, 1)
        success, msg = self.controller.add_feeding("Тато", 120)
        self.assertTrue(success)
        self.assertEqual(msg, "Запис успішно додано")
        self.mock_repo.save.assert_called_once()

    def test_add_feeding_failure(self):
        self.mock_repo.save.return_value = (False, 0)
        success, msg = self.controller.add_feeding("Мама", 90)
        self.assertFalse(success)
        self.assertEqual(msg, "Не вдалось записати")

    def test_get_last_feeding_empty(self):
        self.mock_repo.get_last_record.return_value = None
        result = self.controller.get_last_feeding()
        self.assertIn("Записи відсутні", result)

    def test_get_last_feeding_with_data_full_format(self):
        sample_feeding = Feeding(
            id=1,
            user_name="Тато",
            volume_ml=130,
            timestamp="2026-08-31 14:45:00"
        )
        self.mock_repo.get_last_record.return_value = sample_feeding
        result = self.controller.get_last_feeding()
        self.assertIn("Останнє годування: в 14:45", result)
        self.assertIn("Тато", result)
        self.assertIn("130 мл", result)

    def test_delete_feeding_success(self):
        self.mock_repo.delete_by_id.return_value = True
        success, msg = self.controller.delete_feeding(1)
        self.assertTrue(success)
        self.assertIn("успішно видалено", msg)

    def test_delete_feeding_failure(self):
        self.mock_repo.delete_by_id.return_value = False
        success, msg = self.controller.delete_feeding(999)
        self.assertFalse(success)
        self.assertIn("Не вдалося видалити", msg)

    def test_update_feeding_volume_success(self):
        self.mock_repo.update_volume_by_id.return_value = True
        success, msg = self.controller.update_feeding_volume(1, 150)
        self.assertTrue(success)
        self.assertIn("150 мл", msg)

    def test_update_feeding_volume_failure(self):
        self.mock_repo.update_volume_by_id.return_value = False
        success, msg = self.controller.update_feeding_volume(999, 150)
        self.assertFalse(success)
        self.assertIn("Не вдалося оновити", msg)

    def test_get_last_feeding_info_with_data(self):
        sample_feeding = Feeding(
            id=42,
            user_name="Тато",
            volume_ml=130,
            timestamp="2026-08-31 14:45:00"
        )
        self.mock_repo.get_last_record.return_value = sample_feeding
        text, fid = self.controller.get_last_feeding_info()
        self.assertEqual(fid, 42)
        self.assertIn("130 мл", text)

    def test_get_last_feeding_info_empty(self):
        self.mock_repo.get_last_record.return_value = None
        text, fid = self.controller.get_last_feeding_info()
        self.assertIsNone(fid)
        self.assertIn("Записи відсутні", text)

    def test_get_last_feeding_with_data_short_format(self):
        sample_feeding = Feeding(
            id=2,
            user_name="Мама",
            volume_ml=90,
            timestamp="2026-08-31 09:15"
        )
        self.mock_repo.get_last_record.return_value = sample_feeding
        result = self.controller.get_last_feeding()
        self.assertIn("Останнє годування: в 09:15", result)
        self.assertIn("Мама", result)
        self.assertIn("90 мл", result)

    def test_get_daily_report_today_has_records(self):
        records = [
            ("2026-08-31 08:00:00", 90, "Тато"),
            ("2026-08-31 12:00:00", 120, "Мама"),
        ]
        self.mock_repo.get_records_by_date.side_effect = lambda d: records if d == datetime.now().strftime("%Y-%m-%d") else []
        result = self.controller.get_daily_report()
        self.assertIn("ЗВІТ ЗА СЬОГОДНІ", result)
        self.assertIn("Всього годувань: 2", result)
        self.assertIn("Загальний об'єм: 210 мл", result)
        self.assertIn("08:00 — 90 мл (Тато)", result)
        self.assertIn("12:00 — 120 мл (Мама)", result)

    def test_get_daily_report_fallback_to_yesterday(self):
        records = [
            ("2026-08-30 19:30:00", 150, "Бабуся"),
        ]
        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        def side_effect(date_str):
            if date_str == today_str:
                return []
            elif date_str == yesterday_str:
                return records
            return []

        self.mock_repo.get_records_by_date.side_effect = side_effect
        result = self.controller.get_daily_report()
        self.assertIn("ЗА СЬОГОДНІ ПУСТО. ЗВІТ ЗА ВЧОРА", result)
        self.assertIn("Всього годувань: 1", result)
        self.assertIn("Загальний об'єм: 150 мл", result)

    def test_get_daily_report_empty(self):
        self.mock_repo.get_records_by_date.return_value = []
        result = self.controller.get_daily_report()
        self.assertIn("За сьогодні записів ще немає", result)


class TestMixtureController(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = Path(self.temp_dir.name) / "test_timer.json"
        self.controller = MixtureController()
        self.controller.file_path = self.test_file_path

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_start_timer(self):
        res = self.controller.start_timer(user_name="Тато", duration_minutes=60)
        self.assertIn("Таймер успішно запущено на 60 хв!", res)
        self.assertTrue(self.test_file_path.exists())

        with open(self.test_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["user_name"], "Тато")
        self.assertEqual(data["duration"], 60)
        self.assertIn("start_time", data)

    def test_reset_timer(self):
        self.controller.start_timer(user_name="Мама", duration_minutes=90)
        self.assertTrue(self.test_file_path.exists())

        res = self.controller.reset_timer()
        self.assertIn("Таймер придатності суміші скинуто!", res)
        self.assertFalse(self.test_file_path.exists())

    def test_get_time_left_not_started(self):
        res = self.controller.get_time_left()
        self.assertIn("Таймер не запущений", res)

    def test_get_time_left_active(self):
        # Set start_time 10 minutes ago with duration 60 minutes -> 50 min left
        start_time = datetime.now() - timedelta(minutes=10)
        timer_data = {
            "start_time": start_time.strftime(config.DATE_TIME_FORMAT),
            "user_name": "Тато",
            "duration": 60
        }
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            json.dump(timer_data, f)

        res = self.controller.get_time_left()
        self.assertIn("Суміш придатна! ✅", res)
        self.assertIn("Залишилось:", res)
        self.assertIn("Тато", res)

    def test_get_time_left_expired(self):
        # Set start_time 120 minutes ago with duration 60 minutes -> expired
        start_time = datetime.now() - timedelta(minutes=120)
        timer_data = {
            "start_time": start_time.strftime(config.DATE_TIME_FORMAT),
            "user_name": "Мама",
            "duration": 60
        }
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            json.dump(timer_data, f)

        res = self.controller.get_time_left()
        self.assertIn("Суміш ПРОТЕРМІНОВАНА! ❌", res)
        self.assertIn("Мама", res)

if __name__ == "__main__":
    unittest.main()

