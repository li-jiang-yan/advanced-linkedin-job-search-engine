# Add GitHub Actions CI workflow for lint and test

**Labels:** `infrastructure`, `ci`

## Summary
Run linting and unit tests automatically on pull requests and pushes to `main`.

## Tasks
- [ ] Add `.github/workflows/ci.yml` triggered on `push` and `pull_request` to `main`
- [ ] Matrix or single job on Ubuntu with supported Python version(s) (e.g. 3.11, 3.12)
- [ ] Steps: checkout, setup Python, cache pip, install deps, run Ruff lint/format check, run pytest
- [ ] Fail the workflow if lint or tests fail
- [ ] Add CI status badge to README

## Acceptance criteria
- Opening a PR runs CI and reports pass/fail on GitHub
- Workflow completes in a reasonable time (< 5 min for scaffold project)
- README shows CI badge linked to Actions

## Depends on
- Linting/formatting configuration issue
- pytest setup issue
