# Analysis findings

## Scope and transparency

This report summarises the fixed synthetic dataset in `data/orders.csv` (360 generated orders, January–December 2025). All values are calculated from the dataset using the metric rules documented in the project README. Monetary amounts are arbitrary synthetic units, not rubles or another real currency.

These results demonstrate an analysis workflow. They are not evidence about a real company, market or customer population.

## KPI snapshot

| KPI | Result |
|---|---:|
| Total orders | 360 |
| Paid orders | 257 (71.4%) |
| Completed orders (paid, not returned) | 244 |
| Cancelled orders | 51 (14.2%) |
| Pending orders | 52 (14.4%) |
| Returned paid orders | 13 |
| Recognised revenue | 5,626,785.20 |
| Average order value | 23,060.60 |
| Return rate among paid orders | 5.06% |
| Distinct customers | 120 |
| Repeat customers | 30 |
| Repeat customer rate | 25.0% |

## Segment observations

### Regions

| Region | Orders | Recognised revenue |
|---|---:|---:|
| Novosibirsk | 72 | 1,206,322.40 |
| Kazan | 72 | 1,157,624.60 |
| Moscow | 72 | 1,142,699.20 |
| Saint Petersburg | 72 | 1,062,248.00 |
| Yekaterinburg | 72 | 1,057,891.00 |

The synthetic dataset assigns exactly 72 orders to each region. Therefore, this ranking reflects differences in generated order values and status mix, not differences in regional demand or market size.

### Product categories

| Category | Orders | Recognised revenue |
|---|---:|---:|
| Electronics | 103 | 1,950,222.20 |
| Home | 103 | 1,691,219.70 |
| Sports | 103 | 1,380,323.20 |
| Beauty | 51 | 605,020.10 |

Electronics generates the largest recognised revenue in this sample. Beauty has fewer orders, so revenue alone is not enough to conclude that its products perform worse; unit economics, price bands and product mix would be needed.

### Acquisition channels

| Channel | Orders | Recognised revenue |
|---|---:|---:|
| web | 138 | 2,151,297.70 |
| marketplace | 111 | 1,908,265.30 |
| mobile | 111 | 1,567,222.20 |

Web has the highest order count and revenue in the generated sample. Without sessions, conversion, advertising spend and acquisition costs, this cannot be interpreted as the most efficient channel.

## Monthly pattern

- Highest recognised revenue: **November 2025 — 524,300.30**.
- Lowest recognised revenue: **July 2025 — 399,865.30**.

The dataset contains exactly 30 orders per month by construction. The monthly comparison therefore demonstrates revenue aggregation but does not establish real seasonality or changes in demand.

## Follow-up questions a real analyst would investigate

1. What are the return reasons and product-level return rates in Kazan and Moscow?
2. Does the higher web revenue remain attractive after traffic costs and conversion rates are included?
3. Is the lower Beauty revenue explained by fewer orders, lower prices, discounts or product mix?
4. What proportion of repeat customers make a second paid purchase, and how long does it take?

## Limitations

- The data is generated, not collected from a real business.
- The distribution is deliberately structured for repeatable demonstrations.
- There are no sessions, marketing costs, profit margins, refund amounts or return reasons.
- Correlation and causation cannot be inferred from this sample.
