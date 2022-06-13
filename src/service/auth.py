from sqlalchemy.orm import Session
from fastapi import Depends


from src.DTO import tables
from src.DTO.database import get_session
from passlib.hash import bcrypt

JWT_SECRET_KEY = "green"


class Authentication:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def registration(self, login, password):
        if self.get_user_by_login(login=login) == None:
            user = tables.User(login=login, password=bcrypt.hash(password))
            self.session.add(user)
            self.session.commit()
            return True
        return False

    def auth(self, login, password):
        user = self.get_user_by_login(login)
        if user == None or not bcrypt.verify(password, user.password):
            return None
        else:
            return user

    def get_user_by_login(self, login):
        return self.session.query(tables.User).filter_by(login=login).first()

