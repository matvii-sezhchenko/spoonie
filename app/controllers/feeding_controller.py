from datetime import datetime
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
        
        dt_object = datetime.strptime(last_feeding.timestamp, config.DATE_TIME_FORMAT)
        only_time = dt_object.strftime(config.TIME_FORMAT)

        return f"""====================================
Останнє годування: в {only_time}
Запис зроблено: {last_feeding.user_name}
Об'єм: {last_feeding.volume_ml} мл
===================================="""

        