# QA Case: Checkout & Cart Regression

> Fictional e-commerce application. All requirements, test results, and defects in this case are authored simulations; they are not claims about testing a real production system.

## Context
A storefront is releasing changes to cart totals, promo codes, delivery selection, and checkout validation. The QA objective is to protect the order path and prevent incorrect totals or duplicate orders.

## Scope
**In scope:** cart add/remove/update, quantity boundaries, subtotal/discount/shipping calculation, promo-code validation, delivery option, required checkout fields, order confirmation, repeated submission.
**Out of scope:** payment-provider certification, real inventory, email delivery, load testing.

## Risk-based priorities
- **P0:** order amount is incorrect or duplicate orders can be created.
- **P1:** checkout is blocked for valid customers or discounts/shipping are wrong.
- **P2:** validation messages, layout, and low-impact usability defects.

## Deliverables
- [Test plan](test-plan.md)
- [Test cases](test-cases.md)
- [Exploratory charter](exploratory-charter.md)
- [Simulated defect reports](bug-reports.md)

## Approach
1. Review requirements and identify calculation/transaction risks.
2. Execute happy-path and negative checks across cart and checkout.
3. Explore quantity, promo-code, and submit-button state transitions.
4. Record defects with reproducible steps, expected/actual, severity, and evidence placeholder.
5. Regression focus: total calculation and duplicate order prevention.

## Exit criteria (proposed)
- All P0 tests pass.
- No open P1 defects.
- P2 issues documented and accepted by product owner.
- Order totals are consistent across cart and checkout.

## Test data
| Item | Price | Stock (simulated) |
|---|---:|---:|
| Basic | 100.00 | 10 |
| Premium | 250.00 | 3 |
| Gift item | 25.00 | 0 |

Promo examples: `SAVE10` (10% off eligible subtotal), `EXPIRED` (expired), `INVALID` (unknown code). Currency is fictional test currency (CU).
