python3 manage.py migrate
python3 manage.py createsuperuser --password=${SUPERUSER_PASSWORD} --username=${SUPERUSER_USERNAME} --no-input
python3 manage.py runserver 0.0.0.0:8000
