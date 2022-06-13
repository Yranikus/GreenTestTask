import io
import os
from typing import List

from fastapi import Depends
from minio import Minio
from minio.deleteobjects import DeleteObject
from sqlalchemy.orm import Session

from src.DTO import tables
from src.DTO.database import get_session
from src.minio.minioconnect import getMinioClient


class DeleteAndGetService:
    def __init__(self, session: Session = Depends(get_session), client: Minio = Depends(getMinioClient)):
        self.session = session
        self.client = client

    def get(self, requestCode) -> List[tables.Img]:
        imges = self.session.query(tables.Img).filter_by(code=requestCode).all()
        return imges

    def delete(self, requestCode):
        self.session.query(tables.Img).filter_by(code=requestCode).delete()
        self.session.commit()
        # В документации написано удалять так , но я не знаю почему у меня на домашней машине это не сработало
        # deleting_obj_lis = map(lambda x: DeleteObject(x.object_name),
        #                        self.client.list_objects(bucket_name="testgreen", prefix="/" + requestCode + "/", recursive=True))
        # self.client.remove_objects(bucket_name="testgreen", delete_object_list=deleting_obj_lis)
        kek = self.client.list_objects(bucket_name="testgreen", prefix="/" + requestCode + "/", recursive=True)
        for obj in kek:
            self.client.remove_object("testgreen", obj.object_name)
        return 200
