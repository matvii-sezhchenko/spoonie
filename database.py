import sqlite3
import logging
from datetime import datetime

DB_NAME = 'baby_tracker.db'

def get_connection():
	return sqlite3.connect(DB_NAME)

def init_db():
	with get_connection() as conn:
		cursor = conn.cursor()

		# Table from feedings
		cursor.execute ('''
			CREATE TABLE IF NOT EXISTS feedings (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_name TEXT,
				volume_ml INTEGER,
				timestamp TEXT
			)	
		''')

		# Table from sleeping
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS sleep (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_name TEXT,
				start_time TEXT,
				end_time TEXT
			)
		''')

		conn.commit()
		logging.info("База даних успішно ініціалізована")


def add_feeding(user_name, volume):
	with get_connection() as conn:
		cursor = conn.cursor()

		now = datetime.now().strftime("%d.%m %H:%M")

		cursor.execute(
			'INSERT INTO feedings (user_name, volume_ml, timestamp) VALUES (?,?,?)', (user_name, volume, now)
		)

		conn.commit()


def add_sleep(user_name, action_type):
	with get_connection() as conn:
		cursor = conn.cursor()

		now = datetime.now().strftime("%d.%m %H:%M")

		cursor.execute(
			'INSERT INTO sleep (user_name, start_time) VALUES (?,?)', (user_name, f"{action_type}: {now}")
		)

		conn.commit()

if __name__ == "__main__":
    print("Тестуємо базу даних...")
    init_db()
    add_feeding("Тест-Тато", 120)
    print("Запис додано успішно!")