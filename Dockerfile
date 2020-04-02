FROM python:3.7.7-buster

RUN apt-get update -y
RUN apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y

RUN pip install poetry

WORKDIR /app


COPY poetry.lock pyproject.toml /app/


RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi


