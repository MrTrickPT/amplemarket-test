.PHONY: tests

setup-env:
	python -m venv .venv
	. .venv/bin/activate && \
	source .venv/bin/activate


install: setup-env
	pip install --upgrade pip && \
	pip install -r requirements.txt

linter:
	.venv/bin/black . --check

format:
	.venv/bin/black .

run-api:
	./.venv/bin/python src/api.py
