"""Classify common Linux and web-service log patterns for the support lab.

This utility uses only the Python standard library. Findings are diagnostic
leads, not proof of root cause; correlate timestamps and verify each hypothesis.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    title: str
    pattern: re.Pattern[str]
    recommendation: str


def _rule(rule_id: str, severity: str, title: str, pattern: str, recommendation: str) -> Rule:
    return Rule(rule_id, severity, title, re.compile(pattern, re.IGNORECASE), recommendation)


RULES: tuple[Rule, ...] = (
    _rule("SYSTEMD_UNIT_FAILED", "CRITICAL", "systemd unit failed",
          r"(failed to start|main process exited|entered failed state)",
          "systemctl status <unit>; journalctl -u <unit> -n 100 --no-pager; inspect the first failure, not only restart messages"),
    _rule("DISK_SPACE", "CRITICAL", "disk space or quota exhausted",
          r"(no space left on device|disk quota exceeded|filesystem.{0,30}100%\s*$)",
          "df -h; df -i; du -xhd1 /var; inspect log rotation and deleted-but-open files before removing data"),
    _rule("OOM_KILL", "CRITICAL", "kernel OOM killer terminated a process",
          r"(out of memory|oom-kill|killed process\s+\d+)",
          "journalctl -k; free -h; inspect memory limits and process RSS; correlate restart time and workload"),
    _rule("TLS_EXPIRED", "HIGH", "TLS certificate appears expired",
          r"(certificate has expired|certificate.{0,40}expired)",
          "openssl s_client -connect <host>:443 -servername <host>; inspect certificate dates and renewal logs"),
    _rule("DB_POOL_EXHAUSTED", "HIGH", "database connection capacity exhausted",
          r"(too many connections|remaining connection slots are reserved|pool.{0,40}(exhausted|timeout|limit))",
          "inspect active DB sessions, pool size, connection leaks and query duration; avoid increasing limits without capacity checks"),
    _rule("NGINX_UPSTREAM_TIMEOUT", "HIGH", "Nginx upstream timed out",
          r"(upstream timed out|gateway timeout)",
          "inspect upstream latency and saturation; curl the upstream directly; compare proxy timeouts with application logs"),
    _rule("NGINX_UPSTREAM_REFUSED", "HIGH", "Nginx could not connect to its upstream",
          r"(connect\(\) failed \(111: connection refused\)|upstream prematurely closed connection)",
          "systemctl status <upstream>; ss -lntp; verify upstream host, port, readiness and recent restarts"),
    _rule("DNS_FAILURE", "HIGH", "DNS or hostname resolution failed",
          r"(temporary failure in name resolution|name or service not known|could not resolve host)",
          "getent hosts <hostname>; dig <hostname>; check resolver configuration and whether the failure is host-wide or dependency-specific"),
    _rule("PERMISSION_DENIED", "MEDIUM", "filesystem permission or ownership issue",
          r"(permission denied|operation not permitted)",
          "namei -l <path>; stat <path>; inspect service user, parent-directory execute bits and SELinux/AppArmor denials"),
    _rule("CONNECTION_REFUSED", "MEDIUM", "TCP connection was refused",
          r"(econnrefused|connection refused)",
          "ss -lntp; check the target process, bind address, port, firewall rules and dependency health"),
)

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def analyze_lines(lines: Iterable[str], source: str = "<input>") -> list[dict[str, object]]:
    """Return one highest-priority matching finding per log line."""
    findings: list[dict[str, object]] = []
    for line_number, raw_line in enumerate(lines, start=1):
        message = raw_line.rstrip("\r\n")
        for rule in RULES:
            if rule.pattern.search(message):
                findings.append({
                    "source": source,
                    "line_number": line_number,
                    "rule_id": rule.rule_id,
                    "severity": rule.severity,
                    "title": rule.title,
                    "message": message.strip(),
                    "recommendation": rule.recommendation,
                })
                break
    findings.sort(key=lambda item: (
        SEVERITY_ORDER[str(item["severity"])],
        str(item["source"]),
        int(item["line_number"]),
    ))
    return findings


def analyze_file(path: Path) -> list[dict[str, object]]:
    """Analyze a UTF-8 log file, replacing undecodable bytes safely."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return analyze_lines(handle, source=str(path))


def render_text(findings: Sequence[dict[str, object]]) -> str:
    if not findings:
        return "No known patterns found. This does not prove the system is healthy."
    output: list[str] = []
    for item in findings:
        output.extend([
            f"[{item['severity']}] {item['rule_id']} — {item['title']}",
            f"  evidence: {item['source']}:{item['line_number']}",
            f"  message: {item['message']}",
            f"  next: {item['recommendation']}",
            "",
        ])
    return "\n".join(output).rstrip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Classify common Linux, Nginx and database log patterns."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="one or more UTF-8 log files")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--min-severity",
        choices=("CRITICAL", "HIGH", "MEDIUM", "LOW"),
        default="LOW",
        help="hide findings below this severity",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    findings: list[dict[str, object]] = []
    failures: list[str] = []

    for path in args.paths:
        if not path.is_file():
            failures.append(f"{path}: file not found")
            continue
        try:
            findings.extend(analyze_file(path))
        except OSError as exc:
            failures.append(f"{path}: {exc}")

    threshold = SEVERITY_ORDER[args.min_severity]
    findings = [
        item for item in findings
        if SEVERITY_ORDER[str(item["severity"])] <= threshold
    ]
    findings.sort(key=lambda item: (
        SEVERITY_ORDER[str(item["severity"])],
        str(item["source"]),
        int(item["line_number"]),
    ))

    if args.format == "json":
        print(json.dumps(
            {"findings": findings, "errors": failures, "finding_count": len(findings)},
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print(render_text(findings))
        if failures:
            print("\nInput errors:")
            print("\n".join(f"- {failure}" for failure in failures))

    return 2 if failures else 0


if __name__ == "__main__":
    sys.exit(main())