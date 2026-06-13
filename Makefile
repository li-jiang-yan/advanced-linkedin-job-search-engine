# Makefile for common development tasks

.PHONY: install run test test-cov lint format format-check check

install:
	pip install -r requirements-dev.txt

run:
	flask --app app run

test:
	pytest

test-cov:
	pytest --cov

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

check: lint format-check test
