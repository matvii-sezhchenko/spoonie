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

def get_sleep_report_by_days(days=3):
	with get_connection() as conn:
		cursor = conn.cursor()

		cursor.execute('SELECT start_time, end_time FROM sleep WHERE end_time IS NOT NULL')
		rows = cursor.fetchall()

		daily_sleep = {}
		fmt = "%d.%m %H:%M"

		for start_str, end_str in rows:
			try:
				start_dt = datetime.strftime(start_str, fmt)
				end_dt = datetime.strftime(end_str, fmt)

				day_key = start_dt.startime("%d.%m.%Y")

				duration = (end_dt - start_dt).total_seconds() / 60

				daily_sleep[day_key] = daily_sleep.get(day_key, 0) + duration
			except:
				continue

	sorted_days = sorted(daily_sleep.items(), reverse=True)[:days]
	return sorted_days


def get_feeding_report(days=3):
	with get_connection() as conn:
		cursor = conn.cursor()

		cursor.execute('''
			SELECT SUM(volume_ml) FROM feedings
			WHERE timestamp >= date('now', '-3 days')
		''')

		result = cursor.fetchone()[0]

		return result if result else 0