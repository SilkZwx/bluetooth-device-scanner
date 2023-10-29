import subprocess
import time
from datetime import datetime
from mongo_manager import MongoManager
import os
from dotenv import load_dotenv


def add_user(mongo: MongoManager, id: str, mac_address: str):
    mongo.add_user({"_id": id, "mac_address": mac_address, "timestamps": []})


def add_timestamp(
    mongo: MongoManager, mac_address: str, in_time: datetime, out_time: datetime
):
    previous_timestamps = mongo.get_timestamps(mac_address, 1)
    prev_timestamp = previous_timestamps[0]

    if prev_timestamp["out"].date() == out_time.date():
        # 今日の日付のデータが既にある場合は退出時刻を更新する
        prev_timestamp["out"] = out_time
        mongo.add_timestamp(mac_address, prev_timestamp)
    else:
        # 今日の日付のデータがない場合は新しくデータを追加する
        timestamp = {"in": in_time, "out": out_time}
        mongo.add_timestamp(mac_address, timestamp)


def check_bluetooth_devices(mongo: MongoManager):
    mac_addresses = mongo.get_mac_addresses()

    users_timestamp = []
    for mac_address in mac_addresses:
        users_timestamp.append(
            {
                "mac_address": mac_address,
                "attend": False,
                "in_time": None,
                "out_time": None,
            }
        )

    # bluetoothctlをサブプロセスとして起動
    process = subprocess.Popen(
        ["bluetoothctl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    while True:
        # 各デバイスに対して接続を試みる
        for user_timestamp in users_timestamp:
            mac_address = user_timestamp["mac_address"]
            print(f"Trying to connect to {mac_address}...")
            process.stdin.write(f"connect {mac_address}\n")
            process.stdin.flush()
            time.sleep(2)  # 接続を待つ

            # stdoutから接続結果を読み取る
            while True:
                connect_output = process.stdout.readline().strip()
                if "Connection successful" in connect_output:
                    print(f"Successfully connected to {mac_address}")
                    if not user_timestamp["attend"]:
                        user_timestamp["attend"] = True
                        user_timestamp["in_time"] = datetime.now()

                    process.stdin.write(f"disconnect {mac_address}\n")
                    process.stdin.flush()
                    break
                elif (
                    "Failed to connect" in connect_output
                    or "not available" in connect_output
                ):
                    # 一度検出されたデバイスが検出されなくなった場合
                    if user_timestamp["attend"]:
                        user_timestamp["attend"] = False
                        user_timestamp["out_time"] = datetime.now()
                        add_timestamp(
                            mongo,
                            mac_address,
                            user_timestamp["in_time"],
                            user_timestamp["out_time"],
                        )
                        print(f"recorded {mac_address}")
                    else:
                        print(f"Failed to connect to {mac_address}")
                    break

        time.sleep(120)


if __name__ == "__main__":
    load_dotenv()
    db_name = os.environ.get("MONGO_DBNAME")
    collection_name = os.environ.get("MONGO_COLLECTIONNAME")
    mongo = MongoManager(db_name=db_name, collection_name=collection_name)
    check_bluetooth_devices(mongo)
