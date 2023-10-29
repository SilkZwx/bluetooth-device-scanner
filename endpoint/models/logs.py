from pydantic import BaseModel


class Log(BaseModel):
    id: str
    mac_address: str
    timestamps: list[dict]
