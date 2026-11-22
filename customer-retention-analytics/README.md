[![Customer Retention Analytics](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/customer-retention-analytics.yml)

[**Live case study page**](https://blvxx.github.io/portfolio/customer-retention-analytics/) · [Repository source](https://github.com/blvxx/portfolio/tree/main/customer-retention-analytics)

# Customer Retention & Sales Analytics

An end-to-end retail analytics case study built around the public **UCI Online Retail** transaction dataset. The project covers data validation, cancellation/refund handling, SQL-style business metrics in pandas, RFM segmentation, cohort retention and an interactive dashboard.

> **Data provenance:** the primary workbook is published by the UCI Machine Learning Repository under CC BY 4.0. This repository does not redistribute the 22.6 MB source workbook. The included CSV is a small synthetic fixture for offline tests and dashboard preview; it is not a subset of the UCI records.

## What the project demonstrates

- Reproducible retrieval of the official UCI workbook.
- Data cleaning with explicit treatment of cancellations, returns, invalid rows and missing customer identifiers.
- Gross sales, refunds, net sales, invoices, customer and repeat-purchase KPIs.
- Monthly sales, country contribution and top-product analysis.
- RFM customer segmentation and cohort retention matrix.
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
pytest
```

The reproducible pipeline writes monthly sales, country performance, top products, customer RFM, cohort retention, a JSON KPI summary and a generated findings report under outputs/.

## Interactive dashboard

Install the optional dashboard dependencies:

```bash
pip install -r requirements-dashboard.txt
streamlit run app.py
```

Without an uploaded workbook, the app opens with a clearly labelled synthetic preview fixture. Use the sidebar uploader to load the official UCI Excel workbook and review the actual dataset.

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
- RFM scores are relative quartiles within the observed time window, not model probabilities.
- The dataset is historical and observational. It does not support current-market claims or causal conclusions about marketing activity.
- No headline finding is claimed until the full UCI workbook has been downloaded and the pipeline has been run.

## Source attribution

Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0. Please retain source attribution when reusing the dataset or derived materials.
