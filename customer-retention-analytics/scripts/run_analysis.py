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


def run(input_path: Path, output_dir: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Workbook not found: {input_path}. Run python scripts/download_data.py first."
        )
    raw = pd.read_excel(input_path)
    sales, refunds = clean_transactions(raw)
    output_dir.mkdir(parents=True, exist_ok=True)

    kpis = summarize_sales(sales, refunds)
    monthly = monthly_sales(sales)
    countries = country_sales(sales)
    products = top_products(sales)
    rfm = build_rfm(sales, refunds)
    cohorts = build_cohort_retention(sales)

    monthly.to_csv(output_dir / "monthly_sales.csv", index=False)
    countries.to_csv(output_dir / "country_sales.csv", index=False)
    products.to_csv(output_dir / "top_products.csv", index=False)
    rfm.to_csv(output_dir / "rfm_customers.csv", index=False)
    cohorts.to_csv(output_dir / "cohort_retention.csv", index=True)

    summary = {
        **kpis,
        "source_rows": int(len(raw)),
        "valid_sales_rows": int(len(sales)),
        "refund_rows": int(len(refunds)),
        "date_start": sales["InvoiceDate"].min().date().isoformat() if not sales.empty else None,
        "date_end": sales["InvoiceDate"].max().date().isoformat() if not sales.empty else None,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    top_country = countries.iloc[0]["Country"] if not countries.empty else "n/a"
    top_product = products.iloc[0]["Description"] if not products.empty else "n/a"
    segment_counts = rfm["segment"].value_counts().to_dict() if not rfm.empty else {}
    findings = [
        "# Generated analysis findings",
        "",
        "> Generated from the UCI Online Retail workbook. Figures describe this historical dataset only; they are not current market estimates.",
        "",
        "## Headline KPIs",
        "",
        f"- Gross sales: £{kpis['gross_sales_gbp']:,.2f}",
        f"- Refunds / cancellations: £{kpis['refunds_gbp']:,.2f}",
        f"- Net sales: £{kpis['net_sales_gbp']:,.2f}",
        f"- Invoices: {kpis['orders']:,}",
        f"- Identified customers: {kpis['customers']:,}",
        f"- Repeat customer rate: {kpis['repeat_customer_rate_pct']:.2f}%",
        "",
        "## Leading categories",
        "",
        f"- Highest-revenue country: {top_country}",
        f"- Highest-revenue product: {top_product}",
        "",
        "## RFM segment counts",
        "",
    ]
    findings.extend(f"- {name}: {count:,}" for name, count in segment_counts.items())
    findings.extend([
        "",
        "## Interpretation checklist",
        "",
        "- Compare gross sales with refunds before discussing net performance.",
        "- Review the monthly trend for seasonality and large invoice-level spikes.",
        "- Check the size and value of the at-risk segment before proposing win-back activity.",
        "- Treat customer retention as observed repeat purchasing in this dataset, not proof of campaign impact.",
        "",
        "## Limitations",
        "",
        "- The data covers a historical period from 2010–2011 and should not be used as a current market benchmark.",
        "- Customer IDs are missing for some lines; those lines remain in sales totals but are excluded from customer-level analysis.",
        "- RFM segments are relative quartile-based groups and depend on the selected observation window.",
        "- The dataset is observational; correlations do not establish why customers purchased or stopped purchasing.",
    ])
    (output_dir / "findings.md").write_text("\n".join(findings) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run retail sales and customer retention analysis.")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "outputs")
    args = parser.parse_args()
    result = run(args.input, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
