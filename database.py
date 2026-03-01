import sqlite3
import logging
from datetime import datetime, timedelta

# Новий стандарт формату дат
TIME_FORMAT = "%Y-%m-%d %H:%M"

DB_NAME = 'baby_tracker.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                volume_ml INTEGER,
                timestamp TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sleep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                start_time TEXT,
                end_time TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diapers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                type TEXT,
                timestamp TEXT
            )
        ''')

        conn.commit()
        logging.info("База даних успішно ініціалізована за стандартом YYYY-MM-DD")

def add_feeding(user_name, volume):
    with get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().strftime(TIME_FORMAT)
        cursor.execute(
            'INSERT INTO feedings (user_name, volume_ml, timestamp) VALUES (?,?,?)', 
            (user_name, volume, now)
        )
        conn.commit()

def start_sleep(user_name):
    now = datetime.now().strftime(TIME_FORMAT)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sleep (user_name, start_time) VALUES (?, ?)', 
            (user_name, now)
        )
        conn.commit()

def finish_sleep():
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

def add_diaper(user, diaper_type):
    timestamp = datetime.now().strftime(TIME_FORMAT)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO diapers (user, type, timestamp) VALUES (?, ?, ?)',
            (user, diaper_type, timestamp)
        )
        conn.commit()

def get_active_sleep():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, start_time, user_name FROM sleep WHERE end_time IS NULL ORDER BY id DESC LIMIT 1')
        return cursor.fetchone()

def get_last_feeding():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT volume_ml, timestamp FROM feedings ORDER BY timestamp DESC LIMIT 1')
        return cursor.fetchone()

def get_feeding_stats(cursor, days):
    cursor.execute('''
        SELECT SUBSTR(timestamp, 1, 10) as day, COUNT(*), SUM(volume_ml)
        FROM feedings
        GROUP BY day
        ORDER BY day DESC
        LIMIT ?
    ''', (days))
    return {row[0]: (row[1], row[2]) for now in cursor.fetchall()}

def get_diaper_stats(cursor, days):
    cursor.execute('''
        SELECT SUBSTR(timestamp, 1, 10) as day, COUNT(*)
        FROM diapers
        WHERE type != '🤮 Зригнув'
        GROUP BY day
        ORDER BY day DESC
        LIMIT ?    
    ''', (days,))
    return {row[0]: row[1] for row in cursor.fetchall()}

def get_sleep_stats (cursor, days, TIME_FORMAT):
    cursor.execute('''
        SELECT SUBSTR(start_time, 1, 10) as day, start_time, end_time
        FROM sleep
        WHERE end_time IS NOT NULL AND (start_time >= date('now', ?)
    ''', (f' -{days} days',))

    rows = cursor.fetchall()
    stats = {}
    for day, start, end in rows
        try:
            duration = (datetime.strptime(end, TIME_FORMAT) -
                datetime.strptime(start, TIME_FORMAT)).total_seconds() / 3600
            stats[day] = stats.get(day, 0) + duration
        except (ValueError, TypeError):
            continue
    return stats



def get_full_report_data(days=3):
    with get_connection() as conn:
        cursor = conn.cursor()

        feeds = get_feeding_stats(cursor, days)
        diapers = get_diaper_stats(cursor, days)
        sleep = get_sleep_stats(cursor, days, TIME_FORMAT)

        cursor.execute("SELECT timestamp FROM feedings ORDER BY timestamp DESC LIMIT 50")
        history = [row[0] for row in cursor.fetchall()]

    return feeds, diapers, sleep