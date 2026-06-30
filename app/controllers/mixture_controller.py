import json
from datetime import datetime, timedelta

from app import config

class MixtureController:
    def __init__(self):
        self.file_path = config.TIMER_FILE_PATH

    def start_timer(self, user_name: str, duration_minutes: int) -> str:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        current_time_str = datetime.now().strftime(config.DATE_TIME_FORMAT)

        timer_data = {
            "start_time": current_time_str,
            "user_name": user_name,
            "duration": duration_minutes
        }
    
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(timer_data, f, ensure_ascii=False, indent=4)

        return f"Таймер успішно запущено на {duration_minutes} хв!"
    
    def reset_timer(self) -> str:
        self.file_path.unlink(missing_ok=True)
        return "Таймер придатності суміші скинуто! 🗑️"
            

    def get_time_left(self) -> str:
        if not self.file_path.exists(): return "=================================\nТаймер не запущений ⏱️\n================================="

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        start_dt = datetime.strptime(data["start_time"], config.DATE_TIME_FORMAT)
        duration = data["duration"]

        end_dt = start_dt + timedelta(minutes=duration)
        now = datetime.now()

        end_time_str = end_dt.strftime(config.DATE_TIME_FORMAT_UK)

        if now > end_dt:
            return f"""====================================
⏱️ Суміш ПРОТЕРМІНОВАНА! ❌
Придатна до: {end_time_str} ⚠️
Запущено: {start_dt.strftime(config.DATE_TIME_FORMAT_UK)} ({data['user_name']})
Була придатна на: {duration} хв.
====================================="""
        
        time_left = end_dt - now
        left_minutes = int(time_left.total_seconds() / 60)

        return f"""====================================
⏱️ Суміш придатна! ✅
Придатна до: {end_time_str} 🕒
Залишилось: {left_minutes} хв.
Запущено: {start_dt.strftime(config.DATE_TIME_FORMAT_UK)} ({data['user_name']})
====================================="""