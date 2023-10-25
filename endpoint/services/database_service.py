from databese.mongo_manager import MongoManager


class DatabaseService(MongoManager):
    def __init__(self, db_name: str, collection_name: str, url: str):
        super().__init__(db_name, collection_name, url)

    def get_all_logs(self) -> list:
        return list(self.collection.find())
