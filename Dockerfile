FROM python:3.12-alpine
LABEL authors="kkh147.17.3"

RUN pip install poetry

COPY ./pyproject.toml /mandalart/pyproject.toml
WORKDIR /mandalart
RUN poetry install
COPY ./src /mandalart/src
COPY ./.env /mandalart/.env
COPY ./logging_config.json /mandalart/logging_config.json

WORKDIR /mandalart/src
CMD poetry run gunicorn --bind 0:8000 \
            main:app \
          --preload \  
          --workers 2 \
          --worker-class uvicorn.workers.UvicornWorker \
          --access-logfile /var/log/fastapi/access.log \
          --error-logfile /var/log/fastapi/error.log \
          --log-config-json /mandalart/logging_config.json