# SQL + Python Data Analytics: E-commerce Sales

A reproducible end-to-end analytics case study built with **PostgreSQL, Python and pandas**. The project explores a synthetic e-commerce order dataset and turns raw transactions into business KPIs and decision-oriented findings.

> **Data transparency:** every row in `data/orders.csv` is synthetic and generated for this portfolio project. It is not real customer, company or commercial data. The analysis demonstrates a workflow and should not be interpreted as evidence of work for a real client.

## Business task

An online store wants to understand sales performance across time, regions, product categories and acquisition channels. The analysis answers:

1. How do order volume and recognised revenue change month to month?
2. Which regions and product categories contribute the most revenue?
3. How large is the average completed order value?
4. What share of paid orders is returned?
5. How many customers place more than one order?
6. Which segments should be investigated for growth or operational issues?

## Dataset

- **360 synthetic orders** covering January–December 2025.
- **120 synthetic customer IDs**, including both one-time and repeat customers.
- Five regions, three sales channels and four product categories.
- Order status: `paid`, `cancelled`, `pending`.
- Discounts, quantities, unit prices, delivery time and return flag.
- Prices and revenue are expressed in arbitrary synthetic monetary units, not a real currency.

See [data dictionary](docs/data_dictionary.md) for field definitions and metric rules.

## Analytical approach

### SQL (PostgreSQL)

- Monthly order funnel and revenue KPIs.
- Revenue, completed orders and return rate by region/category.
- Customer activity, repeat purchase rate and top customers.

### Python (pandas)

The pipeline validates the CSV, calculates recognised revenue only for paid/non-returned orders, and exports KPI, monthly, region, category and channel reports.

### Findings

See [Analysis Findings](docs/analysis_findings.md) for the calculated KPI snapshot, segment comparisons, interpretation and limitations.

### Data quality and tests

Validation checks required columns, unique order IDs, valid dates, positive numeric quantities/prices, discount range, allowed statuses, boolean return flags and delivery duration for paid orders. Unit tests cover revenue rules, KPI calculations, segment return rates and invalid input.

## Key metric definitions

| Metric | Definition |
|---|---|
| Recognised revenue | `quantity × unit_price × (1 − discount_pct)` for paid, non-returned orders; otherwise 0 |
| Completed orders | Paid orders that were not returned |
| Average order value | Recognised revenue / completed orders |
| Return rate | Returned paid orders / all paid orders |
| Repeat customer rate | Customers with more than one order / all distinct customers |

These are demonstration definitions chosen for this dataset. A real business would confirm accounting treatment, refund timing and cohort rules before using the metrics for reporting.

## Run locally

Python 3.10+ is recommended.

```bash
git clone https://github.com/blvxx/portfolio.git
cd portfolio/data-analytics
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install dependencies and run the analysis:

```bash
pip install -r requirements.txt
python src/analysis.py
```

Generated files are written to `reports/`:

- `kpi_summary.json`
- `monthly_kpis.csv`
- `revenue_by_region.csv`
- `revenue_by_category.csv`
- `revenue_by_channel.csv`

Run the tests:

```bash
pip install pytest
python -m pytest -q
```

## Run SQL in PostgreSQL

From the `data-analytics` directory, create the table:

```bash
psql -d analytics -f sql/00_schema.sql
```

Connect to the same database:

```bash
psql -d analytics
```

Then, inside `psql`:

```sql
\copy orders FROM 'data/orders.csv' WITH (FORMAT csv, HEADER true);
\i sql/01_monthly_kpis.sql
\i sql/02_segment_analysis.sql
\i sql/03_customer_analysis.sql
```

If your terminal starts in another directory, adjust the CSV and SQL paths. The scripts use PostgreSQL syntax.

## Project structure

```text
data-analytics/
├── data/
│   └── orders.csv
├── docs/
│   ├── analysis_findings.md
│   └── data_dictionary.md
├── sql/
│   ├── 00_schema.sql
│   ├── 01_monthly_kpis.sql
│   ├── 02_segment_analysis.sql
│   └── 03_customer_analysis.sql
├── src/
│   └── analysis.py
├── tests/
│   └── test_analysis.py
├── requirements.txt
└── README.md
```

## Skills demonstrated

**SQL:** filtering, aggregation, CASE, CTEs, date functions and conditional aggregation.

**Python:** pandas, data validation, reusable functions, CLI workflow, JSON/CSV export and exception handling.

**Analytics:** KPI design, revenue logic, segmentation, customer repeat rate, data quality and translating business questions into queries.

## Limitations and next iteration

- The dataset is synthetic and intentionally small.
- No causal conclusions can be drawn from the patterns.
- No real-world seasonality or business context is claimed.
- A next iteration could add customer cohorts, an interactive dashboard and automated SQL/Python reconciliation checks.
