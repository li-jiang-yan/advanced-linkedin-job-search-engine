# Initialize Flask project structure and application skeleton

**Labels:** `infrastructure`

## Summary
Establish the baseline Python/Flask layout so future features have a consistent home.

## Tasks
- [ ] Choose and create project layout (e.g. `app/` package with `__init__.py`, `routes.py`, `templates/`, `static/`)
- [ ] Add a minimal Flask application factory or entry module (`app.py` or `wsgi.py`)
- [ ] Add a health-check route (e.g. `GET /health`) that returns 200
- [ ] Add starter Jinja2 HTML template(s) under `templates/`
- [ ] Add `.gitignore` for Python, virtual environments, IDE files, and `.env`
- [ ] Add `.editorconfig` for consistent formatting across editors

## Acceptance criteria
- `flask --app <entrypoint> run` starts the app locally without errors
- Project structure is documented briefly in the README
- No secrets or local-only files are committed

## Notes
This issue is the foundation for dependency management, linting, testing, and CI workflows.
