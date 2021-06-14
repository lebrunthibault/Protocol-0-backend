#!make

.PHONY: dev sdk

include .env
export $(shell sed 's/=.*//' .env)

PYTHON := C:\Users\thiba\AppData\Local\Programs\Python\Python39\python.exe

dev:
	uvicorn server.main:app --host ${API_HOST} --port ${API_PORT} --reload

sdk:
	cls
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy --library urllib3 -o api_client -t openapi_templates/python_legacy
	cd api_client && pip install .

sdk_debug:
	cls
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy --library urllib3 -o api_client -t openapi_templates/python_legacy --global-property debugModels=true
	cd api_client && pip install .


mypy:
	cls
	mypy .
