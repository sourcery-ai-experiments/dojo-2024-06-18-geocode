# Copyright 2024 John Hanley. MIT licensed.

SHELL = bash -u -e -o pipefail

VENV_DIR = $(HOME)/.venv/dojo-geocode
ACTIVATE = source $(VENV_DIR)/bin/activate

all: venv libev lint

venv: debug-venv $(VENV_DIR)

debug-venv:
	which python
	python -m site
	python --version

$(VENV_DIR): $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	python -m venv $(VENV_DIR)
	$(ACTIVATE) && which python

	$(ACTIVATE) && pip install -r requirements.txt

# The bjoern WSGI webserver depends on the libev event library.
libev:
	-which brew    &&      brew info libev || brew install libev
	-which apt-get && sudo apt-get install -y libev-dev

URL = http://localhost:8000/

ab:
	bin/python.sh -c 'import bjoern, flask'
	curl $(URL)  2> /dev/null || bin/python.sh web_bench/server.py &
	sleep 1
	curl $(URL)
	@printf '\n\n\n'
	time ab -c 6 -n 10000 $(URL)

lint:
	$(ACTIVATE) && black . && isort . && ruff check .
	$(ACTIVATE) && mypy --strict --warn-unreachable --ignore-missing-imports .

.PHONY: venv debug-venv libev ab lint
