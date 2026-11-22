from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
}


def clean_transactions(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return valid positive sales and refund/cancellation lines.

    Rows without a customer ID remain in sales KPIs but are naturally excluded
    from customer-level RFM and cohort analysis.
    """
    frame = raw.copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    frame["InvoiceNo"] = frame["InvoiceNo"].astype("string").str.strip()
    frame["StockCode"] = frame["StockCode"].astype("string").str.strip()
    frame["CustomerID"] = (
        frame["CustomerID"]
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )
    frame["CustomerID"] = frame["CustomerID"].mask(
        frame["CustomerID"].isin(["", "<NA>", "nan", "None"])
    )
    frame["Country"] = frame["Country"].astype("string").str.strip().fillna("Unknown")
    frame["Description"] = frame["Description"].astype("string").str.strip().fillna("Unknown product")
    frame["Quantity"] = pd.to_numeric(frame["Quantity"], errors="coerce")
    frame["UnitPrice"] = pd.to_numeric(frame["UnitPrice"], errors="coerce")
    raw_dates = frame["InvoiceDate"].astype("string").str.strip()
    iso_date_mask = raw_dates.str.match(r"^\\d{4}[-/]\\d{1,2}[-/]\\d{1,2}", na=False)
    parsed_dates = pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns]")
    parsed_dates.loc[iso_date_mask] = pd.to_datetime(
        raw_dates.loc[iso_date_mask], errors="coerce", dayfirst=False
    )
    parsed_dates.loc[~iso_date_mask] = pd.to_datetime(
        raw_dates.loc[~iso_date_mask], errors="coerce", dayfirst=True
    )
    frame["InvoiceDate"] = parsed_dates

    invoice = frame["InvoiceNo"].str.upper()
    is_cancelled_invoice = invoice.str.startswith("C", na=False)
    valid = (
        frame["InvoiceNo"].notna()
        & frame["InvoiceNo"].ne("")
        & frame["InvoiceDate"].notna()
        & frame["Quantity"].notna()
        & frame["Quantity"].ne(0)
        & frame["UnitPrice"].notna()
        & frame["UnitPrice"].gt(0)
    )
    frame = frame.loc[valid].copy()
    is_cancelled_invoice = is_cancelled_invoice.loc[valid]
    frame["LineAmount"] = frame["Quantity"] * frame["UnitPrice"]

    sales_mask = frame["Quantity"].gt(0) & ~is_cancelled_invoice
    refund_mask = frame["Quantity"].lt(0) | is_cancelled_invoice

    sales = frame.loc[sales_mask].copy()
    sales["Revenue"] = sales["LineAmount"].astype(float)

    refunds = frame.loc[refund_mask].copy()
    refunds["RefundAmount"] = refunds["LineAmount"].abs().astype(float)

    return sales.reset_index(drop=True), refunds.reset_index(drop=True)
