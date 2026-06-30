import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN not found into file .env")

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT_UK = "%d.%m.%Y %H:%M:%S"
DATE_FORMAT_UK = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"

DB_DIR = "database"
DB_NAME = "BTDB.db"
DB_PATH = f"{DB_DIR}/{DB_NAME}"

TIMER_FILE_PATH = Path(__file__).resolve().parent.parent / "jsons" / "mixture_timer.json"
TIMER_SET_HOUR = 60
TIMER_SET_ONE_HALF = 90
TIMER_SET_FULL = 120

