#!make

.PHONY: dev sdk

include .env
export $(shell sed 's/=.*//' .env)

dev:
	python -m uvicorn server.main:app --host ${API_HOST} --port ${API_PORT} --reload

midi:
	python server/midi_app.py

spec:
	cls
	python sdk_generation/generate_api_specs.py

sdk:
	make sdk_system
	make sdk_script

sdk_system:
	cls
	cd sdk_generation/p0_system && openapi-generator generate -i http://${API_HOST}:${API_PORT}/openapi.json -g python-legacy -c openapi_config.json -o api_client -t openapi_templates
	cd sdk_generation/p0_system/api_client && py -2 -m pip install .

sdk_script:
	cls
	python sdk_generation/generate_api_specs.py
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python -c openapi_config.json -o api_client -t openapi_templates
	cd sdk_generation/p0_script/api_client && pip install .


sdk_debug:
	cls
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true


mypy:
	cls
	mypy .
