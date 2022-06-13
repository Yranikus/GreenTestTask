FROM python:3.9 AS builder

COPY ./src /app/src
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--reload"]

