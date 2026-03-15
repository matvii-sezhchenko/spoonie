import logging
import sqlite3

from config import DB_NAME
from schema import TABLES

class BaseDAO:
	def __init__(self):
		self._db_name = DB_NAME

	def get_connection(self):
		return sqlite3.connect(self._db_name)
	
	def initDB (self):
		try:
			with self.get_connection() as conn:
				cursor = conn.cursor()
				for table_name, sql_query in TABLES.items():
					cursor.execute(sql_query)
					logging.info(f'Таблиця {table_name} перевірена/створена.')
				conn.commit()
				logging.info("База даних успішно ініціалізована.")
		except Exception as e:
			logging.error(f"Помилка ініціалізації БД: {e}")