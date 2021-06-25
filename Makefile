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
	cls
	python sdk_generation/generate_api_specs.py

sdk:
	cls
	openapi-generator generate -i http://localhost:8000/openapi.json -g python-legacy -c openapi_config.json -o p0_system_api -t openapi_templates/via_midi/python_legacy
	cd p0_system_api && pip install .

sdk_script:
	cls
	python sdk_generation/generate_api_specs.py
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o api_client -t openapi_templates
	cd sdk_generation/p0_script/api_client && pip install .


sdk_debug:
	cls
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true


mypy:
	cls
	mypy .
