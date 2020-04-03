FROM python:3.7.7-buster

RUN apt-get update -y
RUN apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info locales -y
RUN echo "Europe/Moscow" > /etc/timezone && \
        dpkg-reconfigure -f noninteractive tzdata && \
        sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
        sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
        echo 'LANG="ru_RU.UTF-8"'>/etc/default/locale && \
        dpkg-reconfigure --frontend=noninteractive locales && \
        update-locale LANG=ru_RU.UTF-8

RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /app
CMD gunicorn -b 0.0.0.0:5000 app:app
