# Advanced LinkedIn Job Search Engine

[![CI](https://github.com/li-jiang-yan/advanced-linkedin-job-search-engine/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/li-jiang-yan/advanced-linkedin-job-search-engine/actions/workflows/ci.yml)

## Project Overview

Advanced LinkedIn Job Search Engine is a Flask application for searching LinkedIn
job listings with a cleaner workflow and a structure that makes it easier to add
filters, sorting, and other search improvements over time.

## Prerequisites

- **Python 3.11 or newer**. The project is developed and tested with Python 3.11.
- **Git**
- **pip**

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:li-jiang-yan/advanced-linkedin-job-search-engine.git
cd advanced-linkedin-job-search-engine
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Runtime dependencies only:

```bash
pip install -r requirements.txt
```

For development (tests and linting):

```bash
pip install -r requirements-dev.txt
```

To enable automatic checks before each commit:

```bash
pre-commit install
```

## Running the App

With the virtual environment activated:

```bash
flask --app app run
```

Open http://127.0.0.1:5000/ in your browser.

Health check: http://127.0.0.1:5000/health

## Linting and formatting

This project uses Ruff for linting and formatting.

### Check for linting violations

```bash
make lint
```

Or directly with Ruff:

```bash
ruff check .
```

### Auto-fix formatting issues

```bash
make format
```

Or directly with Ruff:

```bash
ruff format .
```

### Verify formatting without modifying files

```bash
ruff format --check .
```

## Testing

With the virtual environment activated and development dependencies installed,
run the test suite locally with:

```bash
pytest
```

To include coverage reporting, run:

```bash
pytest --cov
```

## Pre-commit Hooks

This repository uses pre-commit to run Ruff and pytest before each commit.

Install the hook once after installing the development dependencies:

```bash
pre-commit install
```

Run the hooks against all files whenever you want a full local check:

```bash
pre-commit run --all-files
```

## Quick Reference

### Install

```bash
pip install -r requirements-dev.txt
```

### Run

```bash
flask --app app run
```

### Test

```bash
pytest
pytest --cov
```

### Lint

```bash
make lint
make format
make format-check
```

### Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Planned Work

The current roadmap and open tasks are tracked in the GitHub Issues list:

https://github.com/li-jiang-yan/advanced-linkedin-job-search-engine/issues

### 4. Configure environment variables (optional)

Copy the example file and adjust values for local development:

**Windows (PowerShell):**

```powershell
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

See `.env.example` for available variables.
