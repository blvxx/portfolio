# API Automation — Python, pytest, requests

Portfolio project demonstrating REST API testing with a reusable client, JSON Schema validation, parametrized cases, negative scenarios, and CI.

## Coverage
- `GET /posts`: status code, JSON content type, list size, schema validation for every returned item
- `GET /posts/{id}`: required fields, response schema, several valid IDs
- `GET /posts?userId={id}`: filtering and schema checks
- Negative cases: invalid IDs return 404; unknown user filters return an empty list
- Schema unit check: invalid data is rejected


## Tech stack
Python 3.10+ · pytest · requests · jsonschema · Allure · GitHub Actions

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```
Run smoke tests only:
```bash
pytest -m smoke
```
Collect Allure results:
```bash
pytest --alluredir=allure-results
```

## Project layout
```
api-automation/
├── api_client.py
├── requirements.txt
├── pytest.ini
├── schemas/
│   └── post.schema.json
└── tests/
    └── test_posts_api.py
```

The test suite calls the live JSONPlaceholder demo API, so internet access is required. The schema and negative payload test are local. This project is a learning/portfolio example, not a production contract.
