-- PostgreSQL schema for the synthetic e-commerce dataset.
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id       TEXT PRIMARY KEY,
    order_date     DATE NOT NULL,
    customer_id    TEXT NOT NULL,
    region         TEXT NOT NULL,
    channel        TEXT NOT NULL,
    category       TEXT NOT NULL,
    product        TEXT NOT NULL,
    quantity       INTEGER NOT NULL CHECK (quantity > 0),
    unit_price     NUMERIC(12, 2) NOT NULL CHECK (unit_price > 0),
    discount_pct   NUMERIC(5, 4) NOT NULL CHECK (discount_pct BETWEEN 0 AND 1),
    payment_status TEXT NOT NULL CHECK (payment_status IN ('paid', 'cancelled', 'pending')),
    delivery_days  INTEGER,
    is_returned    BOOLEAN NOT NULL DEFAULT FALSE
);
