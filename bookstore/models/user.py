from pydantic import BaseModel
import enum
from fastapi import Query


class Role(enum.Enum):
    admin: str = "admin"
    personnel: str = "personnel"


class User(BaseModel):
    name: str
    password: str
    mail: str = Query(...,
                      regex="[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:["
                            "a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    role: Role