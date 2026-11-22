# E-commerce Business Analytics Dashboard

An interactive presentation layer for the existing synthetic e-commerce analysis. It reuses the validated dataset and KPI preparation logic rather than duplicating metric definitions.

## Run locally

From `portfolio/data-analytics/`:

```bash
python -m venv .venv
```

Activate the environment, then install the optional dashboard dependencies:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements-dashboard.txt
streamlit run dashboard/app.py
```

Streamlit prints a local URL (normally http://localhost:8501).

## Dashboard contents

- Filter by order period, region and product category.
- Headline order, recognised revenue, average order value and return-rate metrics.
- Monthly revenue trend.
- Revenue by product category and sales channel.
- Payment-status composition.
- Filtered order-level table and CSV download.

## Metric and data boundaries

The dashboard calls the same validation and preparation functions as the CLI analysis. Recognised revenue counts paid, non-returned orders only. All 360 orders are synthetic; the dashboard is a portfolio demonstration, not a report about a real company.

The optional UI dependencies are kept separate from `requirements.txt`, so the core pandas analysis and unit tests remain lightweight.
