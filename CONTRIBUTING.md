# Contributing

Thanks for helping improve Advanced LinkedIn Job Search Engine.

## Branch Naming

Use a short, descriptive branch name that includes the issue number when
possible. The repository currently uses names like:

- `feature/39-expand-readme-project-overview-prerequisites-install-run-run-test-lint-commands`
- `feature/38-add-ci-status-badge-to-readme`
- `feature/36-steps-checkout-setup-python-cache-pip-install-deps-run-ruff-lintformat-check-run-pytest`

General guidance:

- Prefer lowercase names with hyphens.
- Keep the purpose clear and focused.
- Include the issue number when the work is tied to a specific issue.

## Pull Requests

Before opening a pull request:

- Push the branch to GitHub.
- Open the PR against `main`.
- Include a short summary of what changed and why.
- Link the related issue when applicable.
- Keep the PR focused on one issue or one small set of related changes.

## Quality Checks

Run the same checks locally that the CI workflow uses:

```bash
ruff check .
ruff format --check .
pytest --cov
```

If you want those checks to run automatically before each commit, install the
repository's pre-commit hook:

```bash
pre-commit install
```

If you are working on a new feature or fix, make sure the checks pass before
requesting review.

## PR Checklist

- [ ] `pytest` passes locally.
- [ ] `ruff check .` passes locally.
- [ ] `ruff format --check .` passes locally.
- [ ] No secrets or environment-specific files are committed.
- [ ] The PR description explains what changed and why.
- [ ] The PR is linked to the relevant issue when applicable.

## Notes

- Development dependencies are listed in `requirements-dev.txt`.
- The CI workflow lives in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
