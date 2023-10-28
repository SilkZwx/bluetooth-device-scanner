from pymongo import MongoClient
import os


class MongoManager:
    def __init__(self, db_name: str, collection_name: str):
        url = os.environ.get("MONGO_URL")
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_user(self, user_data: dict) -> None:
        """
        user_data = {
            "_id": str,
            "mac_address": str,
            "timestamps": []
            }
        """
        self.collection.insert_one(user_data)

    def add_timestamp(self, mac_address: str, timestamp: dict) -> None:
        """
        timestamp = {
            "in": datetime,
            "out": datetime
            }
        """
        self.collection.update_one(
            {"mac_address": mac_address},
            {"$push": {"timestamps": {"$each": [timestamp], "$position": 0}}},
        )

    def get_mac_addresses(self) -> list:
        macaddresses = []
        for user in self.collection.find():
            macaddresses.append(user["mac_address"])
        return macaddresses

    def get_timestamps(self, mac_address: str, count: int) -> list[dict]:
        """
        dict = {
            "in": datetime,
            "out": datetime
            }
        """
        query = {"mac_address": mac_address}
        projection = {"timestamps": {"$slice": -count}}
        result = self.collection.find_one(query, projection)
        if result:
            return result.get("timestamps", [])
        else:
            # 該当するMACアドレスのデータがない場合
            return None
