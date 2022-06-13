import uvicorn
from DTO.database import engine, Session
from DTO.tables import Base, Img
import sqlalchemy


uvicorn.run(
    'src.main:app',
)