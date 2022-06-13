import sqlalchemy
from fastapi import FastAPI

from .DTO.database import engine
from .DTO.tables import Base
from .api import router


#если таблица не существует , она создастся
if not sqlalchemy.inspect(engine).has_table("inbox") or not sqlalchemy.inspect(engine).has_table("user"):
    Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(router)

