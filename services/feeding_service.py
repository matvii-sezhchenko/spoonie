from datetime import datetime, timedelta
from config import DATETIME_FORMAT

from dao.feeding_dao import FeedingDAO

class FeedingService:
    def __init__(self):
        self.dao = FeedingDAO()

    def add_new_feeding(self, user_name, volume_ml_text):
        try:
            volume_ml = int(volume_ml_text.replace(" ", "").replace("мл", ""))
            self.dao.add_feeding(user_name, volume_ml)
            return True, f"✅ Записано {volume_ml} мл."
        except ValueError as e:
            return False, f"❌ Помилка: {str(e)}"
        except Exception as e:
            return False, f"❌ Не вдалось зберегти спожитий об'єм. {str(e)}"
        
    def get_three_days_analytics(self):
        history = self.dao.get_feeding_history(days=3)

        if not history:
            return "Дані, стосовно споживання їжі, відсутні."
        
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        before_yesterday = today - timedelta(days=2)

        daily_volumes = {
            today: 0,
            yesterday: 0,
            before_yesterday: 0
        }

        last_feeding = history[0]['volume_ml']
        who_last_feeded = history[0]['user_name']
        total_volume = 0

        for item in history:
            item_date = datetime.strptime(item['timestamp'], DATETIME_FORMAT).date()

            volume = item['volume_ml']
            total_volume += volume

            if item_date in daily_volumes:
                daily_volumes[item_date] += volume

        abg_feeding = round(total_volume / 3, 1)

        return(
            f"━━━━━━━━━━━━━━━\n"
            f"🥤 Спожито усього за 3 доби: {total_volume}\n"
            f"⚖️ Середньо-спожитий об'єм за три доби: {abg_feeding} мл\n"
            f"━━━━━━━━━━━━━━━\n"
            f"Спожито за {today}: {daily_volumes[today]}\n"
            f"Спожито за {yesterday}: {daily_volumes[yesterday]}\n"
            f"Спожито за {before_yesterday}: {daily_volumes[before_yesterday]}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 Останній годував(ла): {who_last_feeded}\n"
            f"🍼 Останній спожитий об'єм: {last_feeding}\n"
            f"━━━━━━━━━━━━━━━\n"
        )
    
    def get_monthly_analytics(self):
        deys = 30
        history = self.dao.get_feeding_history(days=deys)

        if not history:
            return "Дані, стосовно споживання їжі, відсутні."

        last_feeding = history[0]['volume_ml']
        who_last_feeded = history[0]['user_name']
        total_volume = 0

        unique_days = {datetime.strptime(item['timestamp'], DATETIME_FORMAT).date() for item in history}
        final_count_days = len(unique_days)

        for item in history:
            volume = item['volume_ml']
            total_volume += volume

        abg_feeding = round(total_volume / final_count_days, 1)

        return(
            f"━━━━━━━━━━━━━━━\n"
            f"🥤 Спожито усього за {final_count_days} діб: {total_volume} мл. ({total_volume/1000} л.)\n"
            f"⚖️ Середньо-спожитий об'єм за {final_count_days} діб: {abg_feeding} мл\n"
            f"👤 Останній годував(ла): {who_last_feeded}\n"
            f"🍼 Останній спожитий об'єм: {last_feeding}\n"
            f"━━━━━━━━━━━━━━━\n"
        )
    
    def get_one_day(self):
        deys = 1
        history = self.dao.get_feeding_history(days=deys)

        if not history:
            return "Дані, стосовно споживання їжі, відсутні."
        
        dt_obj = datetime.strptime(history[0]['timestamp'], DATETIME_FORMAT)
        last_feeding, in_time = history[0]['volume_ml'], dt_obj.strftime("%H:%M")
        who_last_feeded = history[0]['user_name']
        total_volume = 0

        for item in history:
            volume = item['volume_ml']
            total_volume += volume

        return(
            f"━━━━━━━━━━━━━━━\n"
            f"🥤 Спожито усього за сьогодні: {total_volume}\n"
            f"👤 Останній годував(ла): {who_last_feeded} в {in_time}\n"
            f"🍼 Останній спожитий об'єм: {last_feeding}\n"
            f"━━━━━━━━━━━━━━━\n"
        )