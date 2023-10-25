import os
from dotenv import load_dotenv
from fastapi import APIRouter
from models.logs_request import User
from models.logs_response import AllUserLogResponse
from services.database_service import DatabaseService

load_dotenv()
url = os.environ.get("MONGO_URL")
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
mongo = DatabaseService(db_name=db_name, collection_name=collection_name, url=url)
router = APIRouter()


@router.post("/")
def create_log(user: User):
    try:
        mongo.add_user(
            {"_id": user.user_id, "mac_address": user.mac_address, "timestamps": []}
        )
    except Exception as e:
        # print(e)
        return {"message": "Failed to create log"}
    return {"message": "Log created"}


@router.get("/")
def get_all_logs() -> AllUserLogResponse:
    try:
        logs = mongo.get_all_logs()
        mapped_logs = [{**log, "id": log.pop("_id")} for log in logs]
        response = AllUserLogResponse.model_validate({"logs": mapped_logs})
        return response
    except Exception as e:
        # print(e)
        return {"message": "Failed to get all logs"}
