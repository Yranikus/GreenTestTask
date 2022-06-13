from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from ..DTO import tables
from ..service.auth import Authentication
from ..models.schemas import User
import jwt
import json

router = APIRouter(
    prefix=""
)

JWT_SECRET_KEY = "green"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        user = tables.User(id=payload.get('id'), login=payload.get('login'), password=payload.get('password'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid login or pass")
    return user


@router.post("/reg")
async def reg(user: User, secure: Authentication = Depends()):
    if secure.registration(user.login, user.password):
        return "регистрация прошла успешно"
    return "логин занят"


@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), secure: Authentication = Depends()):
    user = secure.auth(form_data.username, form_data.password)
    if user == None:
        return {"error": 'invalid credentials'}
    token = jwt.encode({
        "id": user.id,
        "login": user.login,
        "password": user.password
    }, JWT_SECRET_KEY)
    return {'access_token': token, 'token_type': 'bearer'}
