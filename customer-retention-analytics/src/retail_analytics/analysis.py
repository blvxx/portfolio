from __future__ import annotations

import pandas as pd


def summarize_sales(sales: pd.DataFrame, refunds: pd.DataFrame | None = None) -> dict[str, float | int]:
    """Calculate headline KPIs; revenue values use the dataset's GBP unit."""
    refunds = refunds if refunds is not None else pd.DataFrame()
    gross = float(sales["Revenue"].sum()) if not sales.empty else 0.0
    refunded = float(refunds["RefundAmount"].sum()) if not refunds.empty else 0.0
    customer_sales = sales.dropna(subset=["CustomerID"])
    customer_orders = customer_sales.groupby("CustomerID")["InvoiceNo"].nunique()
    customer_count = int(customer_sales["CustomerID"].nunique())
    repeat_count = int(customer_orders.gt(1).sum())
    return {
        "gross_sales_gbp": round(gross, 2),
        "refunds_gbp": round(refunded, 2),
        "net_sales_gbp": round(gross - refunded, 2),
        "orders": int(sales["InvoiceNo"].nunique()) if not sales.empty else 0,
        "customers": customer_count,
        "repeat_customers": repeat_count,
        "repeat_customer_rate_pct": round((repeat_count / customer_count) * 100, 2) if customer_count else 0.0,
        "sales_lines": int(len(sales)),
        "refund_lines": int(len(refunds)),
    }


def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    columns = ["month", "revenue_gbp", "orders", "units", "average_order_value_gbp"]
    if sales.empty:
        return pd.DataFrame(columns=columns)
    frame = sales.copy()
    frame["month"] = frame["InvoiceDate"].dt.to_period("M").astype(str)
    result = (
        frame.groupby("month", as_index=False)
        .agg(
            revenue_gbp=("Revenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            units=("Quantity", "sum"),
        )
        .sort_values("month")
    )
    result["average_order_value_gbp"] = (
        result["revenue_gbp"] / result["orders"].replace(0, pd.NA)
    ).fillna(0).round(2)
    result["revenue_gbp"] = result["revenue_gbp"].round(2)
    return result[columns]


def country_sales(sales: pd.DataFrame) -> pd.DataFrame:
    columns = ["Country", "revenue_gbp", "orders", "customers"]
    if sales.empty:
        return pd.DataFrame(columns=columns)
    return (
        sales.groupby("Country", as_index=False)
        .agg(
            revenue_gbp=("Revenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            customers=("CustomerID", "nunique"),
        )
        .sort_values("revenue_gbp", ascending=False)
        .assign(revenue_gbp=lambda frame: frame["revenue_gbp"].round(2))
        [columns]
    )


def top_products(sales: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    columns = ["StockCode", "Description", "revenue_gbp", "units"]
    if sales.empty:
        return pd.DataFrame(columns=columns)
    return (
        sales.groupby(["StockCode", "Description"], as_index=False)
        .agg(revenue_gbp=("Revenue", "sum"), units=("Quantity", "sum"))
        .sort_values("revenue_gbp", ascending=False)
        .head(limit)
        .assign(revenue_gbp=lambda frame: frame["revenue_gbp"].round(2))
        [columns]
    )


def _quartile_score(values: pd.Series, higher_is_better: bool = True) -> pd.Series:
    percentile = values.rank(method="average", pct=True)
    score = (percentile.mul(4).apply(lambda value: int(value + 0.999999))).clip(1, 4)
    if not higher_is_better:
        score = 5 - score
    return score.astype(int)


def build_rfm(
    sales: pd.DataFrame,
    refunds: pd.DataFrame | None = None,
    reference_date: str | pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Build recency, frequency and net monetary metrics for identified customers."""
    columns = ["CustomerID", "recency_days", "frequency", "monetary_gbp", "R", "F", "M", "segment"]
    identified = sales.dropna(subset=["CustomerID"]).copy()
    if identified.empty:
        return pd.DataFrame(columns=columns)

    customer = (
        identified.groupby("CustomerID")
        .agg(
            last_purchase=("InvoiceDate", "max"),
            frequency=("InvoiceNo", "nunique"),
            gross_monetary=("Revenue", "sum"),
        )
        .reset_index()
    )
    if refunds is not None and not refunds.empty:
        refund_by_customer = (
            refunds.dropna(subset=["CustomerID"])
            .groupby("CustomerID")["RefundAmount"]
            .sum()
        )
        customer["refunds"] = customer["CustomerID"].map(refund_by_customer).fillna(0)
    else:
        customer["refunds"] = 0.0
    customer["monetary_gbp"] = (
        customer["gross_monetary"] - customer["refunds"]
    ).clip(lower=0).round(2)

    anchor = pd.Timestamp(reference_date) if reference_date is not None else (
        identified["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)
    )
    customer["recency_days"] = (anchor.normalize() - customer["last_purchase"].dt.normalize()).dt.days.clip(lower=0)
    customer["R"] = _quartile_score(customer["recency_days"], higher_is_better=False)
    customer["F"] = _quartile_score(customer["frequency"], higher_is_better=True)
    customer["M"] = _quartile_score(customer["monetary_gbp"], higher_is_better=True)

    def classify(row: pd.Series) -> str:
        if row["R"] >= 4 and row["F"] >= 4 and row["M"] >= 4:
            return "Champions"
        if row["R"] >= 3 and row["F"] >= 3:
            return "Loyal customers"
        if row["R"] >= 3 and row["F"] <= 2:
            return "Promising"
        if row["R"] <= 2 and row["F"] >= 3:
            return "At risk"
        return "Needs attention"

    customer["segment"] = customer.apply(classify, axis=1)
    return customer[columns].sort_values(
        ["R", "F", "M"], ascending=[False, False, False]
    ).reset_index(drop=True)


def build_cohort_retention(sales: pd.DataFrame) -> pd.DataFrame:
    """Return a cohort x elapsed-month retention matrix (0.0–1.0)."""
    frame = sales.dropna(subset=["CustomerID"]).copy()
    if frame.empty:
        return pd.DataFrame()
    frame["invoice_month"] = frame["InvoiceDate"].dt.to_period("M")
    first_month = frame.groupby("CustomerID")["invoice_month"].min().rename("cohort_month")
    frame = frame.join(first_month, on="CustomerID")
    frame["month_index"] = (
        (frame["invoice_month"].dt.year - frame["cohort_month"].dt.year) * 12
        + frame["invoice_month"].dt.month
        - frame["cohort_month"].dt.month
    )
    cohort_data = (
        frame.groupby(["cohort_month", "month_index"])["CustomerID"]
        .nunique()
        .unstack(fill_value=0)
    )
    if 0 not in cohort_data.columns:
        return pd.DataFrame()
    retention = cohort_data.div(cohort_data[0], axis=0)
    retention.index = retention.index.astype(str)
    retention.columns = [f"month_{int(column)}" for column in retention.columns]
    return retention.round(4)
