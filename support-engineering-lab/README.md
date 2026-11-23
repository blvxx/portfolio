# Linux Support Engineering Lab

A reproducible troubleshooting lab for **Technical Support, Application Support L2 and Support Engineering**. The workflow is evidence-first: establish impact, inspect the relevant layer, isolate the fault, apply a safe recovery and verify the result.

> **Scope:** all incidents and log entries are generated examples. This is a practice lab—not a real production incident or client engagement.

## Incident coverage

| Scenario | Initial signal | First checks |
|---|---|---|
| systemd service failure | Service inactive / restart loop | `systemctl status`, `journalctl -u`, unit config |
| Disk or inode pressure | Writes fail / disk full | `df -h`, `df -i`, `du`, deleted-open files |
| Nginx 502 | Bad Gateway | upstream status, listener, direct health check |
| Nginx 504 | Gateway timeout | upstream latency, saturation, DB/dependency wait |
| DNS failure | Hostname cannot resolve | `getent`, `dig`, resolver config |
| TLS certificate | Certificate expired / handshake failure | dates, SNI, chain, renewal logs |
| OOM / memory pressure | Process killed / instability | kernel journal, memory, cgroup limits |
| PostgreSQL pool exhaustion | Connection timeout | active sessions, pool size, long transactions |
| Permission denied | Access failure | `namei`, ownership, ACL, service account |
| Port conflict | Bind failure / refused connection | `ss -lntp`, process, bind address |

Detailed command sequences and recovery/verification notes: **[10 incident playbooks](docs/incident-playbooks.md)**.

## Log triage CLI

A standard-library Python utility scans sample logs, returns severity-ranked findings, preserves source and line number, and suggests the next diagnostic check. It is a heuristic aid—not a root-cause oracle.

### Run it

Python 3.10+; no third-party packages required. Run from the repository root:

```bash
python support-engineering-lab/scripts/log_triage.py \
  support-engineering-lab/sample-logs/system.log \
  support-engineering-lab/sample-logs/nginx-error.log
```

JSON output and tests:

```bash
python support-engineering-lab/scripts/log_triage.py \
  support-engineering-lab/sample-logs/system.log --format json

python -m unittest discover -s support-engineering-lab/tests -v
```

### Example finding

```text
[HIGH] DNS_FAILURE — DNS or hostname resolution failed
  evidence: sample.log:12
  message: Temporary failure in name resolution
  next: getent hosts <hostname>; dig <hostname>; check resolver configuration...
```

The exact output depends on the input log. Findings include a rule ID, severity, source file, line number, matched message and suggested next check.

## Investigation workflow

1. **Scope:** who/what is affected, endpoint, start time, business impact.
2. **Service:** status, restart history, recent journal and deployment/config changes.
3. **Host:** CPU, memory, disk, inodes, processes and file descriptors.
4. **Connectivity:** DNS, route, TCP listener, TLS, proxy and upstream.
5. **Dependencies:** database, connection pools, queues and external services.
6. **Evidence:** correlate timestamps/request IDs; test hypotheses rather than assume.
7. **Recovery:** use an approved, minimal change; preserve relevant evidence.
8. **Verification:** service health, representative request, logs and monitoring.
9. **Handover:** impact, timeline, root cause (if confirmed), mitigation, recovery and remaining risk.

## Repository map

- `scripts/log_triage.py` — log-pattern classifier and CLI (text/JSON).
- `sample-logs/` — generated Linux, kernel and Nginx log samples.
- `tests/test_log_triage.py` — rule ordering, evidence, JSON and input-error checks.
- `docs/incident-playbooks.md` — command-level troubleshooting and verification steps.
- `docs/incident-report-template.md` — reusable incident notes/handover.

## Quality checks

GitHub Actions runs unit tests and publishes a JSON triage artifact. The workflow definition is not itself evidence of a passing run; check the linked Actions status for the latest result.

## Skills shown

Linux · systemd · journalctl · Nginx · HTTP · DNS · TCP/IP · TLS · PostgreSQL · Python · log analysis · incident triage · RCA · recovery verification · technical documentation
