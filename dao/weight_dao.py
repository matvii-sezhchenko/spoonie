import sqlite3
from datetime import datetime
from .base_dao import BaseDAO
from config import DATETIME_FORMAT

_MIN_WEIGHT = 1000
_MAX_WEIGHT = 30000

class WeightDAO(BaseDAO):
	def add_weight(self, user_name, weight_gram):
		if not _MIN_WEIGHT <= weight_gram <= _MAX_WEIGHT:
			raise ValueError (f"Вага має бути в межах від {_MIN_WEIGHT} до {_MAX_WEIGHT}")

		now = datetime.now().strftime(DATETIME_FORMAT)
		with self.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute(
				'''
				INSERT INTO weight (user_name, weight_gram, date_fixation)
				VALUES (?, ?, ?)
				''', (user_name, weight_gram, now)
			)
			conn.commit()

	def get_weight_history(self, days=30):
		with self.get_connection() as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()

			cursor.execute(
				'''
				SELECT user_name, weight_gram, date_fixation
				FROM weight
				WHERE date_fixation >= datetime('now', ?, 'localtime')
				ORDER BY date_fixation DESC
				''', (f'-{days} days',)
				)

			rows = cursor.fetchall()

			return [dict(row) for row in rows]