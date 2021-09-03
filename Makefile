#!make

.PHONY: dev sdk sdk_system sdk_script sdk_debug mypy test flake8 vulture

include .env
export $(shell sed 's/=.*//' .env)

dev:
	python -m uvicorn api.main:app --host ${API_HOST} --port ${API_PORT} --reload


sdk:
	make sdk_system
	make sdk_script

sdk_system:
	cls
	py sdk_generation/p0_system/generate_openapi_specs.py
	cd sdk_generation/p0_script && rm -rf api_client
	cd sdk_generation/p0_system && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o api_client -t openapi_templates
	cd sdk_generation/p0_system/api_client && py -2 -m pip install .

sdk_script:
	cls
	py -2.7 sdk_generation/p0_script/generate_openapi_specs.py
	cd sdk_generation/p0_script && rm -rf api_client
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python -c openapi_config.json -o api_client -t openapi_templates
	cd sdk_generation/p0_script/api_client && pip install .


sdk_debug:
	cls
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true

mypy:
	cls
	mypy .

flake8:
	cls
	flake8 .

test:
	cls
	pytest -s tests

vulture:
	cls
	vulture . .\vulture_whitelist.py
