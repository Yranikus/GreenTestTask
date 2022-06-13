from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from src.settings import settings

engine = create_engine(
    settings.test_db_url
)

Session = sessionmaker(engine,
                       autocommit=False,
                       autoflush=False)

def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()