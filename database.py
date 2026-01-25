import sqlite3
import logging
from datetime import datetime, timedelta

TIME_FORMAT = "%d.%m %H:%M"

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

		# Table from diapers
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS diapers(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user TEXT,
				type TEXT,
				timestamp TEXT
			)
		''')

		conn.commit()
		logging.info("База даних успішно ініціалізована")


def add_feeding(user_name, volume):
	with get_connection() as conn:
		cursor = conn.cursor()

		now = datetime.now().strftime(TIME_FORMAT)

		cursor.execute(
			'INSERT INTO feedings (user_name, volume_ml, timestamp) VALUES (?,?,?)', (user_name, volume, now)
		)

		conn.commit()


def add_sleep(user_name, action_type):
	with get_connection() as conn:
		cursor = conn.cursor()

		now = datetime.now().strftime(TIME_FORMAT)

		cursor.execute(
			'INSERT INTO sleep (user_name, start_time) VALUES (?,?)', (user_name, f"{action_type}: {now}")
		)

		conn.commit()

def get_active_sleep():
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT id, start_time, user_name FROM sleep WHERE end_time IS NULL LIMIT 1')
		return cursor.fetchone()


def start_sleep(user_name):
	now = datetime.now().strftime(TIME_FORMAT)
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			'INSERT INTO sleep (user_name, start_time) VALUES (?, ?)', (user_name, now)
		)
		conn.commit()


def finish_sleep ():
	now = datetime.now().strftime(TIME_FORMAT)
	with get_connection() as conn:
		cursor = conn.cursor()
		active_sleep = get_active_sleep()
		if active_sleep:
			sleep_id = active_sleep[0]
			cursor.execute(
				'UPDATE sleep SET end_time = ? WHERE id = ?', (now, sleep_id)
			)
			conn.commit()
			return active_sleep
		return None


def finish_sleep_auto (minutes_ago=10):
	wake_time = (datetime.now() - timedelta(minutes=minutes_ago)).strftime(TIME_FORMAT)
	with get_connection() as conn:
		cursor = conn.cursor()

		active_sleep = get_active_sleep()
		if active_sleep:
			sleep_id = active_sleep[0]
			cursor.execute(
				'UPDATE sleep SET end_time = ? WHERE id = ?', (wake_time, sleep_id)
			)
			conn.commit()
			return active_sleep
		return None


def add_diaper(user, diaper_type):
	timestamp = datetime.now().strftime(TIME_FORMAT)
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			'INSERT INTO diapers (user, type, timestamp) VALUES (?, ?, ?)',
			(user, diaper_type, timestamp)
		)
		conn.commit()


def get_last_feeding():
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT volume_ml, timestamp FROM feedings ORDER BY id DESC LIMIT 1')
		row = cursor.fetchone()
		return row


def get_full_report_data(days=3):
	with get_connection() as conn:
		cursor = conn.cursor()

		cursor.execute('''
			SELECT SUBSTR(timestamp, 1, 5) as day, COUNT(*), SUM(volume_ml)
			FROM feedings GROUP BY day ORDER BY id DESC LIMIT ?
		''', (days,))
		feeds = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

		cursor.execute('''
			SELECT SUBSTR(timestamp, 1, 5) as day, COUNT(*)
			FROM diapers WHERE type != '🤮 Зригнув'
			GROUP BY day ORDER BY id DESC LIMIT ?
		''', (days,))
		diapers = {row[0]: row[1] for row in cursor.fetchall()}

		cursor.execute('''
			SELECT SUBSTR(start_time, 1, 5) as day, start_time, end_time
			FROM sleep WHERE end_time IS NOT NULL
		''')
		sleep_rows = cursor.fetchall()
		sleep_stats = {}
		fmt = "%d.%m %H:%M"
		for day, start, end in sleep_rows:
			try:
				duration = (datetime.strptime(end, fmt) - datetime.strptime(start, fmt)).total_seconds() / 3600
				sleep_stats[day] = sleep_stats.get(day, 0) + duration
			except: continue

		# 4. Всі годування для розрахунку середнього інтервалу
		cursor.execute("SELECT timestamp FROM feedings ORDER BY id DESC LIMIT 50")
		all_times = [row[0] for row in cursor.fetchall()]

		return feeds, diapers, sleep_stats, all_times
