# Test Plan — Checkout & Cart Regression

## Objective
Validate that cart operations, pricing, discounts, shipping, and checkout submission preserve correct business rules.

## Environment
Simulated responsive web storefront; desktop and mobile viewport checks; fresh test account; isolated test data. No live payment processing.

## Test strategy
- Functional: cart and checkout workflow.
- Negative: invalid quantity, missing fields, invalid/expired promo.
- Boundary: quantity 1, maximum allowed, stock boundary, zero-stock item.
- Regression: totals after each cart mutation and repeated submission.
- UX: error placement, keyboard focus, clear feedback.

## Risks and mitigations
| Risk | Test focus |
|---|---|
| Incorrect final price | Recalculate subtotal, discount, shipping at each state |
| Duplicate order | Double-click and retry after delayed response |
| Inventory oversell | Quantity beyond stock and zero-stock product |
| Discount abuse | Expired, invalid, stacking and removed-item scenarios |
| Form bypass | Required-field validation and invalid formats |

## Execution status
This is a designed QA pack, not execution against a real application. Statuses are intentionally **Not Run** until a target build is available.
