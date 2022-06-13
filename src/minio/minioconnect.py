from minio import Minio
from src.minio.cfg import access_key, secret_key, secure, address

def getMinioClient() -> Minio:
    client = Minio(address, access_key=access_key, secret_key=secret_key, secure=secure)
    if not client.bucket_exists("testgreen"):
        client.make_bucket("testgreen")
    return client

