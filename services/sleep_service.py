from datetime import datetime, timedelta

from config import DATE_ONLY_FORMAT, DATETIME_FORMAT, format_hour_minutes
from dao.sleep_dao import SleepDAO

class SleepService:
    def __init__(self):
        self.dao = SleepDAO()

    def reg_sleep (self, user_name, start_time=None):
        try:
            start_time_sleep = self.dao.add_sleep(user_name, start_time)
            return f"✅ Зареєстровано початок сну: {start_time_sleep} відкрив(ла) сесію: {user_name}"
        except Exception as e:
            return f"❌ Не вдалось записати сон: {str(e)}"
        
    def close_sleep_session (self, end_time=None):
        try:
            end_time_session_sleep = self.dao.close_sleep(end_time)
            return f"✅ Закрито сессію сну: {end_time_session_sleep}"
        except Exception as e:
            return f"❌ Не вдалось закрити сон: {str(e)}"
        
    def get_active_session (self):
        try:
            session = self.dao.get_active_session_sleep()

            if session is not None:
                start_time_sleep = datetime.strptime(session['start_time'], DATETIME_FORMAT)
                duration = datetime.now() - start_time_sleep
                hours, remainder = divmod(int(duration.total_seconds()), 3600)
                minutes = remainder // 60

                text_result = (
                    f"🛌 Поточна сесія сну відкрита: {session['user_name']}\n"
                    f"⏰ Початок: {start_time_sleep.strftime('%H:%M %d-%m')}\n"
                    f"⏳ Поточна тривалість сну: {hours} годин {minutes} хвилин."
                )
                return True, text_result
            return False, "😴 Активних сесій не знайдено"
        except Exception as e:
            return False, f"❌ Не вдалось отримати активну сесію сну: {str(e)}"
        
    def get_three_days_analytics(self):
        history = self.dao.get_sleep_history(days=3)

        if not history:
            return f"Дані про сон за остані три дні відсутні 😴"
        
        now = datetime.now()
        today = now.strftime(DATE_ONLY_FORMAT)
        yesterday = (now - timedelta(days=1)).strftime(DATE_ONLY_FORMAT)
        before_yesterday = (now - timedelta(days=2)).strftime(DATE_ONLY_FORMAT)

        daily_sleep = {
            today: 0,
            yesterday: 0,
            before_yesterday: 0
        }

        total_minutes = 0

        for item in history:
            start_dt = 0
            end_dt = 0
            start_dt = datetime.strptime(item['start_time'], DATETIME_FORMAT)
            
            if item['end_time']:
                end_dt = datetime.strptime(item['end_time'], DATETIME_FORMAT)
            else:
                end_dt = datetime.now()

            duration_mins = int((end_dt - start_dt).total_seconds() / 60)

            day_key = start_dt.strftime(DATE_ONLY_FORMAT)

            if day_key in daily_sleep:
                daily_sleep[day_key] += duration_mins
                total_minutes += duration_mins

        avg_minutes = total_minutes / 3

        return(
            f"🕒 Cередня тривалість сну: {format_hour_minutes(int(avg_minutes))}\n"
            f"📅 Сьогодні: {today}: {format_hour_minutes(daily_sleep[today])}\n"
            f"📅 Вчора: {yesterday}: {format_hour_minutes(daily_sleep[yesterday])}\n"
            f"📅 Позавчора: {before_yesterday}: {format_hour_minutes(daily_sleep[before_yesterday])}\n"
            f"━━━━━━━━━━━━━━━\n"
        )
        
    def get_monthly_analytics(self):
        days = 30
        history = self.dao.get_sleep_history(days=days)

        if not history:
            return f"Дані про сон за остані {days} відсутні 😴"
        
        total_minutes = 0
        unique_days = set()

        for item in history:
            start_dt = 0
            end_dt = 0
            start_dt = datetime.strptime(item['start_time'], DATETIME_FORMAT)

            unique_days.add(start_dt.date())
            
            if item['end_time']:
                end_dt = datetime.strptime(item['end_time'], DATETIME_FORMAT)
            else:
                end_dt = datetime.now()

            duration_mins = int((end_dt - start_dt).total_seconds() / 60)

            total_minutes += duration_mins
        
        final_count_days = len(unique_days)

        if final_count_days == 0:
            return "Недостатньо даних для аналітики."

        avg_minutes = total_minutes / final_count_days

        return(
            f"━━━━━━━━━━━━━━━\n"
            f"🕒 Cередня тривалість сну за {final_count_days}: {format_hour_minutes(int(avg_minutes))}\n"
            f"━━━━━━━━━━━━━━━\n"
        )
