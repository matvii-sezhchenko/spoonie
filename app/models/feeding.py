

class Feeding:
    def __init__(self, user_name:str, volume_ml: int, timestamp: str, id: int = None):
        self.id = id
        self.user_name = user_name
        self.volume_ml = volume_ml
        self.timestamp = timestamp
