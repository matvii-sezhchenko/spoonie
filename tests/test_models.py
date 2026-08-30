import unittest
from app.models.feeding import Feeding

class TestFeedingModel(unittest.TestCase):
    def test_feeding_initialization_with_id(self):
        feeding = Feeding(user_name="Тато", volume_ml=120, timestamp="2026-08-31 10:00:00", id=1)
        self.assertEqual(feeding.id, 1)
        self.assertEqual(feeding.user_name, "Тато")
        self.assertEqual(feeding.volume_ml, 120)
        self.assertEqual(feeding.timestamp, "2026-08-31 10:00:00")

    def test_feeding_initialization_without_id(self):
        feeding = Feeding(user_name="Мама", volume_ml=90, timestamp="2026-08-31 12:30:00")
        self.assertIsNone(feeding.id)
        self.assertEqual(feeding.user_name, "Мама")
        self.assertEqual(feeding.volume_ml, 90)
        self.assertEqual(feeding.timestamp, "2026-08-31 12:30:00")

if __name__ == "__main__":
    unittest.main()

