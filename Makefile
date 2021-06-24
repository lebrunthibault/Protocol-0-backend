#!make

.PHONY: dev sdk

include .env
export $(shell sed 's/=.*//' .env)

PYTHON := C:\Users\thiba\AppData\Local\Programs\Python\Python37\python.exe

dev:
	${PYTHON} -m uvicorn server.main:app --host ${API_HOST} --port ${API_PORT} --reload

midi:
	${PYTHON} server/midi_app.py

spec:
	${PYTHON} sdk_generation/generate_api_specs.py

sdk:
	cls
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy -c openapi_config.json -o p0_system_api -t openapi_templates/via_midi/python_legacy
	cd p0_system_api && pip install .

sdk_debug:
	cls
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy --library urllib3 -o api_client -t openapi_templates/python_legacy --global-property debugModels=true
	cd api_client && pip install .


mypy:
	cls
	mypy .
