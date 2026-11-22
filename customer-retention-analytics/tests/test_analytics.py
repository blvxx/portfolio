import pandas as pd
import pytest

from retail_analytics import (
    build_cohort_retention,
    build_rfm,
    clean_transactions,
    monthly_sales,
    summarize_sales,
)


@pytest.fixture
def raw_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["10001", "A", "Product A", 2, "2010-12-01 09:00:00", 10.0, 1001, "United Kingdom"],
            ["10002", "B", "Product B", 1, "2010-12-15 10:00:00", 20.0, 1002, "France"],
            ["10003", "A", "Product A", 1, "2011-01-01 11:00:00", 10.0, 1001, "United Kingdom"],
            ["10004", "C", "Product C", 4, "2011-01-04 12:00:00", 5.0, 1003, "Germany"],
            ["10005", "D", "Product D", 1, "2011-02-01 13:00:00", 10.0, 1004, "Spain"],
            ["10006", "B", "Product B", 1, "2011-02-15 14:00:00", 20.0, 1002, "France"],
            ["C10004", "C", "Product C", -4, "2011-01-05 09:00:00", 5.0, 1003, "Germany"],
            ["10002", "B", "Product B", -1, "2011-02-20 15:00:00", 20.0, 1002, "France"],
            ["10007", "E", "Product E", 2, "2011-02-21 16:00:00", 4.0, None, "France"],
            ["10008", "F", "Invalid", 1, "not-a-date", 12.0, 1005, "Spain"],
            ["10009", "G", "Zero price", 1, "2011-02-22 10:00:00", 0.0, 1005, "Spain"],
        ],
        columns=[
            "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
            "UnitPrice", "CustomerID", "Country",
        ],
    )


def test_clean_transactions_separates_sales_and_refunds(raw_transactions):
    sales, refunds = clean_transactions(raw_transactions)
    assert len(sales) == 7
    assert len(refunds) == 2
    assert sales["Revenue"].sum() == pytest.approx(108.0)
    assert refunds["RefundAmount"].sum() == pytest.approx(40.0)
    assert sales["CustomerID"].isna().sum() == 1


def test_kpis_keep_anonymous_sales_but_only_identified_customers(raw_transactions):
    sales, refunds = clean_transactions(raw_transactions)
    kpis = summarize_sales(sales, refunds)
    assert kpis["gross_sales_gbp"] == pytest.approx(108.0)
    assert kpis["refunds_gbp"] == pytest.approx(40.0)
    assert kpis["net_sales_gbp"] == pytest.approx(68.0)
    assert kpis["customers"] == 4
    assert kpis["repeat_customers"] == 2


def test_monthly_sales_aggregates_orders_and_revenue(raw_transactions):
    sales, _ = clean_transactions(raw_transactions)
    monthly = monthly_sales(sales)
    assert monthly["month"].tolist() == ["2010-12", "2011-01", "2011-02"]
    assert monthly["orders"].tolist() == [2, 2, 3]


def test_rfm_uses_reference_date_and_produces_segments(raw_transactions):
    sales, refunds = clean_transactions(raw_transactions)
    rfm = build_rfm(sales, refunds, reference_date="2011-03-01")
    assert rfm["CustomerID"].nunique() == 4
    assert set(rfm["R"].unique()).issubset({1, 2, 3, 4})
    assert set(rfm["F"].unique()).issubset({1, 2, 3, 4})
    assert rfm["recency_days"].min() >= 0
    assert rfm["segment"].notna().all()


def test_cohort_retention_starts_at_one_and_tracks_returning_customers(raw_transactions):
    sales, _ = clean_transactions(raw_transactions)
    retention = build_cohort_retention(sales)
    assert retention.loc["2010-12", "month_0"] == pytest.approx(1.0)
    assert retention.loc["2010-12", "month_1"] == pytest.approx(0.5)
    assert retention.loc["2010-12", "month_2"] == pytest.approx(0.5)


def test_missing_columns_are_reported():
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_transactions(pd.DataFrame({"InvoiceNo": ["1"]}))
