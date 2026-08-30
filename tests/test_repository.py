import unittest
import tempfile
import os
from app.models.feeding import Feeding
from app.repository.database_manager import DatabaseManager
from app.repository.feeding_repository import FeedingRepository

class TestRepository(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for isolation
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

        self.db_manager = DatabaseManager(db_path=self.temp_db_path)
        self.repo = FeedingRepository(self.db_manager)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_database_initialization(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedings';")
            table = cursor.fetchone()
            self.assertIsNotNone(table)
            self.assertEqual(table[0], "feedings")

    def test_save_and_get_all(self):
        feeding1 = Feeding(user_name="Тато", volume_ml=120, timestamp="2026-08-31 08:00:00")
        success, fid = self.repo.save(feeding1)
        self.assertTrue(success)
        self.assertGreater(fid, 0)

        feeding2 = Feeding(user_name="Мама", volume_ml=90, timestamp="2026-08-31 11:30:00")
        self.repo.save(feeding2)

        records = self.repo.get_all()
        self.assertEqual(len(records), 2)
        # Ordered by timestamp DESC
        self.assertEqual(records[0].user_name, "Мама")
        self.assertEqual(records[0].volume_ml, 90)
        self.assertEqual(records[1].user_name, "Тато")
        self.assertEqual(records[1].volume_ml, 120)

    def test_get_last_record(self):
        # When empty
        self.assertIsNone(self.repo.get_last_record())

        # After adding records
        self.repo.save(Feeding(user_name="User1", volume_ml=60, timestamp="2026-08-31 06:00:00"))
        self.repo.save(Feeding(user_name="User2", volume_ml=120, timestamp="2026-08-31 09:00:00"))

        last = self.repo.get_last_record()
        self.assertIsNotNone(last)
        self.assertEqual(last.user_name, "User2")
        self.assertEqual(last.volume_ml, 120)
        self.assertEqual(last.timestamp, "2026-08-31 09:00:00")

    def test_get_records_by_date(self):
        self.repo.save(Feeding(user_name="User1", volume_ml=90, timestamp="2026-08-30 20:00:00"))
        self.repo.save(Feeding(user_name="User2", volume_ml=120, timestamp="2026-08-31 08:00:00"))
        self.repo.save(Feeding(user_name="User3", volume_ml=150, timestamp="2026-08-31 12:00:00"))

        records_31 = self.repo.get_records_by_date("2026-08-31")
        self.assertEqual(len(records_31), 2)
        self.assertEqual(records_31[0][2], "User2")  # timestamp ASC
        self.assertEqual(records_31[1][2], "User3")

        records_30 = self.repo.get_records_by_date("2026-08-30")
        self.assertEqual(len(records_30), 1)
        self.assertEqual(records_30[0][2], "User1")

        records_empty = self.repo.get_records_by_date("2026-01-01")
        self.assertEqual(len(records_empty), 0)

    def test_delete_by_id(self):
        _, fid = self.repo.save(Feeding(user_name="Тато", volume_ml=130, timestamp="2026-08-31 10:00:00"))
        self.assertEqual(len(self.repo.get_all()), 1)

        result = self.repo.delete_by_id(fid)
        self.assertTrue(result)
        self.assertEqual(len(self.repo.get_all()), 0)

        # Deleting non-existent ID
        result_false = self.repo.delete_by_id(9999)
        self.assertFalse(result_false)

    def test_get_todays_and_yesterdays_records(self):
        # Test method calls without syntax or runtime error
        todays = self.repo.get_todays_records()
        self.assertIsInstance(todays, list)

        yesterdays = self.repo.get_yesterdays_records()
        self.assertIsInstance(yesterdays, list)

if __name__ == "__main__":
    unittest.main()

