# Linux Support Incident Playbooks

All exercises use fictional services and generated evidence. A log signature is a diagnostic lead, not proof of root cause.

## 1. systemd service fails to start

```bash
systemctl status api.service --no-pager
journalctl -u api.service --since "30 minutes ago" --no-pager
systemctl show api.service -p ExecStart -p User -p WorkingDirectory -p Restart
```
Check the first fatal error, environment/configuration, missing files, permissions, port collision and dependency order. Correct the proven issue, restart the service and verify with `systemctl is-active`, a health endpoint and a representative request.

## 2. Disk or inode exhaustion

```bash
df -h
df -i
du -xhd1 /var 2>/dev/null | sort -h
lsof +L1
journalctl --disk-usage
```
Check capacity and inodes separately, large logs, temporary files and deleted files still held open. Preserve required evidence; use approved log rotation or cleanup. Never blindly delete database files. Verify free space, inode availability and a harmless write.

## 3. Nginx 502 — upstream unavailable

```bash
nginx -t
systemctl status nginx api.service --no-pager
ss -lntp
curl -sv http://127.0.0.1:8000/health
journalctl -u api.service -n 100 --no-pager
```
Check process, bind address, port, container health and configured upstream URL. Restore the upstream; reload Nginx only after `nginx -t` succeeds. Verify direct upstream first, then the proxied route.

## 4. Nginx 504 — upstream timeout

```bash
curl -w '
connect=%{time_connect} total=%{time_total}
' -o /dev/null -sS http://127.0.0.1:8000/slow
journalctl -u api.service --since "15 minutes ago"
ss -tanp
```
Inspect upstream latency, worker saturation, slow DB queries and dependency queue depth. Fix the slow dependency; increase proxy timeouts only when the longer response is expected and safe. Compare latency before and after.

## 5. DNS resolution failure

```bash
getent hosts payments.internal
resolvectl status
cat /etc/resolv.conf
dig payments.internal
```
Check resolver availability, search domains, recent DNS changes and whether one host or all hosts are affected. Correct resolver/authoritative records through the approved change path; avoid a permanent hardcoded IP workaround. Verify name lookup, TCP and application connectivity.

## 6. Expired TLS certificate

```bash
openssl s_client -connect example.internal:443 -servername example.internal </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
systemctl status certbot.timer --no-pager
journalctl -u certbot.service --since "7 days ago"
```
Check virtual host, SNI, chain, renewal timer and ACME challenge. Renew using approved automation, validate config before reload, then verify notAfter and the full chain from a client.

## 7. OOM kill / memory pressure

```bash
free -h
vmstat 1 5
ps aux --sort=-%mem | head
journalctl -k --since "1 hour ago" | grep -Ei 'oom|killed process|out of memory'
systemctl show api.service -p MemoryCurrent -p MemoryMax
```
Distinguish host memory from cgroup limits. Inspect memory trends, worker count, request bursts and recent deployments. Stabilize workload and adjust limits only from evidence. Verify memory trend and restart count.

## 8. PostgreSQL connection pool exhaustion

```sql
SELECT state, count(*) FROM pg_stat_activity GROUP BY state ORDER BY state;
SELECT pid, usename, application_name, state, wait_event_type, query_start
FROM pg_stat_activity ORDER BY query_start NULLS LAST;
SHOW max_connections;
```
Inspect leaked sessions, long transactions, idle-in-transaction sessions and pool size multiplied by worker count. Terminate only verified abandoned sessions with approval. Verify active sessions stabilize and a read/write transaction succeeds.

## 9. Permission denied

```bash
namei -l /srv/app/config/runtime.yml
stat /srv/app/config/runtime.yml
id api-user
getfacl /srv/app/config/runtime.yml
```
Check ownership, parent directory execute bit, ACLs, service account and SELinux/AppArmor. Apply the narrowest correction. Avoid `chmod -R 777`. Verify access as the service user.

## 10. Port conflict / connection refused

```bash
ss -lntup
systemctl status api.service --no-pager
systemctl cat api.service
curl -sv http://127.0.0.1:8000/health
```
Check listener, bind address, container port mapping, firewall and process crash. Resolve the intended listener conflict; do not kill an unknown process. Verify the expected listener and full upstream request.

## Escalation checklist

Include exact timestamps and timezone, affected users/endpoints, measured business impact, host/service/environment identifiers, commands and relevant output, correlation IDs, recent changes, actions taken, current workaround, recovery state and remaining risk. Redact secrets and customer data.
