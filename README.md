# LCT-A4G Automation Testing Framework demo

[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-FF6B35?style=for-the-badge&logo=allure&logoColor=white)](https://docs.qameta.io/allure/)

A Playwright + pytest automation stack that drives the LCT-A4G Device Dashboard and captures actionable test artifacts for both local experimentation and CI pipelines.

## Overview

- Structured around Playwright page objects, pytest fixtures, and helpers to keep test logic readable and resilient.
- Captures screenshots, traces, and videos per the configured `.env` flags so debugging failures is faster.
- Packs configuration for Chromium, Firefox, and WebKit runs plus optional tracing and reporting hooks.

## Prerequisites

- Python 3.8 or newer
- Git (to clone and keep the repo in sync)
- A supported shell (PowerShell, Command Prompt, or Bash)
- Recommended: create an isolated virtual environment for dependencies.

## Getting started

1. **Clone the repository**
   ```bash
git clone <repository-url>
cd LCT_A4G_AUTO
```
2. **Create a virtual environment**
   ```bash
python -m venv .venv

(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& d:\AEPL_AUTOMATION\LCT_A4G_AUTO\.venv\Scripts\Activate.ps1)
```
3. **Activate the virtual environment**
   ```bash
.venv\Scripts\Activate.ps1
```

# Command Prompt
.venv\Scripts\activate.bat
```
4. **Install Python requirements**
   ```bash
pip install -r requirements.txt
```
5. **Install Playwright browsers**
   ```bash
playwright install
```
6. **Configure the project environment file** at `config/<project>.env`. Set credentials there:
```env
APP_USERNAME=your_username
APP_PASSWORD=your_password
API_USERNAME=your_api_username
API_PASSWORD=your_api_password
```
Project URLs and browser options are in `config/<project>.yaml`; test inputs are in
`test_data/<project>/test_data.yaml`. Environment files are ignored by Git.

## Configuration

| Variable | Description | Suggested values |
|----------|-------------|------------------|
| `APP_USERNAME` / `APP_PASSWORD` | Credentials used during login tests | --- |
| `API_USERNAME` / `API_PASSWORD` | Credentials used for API authentication | --- |

Additional browser launch arguments can be injected in `conftest.py` via the `args` list for custom debugging or CI requirements.

## Multi-project support

The framework supports environment-specific configuration through `config/<project>.yaml`, credentials in `config/<project>.env`,
and test inputs in `test_data/<project>/test_data.yaml`.

Run the suite for a specific project with:
```bash
pytest --project=atcu
pytest --project=lct
pytest --project=sampark
```

A `PROJECT` environment variable may also be used before running tests:
```bash
set PROJECT=lct
pytest
```

## Project layout

```
README.md                 � project guide
requirements.txt          � pinned dependencies
pytest.ini                � pytest defaults and markers
conftest.py               � fixtures, hooks, Playwright setup
config/                   � environment helpers and global variables
pages/                    � Playwright page objects grouped by screen
tests/                    � pytest test modules
utils/                    � shared helper functions
scripts/                  � automation helpers (e.g., report generation)
reports/                  � stored test artifacts (Allure, HTML, screenshots)
```

## Running tests

- Run the full suite: `pytest`
- Target a file: `pytest tests/test_login_page.py`
- Run a specific test: `pytest tests/test_login_page.py::test_login`
- Use keywords: `pytest -k "login"`
- Increase verbosity: `pytest -v`
- Stop after first failure: `pytest -x`
- Disable stdout capture: `pytest -s`

### Parallel execution

- Auto workers: `pytest -n auto`
- Fixed workers: `pytest -n 4`

### Browser-specific flags

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
pytest --headed false  # handy when HEADLESS=false is not respected by default
``` 

### Advanced options

```bash
pytest --alluredir=reports/allure-results
pytest --video=retain-on-failure
pytest --tracing=retain-on-failure
```

## Reporting

- **Allure**: `allure generate reports/allure-results --clean` then `allure open reports/allure-results`
- **HTML**: `pytest --html=reports/report.html`
- **Auto-generated bundle**: `python scripts/generate_reports.py` runs pytest with `--html`, `--self-contained-html`, and `--json-report` to emit:
  - `reports/pytests/report.html` (HTML)
  - `reports/json/report.json` (JSON)
  - `reports/excel/pytest-results.xlsx` (Excel) via pandas transformation

Set `SUITE_NAME` in your environment to customize report prefixes (default `LCT_A4G_AUTO`). Include the generated HTML/Excel when sharing results.

## Development notes

- **Add tests**: Drop new files in `tests/`, name them `test_*.py`, and reuse page objects.
- **Add page objects**: Extend `pages/base_page.py` and keep locators/selectors centralized.
- **Helper utilities**: `utils/helpers.py` exposes methods such as `maximize_browser()`, `wait_for_element()`, and `take_screenshot()` to keep tests concise.

## Useful commands

```
.venv\Scripts\Activate.ps1  # Activate (PowerShell)
.venv\Scripts\activate.bat  # Activate (cmd)
deactivate                    # Exit venv
pip install --upgrade -r requirements.txt
pip install <package-name>
pip freeze > requirements.txt
``` 

Cleanup commands (adapt for your shell):
```
# Remove generated caches and artifacts
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Remove-Item -Recurse -Force screenshots/ videos/ reports/ .pytest_cache/
``` 

## Troubleshooting

- **Playwright browsers missing**: `playwright install`
- **Import errors**: ensure the virtual environment is activated; verify `sys.path` with `python -c "import sys; print(sys.path)"`
- **Pytest discovery issues**: use the `test_*.py` convention; confirm `pytest.ini` markers
- **Env variables not read**: ensure `.env` matches keys expected in `config/config.py`

## CI reporting

A GitHub Actions workflow (`.github/workflows/reporting.yml`) runs `scripts/generate_reports.py` on every push to `master` and every day at 10:00 UTC on `develop`. The job uses `dawidd6/action-send-mail` to email the HTML/Excel payloads; configure the repository secrets `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_TO`, and `MAIL_FROM`. Subject lines include the branch name so recipients can identify manual vs. scheduled runs.

## License

MIT
