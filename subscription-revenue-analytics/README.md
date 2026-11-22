# Subscription Revenue & Retention Analytics

[![PostgreSQL BI Analytics](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml/badge.svg)](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml)

**[Open the visual case study](https://blvxx.github.io/portfolio/subscription-revenue-analytics/)** · **[Source on GitHub](https://github.com/blvxx/portfolio/tree/main/subscription-revenue-analytics)** · **[Workflow runs](https://github.com/blvxx/portfolio/actions/workflows/subscription-revenue-analytics.yml)**

## Overview

A PostgreSQL-first BI case study for a fictional subscription business. It turns an event log into monthly recurring-revenue (MRR) reporting, revenue movement bridges, customer cohorts and channel performance.

The fixture is deliberately synthetic: 30 fictional customer records, 3 plan tiers, 43 subscription events and 18 monthly reporting periods (January 2025–June 2026). It contains no real customer information and is not a market benchmark.

## Business questions

- How do ending MRR and ARR evolve month by month?
- How much recurring revenue comes from new subscriptions, upgrades, downgrades and cancellations?
- Does the monthly MRR bridge reconcile to the ending balance?
- How do customer cohorts retain over subsequent months?
- Which acquisition channels and regions contribute active customers and MRR?
- Which customers have the highest observed MRR-months in this fixture?

## Data model

| Table / view | Grain | Purpose |
|---|---|---|
| bi_customers | One row per customer | Signup date, acquisition channel and region |
| bi_plans | One row per plan | Plan tier and monthly price |
| bi_subscription_events | One row per lifecycle event | Post-event plan and MRR state |
| bi_mart_subscription_month_end | One row per active subscription per month | Month-end state reconstructed from the event log |
| bi_mart_event_movements | One row per subscription event | New, expansion, contraction and churn MRR |
| bi_mart_monthly_kpis | One row per month | MRR / ARR, active base, retention and bridge reconciliation |
| bi_mart_cohort_retention | One row per cohort-month | Active customers and retention percentage |
| bi_mart_channel_performance | One row per month / channel / region | Active customers and MRR contribution |

## SQL techniques demonstrated

- PostgreSQL DDL, primary / foreign keys, CHECK and UNIQUE constraints, numeric precision and indexes.
- Event-state reconstruction with ROW_NUMBER() and month spine generation using generate_series().
- Lifecycle deltas with LAG(), aggregate filters and conditional calculations.
- Retention and moving averages using window functions.
- CTE-based models, reusable views, explicit metric definitions and reconciliation checks.
- SQL-based data-quality assertions that fail CI on invalid transitions or a broken MRR bridge.

## Metric definitions

- **MRR:** sum of active subscriptions' monthly recurring value at month-end.
- **ARR:** ending MRR multiplied by 12; an annualized run-rate estimate, not recognized revenue.
- **New MRR:** MRR added by activations in the reporting month.
- **Expansion MRR:** positive difference on upgrades.
- **Contraction MRR:** previous MRR less post-downgrade MRR.
- **Churned MRR:** the subscription's previous MRR when it is cancelled.
- **GRR:** (opening MRR − contraction MRR − churned MRR) / opening MRR.
- **NRR:** (opening MRR + expansion MRR − contraction MRR − churned MRR) / opening MRR.
- **Observed MRR-months:** sum of monthly MRR snapshots for a customer during the fixture window. It is descriptive and is not presented as true lifetime value.

New MRR is excluded from GRR / NRR by design. For the first month, where opening MRR is zero, retention percentages are NULL.

## Run locally

Requirements: Docker and Docker Compose.

~~~bash
docker compose up -d
docker compose exec -T db psql -U analytics -d subscription_bi -v ON_ERROR_STOP=1 -f /workspace/sql/00_schema.sql
docker compose exec -T db psql -U analytics -d subscription_bi -v ON_ERROR_STOP=1 -f /workspace/sql/01_seed.sql
docker compose exec -T db psql -U analytics -d subscription_bi -v ON_ERROR_STOP=1 -f /workspace/sql/02_marts.sql
docker compose exec -T db psql -U analytics -d subscription_bi -v ON_ERROR_STOP=1 -f /workspace/sql/03_quality_checks.sql
docker compose exec -T db psql -U analytics -d subscription_bi -f /workspace/sql/queries/monthly_kpis.sql
docker compose down
~~~

To explore the remaining outputs, execute the cohort, channel and customer-ranking queries from sql/queries/.

## Automated validation

The [GitHub Actions workflow](../.github/workflows/subscription-revenue-analytics.yml) provisions PostgreSQL 16, loads the schema and deterministic fixture, builds the analytical views, executes quality assertions, exports aggregate CSVs and uploads the results as a workflow artifact.

## Repository map

~~~text
subscription-revenue-analytics/
├── README.md
├── index.html
├── docker-compose.yml
└── sql/
    ├── 00_schema.sql
    ├── 01_seed.sql
    ├── 02_marts.sql
    ├── 03_quality_checks.sql
    └── queries/
        ├── monthly_kpis.sql
        ├── cohort_retention.sql
        ├── channel_performance.sql
        └── customer_mrr_ranking.sql
~~~

## Limitations and transparency

- All entities and events are fictional and created for technical demonstration.
- The fixture is intentionally small; it does not support statistically meaningful commercial conclusions.
- ARR is a run-rate calculation; the model does not calculate accounting revenue recognition, taxes, discounts or annual billing proration.
- Subscription events store post-event MRR. A production implementation would additionally define timezone, late-arriving events, corrections, refunds, contract terms and multi-currency rules.
- The customer ranking is an observed MRR-months proxy, not a predictive or contractual customer lifetime value model.
