import sqlite3
from datetime import datetime
from .base_dao import BaseDAO
from config import DATETIME_FORMAT

_MIN_GROWTH = 40
_MAX_GROWTH = 150

class GrowthDAO(BaseDAO):
	def add_growth(self, user_name, growth_cm):
		if not _MIN_GROWTH <= growth_cm <= _MAX_GROWTH:
			raise ValueError(f"Зріст має бути в межах від {_MIN_GROWTH} до {_MAX_GROWTH}")

		now = datetime.now().strftime(DATETIME_FORMAT)
		with self.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute(
				'''
				INSERT INTO growth (user_name, growth_cm, date_fixation)
				VALUES (?, ?, ?)
				''', (user_name, growth_cm, now)
			)
			conn.commit()

	def get_growth_history(self, days=30):
		with self.get_connection() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()

			cursor.execute(
				'''
				SELECT user_name, growth_cm, date_fixation
				FROM growth
				WHERE date_fixation >= datetime('now', ?, 'localtime')
				ORDER BY date_fixation DESC
				''', (f'-{days} days',)
			)

			rows = cursor.fetchall()

			return [dict(row) for row in rows]