from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union


class Timestamp(BaseModel):
    in_: Union[datetime, str] = Field(..., alias="in")
    out: Union[datetime, str] = Field(..., alias="out")


class Log(BaseModel):
    id: str
    mac_address: str
    timestamps: list[Timestamp]
