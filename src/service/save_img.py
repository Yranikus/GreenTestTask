import io
import string
from datetime import date
import random

from fastapi import Depends
from minio import Minio
from sqlalchemy.orm import Session
from typing import List


from src.DTO import tables
from src.DTO.database import get_session
from src.minio.minioconnect import getMinioClient


class SaveService:
    def __init__(self, session: Session = Depends(get_session), client: Minio = Depends(getMinioClient)):
        self.session = session
        self.client = client

    def save(self, files: List[bytes]) -> List[tables.Img]:
        query = (self.session.
                 query(tables.Img).all()
                 )
        newImg: List[tables.Img] = []
        requestCode = self.generate_alphanum_random_string()
        name = 1
        #я решил названия файлов приравнять к последниму PK в базе данных, это гарантирует их уникальность
        if len(query) == 0:
            name = 1
        else:
            name = self.session.query(tables.Img).order_by(tables.Img.id.desc()).first().id + 1
        for file in files:
            self.client.put_object(bucket_name="testgreen",
                                    object_name=requestCode + "\\" + name.__str__() + ".jpeg",
                                    data=io.BytesIO(file),
                                    length=len(file))
            img = tables.Img(code=requestCode, name = name, date=date.today())
            newImg.append(img)
            name += 1
        self.session.add_all(newImg)
        self.session.commit()
        return self.session.query(tables.Img).filter_by(code=requestCode).all()

    #как я понял , код запроса формируется при загрузке изображений. Вот не сложная функция его генерации.
    def generate_alphanum_random_string(self):
        letters_and_digits = string.ascii_letters + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 8))
        return rand_string



