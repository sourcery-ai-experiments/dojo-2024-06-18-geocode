# Copyright 2024 John Hanley. MIT licensed.

VENV_DIR = $(HOME)/.venv/dojo-geocode
ACTIVATE = source $(VENV_DIR)/bin/activate

all: venv lint

venv: debug-venv $(VENV_DIR)

debug-venv:
	which python
	python -m site
	python --version

$(VENV_DIR):
	python -m venv $(VENV_DIR)
	$(ACTIVATE) && which python

	$(ACTIVATE) && pip install -r requirements.txt

lint:
	$(ACTIVATE) && black . && isort . && ruff check .
	$(ACTIVATE) && mypy --strict .

.PHONY: venv debug-venv lint
