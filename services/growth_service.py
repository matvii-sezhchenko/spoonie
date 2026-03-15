from dao.growth_dao import GrowthDAO

class GrowthService:
	def __init__(self):
		self.dao = GrowthDAO()

	def add_new_growth(self, user_name, growth_cm_text):
		try:
			growth_cm = int(growth_cm_text)
			self.dao.add_growth(user_name, growth_cm)
			return f"✅ Записано {growth_cm} см."
		except ValueError as e:
			return f"❌ Помилка: {str(e)}"
		except Exception as e:
			return f"❌ Не вдалось зберегти зріст. {str(e)}"

	def get_monthly_analytics(self):
		history = self.dao.get_growth_history(days=30)

		if not history:
			return "Дані про зріст за останні 30 днів відсутні."

		current_growth = history[0]['growth_cm']

		if len(history) < 2:
			return f"Поточний зріст: {current_growth} см\n(Для динаміки потрібно хоча б два записи за місяць)."

		first_growth = history[-1]['growth_cm']
		diff = current_growth - first_growth
		trend = ""

		if diff == 0:
			trend = "📏 Без змін"
		else:
			icon = "📈 +" if diff > 0 else "📉 "
			trend += f"{icon}{diff} см"

		return(
			f"📏 Поточний: **{current_growth} см**\n"
			f"🔄 Динаміка: **{trend}**\n"
			f"👤 Останній запис: {history[0]['user_name']}\n"
			f"━━━━━━━━━━━━━━━\n"
			)