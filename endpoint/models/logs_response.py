from pydantic import BaseModel
from models.logs import Log


class AllUserLogResponse(BaseModel):
    logs: list[Log]
