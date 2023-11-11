from pydantic import BaseModel


class AllUserIdResponse(BaseModel):
    ids: list[str]


class IdLogResponse(BaseModel):
    id: str
    timestamps: list[dict]
