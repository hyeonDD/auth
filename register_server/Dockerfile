FROM python:3.12.2-slim

ENV TZ=Asia/Seoul

RUN pip install poetry==1.8.2

COPY poetry.lock pyproject.toml /app/
WORKDIR /app

RUN poetry install

COPY ./register_app/ /app/register_app/

ENTRYPOINT ["poetry", "run", "start_server"]
