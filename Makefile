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
	cd sdk_generation/p0_system/p0_script_client && rm -rf api_client
	cd sdk_generation/p0_system && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_script_client\api_client -t p0_script_client\openapi_templates
	cd "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\protocol0" && .\venv\Scripts\activate.ps1 && venv\Scripts\pip.exe install "C:\Users\thiba\google_drive\music\dev\protocol0_system\sdk_generation\p0_system\p0_script_client\api_client"

	cd sdk_generation/p0_system/p0_system_client && rm -rf api_client
	cd sdk_generation/p0_system && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_system_client\api_client -t p0_system_client\openapi_templates
	pip install ".\sdk_generation\p0_system\p0_system_client\api_client"

sdk_script:
	cls
	py -2.7 sdk_generation/p0_script/generate_openapi_specs.py
	cd sdk_generation/p0_script && rm -rf api_client
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python -c openapi_config.json -o api_client -t openapi_templates
	pip install ".\sdk_generation\p0_script\api_client"

sdk_debug:
	cls
	cd sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true

test:
	cls
	pytest -s tests

flake8:
	cls
	flake8 .

mypy:
	cls
	mypy .

vulture:
	cls
	vulture . .\vulture_whitelist.py

check:
	make flake8
	make mypy
