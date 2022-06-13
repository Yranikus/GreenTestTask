from pydantic import BaseSettings

#url баз данных
class Settings(BaseSettings):
    db_url: str = "postgresql+psycopg2://postgres:root@127.0.0.1:5432/green"
    test_db_url: str = "postgresql+psycopg2://postgres:root@127.0.0.1:5432/testsgreen"

settings = Settings()