.PHONY: dev, migrate, flask, activate

activate:
	 powershell .\venv\Scripts\activate.ps1

dev:
	python manage.py runserver

migrate:
	python manage.py migrate

flask:
	flask run