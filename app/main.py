import subprocess
import re
import time
import datetime
from mongo_manager import MongoManager


def check_bluetooth_devices():
    mongo = MongoManager("sample_database", "sample_collection")
    mongo.add_user(
        {"_id": "m23a01", "mac_address": "D8:1C:79:26:83:50", "timestamps": []}
    )
    mac_addresses = mongo.get_mac_addresses()

    # stdoutから既知のデバイスのリストを読み取る
    # mac_addresses = []
    # while True:
    #     line = process.stdout.readline().strip()
    #     match = re.search(r"Device ([0-9A-Fa-f:]{17})", line)
    #     if match:
    #         mac_address = match.group(1)
    #         mac_addresses.append(mac_address)
    #     if "Agent registered" in line:
    #         print("Done reading devices.")
    #         break

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
                        user_timestamp["in_time"] = datetime.datetime.now()

                    process.stdin.write(f"disconnect {mac_address}\n")
                    process.stdin.flush()
                    break
                elif "Failed to connect" in connect_output:
                    if user_timestamp["attend"]:
                        user_timestamp["attend"] = False
                        user_timestamp["out_time"] = datetime.datetime.now()
                        mongo.add_timestamp(
                            mac_address,
                            {
                                "in": user_timestamp["in_time"],
                                "out": user_timestamp["out_time"],
                            },
                        )
                    print(f"Failed to connect to {mac_address}")
                    break

        # bluetoothctlを終了
        # process.stdin.write("quit\n")
        # process.stdin.flush()
        time.sleep(300)


def record_connect_time():
    address_dict = {}


if __name__ == "__main__":
    check_bluetooth_devices()
