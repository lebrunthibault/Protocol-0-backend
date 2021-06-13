#!make

.PHONY: dev sdk

include .env
export $(shell sed 's/=.*//' .env)

PYTHON := C:\Users\thiba\AppData\Local\Programs\Python\Python39\python.exe
EGG_FILE := C:\Users\thiba\AppData\Roaming\Python\Python27\site-packages\openapi_client-1.0.0-py2.7.egg

dev:
	uvicorn server.main:app --host ${API_HOST} --port ${API_PORT} --reload

sdk:
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy -o api_client -t openapi_templates/python_legacy
	if exist "${EGG_FILE}" rm "${EGG_FILE}"
	cd api_client && python setup.py install --user
	rmdir /s /q "api_client/build"
	rmdir /s /q "api_client/dist"
	cd ..


mypy:
	cls
	mypy .
