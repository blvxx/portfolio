[![Customer Retention Analytics](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml)

[**Live case study page**](https://blvxx.github.io/portfolio/customer-retention-analytics/) · [Repository source](https://github.com/blvxx/portfolio/tree/main/customer-retention-analytics)

# Customer Retention & Sales Analytics

An end-to-end retail analytics case study built around the public **UCI Online Retail** transaction dataset. The project covers data validation, cancellation/refund handling, SQL-style business metrics in pandas, RFM segmentation, cohort retention and an interactive dashboard.

> **Data provenance:** the primary workbook is published by the UCI Machine Learning Repository under CC BY 4.0. This repository does not redistribute the 22.6 MB source workbook. The included CSV is a small synthetic fixture for offline tests and dashboard preview; it is not a subset of the UCI records.

## What the project demonstrates

- Reproducible retrieval of the official UCI workbook.
- Automated CI refresh that computes aggregate-only public results from the official source and publishes generated findings and CSV outputs without customer-level identifiers.
- Data cleaning with explicit treatment of cancellations, returns, invalid rows and missing customer identifiers.
- Gross sales, refunds, net sales, invoices, customer and repeat-purchase KPIs.
- Monthly sales, country contribution and top-product analysis through both pandas and executable SQLite queries.
- SQL CTEs and window functions for repeat-customer rates, RFM quartiles and cohort retention.
- Cross-checks that reconcile SQL gross sales and repeat-customer rates with the pandas pipeline.
- Streamlit + Plotly dashboard with country filters and methodology notes.
- Unit tests for data cleaning, metrics, RFM and cohort calculations.
- GitHub Actions test workflow.

## Dataset

**UCI Online Retail** contains 541,909 transaction rows from a UK-based non-store retailer covering 1 December 2010 to 9 December 2011. The source describes UnitPrice in sterling and lists the dataset license as Creative Commons Attribution 4.0 International.

- [Official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail)
- [Dataset DOI](https://doi.org/10.24432/C5BW33)
- [Data provenance and attribution](data/README.md)

## Quick start

Python 3.10+ is required.

```bash
python -m venv .venv
# Activate the environment, then:
pip install -e ".[dev]"
python scripts/download_data.py
python scripts/run_analysis.py
python scripts/build_public_report.py
pytest
```

The local exploratory pipeline writes detailed working outputs under outputs/. The public-report pipeline writes a privacy-conscious aggregate summary, monthly trends, leading countries/products, RFM segment counts and cohort retention under docs/generated/. Customer-level identifiers are never included in the public report.

## Generated report and data refresh

- [Aggregate findings](docs/generated/findings.md)
- [Summary metrics (JSON)](docs/generated/summary.json)
- [Generated monthly sales](docs/generated/monthly_sales.csv)
- [Top countries](docs/generated/country_sales_top10.csv)
- [Top products](docs/generated/top_products.csv)
- [RFM segment summary](docs/generated/rfm_segments.csv)
- [Cohort sizes](docs/generated/cohort_sizes.csv)
- [Cohort retention matrix](docs/generated/cohort_retention.csv)

The [Retail Dataset Analysis workflow](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-data-refresh.yml) downloads the original workbook in GitHub Actions, generates the public report, runs unit tests, uploads an artifact and commits only aggregate outputs. The raw workbook and customer-level records stay outside Git.

## Interactive dashboard

Install the optional dashboard dependencies:

```bash
pip install -e ".[dashboard,dev]"
streamlit run app.py
```

By default, the dashboard uses the published aggregate-only UCI outputs in `docs/generated/`. Upload the original workbook in the sidebar to recalculate country-filtered sales, customer segments and cohorts interactively. The small bundled synthetic CSV is only a fallback for offline preview when generated outputs are absent.

## Repository map

```text
customer-retention-analytics/
├── app.py
├── data/
│   ├── README.md
│   └── sample_transactions.csv
├── docs/
│   └── analysis-brief.md
├── scripts/
│   ├── download_data.py
│   └── run_analysis.py
├── src/retail_analytics/
│   ├── analysis.py
│   └── etl.py
├── tests/
│   └── test_analytics.py
├── pyproject.toml
└── requirements-dashboard.txt
```

## Methodology and limitations

- Cancellation invoices and negative-quantity lines are separated from positive sales.
- Sales rows without CustomerID remain in revenue totals, but are excluded from RFM and cohort calculations.
- Net sales subtract the observed refund/cancellation line values; the output should be interpreted using the documented row-level rules.
- RFM scores are relative quartiles within the observed time window, not model probabilities. The SQL version uses NTILE(4), which can split ties differently from the pandas rank-based implementation.
- The dataset is historical and observational. It does not support current-market claims or causal conclusions about marketing activity.
- Public findings are generated only by the CI refresh from the original UCI workbook. The small bundled CSV remains a synthetic offline fixture and is never used to populate the published headline metrics.

## Source attribution

Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0. Please retain source attribution when reusing the dataset or derived materials.
