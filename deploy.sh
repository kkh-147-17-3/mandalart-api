#!/bin/zsh
cd src || exit
poetry run gunicorn --bind 0:8000 main:app --worker-class uvicorn.workers.UvicornWorker