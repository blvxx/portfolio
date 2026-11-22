from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_ROOT = PROJECT_ROOT / "sql"


def _to_sql_sales(sales: pd.DataFrame) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "invoice_no": sales["InvoiceNo"].astype("string").astype(str),
            "stock_code": sales["StockCode"].astype("string").astype(str),
            "description": sales["Description"].astype("string").astype(str),
            "quantity": pd.to_numeric(sales["Quantity"], errors="coerce"),
            "invoice_date": pd.to_datetime(sales["InvoiceDate"]).dt.strftime("%Y-%m-%d %H:%M:%S"),
            "unit_price": pd.to_numeric(sales["UnitPrice"], errors="coerce"),
            "customer_id": sales["CustomerID"].astype("object").where(sales["CustomerID"].notna(), None),
            "country": sales["Country"].astype("string").astype(str),
            "revenue": pd.to_numeric(sales["Revenue"], errors="coerce"),
        }
    )
    frame["customer_id"] = frame["customer_id"].where(pd.notna(frame["customer_id"]), None)
    return frame


def _to_sql_refunds(refunds: pd.DataFrame) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "invoice_no": refunds["InvoiceNo"].astype("string").astype(str),
            "stock_code": refunds["StockCode"].astype("string").astype(str),
            "description": refunds["Description"].astype("string").astype(str),
            "quantity": pd.to_numeric(refunds["Quantity"], errors="coerce"),
            "invoice_date": pd.to_datetime(refunds["InvoiceDate"]).dt.strftime("%Y-%m-%d %H:%M:%S"),
            "unit_price": pd.to_numeric(refunds["UnitPrice"], errors="coerce"),
            "customer_id": refunds["CustomerID"].astype("object").where(refunds["CustomerID"].notna(), None),
            "country": refunds["Country"].astype("string").astype(str),
            "refund_amount": pd.to_numeric(refunds["RefundAmount"], errors="coerce"),
        }
    )
    frame["customer_id"] = frame["customer_id"].where(pd.notna(frame["customer_id"]), None)
    return frame


def run_sql_analysis(
    sales: pd.DataFrame,
    refunds: pd.DataFrame,
    output_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Execute SQL KPIs and write aggregate-only CSV outputs.

    SQLite runs in memory. No database file, customer-level rows or identifiers
    are persisted in the repository or returned as public result tables.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(":memory:")
    try:
        schema = (SQL_ROOT / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)

        _to_sql_sales(sales).to_sql("sales", connection, if_exists="append", index=False)
        _to_sql_refunds(refunds).to_sql("refunds", connection, if_exists="append", index=False)

        query_names = (
            "monthly_sales",
            "country_sales",
            "repeat_customers",
            "rfm_segments",
            "cohort_retention",
        )
        outputs: dict[str, pd.DataFrame] = {}
        for name in query_names:
            sql = (SQL_ROOT / "queries" / f"{name}.sql").read_text(encoding="utf-8")
            result = pd.read_sql_query(sql, connection)
            outputs[name] = result
            result.to_csv(output_dir / f"sql_{name}.csv", index=False)

        # Reconciliation assertions make SQL outputs independently checkable.
        sql_gross = float(outputs["monthly_sales"]["revenue_gbp"].sum()) if not outputs["monthly_sales"].empty else 0.0
        pandas_gross = float(sales["Revenue"].sum()) if not sales.empty else 0.0
        if abs(sql_gross - pandas_gross) > 0.02:
            raise AssertionError(
                f"SQL and pandas gross sales do not reconcile: {sql_gross} vs {pandas_gross}"
            )

        if not outputs["repeat_customers"].empty:
            sql_repeat_rate = float(outputs["repeat_customers"].iloc[0]["repeat_customer_rate_pct"])
            customer_sales = sales.dropna(subset=["CustomerID"])
            customer_invoice_counts = customer_sales.groupby("CustomerID")["InvoiceNo"].nunique()
            repeat_count = int(customer_invoice_counts.gt(1).sum())
            pandas_rate = round(repeat_count / customer_sales["CustomerID"].nunique() * 100, 2)
            if sql_repeat_rate != pandas_rate:
                raise AssertionError(
                    f"SQL and pandas repeat-customer rate do not reconcile: {sql_repeat_rate} vs {pandas_rate}"
                )

        return outputs
    finally:
        connection.close()
