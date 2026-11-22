# Linux Support Engineering Lab

A reproducible Linux operations lab for Application Support L2, Technical Support and Support Engineering. It demonstrates a disciplined workflow: observe symptoms, collect evidence, isolate the failing layer, apply a safe recovery step and verify service health.

> **Lab scope:** all logs and incidents are generated examples. No real infrastructure, customer data or production outage is represented.

## What this lab demonstrates

- Linux service inspection with `systemctl` and `journalctl`.
- Process, memory, disk and filesystem troubleshooting.
- Network and DNS diagnosis with `ss`, `ip`, `curl`, `dig` and `getent`.
- Nginx reverse-proxy and HTTP 502/504 investigation.
- TLS certificate checks and permission troubleshooting.
- PostgreSQL connection exhaustion and application dependency analysis.
- Evidence-based incident notes, recovery checks and escalation.

## Quick start

Requirements: Python 3.10+. The analyzer uses only the Python standard library.

From the repository root:

```bash
python support-engineering-lab/scripts/log_triage.py \
  support-engineering-lab/sample-logs/system.log \
  support-engineering-lab/sample-logs/nginx-error.log
```

Generate JSON and run the unit tests:

```bash
python support-engineering-lab/scripts/log_triage.py support-engineering-lab/sample-logs/system.log --format json
python -m unittest discover -s support-engineering-lab/tests -v
```

## Repository map

- `scripts/log_triage.py` — deterministic log classifier with severity, evidence line and next diagnostic check.
- `sample-logs/` — generated system, kernel and Nginx logs.
- `tests/test_log_triage.py` — unit tests for rule matching, ordering and CLI output.
- [Incident playbooks](docs/incident-playbooks.md) — 10 incident drills.
- [Incident report template](docs/incident-report-template.md) — reusable incident handover.

## Investigation workflow

1. Confirm impact, affected endpoint and start time.
2. Check service state, recent journal entries and restart history.
3. Check disk, inodes, memory, processes and open file descriptors.
4. Check DNS, network path, upstream, database and TLS.
5. Correlate timestamps and request IDs; distinguish symptoms from root cause.
6. Preserve evidence and change one thing at a time.
7. Verify health endpoint, business request, logs and monitoring.
8. Record impact, timeline, mitigation, recovery and remaining risk.

## Practice scenarios

systemd failure · disk/inode exhaustion · Nginx 502 · Nginx 504 · DNS failure · expired TLS · OOM kill · PostgreSQL pool exhaustion · permission denied · port conflict.

## Quality checks

GitHub Actions runs the analyzer unit tests and produces a JSON triage artifact on relevant pushes and pull requests. A configured workflow is not represented as a passing run until GitHub Actions confirms it.

## Skills demonstrated

Linux operations · systemd · journalctl · Nginx · HTTP · DNS · TCP/IP · TLS · Python · log analysis · incident triage · root-cause investigation · recovery verification · technical documentation
