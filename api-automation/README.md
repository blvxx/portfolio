# API Automation — Python, pytest, requests

[![API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)

Portfolio project demonstrating a maintainable approach to REST API testing: a reusable HTTP client, contract validation with JSON Schema, parametrized positive and negative scenarios, isolated unit tests, Allure labels, and GitHub Actions CI.

> This is an independent portfolio project against the public JSONPlaceholder demo API. It is not a commercial client delivery or a production API contract.

## What is covered

| Area | Checks |
|---|---|
| Collection endpoint | `GET /posts`, HTTP status, JSON content type, expected collection size, schema validation for each item |
| Resource endpoint | `GET /posts/{id}`, required fields and response schema for IDs 1, 10, 50 and 100 |
| Query filters | `GET /posts?userId={id}`, returned records match the requested user IDs |
| Negative scenarios | Unknown and invalid post IDs return 404; unknown user filters return an empty collection |
| JSON Schema | Schema definition validation; rejection of incorrect types, missing properties, invalid values and unexpected properties |
| API client unit tests | Headers, base URL override, query parameters, timeout propagation, transport exceptions and session lifecycle |

## Test design

- API behavior tests use a real public demo endpoint and therefore require internet access.
- API-client unit tests use mocked sessions and do not require network access.
- Test data is parameterized to cover several valid and invalid inputs.
- Response payloads are checked against a strict JSON Schema (Draft 2020-12).
- Allure feature/story labels help group test results in a report.
- Transport-level exceptions such as request timeouts are allowed to propagate so failures are visible to the test layer.

## Tech stack

- Python 3.10+
- pytest
- requests
- jsonschema
- allure-pytest
- GitHub Actions

## Run locally

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the complete suite:

```bash
pytest -ra
```

Run isolated unit tests (no network required):

```bash
pytest -m unit
```

Run API smoke checks:

```bash
pytest -m smoke
```

Generate JUnit and Allure result files:

```bash
pytest --junitxml=reports/junit.xml --alluredir=allure-results
```

## Configuration

The default API base URL is `https://jsonplaceholder.typicode.com`. It can be overridden without editing source code:

```bash
# macOS / Linux
export API_BASE_URL=https://your-test-environment.example

# Windows PowerShell
$env:API_BASE_URL = "https://your-test-environment.example"
```

You can also pass `base_url` directly when creating `PostsApiClient`. The request timeout defaults to 10 seconds and can be configured in the constructor.

## CI

GitHub Actions runs the suite on Python 3.10 and 3.12 when files under `api-automation/` or the workflow itself change. The workflow uploads JUnit and Allure result files as build artifacts, including when tests fail.

Workflow: [API Automation](https://github.com/blvxx/portfolio/actions/workflows/api-automation.yml)

## Project structure

```text
api-automation/
├── api_client.py
├── pytest.ini
├── requirements.txt
├── schemas/
│   └── post.schema.json
└── tests/
    ├── test_api_client.py
    └── test_posts_api.py
```

## Known limitations

- JSONPlaceholder is a demo service; its behavior should not be treated as a production service-level guarantee.
- Live API tests can fail temporarily due to public-service availability or network restrictions.
- CI results should be checked in the Actions tab; adding tests or a workflow does not itself prove that a run passed.
- The suite focuses on the Posts resource and does not claim authentication, database, load, security or end-to-end coverage.

## Maintainer

Artem Kalinin — [GitHub profile](https://github.com/blvxx)
