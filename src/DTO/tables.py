import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Img(Base):

    __tablename__ = "inbox"
    id = sa.Column(sa.INTEGER, primary_key=True)
    code = sa.Column(sa.String(10), primary_key=False, unique=False)
    name = sa.Column(sa.BIGINT,  primary_key=False)
    date = sa.Column(sa.Date)

class User(Base):

    __tablename__ = "users"
    id = sa.Column(sa.INTEGER, primary_key=True)
    login = sa.Column(sa.String(10),  primary_key=False, unique=True)
    password = sa.Column(sa.String)