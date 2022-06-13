import pathlib

import json
import sqlalchemy
from fastapi import FastAPI
from fastapi.testclient import TestClient
from minio import Minio
from sqlalchemy.orm import Session, sessionmaker

from src.DTO import tables
from src.DTO.database import engine
from src.DTO.tables import Base
from src.api import router
import src.minio.minioconnect as minio

app = FastAPI()
app.include_router(router)

client = TestClient(app)

if not sqlalchemy.inspect(engine).has_table("inbox") or not sqlalchemy.inspect(engine).has_table("user"):
    Base.metadata.create_all(engine)

Session1 = sessionmaker(engine,
                       autocommit=False,
                       autoflush=False)

session : Session = Session1()
clientminio: Minio = minio.getMinioClient()

user = {"login" : 4,
        "password" : 5}

user_login = {"username" : 4,
             "password" : 5}



def test_auth():
    responce = client.post("/reg", json=user)
    assert responce.text.__str__() == '"регистрация прошла успешно"'


def test_save():
    responce2 = client.post("/token", data=user_login)
    token = json.loads(responce2.text)["access_token"]
    #создаю запрос с методом пост , прикрепляю картинку
    responce = client.post("/frames/", files={"files": open(pathlib.Path.cwd() / "src/tests/test_img/2.jpeg", 'rb').read()},
                           headers={"Authorization": f"Bearer {token}"})
    #поскольку в ответе я получаю json с данными о созданной картинке , мне нужно преобразовать ответ в объект что бы получить от туда сгенерированный код запроса
    imges_in_responce = json.loads(responce.text)
    request_code = imges_in_responce[0]["code"]
    #пробую по нему получить записи из базы данных , что бы удостовериться что запись была создана
    imges_in_db = session.query(tables.Img).filter_by(code=request_code).all()
    #так же получаю объект из хранилища
    list_in_minio = clientminio.list_objects(bucket_name="testgreen", prefix="/" + request_code + "/",
                                               recursive=True)
    session.close()
    assert responce.status_code == 200
    #по очереди получаю из двух списков данные об объектах и  сверяю что данные полученные в ответе совпадают с данными в базе данных и в хранилище данных
    for i in range(len(imges_in_responce)):
        imge_in_minio = next(list_in_minio)
        assert imge_in_minio.object_name == (request_code + "/" + imges_in_db[0].name.__str__() + ".jpeg")
        assert imge_in_minio.object_name == (request_code + "/" + imges_in_responce[i]["name"].__str__() + ".jpeg")
        assert imges_in_responce[i]["code"] == imges_in_db[0].code
        assert imges_in_responce[i]["name"] == imges_in_db[0].name

def test_get():
    responce2 = client.post("/token", data=user_login)
    token = json.loads(responce2.text)["access_token"]
    #беру первую запись из бд, что бы получить код запроса
    request_code = session.query(tables.Img).first().code
    #получаю все записи по этому коду
    imges_in_db = session.query(tables.Img).filter_by(code=request_code).all()
    responce = client.get("/frames/" + request_code, headers={"Authorization": f"Bearer {token}"})
    imges_in_responce = json.loads(responce.text)
    list_in_minio = clientminio.list_objects(bucket_name="testgreen", prefix="/" + request_code + "/",
                                             recursive=True)
    assert responce.status_code == 200
    session.close()
    #сверяю дпнные из базы данных и хранилища с тем что пришло в ответе
    for i in range(len(imges_in_responce)):
        imge_in_minio = next(list_in_minio)
        assert imge_in_minio.object_name == (request_code + "/" + imges_in_db[0].name.__str__() + ".jpeg")
        assert imge_in_minio.object_name == (request_code + "/" + imges_in_responce[i]["name"].__str__() + ".jpeg")
        assert imges_in_responce[i]["code"] == imges_in_db[0].code
        assert imges_in_responce[i]["name"] == imges_in_db[0].name

def test_delete():
    responce2 = client.post("/token", data=user_login)
    token = json.loads(responce2.text)["access_token"]
    exist_img = session.query(tables.Img).first()
    session.close()
    code_of_exist_imges = exist_img.code
    respoce = client.delete("/frames/" + code_of_exist_imges, headers={"Authorization": f"Bearer {token}"})
    list_of_deleted_imges = clientminio.list_objects(bucket_name="testgreen", prefix="/" + code_of_exist_imges + "/", recursive=True)
    i = 0
    #проверяю что из хранилища ни пришло ни одного файла , следовательно произошло удаление
    for k in list_of_deleted_imges:
        i += 1
    assert i == 0
    assert respoce.status_code == 200
    #проверяю что из базы так же произошло удаление
    images_after_deleting = session.query(tables.Img).filter_by(code=code_of_exist_imges).count()
    session.query(tables.User).filter_by(login="4").delete()
    session.commit()
    session.close()
    assert images_after_deleting == 0


