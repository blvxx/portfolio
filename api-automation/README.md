# API Automation — Python, pytest, requests

A portfolio project with a reusable API client, smoke checks, parameterized tests, negative scenarios, and GitHub Actions CI against JSONPlaceholder.

## Coverage
- `GET /posts`: status, JSON content type, collection size
- `GET /posts/1`: required fields and basic types
- `GET /posts/{id}`: parameterized valid IDs (1, 10, 100)
- `GET /posts?userId={id}`: filtering for multiple users
- Negative cases: invalid/unknown post IDs (404 and empty object), unknown user filters (empty list)

## Stack
Python 3.10+ · pytest · requests · GitHub Actions

## Setup and run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```
Run only smoke checks: `pytest -m smoke`

## Structure
```
api-automation/
├── api_client.py
├── requirements.txt
├── pytest.ini
└── tests/
    └── test_posts_api.py
```
Tests make live requests to the public demo API and require internet access. This is an educational test suite, not a production API contract.
