# Document local development workflow and contribution guidelines

**Labels:** `infrastructure`, `documentation`

## Summary
Make it easy for contributors to set up the project and understand how quality checks run.

## Tasks
- [ ] Expand README: project overview, prerequisites, install, run, test, lint commands
- [ ] Add `CONTRIBUTING.md` with branch naming, PR expectations, and CI requirements
- [ ] Document expected PR checklist (tests pass, lint clean, no secrets committed)
- [ ] Optionally add `Makefile` or `scripts/dev.ps1` / `scripts/dev.sh` for common tasks
- [ ] Link to GitHub Issues for planned work

## Acceptance criteria
- New contributor can follow docs without asking for missing steps
- CONTRIBUTING.md references the same commands used in CI
- README includes links to CONTRIBUTING.md and Actions status

## Depends on
- Scaffold, dependencies, lint, test, and CI issues (document final commands)
