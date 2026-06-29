import sqlite3
import os

from app.config import DB_PATH

class DatabaseManager:
    def __init__ (self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _init_db (self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        current_dir = os.path.dirname(__file__)
        schema_path = os.path.join(current_dir, "schema.sql")

        if not os.path.exists(schema_path):
            raise FileNotFoundError("Error: file schema.sql not found")
        
        with open(schema_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()