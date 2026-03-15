import sqlite3
from datetime import datetime
from .base_dao import BaseDAO
from config import DATETIME_FORMAT

_MIN_VALUE = 10
_MAX_VALUE = 200

class FeedingDAO(BaseDAO):
    def add_feeding(self, user_name, volume_ml):
        if not (_MIN_VALUE <= volume_ml <=_MAX_VALUE):
            raise ValueError(f"Об'єм має бути в межах від {_MIN_VALUE} до {_MAX_VALUE} мл.")
        
        now = datetime.now().strftime(DATETIME_FORMAT)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO feedings (user_name, volume_ml, timestamp)
                VALUES (?, ?, ?)
                ''', (user_name, volume_ml, now)
            )
            conn.commit()

    def get_feeding_history(self, days=30):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                '''
                    SELECT user_name, volume_ml, timestamp
                    FROM feedings
                    WHERE timestamp >= datetime('now', 'localtime', 'start of day', ?)
                    ORDER BY timestamp DESC
                ''', (f'-{days} days',)
            )

            rows = cursor.fetchall()

            return [dict(row) for row in rows]