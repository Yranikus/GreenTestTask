from datetime import date

from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str



