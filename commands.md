# Test Execution Commands

This document provides quick reference for running different test categories.

## Quick Commands

### Smoke Tests (Fast, Critical Path)
```bash
# Run all smoke tests
pytest -m smoke

# Run smoke tests with verbose output
pytest -m smoke -v

# Run smoke tests and generate Allure report
pytest -m smoke --alluredir=reports/allure-results
```

### Regression Tests (Full Suite)
```bash
# Run all regression tests
pytest -m regression

# Run regression tests with parallel execution
pytest -m regression -n auto

# Run regression tests with video recording on failure
pytest -m regression -v
```

### Sanity Tests (Core Functionality)
```bash
# Run sanity checks only
pytest -m sanity

# Sanity tests with live browser output
pytest -m sanity -v --headed
```

### Critical Tests (Must Always Pass)
```bash
# Run only critical priority tests
pytest -m critical

# Critical tests with extended timeout
pytest -m critical --timeout=60
```

## By Feature/Module

```bash
# Authentication tests only
pytest -m auth

# Dashboard tests only
pytest -m dashboard

# Device management tests only
pytest -m device

# Role management tests only
pytest -m role
```

## By Environment

```bash
# Staging environment tests
pytest -m staging

# Production deployment verification
pytest -m production
```

## Combined Markers

```bash
# Smoke tests that are also critical
pytest -m "smoke and critical"

# Regression excluding slow tests
pytest -m "regression and not slow"

# Dashboard tests excluding known flaky ones
pytest -m "dashboard and not flaky"

# Authentication tests for production
pytest -m "auth and production"
```

## Running Specific Test Files

```bash
# Run a single test file
pytest tests/test_login_page.py

# Run a specific test class
pytest tests/test_login_page.py::TestLoginPage

# Run a specific test method
pytest tests/test_login_page.py::TestLoginPage::test_login_with_valid_credentials

# Run tests matching a keyword
pytest -k "login" -v
```

## Parallel Execution

```bash
# Auto-detect CPU cores for parallel execution
pytest -m regression -n auto

# Use specific number of workers
pytest -m regression -n 4

# Parallel with verbose output
pytest -m regression -n auto -v
```

## Reporting & Artifacts

```bash
# Generate Allure report
pytest -m smoke --alluredir=reports/allure-results

# View Allure report (requires allure CLI)
allure serve reports/allure-results

# Generate HTML report
pytest -m regression --html=reports/report.html --self-contained-html

# Capture detailed logs
pytest -m regression -v --log-cli-level=DEBUG
```

```bash
# Generate custom dashboard report for a specific project
.\.venv\Scripts\python utils\generate_reports.py -p atcu

# Generate custom dashboard report for a different project
.\.venv\Scripts\python utils\generate_reports.py -p lct

# Generate report with multiple test markers (comma-separated, space-separated, or quoted)
.\.venv\Scripts\python utils\generate_reports.py --project lct --markers smoke, ui
.\.venv\Scripts\python utils\generate_reports.py --project lct --markers "smoke, ui"
.\.venv\Scripts\python utils\generate_reports.py --project lct --markers smoke ui

# Trigger GitHub Actions workflow for a specific project with test markers
python utils/trigger_project_report.py --owner Accolade-Qa --repo LCT_A4G_AUTO --token YOUR_TOKEN --project lct --marker smoke, ui
python utils/trigger_project_report.py --owner Accolade-Qa --repo LCT_A4G_AUTO --token YOUR_TOKEN --project lct --marker "smoke or ui"

# Generate report from existing JSON without running pytest
.\.venv\Scripts\python utils\generate_reports.py --project atcu --skip-pytest

# Generate report into a custom directory
.\.venv\Scripts\python utils\generate_reports.py --project atcu --report-dir reports
```

## Browser & Display Options

```bash
# Run with Firefox browser
pytest -m smoke --browser firefox

# Run with WebKit browser
pytest -m smoke --browser webkit

# Run headless (no visual browser window)
pytest -m regression --headed=false

# Run with visual browser window
pytest -m regression --headed
```

## Debugging & Troubleshooting

```bash
# Stop on first failure
pytest -m regression -x

# Show prints and logging
pytest -m regression -s

# Run only failed tests from last run
pytest -m regression --lf

# Run failed tests + new tests
pytest -m regression --ff

# Drop into debugger on failure
pytest -m regression --pdb

# Show slowest tests
pytest -m regression --durations=10
```

## CI Pipeline Examples

```bash
# Quick smoke test run
pytest -m smoke --headless --browser chromium --alluredir=reports/allure-results

# Full regression suite
pytest -m regression -n auto --browser chromium --alluredir=reports/allure-results -v

# Critical path verification
pytest -m critical --browser chromium --alluredir=reports/allure-results
```

## Environment-Specific Setups

```bash
# Ensure .env is set correctly, then run
pytest -m smoke

# Override configuration via environment variables
BASE_URL=https://staging.app.com BROWSER=firefox pytest -m smoke

# Run against production (use with caution!)
DASHBOARD_URL=https://prod.app.com pytest -m "regression and production"
```

## Available Markers

| Marker | Purpose | Speed | Use Case |
|--------|---------|-------|----------|
| `smoke` | Critical path validation | Fast | Pre-deployment checks |
| `regression` | Full feature suite | Medium-Slow | Regular CI runs |
| `sanity` | Core functionality | Fast | Nightly builds |
| `critical` | Must-pass tests | Medium | Gating |
| `auth` | Login & permissions | Medium | Auth changes |
| `dashboard` | Dashboard features | Medium | Dashboard updates |
| `device` | Device management | Medium | Device-related changes |
| `slow` | Long-running tests | Slow | Nightly only |
| `flaky` | Known issues | Variable | Isolated runs |

---

## Quick Setup

If you're new to this repo:

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   playwright install
   ```

2. **Copy & configure `.env`:**
   ```bash
   BASE_URL=https://your-app.com
   DASHBOARD_URL=https://your-app.com/dashboard
   APP_USERNAME=testuser
   APP_PASSWORD=testpass
   BROWSER=chromium
   HEADLESS=false
   ```

3. **Run your first smoke test:**
   ```bash
   pytest -m smoke -v
   ```


## Running All Projects

   PowerShell — run sequentially (sets `PROJECT` per run):
   ```powershell
   $projects = 'lct','sampark','swaraj','trio'
   foreach ($p in $projects) {
      $env:PROJECT = $p
      python -m pytest tests -q --project $p
   }
   ```

   PowerShell — run in parallel using background jobs:
   ```powershell
   $projects = 'lct','sampark','swaraj','trio'
   $jobs = @()
   foreach ($p in $projects) {
      $jobs += Start-Job -ScriptBlock { param($proj) python -m pytest tests -q --project $proj } -ArgumentList $p
   }
   Wait-Job -Job $jobs
   $jobs | Receive-Job
   ```

   PowerShell — run with CPU affinity (use the provided runner):
   ```powershell
   # Launch one pytest process per project and bind to cores
   PowerShell -ExecutionPolicy Bypass -File run-parallel-projects.ps1
   ```

   Bash (Linux / WSL) — sequential:
   ```bash
   for p in lct sampark swaraj trio; do
      PROJECT=$p python -m pytest tests -q --project $p || exit 1
   done
   ```

   Bash — parallel with background processes (logs per project):
   ```bash
   for p in lct sampark swaraj trio; do
      PROJECT=$p python -m pytest tests -q --project $p > tests_$p.log 2>&1 &
   done
   wait
   ```

   Notes:
   - The `run-parallel-projects.ps1` script uses `start /affinity` to set CPU affinity per process. If you prefer `taskset` on Linux/WSL, I can add a bash runner.
   - Tune project list and pytest options (`-n auto`, markers, verbosity) to your CI needs.


## activate the virtual enviroment by command  
```bash
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& d:\AEPL_AUTOMATION\ALL_PROJECTS_AUTOMATION\.venv\Scripts\Activate.ps1)
```

## deactivate virtual envirometn 
```bash
if (Get-Command deactivate -ErrorAction SilentlyContinue) { deactivate }
```

## Remove the __pycache__ folders from all folders
```bash
   Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Force -Recurse
```

## Local Security & Static Analysis

### Python Security Linter (Bandit)

```bash
# Install Bandit
pip install bandit

# Scan all Python files recursively in the current directory
bandit -r .

# Scan excluding virtual environments and tests
bandit -r . -x .venv,tests

# Export scan results to HTML report
bandit -r . -f html -o bandit_report.html
```

### Git Secrets Scanner (Gitleaks)

```powershell
# Install Gitleaks on Windows using winget
winget install Gitleaks.Gitleaks

# Scan the current state of your workspace
gitleaks detect --source . --verbose

# Scan your entire commit history for leaks
gitleaks detect --source . --log-opts="--all" --verbose

# Generate scan report in JSON format
gitleaks detect --source . --report-path leaks_report.json
```

---

## GitHub Actions Reporting Dispatch Guide

This guide captures the complete trigger flow for the reporting workflow, including:

- workflow trigger types
- project and marker selection
- external invocation from Bitbucket or other CI
- token requirements and security considerations

### Supported trigger methods

The reporting workflow can be started by:

1. `push` events on selected branches:
   - `main`
   - `master`
   - `atcu`
2. Manual `workflow_dispatch`
3. External `repository_dispatch`

### What the workflow does

When triggered, the workflow:

- checks out the repository
- installs Python and Playwright dependencies
- runs tests using `python utils/generate_reports.py`
- generates JSON, HTML, and Excel reports
- verifies report files
- uploads artifacts
- sends an email notification with attached reports

### Supported trigger inputs

#### `workflow_dispatch`

Inputs available when run manually from GitHub:

- `project`: target project name, e.g. `lct`, `atcu`
- `marker`: pytest marker expression, e.g. `smoke`, `api`, `regression and not slow`
- `report_dir`: destination directory for reports, default `reports`

#### `repository_dispatch`

External systems must send payload values via `client_payload`:

- `project`: target project name, e.g. `lct`, `atcu`
- `marker`: pytest marker expression
- `report_dir`: destination directory for reports

#### Important compatibility note

- `repository_dispatch` triggers the workflow definition on the default branch (`master`).
- `workflow_dispatch` can target a branch via `ref`.

### Branch behavior

#### When to use `repository_dispatch`

- Use it for external triggers from another CI system or script.
- It runs the workflow defined on the repository default branch.
- In this repo, the default branch is `master`.
- Therefore the workflow file must exist on `master` for `repository_dispatch` to work.

#### When to use `workflow_dispatch`

- Use it when you need to trigger the workflow from a specific branch.
- It can run the workflow file from `atcu`, `master`, or any branch where the file exists.
- This is the best choice if your trigger source needs branch-specific behavior.

### Use cases

#### 1. Trigger from another CI after deploy

Scenario:
- developer pushes code to Bitbucket
- deploy succeeds in Bitbucket pipeline
- the pipeline sends a GitHub API request to trigger the reporting workflow

Result:
- GitHub runs the reporting workflow independently
- no repo clone or GitHub checkout is required on the developer machine

#### 2. External curl trigger from a shell or script

You can trigger the workflow from any system that has network access to GitHub and a valid GitHub token.

#### 3. Developer local trigger

If a developer wants to trigger the workflow manually, they can use:
- a `curl` command, or
- the helper script `utils/trigger_project_report.py`

They do not need the full repository cloned just for triggering.

### Token requirements

#### Which token is needed?

Developers need a **GitHub token**, not a Bitbucket token.

The trigger request authenticates against GitHub, so the API token must be issued by GitHub.

#### Best practice

- each developer should use their own GitHub token, or
- your team should use a shared service account / machine user token stored securely
- never hardcode a token in source code
- store the token in Bitbucket secret variables or GitHub secrets
- rotate or revoke exposed tokens immediately

#### Required GitHub PAT scopes

- `repo` (for private repositories)
- `workflow`

### Example trigger commands

#### Repository dispatch for a single project

Run `lct` smoke tests:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "project": "lct",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

#### Repository dispatch for multiple projects

Run `atcu` and `lct` smoke tests:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "projects": "atcu,lct",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

#### Repository dispatch for full regression

Run regression across all configured projects:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/dispatches \
  -d '{
    "event_type": "run-project-report",
    "client_payload": {
      "marker": "regression",
      "report_dir": "reports"
    }
  }'
```

#### workflow_dispatch with a branch ref

If the workflow file exists on `atcu`, target that branch explicitly:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Accolade-Qa/LCT_A4G_AUTO/actions/workflows/reporting.yml/dispatches \
  -d '{
    "ref": "atcu",
    "inputs": {
      "project": "lct",
      "marker": "smoke",
      "report_dir": "reports"
    }
  }'
```

### Helper script

Use the helper script `utils/trigger_project_report.py` to simplify GitHub dispatch calls.

#### How to Trigger with Different Branches (`--ref`)

Passing the `--ref <branch_name>` parameter tells the script to trigger `workflow_dispatch` on the specified Git branch or tag instead of the default `repository_dispatch`.

##### Parameter Reference:

| Parameter | Required | Description |
| :--- | :---: | :--- |
| `--ref` | **Yes for custom branch** | Target Git branch or tag name (e.g., `atcu`, `main`, `feature/my-branch`) |
| `--owner` | Yes | GitHub repository owner (e.g., `Accolade-Qa`) |
| `--repo` | Yes | GitHub repository name (e.g., `LCT_A4G_AUTO`) |
| `--token` | Yes | GitHub Personal Access Token (PAT) with `repo` permissions |
| `--project` | Optional | Target project name (e.g., `atcu`, `lct`) |
| `--marker` | Optional | Pytest marker expression (e.g., `smoke`, `regression`, `ui`) |
| `--workflow` | Optional | Workflow file name (defaults to `reporting.yml`) |

##### PowerShell Examples (Windows):

- Trigger on the `atcu` branch:
  ```powershell
  python utils/trigger_project_report.py --owner Accolade-Qa --repo LCT_A4G_AUTO --token "YOUR_GITHUB_TOKEN" --project atcu --marker smoke --ref atcu
  ```

- Trigger on a feature branch (e.g., `feature/ticket-dashboard-fix`):
  ```powershell
  python utils/trigger_project_report.py --owner Accolade-Qa --repo LCT_A4G_AUTO --token "YOUR_GITHUB_TOKEN" --project atcu --marker smoke --ref feature/ticket-dashboard-fix
  ```

##### Bash Examples (Linux/macOS):

- Example for `lct` smoke tests using repository_dispatch (default branch):
  ```bash
  python utils/trigger_project_report.py \
    --owner Accolade-Qa \
    --repo LCT_A4G_AUTO \
    --token "$GITHUB_TOKEN" \
    --project lct \
    --marker smoke
  ```

- Example for `atcu` branch-specific workflow_dispatch:
  ```bash
  python utils/trigger_project_report.py \
    --owner Accolade-Qa \
    --repo LCT_A4G_AUTO \
    --token "$GITHUB_TOKEN" \
    --project atcu \
    --marker smoke \
    --ref atcu
  ```

### Common pitfalls

- `repository_dispatch` only triggers workflows on the default branch.
- `workflow_dispatch` can target a specific branch using `--ref`.
- `project` and `projects` cannot be used together.
- The GitHub token must be valid and have the correct scopes.
- Do not share your personal token; use individual tokens or a secure service account.


### Summary

- The trigger source can be Bitbucket, a local shell, or another CI.
- The important token is a GitHub PAT, never a Bitbucket token.
- The workflow file must exist on the branch being dispatched.
- Developers do not need the whole repo cloned just to send the trigger.
- Store tokens securely in CI variables or secrets.

## Check server's connections
```powershell
Test-NetConnection -ComputerName 20.244.15.95 -Port 9090
# or
curl -v https://aepl-tcu4g-qa.accoladeelectronics.com:9090
# or 
ping 20.244.15.95 - to check packets
```