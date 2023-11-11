from databese.mongo_manager import MongoManager
from datetime import datetime, timedelta
from models.logs import Timestamp


class DatabaseService:
    def __init__(self, db_name: str, collection_name: str, url: str):
        self.mongo = MongoManager(db_name, collection_name, url)

    def get_all_ids(self) -> list:
        return self.mongo.get_ids()

    # 1週間分のデータを取得
    def get_id_logs(self, id: str) -> {"id": str, "timestamps": [Timestamp]}:
        today = datetime.now().date()
        one_week_ago = today - timedelta(weeks=1)
        logs = self.mongo.get_timestamps(id=id, count=8)
        filtered_logs = []
        for timestamp in logs:
            day = timestamp["in"].date()
            if one_week_ago < day <= today:
                filtered_logs.append(Timestamp.model_validate(timestamp))
        return {
            "id": id,
            "timestamps": filtered_logs,
        }
