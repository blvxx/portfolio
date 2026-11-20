"""Reproducible KPI analysis for the synthetic e-commerce orders dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = {
    "order_id", "order_date", "customer_id", "region", "channel",
    "category", "product", "quantity", "unit_price", "discount_pct",
    "payment_status", "delivery_days", "is_returned",
}
ALLOWED_STATUSES = {"paid", "cancelled", "pending"}


def validate_orders(df: pd.DataFrame) -> None:
    """Raise ValueError when required fields or business constraints are violated."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("The orders dataset is empty")
    if df["order_id"].isna().any() or df["order_id"].duplicated().any():
        raise ValueError("order_id must be populated and unique")
    if df["customer_id"].isna().any():
        raise ValueError("customer_id must be populated")
    if pd.to_datetime(df["order_date"], errors="coerce").isna().any():
        raise ValueError("order_date contains invalid dates")
    if (pd.to_numeric(df["quantity"], errors="coerce") <= 0).any():
        raise ValueError("quantity must be greater than zero")
    if (pd.to_numeric(df["unit_price"], errors="coerce") <= 0).any():
        raise ValueError("unit_price must be greater than zero")

    discount = pd.to_numeric(df["discount_pct"], errors="coerce")
    if discount.isna().any() or not discount.between(0, 1).all():
        raise ValueError("discount_pct must be between 0 and 1")
    if not set(df["payment_status"].dropna().unique()).issubset(ALLOWED_STATUSES):
        raise ValueError(f"payment_status must be one of {sorted(ALLOWED_STATUSES)}")
    if df["payment_status"].isna().any():
        raise ValueError("payment_status cannot be null")
    if not df["is_returned"].isin([True, False]).all():
        raise ValueError("is_returned must contain boolean values")


def load_orders(path: str | Path) -> pd.DataFrame:
    """Load the CSV and validate its structure and values."""
    df = pd.read_csv(path, parse_dates=["order_date"])
    validate_orders(df)
    return df


def prepare_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Add order-level values used by all KPI calculations."""
    validate_orders(df)
    prepared = df.copy()
    prepared["order_date"] = pd.to_datetime(prepared["order_date"])
    prepared["gross_value"] = prepared["quantity"] * prepared["unit_price"]
    prepared["discounted_value"] = (
        prepared["gross_value"] * (1 - prepared["discount_pct"])
    )
    is_completed = (prepared["payment_status"] == "paid") & (~prepared["is_returned"])
    prepared["recognised_revenue"] = prepared["discounted_value"].where(is_completed, 0.0)
    prepared["is_completed"] = is_completed
    prepared["order_month"] = prepared["order_date"].dt.to_period("M").astype(str)
    return prepared


def calculate_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """Return headline business KPIs using the definitions in the README."""
    data = prepare_orders(df)
    paid_orders = int(data["payment_status"].eq("paid").sum())
    completed_orders = int(data["is_completed"].sum())
    returned_orders = int((data["payment_status"].eq("paid") & data["is_returned"]).sum())
    revenue = float(data["recognised_revenue"].sum())
    customer_orders = data.groupby("customer_id")["order_id"].count()
    unique_customers = int(customer_orders.size)
    repeat_customers = int(customer_orders.gt(1).sum())

    return {
        "total_orders": int(len(data)),
        "paid_orders": paid_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": int(data["payment_status"].eq("cancelled").sum()),
        "pending_orders": int(data["payment_status"].eq("pending").sum()),
        "returned_orders": returned_orders,
        "recognised_revenue": round(revenue, 2),
        "average_order_value": round(revenue / completed_orders, 2) if completed_orders else 0.0,
        "return_rate": round(returned_orders / paid_orders, 4) if paid_orders else 0.0,
        "unique_customers": unique_customers,
        "repeat_customers": repeat_customers,
        "repeat_customer_rate": (
            round(repeat_customers / unique_customers, 4) if unique_customers else 0.0
        ),
    }


def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order volume, revenue and returns by calendar month."""
    data = prepare_orders(df)
    result = (
        data.groupby("order_month", as_index=False)
        .agg(
            total_orders=("order_id", "count"),
            paid_orders=("payment_status", lambda values: values.eq("paid").sum()),
            completed_orders=("is_completed", "sum"),
            recognised_revenue=("recognised_revenue", "sum"),
            returned_orders=("is_returned", lambda values: values.sum()),
        )
        .sort_values("order_month")
    )
    result["average_order_value"] = (
        result["recognised_revenue"] / result["completed_orders"].replace(0, pd.NA)
    ).fillna(0).round(2)
    result["recognised_revenue"] = result["recognised_revenue"].round(2)
    return result


def segment_kpis(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Aggregate performance by a supported business dimension."""
    if dimension not in {"region", "category", "channel"}:
        raise ValueError("dimension must be one of: region, category, channel")
    data = prepare_orders(df)
    result = (
        data.groupby(dimension, as_index=False)
        .agg(
            total_orders=("order_id", "count"),
            completed_orders=("is_completed", "sum"),
            recognised_revenue=("recognised_revenue", "sum"),
            returned_orders=("is_returned", "sum"),
        )
        .sort_values("recognised_revenue", ascending=False)
    )
    result["recognised_revenue"] = result["recognised_revenue"].round(2)
    return result


def run_analysis(input_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Run the pipeline and export reusable reports."""
    orders = load_orders(input_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    kpis = calculate_kpis(orders)
    monthly_kpis(orders).to_csv(output / "monthly_kpis.csv", index=False)
    segment_kpis(orders, "region").to_csv(output / "revenue_by_region.csv", index=False)
    segment_kpis(orders, "category").to_csv(output / "revenue_by_category.csv", index=False)
    segment_kpis(orders, "channel").to_csv(output / "revenue_by_channel.csv", index=False)
    (output / "kpi_summary.json").write_text(
        json.dumps(kpis, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return kpis


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse synthetic e-commerce orders.")
    parser.add_argument(
        "--input", type=Path, default=Path("data/orders.csv"),
        help="Path to source orders CSV (default: data/orders.csv)",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("reports"),
        help="Directory for generated reports (default: reports)",
    )
    args = parser.parse_args()
    try:
        kpis = run_analysis(args.input, args.output)
    except (OSError, ValueError, KeyError, pd.errors.ParserError) as exc:
        parser.error(str(exc))
    print("Analysis completed.")
    print(json.dumps(kpis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
