from datetime import datetime
import sqlite3
from .base_dao import BaseDAO
from config import DATETIME_FORMAT

class SleepDAO(BaseDAO):
    def add_sleep(self, user_name, start_time=None):
        if start_time is None:
            start_time = datetime.now().strftime(DATETIME_FORMAT)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO sleep (user_name, start_time)
                VALUES (?, ?)
                ''', (user_name, start_time)
            )
            conn.commit()
            return start_time

    def close_sleep(self, end_time=None):
        if end_time is None:
            end_time = datetime.now().strftime(DATETIME_FORMAT)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE sleep 
                SET end_time=? 
                WHERE id = (
                    SELECT id
                    FROM sleep
                    WHERE end_time IS NULL
                    ORDER BY start_time DESC
                    LIMIT 1
                )
                ''', (end_time, )
            )
            conn.commit()
            return end_time

    def get_active_session_sleep(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            sql = "SELECT * FROM sleep WHERE end_time IS NULL"
            params = []

            cursor.execute(sql, tuple(params))
            row = cursor.fetchone()

            return dict(row) if row else None
        
    def get_sleep_history(self, days=1):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            sql = '''
                SELECT *
                FROM sleep
                WHERE start_time >= datetime('now', ?, 'localtime') 
                OR end_time >= datetime('now', ?, 'localtime')
                ORDER BY start_time DESC
                '''

            offset = f'-{days} days'
            cursor.execute(sql, (offset, offset, ))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]