import os
from dotenv import load_dotenv
from models.logs_response import AllUserLogResponse
from services.database_service import DatabaseService

load_dotenv()
url = os.environ.get("MONGO_URL")
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
mongo = DatabaseService(db_name=db_name, collection_name=collection_name, url=url)


def test_all_user_log_responce():
    logs = mongo.get_all_logs()
    for log in logs:
        assert log["_id"] is not None
        assert log["mac_address"] is not None
        assert log["timestamps"] is not None
    mapped_logs = [{**log, "id": log.pop("_id")} for log in logs]
    all_log = AllUserLogResponse.model_validate({"logs": mapped_logs})
    assert all_log is not None
    assert all_log.logs[0].id is not None
    assert all_log.logs[0].mac_address is not None
    assert all_log.logs[0].timestamps is not None
