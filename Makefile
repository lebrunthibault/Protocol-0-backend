#!make

.PHONY: celery, celery_flower, midi_server, http_server, sdk, sdk_debug, test, black, flake8, mypy, vulture, check

celery:
	venv/scripts/watchmedo auto-restart --directory=./gui --pattern=*.py --recursive -- venv/Scripts/celery -A gui worker --events --concurrency=10 --without-heartbeat --without-gossip --without-mingle --loglevel=INFO --pool=gevent

celery_flower:
	venv/scripts/watchmedo auto-restart --directory=./gui --pattern=*.py --recursive -- powershell scripts/powershell/start_celery_flower.ps1

http_server:
	venv/scripts/uvicorn api.http_server.main:app --port 8000 --reload --workers 4

midi_server:
	venv\scripts\watchmedo auto-restart --directory=. --pattern="api/midi_server/*.py;api/midi_server/**/*.py;api/client/*.py;lib/*.py;lib/**/*.py;lib/**/**/*.py" --recursive --ignore-directories -- venv\scripts\python .\scripts\start_midi_server.py

logs:
	venv/scripts/python scripts/tail_protocol0_logs.py

sdk:
	cls
	venv/scripts/python scripts/cli.py generate_openapi_specs

	cd api/midi_server/sdk_generation/p0_script_client && del /f /q api_client
	cd api/midi_server/sdk_generation && java -jar openapi-generator-cli.jar generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_script_client\api_client -t p0_script_client\openapi_templates
	cd "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\protocol0" && venv\Scripts\pip.exe install "C:\Users\thiba\dev\protocol0_backend\api\midi_server\sdk_generation\p0_script_client\api_client"

	cd api/midi_server/sdk_generation/p0_backend_client && del /f /q api_client
	cd api/midi_server/sdk_generation && java -jar openapi-generator-cli.jar generate -i openapi.yaml -g python-legacy -c openapi_config.json -o p0_backend_client\api_client -t p0_backend_client\openapi_templates
	venv/scripts/pip install ".\api\midi_server\sdk_generation\p0_backend_client\api_client"

test:
	cls
	venv/scripts/python -u scripts/cli.py test

flake8:
	cls
	venv/scripts/python -m flake8 .

black:
	cls
	venv/scripts/python -m black .

mypy:
	cls
	venv/scripts/python -m mypy .

vulture:
	cls
	./venv/scripts/vulture . .\vulture_whitelist.py --make-whitelist --exclude=venv/,api_client/,routes.py

check:
	make black
	make flake8
	make mypy
	make vulture
	@echo "ok"
