.PHONY: test black flake8 mypy vulture pycharm check

test:
	cls
	pytest -s .

black:
	black .

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
	make test
	make flake8
	make mypy
	make vulture
