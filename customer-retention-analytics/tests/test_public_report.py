import json
import sys
from pathlib import Path

import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from build_public_report import build_public_report  # noqa: E402


def test_public_report_writes_aggregate_outputs_without_customer_ids(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "data" / "sample_transactions.csv"
    output = tmp_path / "generated"

    summary = build_public_report(source, output)

    assert summary["dataset"] == "UCI Online Retail"
    assert summary["source_rows"] == len(pd.read_csv(source))
    assert summary["gross_sales_gbp"] > 0
    assert summary["refunds_gbp"] > 0
    assert summary["net_sales_gbp"] == summary["gross_sales_gbp"] - summary["refunds_gbp"]
    assert summary["customers"] > 0
    assert summary["unique_countries"] > 0
    assert summary["sql_gross_sales_gbp"] == summary["gross_sales_gbp"]
    assert summary["sql_repeat_customer_rate_pct"] == summary["repeat_customer_rate_pct"]

    expected_files = {
        "summary.json",
        "findings.md",
        "monthly_sales.csv",
        "country_sales_top10.csv",
        "top_products.csv",
        "rfm_segments.csv",
        "cohort_sizes.csv",
        "cohort_retention.csv",
        "sql_monthly_sales.csv",
        "sql_country_sales.csv",
        "sql_repeat_customers.csv",
        "sql_rfm_segments.csv",
        "sql_cohort_retention.csv",
    }
    assert expected_files.issubset({path.name for path in output.iterdir()})

    report_json = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert report_json["dataset_doi"] == "https://doi.org/10.24432/C5BW33"
    assert "CustomerID" not in (output / "rfm_segments.csv").read_text(encoding="utf-8")
    assert "CustomerID" not in (output / "cohort_sizes.csv").read_text(encoding="utf-8")
    assert "CustomerID" not in (output / "monthly_sales.csv").read_text(encoding="utf-8")
    assert "customer_id" not in (output / "sql_rfm_segments.csv").read_text(encoding="utf-8")
    assert "customer_id" not in (output / "sql_cohort_retention.csv").read_text(encoding="utf-8")
    assert "customer_id" not in (output / "sql_country_sales.csv").read_text(encoding="utf-8")
    assert "synthetic" not in (output / "findings.md").read_text(encoding="utf-8").lower()


def test_public_report_refuses_missing_workbook(tmp_path):
    missing = tmp_path / "missing.xlsx"
    try:
        build_public_report(missing, tmp_path / "output")
    except FileNotFoundError as error:
        assert "download_data.py" in str(error)
    else:
        raise AssertionError("Expected FileNotFoundError for missing source workbook.")
