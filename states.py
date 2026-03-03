from aiogram.fsm.state import State, StatesGroup

class BabyStats(StatesGroup):
	waiting_for_weight = State()
	waiting_for_growth = State()
	waiting_for_feeding_ml = State()