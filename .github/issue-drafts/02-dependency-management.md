# Add Python dependency management (requirements and dev extras)

**Labels:** `infrastructure`

## Summary
Pin runtime and development dependencies so local setup and CI are reproducible.

## Tasks
- [ ] Add `requirements.txt` with pinned Flask and core runtime dependencies
- [ ] Add `requirements-dev.txt` (or optional extras in `pyproject.toml`) for dev/test/lint tools
- [ ] Document Python version requirement (recommend 3.11+)
- [ ] Add `.env.example` listing required environment variables (no secrets)
- [ ] Update README with virtual environment creation and install steps

## Acceptance criteria
- Fresh clone + documented install steps allow running the Flask app
- Dev dependencies are separated from production/runtime dependencies
- Dependency files are suitable for use in GitHub Actions

## Depends on
- Flask project scaffold issue
