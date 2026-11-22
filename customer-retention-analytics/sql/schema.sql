PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sales (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity REAL NOT NULL,
    invoice_date TEXT NOT NULL,
    unit_price REAL NOT NULL,
    customer_id TEXT,
    country TEXT NOT NULL,
    revenue REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS refunds (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity REAL NOT NULL,
    invoice_date TEXT NOT NULL,
    unit_price REAL NOT NULL,
    customer_id TEXT,
    country TEXT NOT NULL,
    refund_amount REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sales_customer_date
    ON sales(customer_id, invoice_date);

CREATE INDEX IF NOT EXISTS idx_sales_month_country
    ON sales(invoice_date, country);

CREATE INDEX IF NOT EXISTS idx_refunds_customer
    ON refunds(customer_id);
