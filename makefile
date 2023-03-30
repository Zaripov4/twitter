migrate:
	python manage.py migrate

run: migrate
	python manage.py runserver
