import os
from dotenv import load_dotenv
from fastapi import APIRouter
from models.item import User
from databese import mongo_manager

load_dotenv()
db_name = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTIONNAME")
mongo = mongo_manager.MongoManager(db_name=db_name, collection_name=collection_name)
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


# @router.get("/")
# def get_all_logs():
#     return {"message": "All logs"}
