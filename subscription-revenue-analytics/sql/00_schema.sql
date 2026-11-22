-- PostgreSQL 16 schema for the synthetic subscription analytics case.
CREATE TABLE IF NOT EXISTS bi_customers (
 customer_id INTEGER PRIMARY KEY,
 signup_date DATE NOT NULL,
 acquisition_channel TEXT NOT NULL CHECK (acquisition_channel IN ('organic','paid','referral','partner')),
 region TEXT NOT NULL CHECK (region IN ('UK','DACH','West','South'))
);
CREATE TABLE IF NOT EXISTS bi_plans (
 plan_id SMALLINT PRIMARY KEY,
 plan_name TEXT NOT NULL UNIQUE,
 monthly_price NUMERIC(12,2) NOT NULL CHECK (monthly_price > 0)
);
CREATE TABLE IF NOT EXISTS bi_subscription_events (
 event_id BIGSERIAL PRIMARY KEY,
 subscription_id INTEGER NOT NULL,
 customer_id INTEGER NOT NULL REFERENCES bi_customers(customer_id),
 event_type TEXT NOT NULL CHECK (event_type IN ('activated','upgraded','downgraded','cancelled')),
 event_at TIMESTAMPTZ NOT NULL,
 plan_id SMALLINT NOT NULL REFERENCES bi_plans(plan_id),
 mrr_after NUMERIC(12,2) NOT NULL CHECK (mrr_after >= 0),
 CONSTRAINT uq_subscription_event_time UNIQUE (subscription_id,event_at),
 CONSTRAINT ck_cancelled_mrr CHECK (
  (event_type = 'cancelled' AND mrr_after = 0)
  OR (event_type <> 'cancelled' AND mrr_after > 0)
 )
);
CREATE INDEX IF NOT EXISTS ix_bi_events_subscription_time ON bi_subscription_events(subscription_id,event_at,event_id);
CREATE INDEX IF NOT EXISTS ix_bi_events_event_at ON bi_subscription_events(event_at);
CREATE INDEX IF NOT EXISTS ix_bi_events_customer ON bi_subscription_events(customer_id);
