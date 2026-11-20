# Data dictionary

All records are synthetic and created for demonstration. Monetary values are arbitrary synthetic units and do not represent a real currency.

| Column | Type | Description | Validation |
|---|---|---|---|
| order_id | text | Unique order identifier | Not null, unique |
| order_date | date | Date the order was placed | Valid date |
| customer_id | text | Synthetic customer identifier | Not null |
| region | text | Customer delivery region | Not null |
| channel | text | Order acquisition channel | Not null |
| category | text | Product category | Not null |
| product | text | Product name | Not null |
| quantity | integer | Number of units in the order | Greater than 0 |
| unit_price | numeric | Unit price before discount, in synthetic monetary units | Greater than 0 |
| discount_pct | numeric | Discount fraction (0.15 = 15%) | Between 0 and 1 |
| payment_status | text | Payment/order state | paid, cancelled or pending |
| delivery_days | integer | Delivery duration for paid orders | Positive for paid; blank otherwise |
| is_returned | boolean | Whether the order was returned | true / false |

## Metric rules

- Gross merchandise value before discounts: `quantity × unit_price`.
- Net line value after discount: `quantity × unit_price × (1 − discount_pct)`.
- Recognised revenue in this case study: net line value when `payment_status = 'paid'` and `is_returned = false`; zero otherwise.
- A paid but returned order remains in paid-order counts and is included in the return-rate denominator, but contributes zero recognised revenue.
- Average order value uses completed orders (paid and not returned) as its denominator.
- Repeat customer means at least two records in the dataset, regardless of payment status. For production reporting, this definition may need to be restricted to paid orders.
