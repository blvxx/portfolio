#!/usr/bin/env python3
"""Build a consolidated incident summary from logs and reconciliation findings."""
from __future__ import annotations
import argparse
import csv
import json
import re
from collections import Counter
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEFAULT_LOG = BASE / "evidence" / "application.log"
DEFAULT_FINDINGS = BASE / "reports" / "reconciliation_findings.csv"
DEFAULT_JSON = BASE / "reports" / "incident_summary.json"
DEFAULT_HTML = BASE / "reports" / "incident_summary.html"
LOG_RE = re.compile(r"^\S+\s+(INFO|WARN|ERROR)\s+(.*)$")
SIGNATURE = re.compile(r"signature_validation_failed|secret_mismatch|HTTP 401", re.I)
TIMEOUT = re.compile(r"timeout|timed out", re.I)
DOWNSTREAM = re.compile(r"downstream.*5\d\d|HTTP 5\d\d", re.I)
DUPLICATE = re.compile(r"duplicate", re.I)
DELAYED = re.compile(r"delayed|delivery lag", re.I)

def read_findings(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def summarize(log_path: Path, findings: list[dict[str, str]]) -> dict:
    lines = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
    log_counts = Counter()
    malformed = 0
    patterns = Counter()
    for line in lines:
        match = LOG_RE.match(line)
        if not match:
            malformed += 1
            continue
        level, message = match.groups()
        log_counts[level] += 1
        if SIGNATURE.search(message): patterns["signature/authentication failures"] += 1
        if TIMEOUT.search(message): patterns["timeouts"] += 1
        if DOWNSTREAM.search(message): patterns["downstream 5xx"] += 1
        if DUPLICATE.search(message): patterns["duplicate events"] += 1
        if DELAYED.search(message): patterns["delayed events"] += 1
    severity = Counter(item.get("severity", "UNKNOWN") for item in findings)
    issue_types = Counter(item.get("issue", "UNKNOWN") for item in findings)
    affected_orders = sorted({item.get("order_id", "").strip() for item in findings if item.get("order_id", "").strip()})
    high_orders = sorted({item.get("order_id", "").strip() for item in findings if item.get("severity") == "HIGH" and item.get("order_id", "").strip()})
    root_cause_hint = "Review webhook authentication/secret configuration." if patterns["signature/authentication failures"] else "Correlate log events with reconciliation findings; root cause is not established by these inputs."
    priority = "HIGH" if severity["HIGH"] or patterns["signature/authentication failures"] or patterns["timeouts"] or patterns["downstream 5xx"] else "MEDIUM" if findings or patterns else "LOW"
    recommendations = []
    if patterns["signature/authentication failures"]:
        recommendations.append("Validate webhook secret/version, signature algorithm, and provider configuration; confirm with a controlled test event.")
    if patterns["timeouts"] or patterns["downstream 5xx"]:
        recommendations.append("Check dependency health, handler latency, retry behavior, and queue backlog.")
    if issue_types["DUPLICATE_PROVIDER_PAYMENT_ID"] or issue_types["MULTIPLE_PAYMENTS_FOR_ORDER"] or patterns["duplicate events"]:
        recommendations.append("Review idempotency and provider transaction history before replay, refund, or manual state changes.")
    if issue_types["PAYMENT_ORDER_STATUS_MISMATCH"]:
        recommendations.append("Confirm provider payment status and order state; reconcile only after validation.")
    if issue_types["MISSING_PAYMENT"]:
        recommendations.append("Inspect payment initiation and provider transaction history for missing records.")
    if not recommendations:
        recommendations.append("Review the raw logs and findings; no automatic remediation is recommended.")
    return {
        "priority": priority,
        "log_file": str(log_path),
        "logs_present": log_path.exists(),
        "log_lines": len(lines),
        "parsed_log_levels": dict(log_counts),
        "malformed_log_lines": malformed,
        "log_pattern_counts": dict(patterns),
        "finding_count": len(findings),
        "severity_counts": dict(severity),
        "issue_type_counts": dict(issue_types),
        "affected_order_count": len(affected_orders),
        "affected_order_ids": affected_orders,
        "high_severity_order_ids": high_orders,
        "root_cause_hint": root_cause_hint,
        "recommendations": recommendations,
        "disclaimer": "Synthetic portfolio scenario. This summary is a triage aid, not proof of root cause. Validate against authoritative system/provider records."
    }

def write_json(summary: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def write_html(summary: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cards = [
        ("Priority", summary["priority"]),
        ("Log lines", str(summary["log_lines"])),
        ("Findings", str(summary["finding_count"])),
        ("Affected orders", str(summary["affected_order_count"])),
        ("Malformed lines", str(summary["malformed_log_lines"])),
    ]
    card_html = "".join(f'<article class="card"><span>{escape(k)}</span><strong>{escape(v)}</strong></article>' for k,v in cards)
    pattern_rows = "".join(f"<tr><td>{escape(k)}</td><td>{v}</td></tr>" for k,v in sorted(summary["log_pattern_counts"].items())) or "<tr><td colspan=2>No known patterns detected</td></tr>"
    issue_rows = "".join(f"<tr><td>{escape(k)}</td><td>{v}</td></tr>" for k,v in sorted(summary["issue_type_counts"].items())) or "<tr><td colspan=2>No reconciliation findings</td></tr>"
    recs = "".join(f"<li>{escape(item)}</li>" for item in summary["recommendations"])
    orders = ", ".join(escape(x) for x in summary["affected_order_ids"]) or "None"
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Incident Summary</title><style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:15px/1.5 system-ui}}main{{max-width:1000px;margin:auto;padding:28px 16px}}.muted{{color:#91a3ba}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:20px 0}}.card,section{{background:#121d2e;border:1px solid #26364c;border-radius:12px;padding:16px}}.card span{{display:block;color:#91a3ba}}.card strong{{font-size:25px}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;padding:10px;border-bottom:1px solid #26364c}}section{{margin:16px 0}}h1{{font-size:clamp(24px,4vw,34px)}}footer{{font-size:12px;color:#91a3ba;margin-top:20px}}</style></head><body><main>
<h1>Incident Summary</h1><p class="muted">Combined log analysis and payment reconciliation · Synthetic data</p><div class="cards">{card_html}</div>
<section><h2>Detected log patterns</h2><table><thead><tr><th>Pattern</th><th>Count</th></tr></thead><tbody>{pattern_rows}</tbody></table></section>
<section><h2>Reconciliation issue types</h2><table><thead><tr><th>Issue</th><th>Count</th></tr></thead><tbody>{issue_rows}</tbody></table></section>
<section><h2>Affected orders</h2><p>{orders}</p><h2>Root-cause hypothesis</h2><p>{escape(summary["root_cause_hint"])}</p></section>
<section><h2>Recommended next steps</h2><ol>{recs}</ol></section>
<footer>{escape(summary["disclaimer"])}</footer></main></body></html>"""
    path.write_text(html, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Consolidate incident logs and reconciliation findings.")
    parser.add_argument("--logs", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = parser.parse_args()
    summary = summarize(args.logs, read_findings(args.findings))
    write_json(summary, args.json)
    write_html(summary, args.html)
    print(f"Priority: {summary['priority']}")
    print(f"Log lines: {summary['log_lines']} | Findings: {summary['finding_count']} | Affected orders: {summary['affected_order_count']}")
    print(f"JSON: {args.json}")
    print(f"HTML: {args.html}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
