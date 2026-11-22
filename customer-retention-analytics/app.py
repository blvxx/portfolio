from __future__ import annotations

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

st.set_page_config(page_title="Retail Customer Analytics", page_icon="📊", layout="wide")
st.title("Retail sales & customer retention")
st.caption("UCI Online Retail · Sales trends · RFM segmentation · Cohort retention")

uploaded = st.sidebar.file_uploader(
    "Загрузите исходный файл UCI Online Retail.xlsx",
    type=["xlsx"],
    help="Файл доступен на странице UCI Online Retail; он не хранится в этом репозитории.",
)

if uploaded is not None:
    raw_data = pd.read_excel(uploaded)
    source_label = "UCI Online Retail workbook"
    st.sidebar.success("Загружен исходный файл")
else:
    raw_data = pd.read_csv(SAMPLE)
    source_label = "Synthetic preview fixture"
    st.sidebar.info("Показан небольшой синтетический пример. Загрузите workbook UCI, чтобы увидеть анализ исходного датасета.")

sales, refunds = clean_transactions(raw_data)
countries = sorted(sales["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Страны", countries, default=countries)
filtered_sales = sales[sales["Country"].isin(selected_countries)]
filtered_refunds = refunds[refunds["Country"].isin(selected_countries)]

kpis = summarize_sales(filtered_sales, filtered_refunds)
rfm = build_rfm(filtered_sales, filtered_refunds)
monthly = monthly_sales(filtered_sales)
by_country = country_sales(filtered_sales)
products = top_products(filtered_sales, limit=10)
cohorts = build_cohort_retention(filtered_sales)

if source_label.startswith("Synthetic"):
    st.warning("Демонстрационный режим: цифры ниже рассчитаны на маленьком синтетическом fixture и не описывают реальную компанию.")
else:
    st.success("Режим исходных данных UCI. Денежные суммы показаны в GBP согласно описанию набора данных.")

st.caption("Источник данных: " + source_label)
metric_cols = st.columns(4)
metric_cols[0].metric("Net sales", "£{:,.2f}".format(kpis["net_sales_gbp"]))
metric_cols[1].metric("Invoices", "{:,}".format(kpis["orders"]))
metric_cols[2].metric("Identified customers", "{:,}".format(kpis["customers"]))
metric_cols[3].metric("Repeat customer rate", "{:.1f}%".format(kpis["repeat_customer_rate_pct"]))

left, right = st.columns(2)
with left:
    st.subheader("Monthly sales")
    if monthly.empty:
        st.info("Нет продаж для выбранного фильтра.")
    else:
        st.plotly_chart(
            px.line(monthly, x="month", y="revenue_gbp", markers=True, title="Gross sales from positive invoice lines (refunds excluded)"),
            use_container_width=True,
        )
with right:
    st.subheader("Sales by country")
    if by_country.empty:
        st.info("Нет данных по странам.")
    else:
        st.plotly_chart(
            px.bar(by_country.head(10), x="Country", y="revenue_gbp", title="Top 10 countries by gross sales"),
            use_container_width=True,
        )

left, right = st.columns(2)
with left:
    st.subheader("Top products")
    if products.empty:
        st.info("Нет товарных строк для выбранного фильтра.")
    else:
        st.plotly_chart(
            px.bar(products.head(10).sort_values("revenue_gbp"), x="revenue_gbp", y="Description", orientation="h", title="Top products by revenue"),
            use_container_width=True,
        )
with right:
    st.subheader("RFM customer segments")
    if rfm.empty:
        st.info("Для RFM нужны строки с CustomerID.")
    else:
        distribution = rfm["segment"].value_counts().rename_axis("segment").reset_index(name="customers")
        st.plotly_chart(
            px.bar(distribution, x="segment", y="customers", title="Customer count by relative RFM segment"),
            use_container_width=True,
        )

st.subheader("Cohort retention")
if cohorts.empty:
    st.info("Недостаточно идентифицированных клиентов для cohort analysis.")
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

with st.expander("Data quality and methodology"):
    st.write(
        {
            "Rows in loaded file": int(len(raw_data)),
            "Positive sales lines": int(len(sales)),
            "Refund / cancellation lines": int(len(refunds)),
            "Sales lines without CustomerID": int(sales["CustomerID"].isna().sum()),
            "Gross sales (GBP)": kpis["gross_sales_gbp"],
            "Refunds (GBP)": kpis["refunds_gbp"],
        }
    )
    st.markdown(
        "Cancellation invoices and negative-quantity rows are separated from positive sales. "
        "Anonymous sales remain in revenue totals but are excluded from RFM and cohort customer counts. "
        "RFM scores are relative quartiles, not predictive probabilities."
    )
