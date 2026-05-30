# Configure linting and formatting with Ruff

**Labels:** `infrastructure`, `ci`

## Summary
Add automated code quality checks for Python source using Ruff (linter + formatter).

## Tasks
- [ ] Add Ruff to development dependencies
- [ ] Add `pyproject.toml` (or `ruff.toml`) with project rules (line length, target Python version, select rules)
- [ ] Add `make lint` / documented `ruff check` and `ruff format --check` commands
- [ ] Fix or exclude any initial violations in scaffold code
- [ ] Document how to run lint/format locally and auto-fix with `ruff format`

## Acceptance criteria
- `ruff check .` exits 0 on the default branch
- `ruff format --check .` exits 0 on the default branch
- Lint/format configuration is committed and documented

## Depends on
- Project scaffold and dependency management issues
