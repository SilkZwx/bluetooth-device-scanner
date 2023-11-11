import os
from dotenv import load_dotenv
from services.database_service import DatabaseService

load_dotenv()
url = os.environ.get("MONGO_URL")
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
id = os.environ.get("ID")
db = DatabaseService(db_name=db_name, collection_name=collection_name, url=url)


def test_get_id_logs():
    log = db.get_id_logs(id)
    assert log["id"] is not None
    assert log["timestamps"] is not None
    # print(log)
