# UCI Online Retail — generated findings

> Dataset: [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online-retail) · DOI: https://doi.org/10.24432/C5BW33 · License: CC BY 4.0.
> The figures below are computed from the source workbook by this repository's reproducible pipeline.

## Dataset coverage

- Source rows: 541,909
- Transaction period: 2010-12-01 to 2011-12-09
- Countries represented in valid positive sales: 38
- Distinct products represented in valid positive sales: 3,922
- Valid positive sales lines: 530,104
- Refund / cancellation lines: 9,288
- Invalid or excluded rows under the documented cleaning rules: 2,517

## Headline sales and customer metrics

- Gross sales: £10,666,684.54
- Refunds / cancellations: £896,812.49 (8.41% of gross sales)
- Net sales: £9,769,872.05
- Distinct invoices among positive sale lines: 19,960
- Identified customers: 4,338
- Repeat customers: 2,845 (65.58% of identified customers)
- Positive sales lines without CustomerID: 132,220

## Time and geography

- Highest-gross-sales month: 2011-11 (£1,509,496.33)
- Highest-gross-sales country: United Kingdom (£9,025,222.08; 84.61% of gross sales)

## RFM segment counts

- Needs attention: 1,597 customers
- Loyal customers: 949 customers
- Promising: 731 customers
- At risk: 565 customers
- Champions: 496 customers

## Cohort analysis

- First-purchase cohorts represented: 13
- Weighted month-1 retention across cohorts with a full follow-up month: 22.50%

## Interpretation and limitations

- The dataset is historical (2010–2011) and is not a current market benchmark.
- Sales rows without CustomerID remain in sales totals but are excluded from customer-level and cohort calculations.
- RFM uses relative quartiles over the observation window; segments are descriptive, not churn probabilities.
- Refunds and cancellations are aggregated as absolute line amounts. The report does not attempt to match every return to its original sale line.
- The dataset is observational; it does not establish why customers purchased or stopped purchasing or prove marketing impact.
- Country and product rankings reflect gross positive invoice lines, before refunds.

## SQL cross-check
- SQL gross sales: £10,666,684.54 (reconciled against the pandas calculation).
- SQL repeat-customer rate: 65.58% (reconciled against the pandas calculation).
- SQLite CTEs independently calculate monthly sales, country contribution, repeat purchases, RFM segments and cohort retention.
- SQL RFM scoring uses NTILE(4) window functions; ties can be split across quartiles, so its segment allocation may differ slightly from pandas rank-based quartiles.

## Reproduction

```bash
python scripts/download_data.py
python scripts/build_public_report.py
pytest
```

## Attribution

Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed under CC BY 4.0.
