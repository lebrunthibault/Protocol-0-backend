#!make

.PHONY: sdk sdk_debug mypy test flake8 vulture

sdk:
	cls
	py scripts/cli.py generate_openapi_specs

	cd api/sdk_generation/p0_script_client && rm -rf api_client
	cd api/sdk_generation && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_script_client\api_client -t p0_script_client\openapi_templates
	cd "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\protocol0" && .\venv\Scripts\activate.ps1 && venv\Scripts\pip.exe install "C:\Users\thiba\google_drive\music\dev\protocol0_system\api\sdk_generation\p0_script_client\api_client"

	cd api/sdk_generation/p0_backend_client && rm -rf api_client
	cd api/sdk_generation && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_backend_client\api_client -t p0_backend_client\openapi_templates
	pip install ".\api\sdk_generation\p0_backend_client\api_client"

sdk_debug:
	cls
	cd api/sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true

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
