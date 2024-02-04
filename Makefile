.PHONY: tests

setup-env:
	pip install --upgrade poetry
	poetry config virtualenvs.in-project true
	poetry config cache-dir /tmp/poetry-cache

install: setup-env
	poetry install --no-interaction

linter:
	poetry run black . --check

format:
	poetry run black .

run-api:
	poetry run python src/api.py