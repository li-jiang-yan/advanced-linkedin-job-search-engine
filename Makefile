# Makefile for common development tasks

.PHONY: lint format-check check

lint:
	ruff check .

format-check:
	ruff format --check .

check: lint format-check
