.PHONY: dev sdk

PYTHON := C:\Users\thiba\AppData\Local\Programs\Python\Python39\python.exe

dev:
	${PYTHON} server\manage.py runserver

sdk:
	openapi-generator generate -i http://localhost:8000/openapi.json -g python -o api_client -t openapi_templates
	rm -f api_client/dist

mypy:
	cls
	mypy .
