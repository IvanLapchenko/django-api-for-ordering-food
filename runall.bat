@echo off

start docker compose up

timeout /t 10 /nobreak

start celery -A SheepFish worker --loglevel=info -P threads

timeout /t 5 /nobreak

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

start python manage.py runserver

cd frontend
start python -m http.server 3000
