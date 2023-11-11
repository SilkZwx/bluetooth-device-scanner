from pydantic import BaseModel
from models.logs import Timestamp


class AllUserIdResponse(BaseModel):
    ids: list[str]


class IdLogResponse(BaseModel):
    id: str
    timestamps: list[Timestamp]
