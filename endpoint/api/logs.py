import os
from dotenv import load_dotenv
from fastapi import APIRouter
from models.logs_request import User
from models.logs_response import AllUserIdResponse, IdLogResponse
from services.database_service import DatabaseService

load_dotenv()
url = os.environ.get("MONGO_URL")
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
db = DatabaseService(db_name=db_name, collection_name=collection_name, url=url)
router = APIRouter()


@router.post("/")
def create_log(user: User):
    try:
        db.add_user(
            {"_id": user.user_id, "mac_address": user.mac_address, "timestamps": []}
        )
    except Exception as e:
        # print(e)
        return {"message": "Failed to create log"}
    return {"message": "Log created"}


@router.get("/")
def get_all_ids() -> AllUserIdResponse:
    ids = db.get_all_ids()
    response = AllUserIdResponse.model_validate({"ids": ids})
    return response


@router.get("/{id}")
def get_id_logs(id: str):
    try:
        logs = db.get_id_logs(id)
        response = IdLogResponse.model_validate(logs)
        return response
    except Exception as e:
        # print(e)
        return {"message": "Failed to get all logs"}


@router.delete("/{id}")
def delete_user(id: str):
    try:
        db.delete_user(id)
        return {"message": "Log deleted"}
    except Exception as e:
        # print(e)
        return {"message": "Failed to delete log"}


@router.put("/{id}")
def update_user(id: str, user: User):
    if user.user_id != id:
        return {"message": "Invalid user_id"}
    try:
        db.update_user({"id": user.user_id, "mac_address": user.mac_address})
        return {"message": "Log updated"}
    except Exception as e:
        # print(e)
        return {"message": "Failed to update log"}
