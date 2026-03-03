DB_NAME = 'baby_tracker.db'

DATETIME_FORMAT = "%Y-%m-%d %H:%M"
DATE_ONLY_FORMAT = "%Y-%m-%d"

def format_hour_minutes(minutes_total):
    h = minutes_total // 60
    m = minutes_total % 60
    return f"{h} годин {m} хвилин"

