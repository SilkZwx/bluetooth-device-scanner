from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    mac_address: str
