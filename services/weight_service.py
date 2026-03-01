from dao.weight_dao import WeightDAO

class WeightService:
	def __init__(self):
		self.dao = WeightDAO()

	def add_new_weight(self, user_name, weight_gram_text):
		try:
			weight_gram = int(weight_gram_text)
			self.dao.add_weight(user_name, weight_gram)
			return f"✅ Записано: {weight_gram} г. ({weight_gram/1000:.2f} кг.)"
		except ValueError as e:
			return f"❌ Помилка: {str(e)}"
		except Exception:
			return "❌ Не вдалося зберегти вагу. Введіть значення в грамах."

	def get_monthly_analytics(self):
		history = self.dao.get_weight_history(days=30)

		if not history:
			return "Дані про вагу за останні 30 днів відсутні."

		current_weight = history[0]['weight_gram']

		if len(history) < 2:
			return f"Поточна вага: {current_weight}г\n(Для динаміки потрібно хоча б два записи за місяць)."

		first_weight = history[-1]['weight_gram']
		diff = current_weight - first_weight
		trend = ""

		if diff == 0:
			trend = "⚖️ Без змін"
		else:
			icon = "📈 +" if diff > 0 else "📉 "
			trend += f"{diff}г ({diff/1000:.2f} кг.)"

		return(
			f"📊 **Вага за 30 днів:**\n"
			f"⚖️ Поточна: **{current_weight}г**\n"
			f"🔄 Динаміка: **{trend}**\n"
			f"👤 Останній запис: {history[0]['user_name']}\n"
			f"━━━━━━━━━━━━━━━\n"
		)
