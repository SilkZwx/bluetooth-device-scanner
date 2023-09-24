from pymongo import MongoClient
from datetime import datetime
import time
import os


def subscribe_member(user_id, mac_address):
    url = os.environ.get("MONGO_URL")
    # url = "mongodb://mongo:27017/"
    client = MongoClient(url)
    db = client["sample_database"]
    collection = db["sample_collection"]
    print(url)
    new_user = new_user = {"_id": user_id, "mac_address": mac_address, "timestamps": []}
    collection.insert_one(new_user)
    print("User subscribed.")


def insert_timestamp(user_id, time_in, time_out):
    timestamp = {"in": time_in, "out": time_out}
    collection.update_one({"_id": user_id}, {"$push": {"timestamps": timestamp}})
    print("Data inserted.")


def get_timestamps(mac_address):
    query = {"mac_address": mac_address}
    projection = {"timestamps": {"$slice": -5}}
    result = collection.find_one(query, projection)
    if result:
        return result.get("timestamps", [])
    else:
        # 該当するMACアドレスのデータがない場合
        return None


def add_sample_data():
    user_id = "c19001"
    mac_address = "00:1A:2B:3C:4D:5E"
    subscribe_member(user_id, mac_address)
    in_time = datetime.now()
    time.sleep(5)
    out_time = datetime.now()
    insert_timestamp(user_id, in_time, out_time)


def get_sample_data():
    user_id = "c19001"
    user_data = collection.find_one({"_id": user_id})
    mac_address = "00:1A:2B:3C:4D:5E"
    query = {"mac_address": mac_address}
    projection = {"timestamps": {"$slice": -5}}
    result = collection.find_one(query, projection)
    if result:
        return result.get("timestamps", [])
    else:
        # 該当するMACアドレスのデータがない場合
        return None
    return user_data


if __name__ == "__main__":
    url = os.environ.get("MONGO_URL")
    client = MongoClient(url)
    db = client["sample_database"]
    collection = db["sample_collection"]
    # add_sample_data()
    data = get_sample_data()
    print(data)
