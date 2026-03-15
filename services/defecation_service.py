from dao.defecation_dao import DefecationDAO

class DefecationService:
    def __init__(self):
        self.dao = DefecationDAO()

    def fix_peepee(self, user_name):
        try:
            self.dao.add_peepee (user_name)
            return True, f"✅ Записано"
        except ValueError as e:
            return False, f"❌ Помилка: {str(e)}"
        except Exception as e:
            return False, f"❌ Не вдалось зберегти. {str(e)}"

    def fix_poopoo(self, user_name):
        try:
            self.dao.add_poopoo (user_name)
            return True, f"✅ Записано"
        except ValueError as e:
            return False, f"❌ Помилка: {str(e)}"
        except Exception as e:
            return False, f"❌ Не вдалось зберегти. {str(e)}"

    def fix_burped(self, user_name):
        try:
            self.dao.add_burped (user_name)
            return True, f"✅ Записано"
        except ValueError as e:
            return False, f"❌ Помилка: {str(e)}"
        except Exception as e:
            return False, f"❌ Не вдалось зберегти. {str(e)}"
        
    def get_three_days_analytics(self):
        history_peepee = self.dao.get_peepee_history(days=3) or []
        history_poopoo = self.dao.get_poopoo_history(days=3) or []
        history_burped = self.dao.get_burped_history(days=3) or []

        if not any([history_peepee, history_poopoo, history_burped]):
            return "Дані відсутні."
        
        peepee_count = len(history_peepee)
        poopoo_count = len(history_poopoo)
        burped_count = len(history_burped)
        
        return(
            f"💦 зафіксовано: {peepee_count} разів (≈{round(peepee_count/3, 1)}/день)\n"
            f"💩 зафіксовано: {poopoo_count} разів (≈{round(poopoo_count/3, 1)}/день)\n"
            f"🤮 зафіксовано: {burped_count} разів (≈{round(burped_count/3, 1)}/день)\n"
            f"━━━━━━━━━━━━━━━\n"
        )
    
    def get_monthly_analytics(self):
        days = 30
        history_peepee = self.dao.get_peepee_history(days) or []
        history_poopoo = self.dao.get_poopoo_history(days) or []
        history_burped = self.dao.get_burped_history(days) or []

        if not any([history_peepee, history_poopoo, history_burped]):
            return "Дані відсутні."
        
        peepee_count = len(history_peepee)
        poopoo_count = len(history_poopoo)
        burped_count = len(history_burped)
        
        return (
            f"💦 Усього: {peepee_count}\n"
            f"📊 В середньому: {round(peepee_count/days, 1)}/день\n\n"
            f"💩 Усього: {poopoo_count}\n"
            f"📊 В середньому: {round(poopoo_count/days, 1)}/день\n\n"
            f"🤮 Усього: {burped_count}\n"
            f"📊 В середньому: {round(burped_count/days, 1)}/день\n"
            f"━━━━━━━━━━━━━━━\n"
        )