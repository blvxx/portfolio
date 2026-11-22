# Analysis brief

## Business questions

1. How do gross sales, refunds and net sales move over time?
2. Which countries and products contribute the most revenue?
3. How many identified customers place more than one invoice?
4. How does observed purchasing activity change after a customer's first purchase?
5. Which customers fall into relative RFM groups that may warrant different communication strategies?

## Metric definitions

| Metric | Definition |
|---|---|
| Gross sales | Sum of positive sale-line quantity × unit price, excluding cancellation invoices |
| Refunds / cancellations | Absolute value of negative-quantity and cancellation-line amounts |
| Net sales | Gross sales minus refunds / cancellations |
| Orders | Distinct invoice numbers among positive sale lines |
| Identified customers | Distinct non-null CustomerID among positive sale lines |
| Repeat customer rate | Identified customers with more than one distinct invoice ÷ identified customers |
| RFM recency | Days since the customer's latest positive sale, relative to the day after the last observed sale |
| RFM frequency | Distinct positive-sale invoices per customer |
| RFM monetary | Positive sales less linked refund/cancellation values, floored at zero |
| Cohort retention | Customers in a first-purchase month who also purchased in each elapsed month ÷ customers in that cohort |

## Important interpretation rules

- Revenue is in GBP because UnitPrice is denominated in sterling in the source dataset.
- Rows without CustomerID contribute to sales KPIs but cannot be assigned to an individual customer or cohort.
- RFM scores are relative quartiles inside the chosen observation window. They are descriptive groups, not churn predictions.
- This is historical observational data. It cannot by itself establish the cause of customer behavior or the impact of a marketing intervention.
