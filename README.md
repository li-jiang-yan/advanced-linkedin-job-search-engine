# Advanced LinkedIn Job Search Engine

An advanced engine to search for jobs on LinkedIn where users can better filter and sort search results.

## Prerequisites

- **Python 3.11 or newer** (developed and tested with Python 3.11)

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

## Running the app

With the virtual environment activated:

```bash
flask --app app run
```

Open http://127.0.0.1:5000/ in your browser.

Health check: http://127.0.0.1:5000/health
