from dao.base_dao import BaseDAO

class BaseService:
    def __init__(self):
        self.dao = BaseDAO()

    def initDB(self):
        self.dao.initDB()