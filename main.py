import asyncio
import sqlite3
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=tokenTelegram.API_TOKEN)

db = Dispatcher()

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