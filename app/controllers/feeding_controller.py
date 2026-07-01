from datetime import datetime, timedelta
from app.models.feeding import Feeding
from app import config
from datetime import datetime
from app import config

class FeedingController:
    def __init__(self, repository):
        self.repository = repository

    def add_feeding(self, user_name, volume_ml) -> tuple[bool, str]:
        timestr = self.get_timestamp()
        new_feeding = Feeding(user_name=user_name, volume_ml=volume_ml, timestamp=timestr)
        is_success, new_id = self.repository.save(new_feeding)

        if is_success:
            return is_success, "Запис успішно додано"
        else:
            return is_success, "Не вдалось записати"
        
    def get_timestamp(self) -> str:
        current_date_time = datetime.now()
        return current_date_time.strftime(config.DATE_TIME_FORMAT)
    
    def get_last_feeding(self) -> str:
        last_feeding = self.repository.get_last_record()
        if not last_feeding:
            return "=================================\nЗаписи відсутні\n================================="
        
        if len(last_feeding.timestamp) == 16:
            dt_object = datetime.strptime(last_feeding.timestamp, "%Y-%m-%d %H:%M")
        else:
            dt_object = datetime.strptime(last_feeding.timestamp, config.DATE_TIME_FORMAT)

        only_time = dt_object.strftime(config.TIME_FORMAT)

        return f"""====================================
Останнє годування: в {only_time}
Запис зроблено: {last_feeding.user_name}
Об'єм: {last_feeding.volume_ml} мл
===================================="""

    def get_daily_report(self) -> str:
        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        records = self.repository.get_records_by_date(today_str)
        report_title = "📊 ЗВІТ ЗА СЬОГОДНІ"

        if not records:
            records = self.repository.get_records_by_date(yesterday_str)
            report_title = "📊 ЗА СЬОГОДНІ ПУСТО. ЗВІТ ЗА ВЧОРА"

        if not records:
            return "=================================\n📊 За сьогодні записів ще немає\n================================="

        total_volume = 0
        feedings_count = len(records)
        history_lines = []

        for timestamp, volume, user in records:
            total_volume += volume

            if len(timestamp) == 16:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(timestamp, config.DATE_TIME_FORMAT)
                
            time_str = dt.strftime(config.TIME_FORMAT)
            
            history_lines.append(f"• {time_str} — {volume} мл ({user})")

        history_text = "\n".join(history_lines)

        return f"""====================================
{report_title}
====================================
🍼 Всього годувань: {feedings_count}
💧 Загальний об'єм: {total_volume} мл

📝 Історія:
{history_text}
===================================="""
        