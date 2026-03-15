TABLES = {
	'feedings': '''
		CREATE TABLE IF NOT EXISTS feedings(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			volume_ml INTEGER,
			timestamp TEXT
			)
	''',
	'sleep':'''
		CREATE TABLE IF NOT EXISTS sleep(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			start_time TEXT,
			end_time TEXT)
	''',
	'weight':'''
		CREATE TABLE IF NOT EXISTS weight(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			weight_gram INTEGER,
			date_fixation TEXT)
	''',
	'growth':'''
		CREATE TABLE IF NOT EXISTS growth(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			growth_cm INTEGER,
			date_fixation TEXT)
	''',
	'peepee':'''
		CREATE TABLE IF NOT EXISTS peepee(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			date_fixation TEXT)
	''',
	'poopoo':'''
		CREATE TABLE IF NOT EXISTS poopoo(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			date_fixation TEXT)
	''',
	'burped':'''
		CREATE TABLE IF NOT EXISTS burped(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			date_fixation TEXT)
	''',
	'diapers':'''
		CREATE TABLE IF NOT EXISTS diapers(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_name TEXT,
			date_fixation TEXT)
	'''
}