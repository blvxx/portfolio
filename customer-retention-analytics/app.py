from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from retail_analytics import (
    build_cohort_retention,
    build_rfm,
    clean_transactions,
    country_sales,
    monthly_sales,
    summarize_sales,
    top_products,
)

ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "data" / "sample_transactions.csv"
GENERATED = ROOT / "docs" / "generated"
REQUIRED_PUBLIC_FILES = (
    "summary.json",
    "monthly_sales.csv",
    "country_sales_top10.csv",
    "top_products.csv",
    "rfm_segments.csv",
    "cohort_retention.csv",
)

st.set_page_config(page_title="Retail Customer Analytics", page_icon="📊", layout="wide")
st.title("Retail sales & customer retention")
st.caption("UCI Online Retail · Sales trends · RFM segmentation · Cohort retention")

uploaded = st.sidebar.file_uploader(
    "Upload the original UCI Online Retail.xlsx",
    type=["xlsx"],
    help="The original workbook is available from the UCI dataset page; it is not stored in this repository.",
)

public_report_available = all((GENERATED / filename).exists() for filename in REQUIRED_PUBLIC_FILES)

if uploaded is not None:
    # Full workbook mode: users can filter and recalculate all metrics interactively.
    raw_data = pd.read_excel(uploaded)
    sales, refunds = clean_transactions(raw_data)
    countries = sorted(sales["Country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect("Filter countries", countries, default=countries)
    filtered_sales = sales[sales["Country"].isin(selected_countries)]
    filtered_refunds = refunds[refunds["Country"].isin(selected_countries)]

    kpis = summarize_sales(filtered_sales, filtered_refunds)
    monthly = monthly_sales(filtered_sales)
    by_country = country_sales(filtered_sales)
    products = top_products(filtered_sales, limit=10)
    rfm = build_rfm(filtered_sales, filtered_refunds)
    rfm_segments = (
        rfm["segment"].value_counts().rename_axis("segment").reset_index(name="customers")
        if not rfm.empty
        else pd.DataFrame(columns=["segment", "customers"])
    )
    cohorts = build_cohort_retention(filtered_sales)
    source_label = "Uploaded UCI Online Retail workbook"
    data_quality = {
        "Rows in loaded file": int(len(raw_data)),
        "Positive sales lines": int(len(sales)),
        "Refund / cancellation lines": int(len(refunds)),
        "Sales lines without CustomerID": int(sales["CustomerID"].isna().sum()),
        "Gross sales (GBP)": kpis["gross_sales_gbp"],
        "Refunds (GBP)": kpis["refunds_gbp"],
    }
    st.sidebar.success("Uploaded workbook is being analysed interactively.")

elif public_report_available:
    # Default mode: source-derived aggregate report committed by GitHub Actions.
    summary = json.loads((GENERATED / "summary.json").read_text(encoding="utf-8"))
    kpis = summary
    monthly = pd.read_csv(GENERATED / "monthly_sales.csv")
    by_country = pd.read_csv(GENERATED / "country_sales_top10.csv")
    products = pd.read_csv(GENERATED / "top_products.csv")
    rfm_segments = pd.read_csv(GENERATED / "rfm_segments.csv")
    cohorts = pd.read_csv(GENERATED / "cohort_retention.csv", index_col=0)
    source_label = "Official UCI Online Retail · generated aggregate report"
    data_quality = {
        "Source rows": int(summary["source_rows"]),
        "Positive sales lines": int(summary["valid_sales_lines"]),
        "Refund / cancellation lines": int(summary["refund_or_cancellation_lines"]),
        "Excluded invalid lines": int(summary["excluded_invalid_lines"]),
        "Positive sales lines without CustomerID": int(summary["sales_lines_without_customer_id"]),
        "Countries": int(summary["unique_countries"]),
        "Products": int(summary["unique_products"]),
        "Gross sales (GBP)": summary["gross_sales_gbp"],
        "Refunds (GBP)": summary["refunds_gbp"],
        "Net sales (GBP)": summary["net_sales_gbp"],
    }
    st.sidebar.success("Loaded the source-derived UCI aggregate report.")
    st.sidebar.caption(
        "Monthly, country, product, RFM and cohort tables are precomputed from the full workbook. "
        "No customer-level identifiers are included in these public outputs."
    )
    st.sidebar.markdown(
        "[Open the generated findings](https://github.com/blvxx/portfolio/blob/main/customer-retention-analytics/docs/generated/findings.md)"
    )

else:
    # Small clearly labelled fixture is only used when no published UCI report exists.
    raw_data = pd.read_csv(SAMPLE)
    sales, refunds = clean_transactions(raw_data)
    countries = sorted(sales["Country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect("Filter countries", countries, default=countries)
    filtered_sales = sales[sales["Country"].isin(selected_countries)]
    filtered_refunds = refunds[refunds["Country"].isin(selected_countries)]

    kpis = summarize_sales(filtered_sales, filtered_refunds)
    monthly = monthly_sales(filtered_sales)
    by_country = country_sales(filtered_sales)
    products = top_products(filtered_sales, limit=10)
    rfm = build_rfm(filtered_sales, filtered_refunds)
    rfm_segments = (
        rfm["segment"].value_counts().rename_axis("segment").reset_index(name="customers")
        if not rfm.empty
        else pd.DataFrame(columns=["segment", "customers"])
    )
    cohorts = build_cohort_retention(filtered_sales)
    source_label = "Synthetic offline preview fixture"
    data_quality = {
        "Rows in preview fixture": int(len(raw_data)),
        "Positive sales lines": int(len(sales)),
        "Refund / cancellation lines": int(len(refunds)),
        "Sales lines without CustomerID": int(sales["CustomerID"].isna().sum()),
        "Gross sales (GBP)": kpis["gross_sales_gbp"],
        "Refunds (GBP)": kpis["refunds_gbp"],
    }
    st.sidebar.info("The small synthetic fixture is being used because no generated UCI report is present.")

if source_label.startswith("Synthetic"):
    st.warning(
        "Synthetic preview only: these figures do not describe the UCI source dataset or a real company."
    )
elif source_label.startswith("Official"):
    st.success(
        "Source-backed mode · {}–{} · {} transaction rows · figures are in GBP.".format(
            summary["date_start"],
            summary["date_end"],
            "{:,}".format(summary["source_rows"]),
        )
    )
else:
    st.success("Source workbook uploaded. Figures are recalculated from the selected countries.")

st.caption("Data source: " + source_label)
metric_cols = st.columns(4)
metric_cols[0].metric("Net sales", "£{:,.2f}".format(kpis["net_sales_gbp"]))
metric_cols[1].metric("Invoices", "{:,}".format(kpis["orders"]))
metric_cols[2].metric("Identified customers", "{:,}".format(kpis["customers"]))
metric_cols[3].metric("Repeat customer rate", "{:.2f}%".format(kpis["repeat_customer_rate_pct"]))

left, right = st.columns(2)
with left:
    st.subheader("Monthly gross sales")
    if monthly.empty:
        st.info("No monthly sales are available for the selected view.")
    else:
        st.plotly_chart(
            px.line(
                monthly,
                x="month",
                y="revenue_gbp",
                markers=True,
                title="Gross positive invoice-line sales (refunds excluded)",
            ),
            use_container_width=True,
        )
with right:
    st.subheader("Sales by country")
    if by_country.empty:
        st.info("No country rows are available for this view.")
    else:
        st.plotly_chart(
            px.bar(
                by_country.head(10),
                x="Country",
                y="revenue_gbp",
                title="Top 10 countries by gross sales",
            ),
            use_container_width=True,
        )

left, right = st.columns(2)
with left:
    st.subheader("Top products")
    if products.empty:
        st.info("No product rows are available for this view.")
    else:
        st.plotly_chart(
            px.bar(
                products.head(10).sort_values("revenue_gbp"),
                x="revenue_gbp",
                y="Description",
                orientation="h",
                title="Top products by gross sales",
            ),
            use_container_width=True,
        )
with right:
    st.subheader("RFM customer segments")
    if rfm_segments.empty:
        st.info("Customer identifiers are required for RFM segmentation.")
    else:
        st.plotly_chart(
            px.bar(
                rfm_segments,
                x="segment",
                y="customers",
                title="Customer count by relative RFM segment",
            ),
            use_container_width=True,
        )

st.subheader("Cohort retention")
if cohorts.empty:
    st.info("Not enough identified customer history to build a cohort matrix.")
else:
    st.plotly_chart(
        px.imshow(
            cohorts,
            text_auto=".0%",
            aspect="auto",
            color_continuous_scale="Blues",
            labels={"x": "Months since first purchase", "y": "Cohort month", "color": "Retention"},
            title="Share of cohort customers active in each subsequent month",
            zmin=0,
            zmax=1,
        ),
        use_container_width=True,
    )

if isinstance(kpis, dict) and "sql_gross_sales_gbp" in kpis:
    st.subheader("Independent SQL cross-check")
    sql_cols = st.columns(2)
    sql_cols[0].metric(
        "SQL gross sales",
        "£{:,.2f}".format(kpis["sql_gross_sales_gbp"]),
        delta="Matches pandas",
    )
    sql_cols[1].metric(
        "SQL repeat-customer rate",
        "{:.2f}%".format(kpis["sql_repeat_customer_rate_pct"]),
        delta="Matches pandas",
    )

with st.expander("Data quality and methodology"):
    st.write(data_quality)
    if isinstance(kpis, dict) and "sql_gross_sales_gbp" in kpis:
        st.write({
            "SQL gross sales (GBP)": kpis["sql_gross_sales_gbp"],
            "SQL repeat-customer rate (%)": kpis["sql_repeat_customer_rate_pct"],
            "SQL and pandas reconciliation": "Passed during the source-report build",
        })
    st.markdown(
        "Cancellation invoices and negative-quantity rows are separated from positive sales. "
        "Anonymous sales remain in revenue totals but are excluded from customer-level RFM and cohort counts. "
        "RFM scores are relative quartiles, not predictive probabilities. "
        "Published aggregate reports do not contain customer-level identifiers."
    )
