# Makefile for common development tasks

.PHONY: lint format format-check check

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

check: lint format-check
