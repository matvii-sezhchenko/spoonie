import sqlite3
import logging
from datetime import datetime

def init_db():
	conn = sqlite3.connect('baby_tracker.db')
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
	conn.close()
	logging.info("База даних успішно ініціалізована")
	

def add_feeding(user_name, volume):
	conn = sqlite3.connect('baby_tracker.db')
	cursor = conn.cursor()

	now = datetime.now().strftime("%d.%m %H:%M")

	cursor.execute(
		'INSERT INTO feedings (user_name, volume_ml, timestamp) VALUES (?,?,?)', (user_name, volume, now)
	)

	conn.commit()
	conn.close()


def add_sleep(user_name, action_type):
	conn = sqlite3.connect('baby_tracker.db')
	cursor = conn.cursor()

	now = datetime.now().strftime("%d.%m %H:%M")

	cursor.execute(
		'INSERT INTO sleep (user_name, start_time) VALUES (?,?)', (user_name, f"{action_type}: {now}")
	)

	conn.commit()
	conn.close()