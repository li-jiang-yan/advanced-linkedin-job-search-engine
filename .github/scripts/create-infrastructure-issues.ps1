# Creates GitHub issues for repository infrastructure work.
# Prerequisites: gh auth login
# Usage: powershell -ExecutionPolicy Bypass -File .github/scripts/create-infrastructure-issues.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $RepoRoot

gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "GitHub CLI is not authenticated. Run: gh auth login"
    Write-Host "Then re-run: powershell -ExecutionPolicy Bypass -File .github/scripts/create-infrastructure-issues.ps1"
    exit 1
}

$milestoneTitle = "Infrastructure v1"
$milestoneDescription = "Repository scaffold, dependencies, linting, testing, CI, and contributor docs."

function Ensure-Label {
    param([string]$Name, [string]$Color, [string]$Description)
    gh label create $Name --color $Color --description $Description --force 2>$null | Out-Null
}

function Ensure-Milestone {
    param([string]$Title, [string]$Description)
    $milestones = gh api "repos/{owner}/{repo}/milestones" | ConvertFrom-Json
    $existing = ($milestones | Where-Object { $_.title -eq $Title }).number
    if ($existing) {
        Write-Host "Milestone already exists: $Title (#$existing)"
        return [int]$existing
    }
    $created = gh api -X POST "repos/{owner}/{repo}/milestones" `
        -f title="$Title" `
        -f description="$Description" `
        -f state="open" | ConvertFrom-Json
    Write-Host "Created milestone: $Title (#$($created.number))"
    return [int]$created.number
}

Ensure-Label "infrastructure" "0E8A16" "Repository setup, tooling, and CI/CD"
Ensure-Label "ci" "1D76DB" "Continuous integration and GitHub Actions"
Ensure-Label "testing" "FBCA04" "Unit and integration tests"
Ensure-Label "documentation" "0075CA" "Docs and contributor guidance"

$milestoneNumber = Ensure-Milestone -Title $milestoneTitle -Description $milestoneDescription

$issueTemplates = @(
    @{
        Title = "Initialize Flask project structure and application skeleton"
        Labels = "infrastructure"
        DependsOn = @()
        Body = @"
## Summary
Establish the baseline Python/Flask layout so future features have a consistent home.

## Tasks
- [ ] Choose and create project layout (e.g. ``app/`` package with ``__init__.py``, ``routes.py``, ``templates/``, ``static/``)
- [ ] Add a minimal Flask application factory or entry module (``app.py`` or ``wsgi.py``)
- [ ] Add a health-check route (e.g. ``GET /health``) that returns 200
- [ ] Add starter Jinja2 HTML template(s) under ``templates/``
- [ ] Add ``.gitignore`` for Python, virtual environments, IDE files, and ``.env``
- [ ] Add ``.editorconfig`` for consistent formatting across editors

## Acceptance criteria
- ``flask --app <entrypoint> run`` starts the app locally without errors
- Project structure is documented briefly in the README
- No secrets or local-only files are committed

## Notes
This issue is the foundation for dependency management, linting, testing, and CI workflows.
"@
    },
    @{
        Title = "Add Python dependency management (requirements and dev extras)"
        Labels = "infrastructure"
        DependsOn = @("scaffold")
        Body = @"
## Summary
Pin runtime and development dependencies so local setup and CI are reproducible.

## Tasks
- [ ] Add ``requirements.txt`` with pinned Flask and core runtime dependencies
- [ ] Add ``requirements-dev.txt`` (or optional extras in ``pyproject.toml``) for dev/test/lint tools
- [ ] Document Python version requirement (recommend 3.11+)
- [ ] Add ``.env.example`` listing required environment variables (no secrets)
- [ ] Update README with virtual environment creation and install steps

## Acceptance criteria
- Fresh clone + documented install steps allow running the Flask app
- Dev dependencies are separated from production/runtime dependencies
- Dependency files are suitable for use in GitHub Actions

## Depends on
{{DEPENDS_ON}}
"@
    },
    @{
        Title = "Configure linting and formatting with Ruff"
        Labels = "infrastructure,ci"
        DependsOn = @("scaffold", "dependencies")
        Body = @"
## Summary
Add automated code quality checks for Python source using Ruff (linter + formatter).

## Tasks
- [ ] Add Ruff to development dependencies
- [ ] Add ``pyproject.toml`` (or ``ruff.toml``) with project rules (line length, target Python version, select rules)
- [ ] Add ``make lint`` / documented ``ruff check`` and ``ruff format --check`` commands
- [ ] Fix or exclude any initial violations in scaffold code
- [ ] Document how to run lint/format locally and auto-fix with ``ruff format``

## Acceptance criteria
- ``ruff check .`` exits 0 on the default branch
- ``ruff format --check .`` exits 0 on the default branch
- Lint/format configuration is committed and documented

## Depends on
{{DEPENDS_ON}}
"@
    },
    @{
        Title = "Set up pytest unit testing framework"
        Labels = "infrastructure,testing"
        DependsOn = @("scaffold", "dependencies")
        Body = @"
## Summary
Introduce a test suite with pytest and Flask test client support.

## Tasks
- [ ] Add ``pytest`` and ``pytest-cov`` to development dependencies
- [ ] Create ``tests/`` package with ``conftest.py`` exposing a Flask test client fixture
- [ ] Add initial unit tests (e.g. health route returns 200, app factory creates app)
- [ ] Add ``pytest.ini`` or ``pyproject.toml`` ``[tool.pytest.ini_options]`` configuration
- [ ] Document running tests locally: ``pytest`` and ``pytest --cov``

## Acceptance criteria
- ``pytest`` runs and passes locally with at least one meaningful Flask route test
- Test layout follows pytest conventions and is ready for CI
- Coverage reporting is configured (threshold optional for now)

## Depends on
{{DEPENDS_ON}}
"@
    },
    @{
        Title = "Add GitHub Actions CI workflow for lint and test"
        Labels = "infrastructure,ci"
        DependsOn = @("lint", "testing")
        Body = @"
## Summary
Run linting and unit tests automatically on pull requests and pushes to ``main``.

## Tasks
- [ ] Add ``.github/workflows/ci.yml`` triggered on ``push`` and ``pull_request`` to ``main``
- [ ] Matrix or single job on Ubuntu with supported Python version(s) (e.g. 3.11, 3.12)
- [ ] Steps: checkout, setup Python, cache pip, install deps, run Ruff lint/format check, run pytest
- [ ] Fail the workflow if lint or tests fail
- [ ] Add CI status badge to README

## Acceptance criteria
- Opening a PR runs CI and reports pass/fail on GitHub
- Workflow completes in a reasonable time (< 5 min for scaffold project)
- README shows CI badge linked to Actions

## Depends on
{{DEPENDS_ON}}
"@
    },
    @{
        Title = "Document local development workflow and contribution guidelines"
        Labels = "infrastructure,documentation"
        DependsOn = @("scaffold", "dependencies", "lint", "testing", "ci")
        Body = @"
## Summary
Make it easy for contributors to set up the project and understand how quality checks run.

## Tasks
- [ ] Expand README: project overview, prerequisites, install, run, test, lint commands
- [ ] Add ``CONTRIBUTING.md`` with branch naming, PR expectations, and CI requirements
- [ ] Document expected PR checklist (tests pass, lint clean, no secrets committed)
- [ ] Optionally add ``Makefile`` or ``scripts/dev.ps1`` / ``scripts/dev.sh`` for common tasks
- [ ] Link to GitHub Issues for planned work

## Acceptance criteria
- New contributor can follow docs without asking for missing steps
- CONTRIBUTING.md references the same commands used in CI
- README includes links to CONTRIBUTING.md and Actions status

## Depends on
{{DEPENDS_ON}}
"@
    }
)

$issueKeys = @("scaffold", "dependencies", "lint", "testing", "ci", "docs")
$issueRefs = @{}

Write-Host "Creating infrastructure issues on $(gh repo view --json nameWithOwner -q .nameWithOwner)..."

$created = @()
for ($i = 0; $i -lt $issueTemplates.Count; $i++) {
    $template = $issueTemplates[$i]
    $key = $issueKeys[$i]

    $dependsLines = @()
    foreach ($dep in $template.DependsOn) {
        if ($issueRefs.ContainsKey($dep)) {
            $ref = $issueRefs[$dep]
            $dependsLines += "- #$($ref.Number) $($ref.Title)"
        }
    }
    if ($dependsLines.Count -eq 0) {
        $dependsText = "- None (start here)"
    } else {
        $dependsText = ($dependsLines -join "`n")
    }

    $body = $template.Body -replace "\{\{DEPENDS_ON\}\}", $dependsText
    $labelArgs = ($template.Labels -split "," | ForEach-Object { "--label"; $_.Trim() })

    $bodyFile = New-TemporaryFile
    try {
        Set-Content -Path $bodyFile -Value $body -Encoding utf8
        Write-Host "Creating: $($template.Title)"
        $url = gh issue create `
            --title $template.Title `
            @labelArgs `
            --milestone $milestoneTitle `
            --body-file $bodyFile
        $number = ($url -replace ".*/", "")
        $issueRefs[$key] = [PSCustomObject]@{ Number = [int]$number; Title = $template.Title; Url = $url }
        $created += $issueRefs[$key]
        Write-Host "  -> $url"
    }
    finally {
        Remove-Item $bodyFile -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "Milestone: $milestoneTitle (#$milestoneNumber)"
Write-Host "Created $($created.Count) issues:"
$created | ForEach-Object { Write-Host "  #$($_.Number)  $($_.Url)" }
