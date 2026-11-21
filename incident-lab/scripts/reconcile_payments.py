#!/usr/bin/env python3
"""Reconcile synthetic order and payment CSV files and write CSV + HTML findings."""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEFAULT_ORDERS = BASE / "data" / "sample_orders.csv"
DEFAULT_PAYMENTS = BASE / "data" / "sample_payments.csv"
DEFAULT_OUTPUT = BASE / "reports" / "reconciliation_findings.csv"
DEFAULT_HTML = BASE / "reports" / "reconciliation_report.html"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def reconcile(orders: list[dict[str, str]], payments: list[dict[str, str]]) -> list[dict[str, str]]:
    by_order: dict[str, list[dict[str, str]]] = defaultdict(list)
    provider_counts = Counter()
    for payment in payments:
        by_order[payment.get("order_id", "").strip()].append(payment)
        provider_id = payment.get("provider_payment_id", "").strip()
        if provider_id:
            provider_counts[provider_id] += 1
    findings = []
    for order in orders:
        order_id = order.get("order_id", "").strip()
        status = order.get("status", "").strip().lower()
        related = by_order.get(order_id, [])
        if not related:
            findings.append({"severity":"HIGH","issue":"MISSING_PAYMENT","order_id":order_id,"payment_ids":"","details":"Order exists but no payment record was found.","recommended_action":"Check payment initiation and provider transaction history."})
            continue
        succeeded = [p for p in related if p.get("status","").strip().lower()=="succeeded"]
        failed = [p for p in related if p.get("status","").strip().lower()=="failed"]
        pending = [p for p in related if p.get("status","").strip().lower() in {"pending","processing"}]
        payment_ids = ",".join(p.get("payment_id","") for p in related)
        if len(related)>1:
            findings.append({"severity":"HIGH","issue":"MULTIPLE_PAYMENTS_FOR_ORDER","order_id":order_id,"payment_ids":payment_ids,"details":f"{len(related)} payment records are linked to this order.","recommended_action":"Verify transaction history and idempotency before any replay or refund."})
        duplicates = sorted({p.get("provider_payment_id","").strip() for p in related if p.get("provider_payment_id","").strip() and provider_counts[p.get("provider_payment_id","").strip()]>1})
        if duplicates:
            findings.append({"severity":"HIGH","issue":"DUPLICATE_PROVIDER_PAYMENT_ID","order_id":order_id,"payment_ids":payment_ids,"details":"Repeated provider ID(s): "+", ".join(duplicates),"recommended_action":"Confirm duplicate delivery/records and check idempotency handling."})
        if succeeded and status!="paid":
            findings.append({"severity":"HIGH","issue":"PAYMENT_ORDER_STATUS_MISMATCH","order_id":order_id,"payment_ids":payment_ids,"details":"Payment succeeded but order status is not paid.","recommended_action":"Validate provider payment, then investigate webhook processing and reconcile safely."})
        if failed:
            findings.append({"severity":"MEDIUM","issue":"FAILED_PAYMENT","order_id":order_id,"payment_ids":payment_ids,"details":f"{len(failed)} failed payment record(s).","recommended_action":"Review provider error details and confirm retry policy."})
        if pending:
            findings.append({"severity":"MEDIUM","issue":"PENDING_PAYMENT","order_id":order_id,"payment_ids":payment_ids,"details":f"{len(pending)} pending/processing payment record(s).","recommended_action":"Check provider status and timeout/reconciliation policy."})
    return findings

def write_csv_report(findings: list[dict[str,str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns=["severity","issue","order_id","payment_ids","details","recommended_action"]
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=columns)
        writer.writeheader()
        writer.writerows(findings)

def write_html_report(findings: list[dict[str,str]], path: Path, orders_checked: int) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    severity=Counter(item["severity"] for item in findings)
    issue_counts=Counter(item["issue"] for item in findings)
    rows=[]
    for item in findings:
        cells="".join("<td>"+escape(item.get(key,""))+"</td>" for key in ["severity","issue","order_id","payment_ids","details","recommended_action"])
        rows.append('<tr data-severity="'+escape(item["severity"])+'">'+cells+"</tr>")
    rows_html="".join(rows) or '<tr><td colspan="6" class="empty">No findings. Data appears consistent.</td></tr>'
    breakdown="".join('<span class="pill">'+escape(issue)+' <b>'+str(count)+'</b></span>' for issue,count in sorted(issue_counts.items())) or '<p>No issues detected.</p>'
    template="""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Payment Reconciliation Report</title><style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#121d2e;--line:#26364c;--text:#e8eef7;--muted:#91a3ba;--accent:#73b7ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:32px 20px}
h1{margin:0;font-size:clamp(24px,4vw,34px)}.muted{color:var(--muted)}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:20px 0}
.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}.card span{display:block;color:var(--muted);font-size:13px}.card strong{font-size:28px}
.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:18px 0}select{background:var(--panel);color:var(--text);border:1px solid var(--line);padding:10px;border-radius:8px}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:12px}table{border-collapse:collapse;width:100%;min-width:920px;background:var(--panel)}
th,td{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.04em}td{font-size:13px}
tr[data-severity="HIGH"] td:first-child{color:#ff8585;font-weight:bold}tr[data-severity="MEDIUM"] td:first-child{color:#ffd27d;font-weight:bold}
.pill{display:inline-flex;gap:8px;background:#1a2a40;border:1px solid var(--line);padding:8px 12px;border-radius:999px;margin:5px}.empty{color:var(--muted);padding:18px}footer{color:var(--muted);font-size:12px;margin-top:20px}
@media(max-width:600px){main{padding:20px 12px}.card{padding:14px}}</style></head><body><main>
<h1>Payment Reconciliation</h1><p class="muted">Automated orders vs. payment records · Synthetic portfolio dataset</p>
<section class="cards"><div class="card"><span>Orders checked</span><strong>__ORDERS__</strong></div><div class="card"><span>Affected orders</span><strong>__AFFECTED__</strong></div><div class="card"><span>Total findings</span><strong>__TOTAL__</strong></div><div class="card"><span>High severity</span><strong>__HIGH__</strong></div><div class="card"><span>Medium severity</span><strong>__MEDIUM__</strong></div><div class="card"><span>Issue types</span><strong>__TYPES__</strong></div></section>
<section class="panel"><h2>Issue breakdown</h2>__BREAKDOWN__</section>
<div class="toolbar"><label for="filter">Filter severity:</label><select id="filter"><option value="ALL">All findings</option><option value="HIGH">High</option><option value="MEDIUM">Medium</option><option value="LOW">Low</option></select><span id="visible" class="muted"></span></div>
<div class="table-wrap"><table><thead><tr><th>Severity</th><th>Issue</th><th>Order ID</th><th>Payment IDs</th><th>Details</th><th>Recommended action</th></tr></thead><tbody id="findings">__ROWS__</tbody></table></div>
<footer>Generated automatically. Read-only report. Validate findings with the payment provider before action. All records are fictional.</footer></main>
<script>const filter=document.getElementById('filter'),rows=[...document.querySelectorAll('#findings tr[data-severity]')],visible=document.getElementById('visible');function update(){let n=0;rows.forEach(row=>{const match=filter.value==='ALL'||row.dataset.severity===filter.value;row.hidden=!match;if(match)n++});visible.textContent=n+' row(s) shown'}filter.addEventListener('change',update);update();</script></body></html>"""
    replacements={"__ORDERS__":str(orders_checked),"__AFFECTED__":str(len({item.get("order_id","") for item in findings if item.get("order_id")})),"__TOTAL__":str(len(findings)),"__HIGH__":str(severity.get("HIGH",0)),"__MEDIUM__":str(severity.get("MEDIUM",0)),"__TYPES__":str(len(issue_counts)),"__BREAKDOWN__":breakdown,"__ROWS__":rows_html}
    for marker,value in replacements.items():
        template=template.replace(marker,value)
    path.write_text(template,encoding="utf-8")

def main() -> int:
    parser=argparse.ArgumentParser(description="Reconcile order and payment CSV exports.")
    parser.add_argument("--orders",type=Path,default=DEFAULT_ORDERS,help="Orders CSV input")
    parser.add_argument("--payments",type=Path,default=DEFAULT_PAYMENTS,help="Payments CSV input")
    parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT,help="Findings CSV output")
    parser.add_argument("--html",type=Path,default=DEFAULT_HTML,help="HTML dashboard output")
    args=parser.parse_args()
    orders=read_csv(args.orders)
    payments=read_csv(args.payments)
    findings=reconcile(orders,payments)
    write_csv_report(findings,args.output)
    write_html_report(findings,args.html,len(orders))
    counts=Counter(item["issue"] for item in findings)
    print(f"Orders checked: {len(orders)}")
    print(f"Findings: {len(findings)}")
    for issue,count in sorted(counts.items()):
        print(f"  {issue}: {count}")
    print(f"CSV report written to: {args.output}")
    print(f"HTML report written to: {args.html}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
