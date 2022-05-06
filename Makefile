#!make

.PHONY: midi_server, http_server, celery, sdk, sdk_debug, test, flake8, mypy, vulture, check

celery:
	watchmedo auto-restart --directory=./gui --pattern=*.py --recursive -- celery -A gui worker -E --without-heartbeat --without-gossip --without-mingle -l info --loglevel=INFO

celery_flower:
	watchmedo auto-restart --directory=./gui --pattern=*.py --recursive -- powershell scripts/powershell/start_celery_flower.ps1

http_server:
	uvicorn api.http_server.main:app --port 8000 --reload

midi_server:
	watchmedo auto-restart --directory=. --pattern="api/midi_server/*.py;api/midi_server/**/*.py;api/client/*.py;lib/*.py;lib/**/*.py" --recursive --ignore-directories -- python .\scripts\start_midi_server.py

sdk:
	cls
	py -3.7 scripts/cli.py generate_openapi_specs

	cd api/midi_server/sdk_generation/p0_script_client && rm -rf api_client
	cd api/midi_server/sdk_generation && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_script_client\api_client -t p0_script_client\openapi_templates
	cd "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\protocol0" && .\venv\Scripts\activate.ps1 && venv\Scripts\pip.exe install "C:\Users\thiba\dev\protocol0_backend\api\midi_server\sdk_generation\p0_script_client\api_client"

	cd api/midi_server/sdk_generation/p0_backend_client && rm -rf api_client
	cd api/midi_server/sdk_generation && openapi-generator generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_backend_client\api_client -t p0_backend_client\openapi_templates
	pip install ".\api\midi_server\sdk_generation\p0_backend_client\api_client"

sdk_debug:
	cls
	cd api/midi_server/sdk_generation/p0_script && openapi-generator generate -i openapi.yaml -g python-legacy -o api_client -t ../openapi_templates/via_midi/python_legacy --global-property debugOperations=true

cli-test:
	cls
	py -3.7 scripts/cli.py test

test:
	cls
	pytest -s tests

flake8:
	cls
	py -3.7 -m flake8 .

mypy:
	cls
	py -3.7 -m mypy .

vulture:
	cls
	vulture . .\vulture_whitelist.py

check:
	make flake8
	make mypy
