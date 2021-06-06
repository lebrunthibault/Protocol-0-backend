.PHONY: dev, migrate, flask, activate

activate:
	 powershell .\venv\Scripts\activate.ps1

dev:
	C:\Users\thiba\AppData\Local\Microsoft\WindowsApps\python3.exe manage.py runserver

migrate:
	python manage.py migrate

flask:
	flask run