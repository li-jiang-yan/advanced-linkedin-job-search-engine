# Set up pytest unit testing framework

**Labels:** `infrastructure`, `testing`

## Summary
Introduce a test suite with pytest and Flask test client support.

## Tasks
- [ ] Add `pytest` and `pytest-cov` to development dependencies
- [ ] Create `tests/` package with `conftest.py` exposing a Flask test client fixture
- [ ] Add initial unit tests (e.g. health route returns 200, app factory creates app)
- [ ] Add `pytest.ini` or `pyproject.toml` `[tool.pytest.ini_options]` configuration
- [ ] Document running tests locally: `pytest` and `pytest --cov`

## Acceptance criteria
- `pytest` runs and passes locally with at least one meaningful Flask route test
- Test layout follows pytest conventions and is ready for CI
- Coverage reporting is configured (threshold optional for now)

## Depends on
- Project scaffold and dependency management issues
