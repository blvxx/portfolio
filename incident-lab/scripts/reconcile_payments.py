#!/usr/bin/env python3
"""Reconcile synthetic order and payment CSV files and write a findings report."""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_ORDERS = Path(__file__).resolve().parents[1] / "data" / "sample_orders.csv"
DEFAULT_PAYMENTS = Path(__file__).resolve().parents[1] / "data" / "sample_payments.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "reports" / "reconciliation_findings.csv"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def reconcile(orders: list[dict[str, str]], payments: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return actionable findings. Duplicate provider IDs are detected globally."""
    by_order: dict[str, list[dict[str, str]]] = defaultdict(list)
    provider_counts = Counter()
    for payment in payments:
        by_order[payment.get("order_id", "")].append(payment)
        provider_id = payment.get("provider_payment_id", "").strip()
        if provider_id:
            provider_counts[provider_id] += 1

    findings: list[dict[str, str]] = []
    for order in orders:
        order_id = order.get("order_id", "").strip()
        status = order.get("status", "").strip().lower()
        related = by_order.get(order_id, [])
        if not related:
            findings.append({"severity": "HIGH", "issue": "MISSING_PAYMENT", "order_id": order_id,
                            "payment_ids": "", "details": "Order exists but no payment record was found.",
                            "recommended_action": "Check payment initiation and provider transaction history."})
            continue

        succeeded = [p for p in related if p.get("status", "").strip().lower() == "succeeded"]
        failed = [p for p in related if p.get("status", "").strip().lower() == "failed"]
        pending = [p for p in related if p.get("status", "").strip().lower() in {"pending", "processing"}]
        payment_ids = ",".join(p.get("payment_id", "") for p in related)

        if len(related) > 1:
            findings.append({"severity": "HIGH", "issue": "MULTIPLE_PAYMENTS_FOR_ORDER", "order_id": order_id,
                            "payment_ids": payment_ids, "details": f"{len(related)} payment records are linked to this order.",
                            "recommended_action": "Verify transaction history and idempotency before any replay or refund."})
        duplicate_providers = sorted({p.get("provider_payment_id", "").strip() for p in related
                                     if p.get("provider_payment_id", "").strip() and provider_counts[p.get("provider_payment_id", "").strip()] > 1})
        if duplicate_providers:
            findings.append({"severity": "HIGH", "issue": "DUPLICATE_PROVIDER_PAYMENT_ID", "order_id": order_id,
                            "payment_ids": payment_ids, "details": "Repeated provider ID(s): " + ", ".join(duplicate_providers),
                            "recommended_action": "Confirm whether duplicate webhook delivery created duplicate records; check idempotency handling."})
        if succeeded and status != "paid":
            findings.append({"severity": "HIGH", "issue": "PAYMENT_ORDER_STATUS_MISMATCH", "order_id": order_id,
                            "payment_ids": payment_ids, "details": "Payment succeeded but order status is not paid.",
                            "recommended_action": "Validate provider payment, then investigate webhook processing and reconcile safely."})
        if failed:
            findings.append({"severity": "MEDIUM", "issue": "FAILED_PAYMENT", "order_id": order_id,
                            "payment_ids": payment_ids, "details": f"{len(failed)} failed payment record(s).",
                            "recommended_action": "Review provider error details and confirm retry policy."})
        if pending:
            findings.append({"severity": "MEDIUM", "issue": "PENDING_PAYMENT", "order_id": order_id,
                            "payment_ids": payment_ids, "details": f"{len(pending)} pending/processing payment record(s).",
                            "recommended_action": "Check provider status and timeout/reconciliation policy."})
    return findings

def write_report(findings: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["severity", "issue", "order_id", "payment_ids", "details", "recommended_action"]
    with output_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(findings)

def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile order and payment CSV exports.")
    parser.add_argument("--orders", type=Path, default=DEFAULT_ORDERS, help="Orders CSV input")
    parser.add_argument("--payments", type=Path, default=DEFAULT_PAYMENTS, help="Payments CSV input")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Findings CSV output")
    args = parser.parse_args()
    findings = reconcile(read_csv(args.orders), read_csv(args.payments))
    write_report(findings, args.output)
    counts = Counter(f["issue"] for f in findings)
    print(f"Orders checked: {len(read_csv(args.orders))}")
    print(f"Findings: {len(findings)}")
    for issue, count in sorted(counts.items()):
        print(f"  {issue}: {count}")
    print(f"Report written to: {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
