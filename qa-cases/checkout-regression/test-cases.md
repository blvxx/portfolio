# Checkout Test Cases

Statuses: **Not Run**. Test cases are designed for a fictional application; no execution is claimed.

| ID | Priority | Preconditions / data | Steps | Expected result |
|---|---|---|---|---|
| CART-001 | P1 | Product in stock | Add Basic item | Cart shows item, price and quantity 1 |
| CART-002 | P1 | Product in stock | Increase quantity to 2 | Quantity and subtotal update |
| CART-003 | P1 | Cart has 2 items | Remove one item | Removed item disappears; total recalculates |
| CART-004 | P1 | Quantity 1 | Decrease quantity | Quantity cannot become 0; removal is explicit |
| CART-005 | P1 | Stock 3 | Set quantity to 4 | Clear stock-limit feedback; invalid quantity not accepted |
| CART-006 | P1 | Zero-stock Gift item | Attempt to add | Add action disabled or clear unavailable message |
| CART-007 | P1 | Two different items | Change quantities | Subtotal equals sum of line totals |
| PROMO-001 | P1 | Eligible subtotal; SAVE10 | Apply promo | Discount equals 10% of eligible subtotal |
| PROMO-002 | P1 | EXPIRED | Apply promo | Promo rejected with clear reason; total unchanged |
| PROMO-003 | P1 | INVALID | Apply promo | Invalid-code feedback; no discount |
| PROMO-004 | P2 | SAVE10 applied | Remove eligible item | Discount recalculates from remaining eligible items |
| PROMO-005 | P1 | SAVE10 applied | Apply code a second time | No duplicate discount |
| SHIP-001 | P1 | Cart has items | Select delivery method | Shipping charge and final total update |
| SHIP-002 | P1 | Cart has items | Switch delivery method twice | Only selected method's fee is included |
| CHECK-001 | P0 | Valid cart and customer data | Submit order once | One order created; confirmation displayed |
| CHECK-002 | P0 | Valid cart | Double-click submit | At most one order is created |
| CHECK-003 | P1 | Missing email | Submit checkout | Inline validation; order not created |
| CHECK-004 | P1 | Invalid email format | Submit checkout | Email validation feedback; order not created |
| CHECK-005 | P1 | Missing address for delivery | Submit checkout | Address required; order not created |
| CHECK-006 | P1 | Valid data | Refresh confirmation page | No second order created |
| CHECK-007 | P1 | Valid data | Back to cart after submit | Order state remains consistent; no stale cart duplication |
| UX-001 | P2 | Checkout form | Navigate with keyboard only | Controls reachable; focus visible and logical |
| UX-002 | P2 | Mobile viewport | Complete cart review | No horizontal overflow; key actions visible |
