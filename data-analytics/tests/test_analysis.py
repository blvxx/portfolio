import pandas as pd
import pytest

from src.analysis import calculate_kpis, prepare_orders, segment_kpis, validate_orders


@pytest.fixture
def sample_orders() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "order_id": "ORD-1", "order_date": "2025-01-05", "customer_id": "C-1",
                "region": "Moscow", "channel": "web", "category": "Electronics",
                "product": "Headphones", "quantity": 2, "unit_price": 100.0,
                "discount_pct": 0.10, "payment_status": "paid",
                "delivery_days": 2, "is_returned": False,
            },
            {
                "order_id": "ORD-2", "order_date": "2025-01-11", "customer_id": "C-1",
                "region": "Kazan", "channel": "mobile", "category": "Home",
                "product": "Lamp", "quantity": 1, "unit_price": 50.0,
                "discount_pct": 0.0, "payment_status": "paid",
                "delivery_days": 3, "is_returned": True,
            },
            {
                "order_id": "ORD-3", "order_date": "2025-02-02", "customer_id": "C-2",
                "region": "Moscow", "channel": "web", "category": "Sports",
                "product": "Mat", "quantity": 1, "unit_price": 80.0,
                "discount_pct": 0.25, "payment_status": "cancelled",
                "delivery_days": None, "is_returned": False,
            },
        ]
    )


def test_recognised_revenue_excludes_cancelled_and_returned_orders(sample_orders):
    prepared = prepare_orders(sample_orders)
    assert prepared["recognised_revenue"].tolist() == pytest.approx([180.0, 0.0, 0.0])


def test_kpis_use_completed_orders_for_average_order_value(sample_orders):
    result = calculate_kpis(sample_orders)
    assert result["total_orders"] == 3
    assert result["paid_orders"] == 2
    assert result["completed_orders"] == 1
    assert result["returned_orders"] == 1
    assert result["recognised_revenue"] == 180.0
    assert result["average_order_value"] == 180.0
    assert result["return_rate"] == 0.5


def test_repeat_customer_rate(sample_orders):
    result = calculate_kpis(sample_orders)
    assert result["unique_customers"] == 2
    assert result["repeat_customers"] == 1
    assert result["repeat_customer_rate"] == 0.5


def test_duplicate_order_id_is_rejected(sample_orders):
    duplicated = pd.concat([sample_orders, sample_orders.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="unique"):
        validate_orders(duplicated)


def test_discount_outside_range_is_rejected(sample_orders):
    invalid = sample_orders.copy()
    invalid.loc[0, "discount_pct"] = 1.2
    with pytest.raises(ValueError, match="between 0 and 1"):
        validate_orders(invalid)


def test_unknown_segment_is_rejected(sample_orders):
    with pytest.raises(ValueError, match="dimension"):
        segment_kpis(sample_orders, "customer_id")
