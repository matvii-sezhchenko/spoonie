import sqlite3
from config import DB_NAME

class BaseDAO:
	def __init__(self):
		self._db_name = DB_NAME

	def get_connection(self):
		return sqlite3.connect(self._db_name)