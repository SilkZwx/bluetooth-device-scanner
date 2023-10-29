from databese.mongo_manager import MongoManager
from datetime import datetime, timedelta


class DatabaseService(MongoManager):
    def __init__(self, db_name: str, collection_name: str, url: str):
        super().__init__(db_name, collection_name, url)

    def get_all_logs(self) -> list:
        return list(self.collection.find())

    # 1週間分のデータを取得
    def get_id_logs(self, id: str) -> dict:
        today = datetime.now().date()
        one_week_ago = today - timedelta(weeks=1)
        logs = self.get_timestamps(id=id, count=8)
        filtered_logs = []
        for timestamp in logs:
            day = timestamp["in"].date()
            if one_week_ago < day <= today:
                filtered_logs.append(timestamp)
        return {
            "id": id,
            "timestamps": filtered_logs,
        }
