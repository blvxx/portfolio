# Support Operations Analytics — SQL Case Study

A SQL-first operational analytics case study for a SaaS support team. The project uses a small **synthetic** dataset to answer questions about ticket volume, SLA performance, backlog, customer impact and agent workload.

## Business questions
- How is ticket volume and backlog changing week over week?
- What share of tickets meets the first-response SLA and resolution SLA?
- Which priority, channel or issue category contributes most to SLA breaches?
- Which agents have the highest workload, and how should workload be interpreted alongside ticket complexity?
- How long do tickets take to resolve across priorities?

## Dataset & assumptions
All included records are fictional and designed for demonstration. Timestamps are ISO-8601 UTC. SLA targets are defined in the SQL as first response within 60 minutes for P1/P2 and 240 minutes for P3/P4; resolution targets are 8, 24, 72 and 120 hours by priority. This is a simplified case—not a real company's policy or performance.

## SQL skills
- Relational schema and constraints
- JOINs, CTEs, conditional aggregation, date truncation
- Window functions (rolling averages, ranking)
- Percentiles and SLA calculations
- Backlog snapshots by day and ticket age buckets
- Data quality checks and metric definitions

## Files
- `sql/schema.sql` — tables and relationships
- `sql/seed.sql` — synthetic ticket and agent records
- `sql/01_weekly_volume_backlog.sql`
- `sql/02_sla_performance.sql`
- `sql/03_agent_workload.sql`
- `sql/04_resolution_time_by_priority.sql`
- `sql/05_backlog_age.sql`
- `sql/06_data_quality.sql`

## Run
Requires PostgreSQL 14+.

```bash
psql -d support_analytics -f sql/schema.sql
psql -d support_analytics -f sql/seed.sql
psql -d support_analytics -f sql/01_weekly_volume_backlog.sql
psql -d support_analytics -f sql/02_sla_performance.sql
```

## Metric definitions
- **First-response SLA met**: first response timestamp minus creation timestamp is within the priority target.
- **Resolution SLA met**: resolved timestamp minus creation timestamp is within priority target.
- **Backlog**: tickets without a resolved timestamp at the snapshot cutoff. Queries use current fixture timestamps; for historical backlog trend reporting, a ticket-event history or daily snapshot table would be required.
- **Agent workload**: assigned tickets and median resolution time; not a productivity score without context for ticket complexity, shift hours and reopened work.

## Limitations
The dataset is intentionally small and synthetic; results must not be presented as real operational benchmarks. SQL assumes timestamps are stored as `timestamptz`. SLA rules are illustrative and are not universal. The project is intended to show analytical reasoning, query design and metric caveats.

