CREATE TABLE agents (
    agent_id INTEGER PRIMARY KEY,
    agent_name TEXT NOT NULL,
    team TEXT NOT NULL
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    agent_id INTEGER REFERENCES agents(agent_id),
    created_at TIMESTAMPTZ NOT NULL,
    first_response_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    priority TEXT NOT NULL CHECK (priority IN ('P1','P2','P3','P4')),
    channel TEXT NOT NULL CHECK (channel IN ('email','chat','web')),
    category TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open','pending','resolved')),
    reopened_count INTEGER NOT NULL DEFAULT 0 CHECK (reopened_count >= 0)
);
CREATE INDEX idx_tickets_created ON tickets(created_at);
CREATE INDEX idx_tickets_priority_status ON tickets(priority,status);
CREATE INDEX idx_tickets_agent_created ON tickets(agent_id,created_at);
