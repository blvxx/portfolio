#!/usr/bin/env python3
"""Unified CLI for the synthetic Incident Operations Lab."""
from __future__ import annotations
import argparse
import csv
import importlib.util
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent

def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module

def classify_impact(summary: dict) -> dict:
    affected = int(summary.get("affected_order_count", 0))
    findings = int(summary.get("finding_count", 0))
    priority = summary.get("priority", "LOW")
    if priority == "HIGH" or affected >= 3:
        tier = "SEV-2"
    elif findings or affected:
        tier = "SEV-3"
    else:
        tier = "SEV-4"
    return {"severity": tier, "affected_entities": affected, "finding_count": findings,
            "priority": priority, "basis": "Synthetic triage heuristic; validate against service impact and incident policy."}

def run_logs(args):
    analyzer = load_module("incident_summary", "incident_summary.py")
    summary = analyzer.summarize(args.log, [])
    print(f"Log analysis: {summary['priority']} priority | {summary['log_lines']} lines | {summary['log_pattern_counts']}")
    return summary

def run_reconcile(args):
    reconciler = load_module("reconcile_payments", "reconcile_payments.py")
    orders, payments = reconciler.read_csv(args.orders), reconciler.read_csv(args.payments)
    findings = reconciler.reconcile(orders, payments)
    reconciler.write_csv_report(findings, args.findings)
    reconciler.write_html_report(findings, args.reconciliation_html, len(orders))
    print(f"Reconciliation: {len(findings)} findings across {len(orders)} orders")
    return findings

def run_summary(args):
    analyzer = load_module("incident_summary", "incident_summary.py")
    findings = analyzer.read_findings(args.findings)
    summary = analyzer.summarize(args.log, findings)
    summary["impact_assessment"] = classify_impact(summary)
    analyzer.write_json(summary, args.json)
    analyzer.write_html(summary, args.html)
    print(f"Summary: {summary['priority']} priority / {summary['impact_assessment']['severity']} | {summary['affected_order_count']} affected orders")
    return summary

def parser():
    p = argparse.ArgumentParser(description="Incident Operations Toolkit — synthetic incident triage and diagnostics")
    sub = p.add_subparsers(dest="command", required=True)
    logs = sub.add_parser("analyze-logs", help="Analyze log patterns")
    logs.add_argument("--log", type=Path, default=BASE / "evidence/application.log")
    logs.set_defaults(func=run_logs)
    rec = sub.add_parser("reconcile", help="Reconcile order and payment CSV data")
    rec.add_argument("--orders", type=Path, default=BASE / "data/sample_orders.csv")
    rec.add_argument("--payments", type=Path, default=BASE / "data/sample_payments.csv")
    rec.add_argument("--findings", type=Path, default=BASE / "reports/reconciliation_findings.csv")
    rec.add_argument("--html", dest="reconciliation_html", type=Path, default=BASE / "reports/reconciliation_report.html")
    rec.set_defaults(func=run_reconcile)
    summ = sub.add_parser("summary", help="Generate combined incident reports")
    summ.add_argument("--log", type=Path, default=BASE / "evidence/application.log")
    summ.add_argument("--findings", type=Path, default=BASE / "reports/reconciliation_findings.csv")
    summ.add_argument("--json", type=Path, default=BASE / "reports/incident_summary.json")
    summ.add_argument("--html", type=Path, default=BASE / "reports/incident_summary.html")
    summ.set_defaults(func=run_summary)
    all_cmd = sub.add_parser("all", help="Run log analysis, reconciliation, and combined reports")
    all_cmd.add_argument("--log", type=Path, default=BASE / "evidence/application.log")
    all_cmd.add_argument("--orders", type=Path, default=BASE / "data/sample_orders.csv")
    all_cmd.add_argument("--payments", type=Path, default=BASE / "data/sample_payments.csv")
    all_cmd.add_argument("--findings", type=Path, default=BASE / "reports/reconciliation_findings.csv")
    all_cmd.add_argument("--reconciliation-html", type=Path, default=BASE / "reports/reconciliation_report.html")
    all_cmd.add_argument("--json", type=Path, default=BASE / "reports/incident_summary.json")
    all_cmd.add_argument("--html", type=Path, default=BASE / "reports/incident_summary.html")
    all_cmd.set_defaults(func=run_all)
    return p

def run_all(args):
    run_logs(args)
    run_reconcile(args)
    run_summary(args)
    return 0

def main(argv=None):
    args = parser().parse_args(argv)
    result = args.func(args)
    if isinstance(result, dict) and "impact_assessment" in result:
        print(f"Impact assessment: {result['impact_assessment']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
