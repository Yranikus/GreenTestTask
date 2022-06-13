import uvicorn
from DTO.database import engine, Session
from DTO.tables import Base, Img
import sqlalchemy

#если таблица не существует , она создастся
if not sqlalchemy.inspect(engine).has_table("inbox") or not sqlalchemy.inspect(engine).has_table("user"):
    Base.metadata.create_all(engine)


uvicorn.run(
    'src.main:app',
)