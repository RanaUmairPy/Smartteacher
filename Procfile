web: gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers=1
release: python manage.py makemigrations && python manage.py migrate
