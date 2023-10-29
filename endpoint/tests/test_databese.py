import os
from dotenv import load_dotenv
from services.database_service import DatabaseService

load_dotenv()
url = os.environ.get("MONGO_URL")
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
mongo = DatabaseService(db_name=db_name, collection_name=collection_name, url=url)


def test_get_all_logs():
    logs = mongo.get_all_logs()
    for log in logs:
        assert log["_id"] is not None
        assert log["mac_address"] is not None
        assert log["timestamps"] is not None


def test_get_id_logs():
    log = mongo.get_id_logs("c19009")
    assert log["id"] is not None
    assert log["timestamps"] is not None
    print(log)
