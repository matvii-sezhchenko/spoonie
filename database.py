import sqlite3
import logging

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