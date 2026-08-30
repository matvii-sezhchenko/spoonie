import sqlite3
from typing import List, Optional
from app.repository.database_manager import DatabaseManager
from app.models.feeding import Feeding
from app.repository.feeding_queries import GET_FEEDINGS_BY_DATE, INSERT_FEEDING, GET_ALL_FEEDINGS, DELETE_FEEDING, GET_LAST_FEEDING, GET_TODAYS_FEEDINGS, GET_YESTERDAYS_FEEDINGS

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
            cursor.execute(DELETE_FEEDING, (feeding_id,))
            conn.commit()

            return cursor.rowcount > 0
        
    def get_last_record(self) -> Optional[Feeding]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_LAST_FEEDING)
            row = cursor.fetchone()

            if not row:
                return None
            
            return Feeding(
                id=row[0],
                user_name=row[1],
                volume_ml=row[2],
                timestamp=row[3]
            )

    def get_todays_records(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_TODAYS_FEEDINGS)
            return cursor.fetchall()
    
    def get_yesterdays_records(self):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_YESTERDAYS_FEEDINGS)
            return cursor.fetchall()
        
    def get_records_by_date(self, date_str: str):
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_FEEDINGS_BY_DATE, (date_str,))
            return cursor.fetchall()