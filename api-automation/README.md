# API Automation (Python + pytest + requests)

A portfolio project demonstrating REST API checks with **pytest** and **requests** against JSONPlaceholder.

## Covered scenarios
- GET /posts — status code, response type, basic schema
- GET /posts/1 — single resource and required fields
- GET /posts?userId=1 — query parameter filtering
- GET /posts/999999 — not-found response

## Requirements
Python 3.10+

## Run locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pytest -v
```

The tests use a public demo API; network access is required. This is an educational test suite, not a production API contract.
