FROM python:3.12.2-slim

ENV TZ=Asia/Seoul

# RUN apt update && apt-get -y install gcc

RUN pip install poetry==1.8.2

COPY poetry.lock pyproject.toml /app/
WORKDIR /app

RUN poetry install --without test

COPY ./auth_app/ /app/auth_app/

ENTRYPOINT ["poetry", "run", "start_server"]
