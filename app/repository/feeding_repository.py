import sqlite3
from typing import List
from app.repository.database_manager import DatabaseManager
from app.models.feeding import Feeding
from app.repository.feeding_queries import INSERT_FEEDING, GET_ALL_FEEDINGS, DELETE_FEEDING

class FeedingRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save (self, feeding: Feeding) -> tuple[bool, int]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_FEEDING, (feeding.user_name, feeding.volume_ml, feeding.timestamp))

            genereted_id = cursor.lastrowid

            if genereted_id and genereted_id > 0:
                return True, genereted_id
            else:
                return False, 0
            

    def get_all(self) -> List[Feeding]:
        feedings = []
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_ALL_FEEDINGS)
            rows = cursor.fetchall()

            for row in rows:
                feedings_obj = Feeding(
                    id=row[0],
                    user_name=row[1],
                    volume_ml=row[2],
                    timestamp=row[3]
                )
                feedings.append(feedings_obj)
        
        return feedings

    def delete_by_id(self, feeding_id: int) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETE_FEEDING, (feeding_id))
            conn.commit()

            return cursor.rowcount > 0