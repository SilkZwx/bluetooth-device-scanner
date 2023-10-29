from pydantic import BaseModel
from models.logs import Log


class AllUserLogResponse(BaseModel):
    logs: list[Log]


class IdLogResponse(BaseModel):
    id: str
    timestamps: list[dict]
