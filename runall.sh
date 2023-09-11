#!/bin/bash

docker-compose up &

sleep 10

celery -A SheepFish worker --loglevel=info -P threads &

sleep 5

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

cd frontend
python -m http.server 3000 &
