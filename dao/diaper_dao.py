import sqlite3
from datetime import datetime
from .base_dao import BaseDAO
from config import DATETIME_FORMAT

class DiaperDAO(BaseDAO):
    def add_used_diaper(self, user_name):        
        now = datetime.now().strftime(DATETIME_FORMAT)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO diapers (user_name, date_fixation)
                VALUES (?, ?)
                ''', (user_name, now)
            )
            conn.commit()

    def get_use_diaper_history(self, days=30):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                '''
                    SELECT user_name, date_fixation
                    FROM diapers
                    WHERE date_fixation >= datetime('now', 'localtime', 'start of day', ?)
                    ORDER BY date_fixation DESC
                ''', (f'-{days} days',)
            )

            rows = cursor.fetchall()

            return [dict(row) for row in rows]