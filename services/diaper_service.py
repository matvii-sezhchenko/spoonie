from dao.diaper_dao import DiaperDAO

class DiaperService:
    def __init__(self):
        self.dao = DiaperDAO()

    def fix_diaper(self, user_name):
        try:
            self.dao.add_used_diaper (user_name)
            return True, f"✅ Записано"
        except ValueError as e:
            return False, f"❌ Помилка: {str(e)}"
        except Exception as e:
            return False, f"❌ Не вдалось зберегти. {str(e)}"
        
    def get_three_days_analytics(self):
        days=3
        history = self.dao.get_use_diaper_history(days) or []

        if not history:
            return "Дані відсутні."
        
        return(
            f"🩲 змінено: {len(history)} разів (≈{round(len(history)/3, 1)}/день)\n"
            f"━━━━━━━━━━━━━━━\n"
        )
    
    def get_month_analytics(self):
        days=30
        history = self.dao.get_use_diaper_history(days) or []

        if not history:
            return "Дані відсутні."
        
        return(
            f"🩲 змінено: {len(history)} разів (≈{round(len(history)/days, 1)}/день)\n"
            f"━━━━━━━━━━━━━━━\n"
        )