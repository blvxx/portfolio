# API Automation — Python, pytest, requests

[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)

Portfolio project demonstrating REST API test automation: a reusable HTTP client, CRUD request coverage, strict JSON Schema checks, parametrized positive and negative scenarios, isolated unit tests, static analysis, Allure labels, and GitHub Actions CI.

> This is an independent portfolio project against the public JSONPlaceholder demo API. It is not a commercial client delivery or a production API contract.

## Coverage

| Area | Scenarios |
|---|---|
| Read | `GET /posts`, `GET /posts/{id}`, response status, content type, filtering and response schema |
| Create | `POST /posts`, request payload validation, `201 Created`, generated ID and response fields |
| Replace | `PUT /posts/{id}`, full JSON payload and response contract |
| Partial update | `PATCH /posts/{id}`, partial JSON payload and updated resource representation |
| Delete | `DELETE /posts/{id}`, successful deletion response |
| Negative | Unknown IDs, invalid filters, incorrect types, missing fields and unexpected request/response properties |
| Unit | HTTP method, URL, headers, query parameters, JSON body, timeout propagation, environment configuration and session lifecycle |

## Test design

- API behavior tests call a public demo endpoint and require internet access.
- API-client unit tests use mocked `requests.Session` objects and do not require network access.
- Positive, negative and CRUD scenarios are grouped with pytest markers.
- Request and response payloads are validated against JSON Schema (Draft 2020-12).
- Parametrization checks several values without duplicating test functions.
- Allure feature/story labels and JSON attachments make request/response evidence easier to inspect.
- Ruff checks the Python code for common errors and unused imports.
- Transport exceptions such as request timeouts are not swallowed by the client.

## Important limitation of the demo API

JSONPlaceholder simulates write operations. A successful `POST`, `PUT`, `PATCH` or `DELETE` response demonstrates the HTTP contract, but the change is not persisted in the server's data. For example, a created post may be returned with an ID, but fetching that generated ID later still returns 404. This is expected demo-service behavior, not a defect in the test suite.

See the [official JSONPlaceholder guide](https://jsonplaceholder.typicode.com/guide.html) for examples and the write-operation limitation.

## Tech stack

- Python 3.10+
- pytest
- requests
- jsonschema
- allure-pytest
- Ruff
- GitHub Actions

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install runtime and development dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Run static checks:

```bash
ruff check api_client.py tests/
```

Run the complete suite:

```bash
pytest -ra
```

Run tests that do not call the external API:

```bash
pytest -m unit
```

Run CRUD scenarios only:

```bash
pytest -m crud
```

Run the smoke checks:

```bash
pytest -m smoke
```

Generate JUnit and Allure result files:

```bash
pytest --junitxml=reports/junit.xml --alluredir=allure-results
```

## Configuration

The default base URL is `https://jsonplaceholder.typicode.com`. Override it without editing source code:

```bash
# macOS / Linux
export API_BASE_URL=https://your-test-environment.example

# Windows PowerShell
$env:API_BASE_URL = "https://your-test-environment.example"
```

The client also accepts `base_url` in its constructor. The request timeout defaults to 10 seconds and can be set when creating the client.

## CI

GitHub Actions runs static checks, isolated unit tests and the complete suite on Python 3.10 and 3.12 when files under `api-automation/` or the workflow change. JUnit and Allure result files are uploaded as artifacts, including when tests fail.

- [Latest workflow runs](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)
- [Workflow definition](../../.github/workflows/api-automation.yml)

Check the Actions tab for the actual result of each run; workflow configuration alone does not prove that a run passed.

## Project structure

```text
api-automation/
├── api_client.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── schemas/
│   ├── post.schema.json
│   └── post-create-request.schema.json
└── tests/
    ├── test_api_client.py
    └── test_posts_api.py
```

## Known limitations and next steps

- The public demo API may be temporarily unavailable or slow; live API tests can therefore fail because of external conditions.
- Demo write operations are not persistent and must not be treated as database persistence checks.
- The project currently focuses on the Posts resource; it does not claim authentication, database, load, security or end-to-end coverage.
- Future extensions can add relationship endpoints, pagination checks, reusable test data builders and a local mock API for deterministic failure scenarios.

## Maintainer

Artem Kalinin — [GitHub profile](https://github.com/blvxx)
