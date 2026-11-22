"""Interactive Streamlit dashboard for the synthetic e-commerce case study."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis import load_orders, prepare_orders  # noqa: E402


st.set_page_config(
    page_title="E-commerce Analytics | Portfolio",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def get_orders() -> pd.DataFrame:
    return prepare_orders(load_orders(PROJECT_ROOT / "data" / "orders.csv"))


orders = get_orders()
st.title("E-commerce performance dashboard")
st.caption(
    "Portfolio case study · synthetic dataset · generated demonstration values, "
    "not real company or customer data"
)

with st.sidebar:
    st.header("Filters")
    all_regions = sorted(orders["region"].unique().tolist())
    selected_regions = st.multiselect("Regions", all_regions, default=all_regions)
    all_categories = sorted(orders["category"].unique().tolist())
    selected_categories = st.multiselect(
        "Product categories", all_categories, default=all_categories
    )
    min_date = orders["order_date"].min().date()
    max_date = orders["order_date"].max().date()
    selected_dates = st.date_input(
        "Order period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

filtered = orders[
    orders["region"].isin(selected_regions)
    & orders["category"].isin(selected_categories)
].copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered = filtered[
        filtered["order_date"].dt.date.between(start_date, end_date)
    ]
elif selected_dates:
    filtered = filtered[filtered["order_date"].dt.date.eq(selected_dates)]

if filtered.empty:
    st.warning("No orders match the selected filters. Expand the filter selection.")
    st.stop()

paid = filtered["payment_status"].eq("paid")
completed = filtered["is_completed"]
paid_count = int(paid.sum())
completed_count = int(completed.sum())
revenue = float(filtered["recognised_revenue"].sum())
aov = revenue / completed_count if completed_count else 0.0
return_rate = (
    float(filtered["is_paid_returned"].sum()) / paid_count if paid_count else 0.0
)

metric_cols = st.columns(4)
metric_cols[0].metric("Orders", f"{len(filtered):,}")
metric_cols[1].metric("Recognised revenue", f"{revenue:,.0f}")
metric_cols[2].metric("Average order value", f"{aov:,.0f}")
metric_cols[3].metric("Return rate", f"{return_rate:.1%}")

monthly = (
    filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)
    .agg(revenue=("recognised_revenue", "sum"), orders=("order_id", "count"))
)
category = (
    filtered.groupby("category", as_index=False)
    .agg(revenue=("recognised_revenue", "sum"), orders=("order_id", "count"))
    .sort_values("revenue", ascending=False)
)
channel = (
    filtered.groupby("channel", as_index=False)
    .agg(revenue=("recognised_revenue", "sum"), orders=("order_id", "count"))
)
status = (
    filtered.groupby("payment_status", as_index=False)
    .agg(orders=("order_id", "count"))
)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by month")
    fig = px.line(
        monthly, x="month", y="revenue", markers=True,
        labels={"month": "Month", "revenue": "Recognised revenue"},
    )
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by category")
    fig = px.bar(
        category, x="category", y="revenue", color="category",
        labels={"category": "Category", "revenue": "Recognised revenue"},
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Orders by payment status")
    fig = px.pie(status, names="payment_status", values="orders", hole=0.55)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Channel comparison")
    fig = px.bar(
        channel, x="channel", y="revenue", color="channel",
        labels={"channel": "Channel", "revenue": "Recognised revenue"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered order data")
display_columns = [
    "order_id", "order_date", "region", "channel", "category",
    "payment_status", "quantity", "unit_price", "discount_pct",
    "recognised_revenue", "is_returned",
]
st.dataframe(
    filtered[display_columns].sort_values("order_date", ascending=False),
    use_container_width=True,
    hide_index=True,
)

csv = filtered[display_columns].to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data (CSV)",
    data=csv,
    file_name="filtered-ecommerce-orders.csv",
    mime="text/csv",
)

st.info(
    "Metric note: recognised revenue includes paid, non-returned orders only. "
    "The dataset is generated for demonstration and must not be interpreted as "
    "evidence of real market performance."
)
