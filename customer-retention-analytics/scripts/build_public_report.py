from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from retail_analytics import (
    build_cohort_retention,
    build_rfm,
    clean_transactions,
    country_sales,
    monthly_sales,
    summarize_sales,
    top_products,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_URL = "https://archive.ics.uci.edu/dataset/352/online-retail"
DATASET_DOI = "https://doi.org/10.24432/C5BW33"


def build_public_report(input_path: Path, output_dir: Path) -> dict:
    """Build reproducible, aggregate-only outputs from the attributed UCI workbook.

    Customer-level rows and identifiers are deliberately never exported.
    """
    if not input_path.exists():
        raise FileNotFoundError(
            f"Workbook not found: {input_path}. Run python scripts/download_data.py first."
        )

    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        raw = pd.read_csv(input_path)
    elif suffix in {".xlsx", ".xlsm"}:
        raw = pd.read_excel(input_path)
    else:
        raise ValueError("Input must be a CSV fixture or an Excel workbook (.xlsx / .xlsm).")

    sales, refunds = clean_transactions(raw)
    if sales.empty:
        raise ValueError("The source workbook produced no valid positive sales rows.")

    output_dir.mkdir(parents=True, exist_ok=True)

    kpis = summarize_sales(sales, refunds)
    monthly = monthly_sales(sales)
    countries = country_sales(sales)
    products = top_products(sales, limit=10)
    rfm = build_rfm(sales, refunds)
    cohorts = build_cohort_retention(sales)

    # Aggregate RFM: no customer identifiers or customer-level records are exported.
    if rfm.empty:
        rfm_segments = pd.DataFrame(
            columns=[
                "segment",
                "customers",
                "avg_recency_days",
                "median_frequency",
                "avg_monetary_gbp",
                "median_monetary_gbp",
            ]
        )
    else:
        rfm_segments = (
            rfm.groupby("segment", as_index=False)
            .agg(
                customers=("segment", "size"),
                avg_recency_days=("recency_days", "mean"),
                median_frequency=("frequency", "median"),
                avg_monetary_gbp=("monetary_gbp", "mean"),
                median_monetary_gbp=("monetary_gbp", "median"),
            )
            .sort_values("customers", ascending=False)
        )
        for column in ("avg_recency_days", "median_frequency", "avg_monetary_gbp", "median_monetary_gbp"):
            rfm_segments[column] = rfm_segments[column].round(2)

    # Cohort sizes are aggregate-only. Month-1 retention is omitted where a full
    # subsequent calendar month is not present in the observation window.
    identified = sales.dropna(subset=["CustomerID"]).copy()
    identified["invoice_month"] = identified["InvoiceDate"].dt.to_period("M")
    first_month = identified.groupby("CustomerID")["invoice_month"].min()
    cohort_sizes = first_month.value_counts().sort_index().rename_axis("cohort_month").reset_index(name="customers")
    cohort_sizes["cohort_month"] = cohort_sizes["cohort_month"].astype(str)
    if not cohorts.empty and "month_1" in cohorts.columns:
        cohort_sizes["month_1_retention_pct"] = (
            cohort_sizes["cohort_month"].map(cohorts["month_1"]).mul(100).round(2)
        )
    else:
        cohort_sizes["month_1_retention_pct"] = pd.NA

    top_countries = countries.head(10).copy()
    if not top_countries.empty and kpis["gross_sales_gbp"] > 0:
        top_countries["revenue_share_pct"] = (
            top_countries["revenue_gbp"] / kpis["gross_sales_gbp"] * 100
        ).round(2)
    else:
        top_countries["revenue_share_pct"] = 0.0

    raw_invoice = raw["InvoiceNo"].astype("string").str.strip().str.upper()
    cancellation_mask = raw_invoice.str.startswith("C", na=False)
    raw_quantity = pd.to_numeric(raw["Quantity"], errors="coerce")
    missing_customer_rows = int(sales["CustomerID"].isna().sum())
    identified_customer_count = int(sales["CustomerID"].nunique(dropna=True))
    country_count = int(sales["Country"].nunique(dropna=True))
    product_count = int(sales["StockCode"].nunique(dropna=True))
    refunds_pct = (
        round(kpis["refunds_gbp"] / kpis["gross_sales_gbp"] * 100, 2)
        if kpis["gross_sales_gbp"] > 0
        else 0.0
    )

    peak_month = (
        monthly.sort_values("revenue_gbp", ascending=False).iloc[0].to_dict()
        if not monthly.empty
        else {}
    )
    peak_country = top_countries.iloc[0].to_dict() if not top_countries.empty else {}
    peak_product = products.iloc[0].to_dict() if not products.empty else {}
    segment_totals = (
        {row["segment"]: int(row["customers"]) for _, row in rfm_segments.iterrows()}
        if not rfm_segments.empty
        else {}
    )

    summary = {
        "dataset": "UCI Online Retail",
        "dataset_url": DATASET_URL,
        "dataset_doi": DATASET_DOI,
        "license": "CC BY 4.0",
        "currency": "GBP",
        "source_rows": int(len(raw)),
        "source_columns": int(len(raw.columns)),
        "valid_sales_lines": int(len(sales)),
        "refund_or_cancellation_lines": int(len(refunds)),
        "excluded_invalid_lines": int(len(raw) - len(sales) - len(refunds)),
        "cancellation_invoice_lines": int(cancellation_mask.sum()),
        "unique_cancellation_invoices": int(raw_invoice.loc[cancellation_mask].nunique()),
        "negative_quantity_source_lines": int(raw_quantity.lt(0).sum()),
        "sales_lines_without_customer_id": missing_customer_rows,
        "date_start": sales["InvoiceDate"].min().date().isoformat(),
        "date_end": sales["InvoiceDate"].max().date().isoformat(),
        "unique_countries": country_count,
        "unique_products": product_count,
        **kpis,
        "refunds_as_pct_of_gross_sales": refunds_pct,
        "peak_month": str(peak_month.get("month", "")),
        "peak_month_gross_sales_gbp": round(float(peak_month.get("revenue_gbp", 0)), 2),
        "top_country": str(peak_country.get("Country", "")),
        "top_country_gross_sales_gbp": round(float(peak_country.get("revenue_gbp", 0)), 2),
        "top_country_revenue_share_pct": round(float(peak_country.get("revenue_share_pct", 0)), 2),
        "top_product": str(peak_product.get("Description", "")),
        "top_product_gross_sales_gbp": round(float(peak_product.get("revenue_gbp", 0)), 2),
        "rfm_segment_customers": segment_totals,
        "identified_customers_with_multiple_invoices": int(kpis["repeat_customers"]),
        "cohort_count": int(len(cohort_sizes)),
        "weighted_month_1_retention_pct": (
            round(
                float(
                    (
                        cohort_sizes.dropna(subset=["month_1_retention_pct"])
                        .assign(weighted=lambda frame: frame["customers"] * frame["month_1_retention_pct"])
                        ["weighted"].sum()
                        / cohort_sizes.dropna(subset=["month_1_retention_pct"])["customers"].sum()
                    )
                ),
                2,
            )
            if not cohort_sizes.dropna(subset=["month_1_retention_pct"]).empty
            else None
        ),
    }

    # Only aggregate and non-identifying tables are exported.
    monthly.to_csv(output_dir / "monthly_sales.csv", index=False)
    top_countries.to_csv(output_dir / "country_sales_top10.csv", index=False)
    products.to_csv(output_dir / "top_products.csv", index=False)
    rfm_segments.to_csv(output_dir / "rfm_segments.csv", index=False)
    cohort_sizes.to_csv(output_dir / "cohort_sizes.csv", index=False)
    cohorts.to_csv(output_dir / "cohort_retention.csv", index=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    findings = [
        "# UCI Online Retail — generated findings",
        "",
        f"> Dataset: [UCI Online Retail]({DATASET_URL}) · DOI: {DATASET_DOI} · License: CC BY 4.0.",
        "> The figures below are computed from the source workbook by this repository's reproducible pipeline.",
        "",
        "## Dataset coverage",
        "",
        f"- Source rows: {summary['source_rows']:,}",
        f"- Transaction period: {summary['date_start']} to {summary['date_end']}",
        f"- Countries represented in valid positive sales: {country_count:,}",
        f"- Distinct products represented in valid positive sales: {product_count:,}",
        f"- Valid positive sales lines: {len(sales):,}",
        f"- Refund / cancellation lines: {len(refunds):,}",
        f"- Invalid or excluded rows under the documented cleaning rules: {summary['excluded_invalid_lines']:,}",
        "",
        "## Headline sales and customer metrics",
        "",
        f"- Gross sales: £{kpis['gross_sales_gbp']:,.2f}",
        f"- Refunds / cancellations: £{kpis['refunds_gbp']:,.2f} ({refunds_pct:.2f}% of gross sales)",
        f"- Net sales: £{kpis['net_sales_gbp']:,.2f}",
        f"- Distinct invoices among positive sale lines: {kpis['orders']:,}",
        f"- Identified customers: {identified_customer_count:,}",
        f"- Repeat customers: {kpis['repeat_customers']:,} ({kpis['repeat_customer_rate_pct']:.2f}% of identified customers)",
        f"- Positive sales lines without CustomerID: {missing_customer_rows:,}",
        "",
        "## Time and geography",
        "",
        f"- Highest-gross-sales month: {summary['peak_month']} (£{summary['peak_month_gross_sales_gbp']:,.2f})",
        f"- Highest-gross-sales country: {summary['top_country']} (£{summary['top_country_gross_sales_gbp']:,.2f}; {summary['top_country_revenue_share_pct']:.2f}% of gross sales)",
        "",
        "## RFM segment counts",
        "",
    ]
    findings.extend(
        f"- {segment}: {count:,} customers"
        for segment, count in sorted(segment_totals.items(), key=lambda item: item[1], reverse=True)
    )
    findings.extend([
        "",
        "## Cohort analysis",
        "",
        f"- First-purchase cohorts represented: {summary['cohort_count']:,}",
        (
            f"- Weighted month-1 retention across cohorts with a full follow-up month: {summary['weighted_month_1_retention_pct']:.2f}%"
            if summary["weighted_month_1_retention_pct"] is not None
            else "- Month-1 retention is unavailable for the available cohort window."
        ),
        "",
        "## Interpretation and limitations",
        "",
        "- The dataset is historical (2010–2011) and is not a current market benchmark.",
        "- Sales rows without CustomerID remain in sales totals but are excluded from customer-level and cohort calculations.",
        "- RFM uses relative quartiles over the observation window; segments are descriptive, not churn probabilities.",
        "- Refunds and cancellations are aggregated as absolute line amounts. The report does not attempt to match every return to its original sale line.",
        "- The dataset is observational; it does not establish why customers purchased or stopped purchasing or prove marketing impact.",
        "- Country and product rankings reflect gross positive invoice lines, before refunds.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python scripts/download_data.py",
        "python scripts/build_public_report.py",
        "pytest",
        "```",
        "",
        "## Attribution",
        "",
        "Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0.",
    ])
    (output_dir / "findings.md").write_text("\n".join(findings) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build an aggregate-only report from the official UCI Online Retail workbook."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "docs" / "generated",
    )
    args = parser.parse_args()
    print(json.dumps(build_public_report(args.input, args.output), ensure_ascii=False, indent=2))
