import os
import uuid

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.main import Base, Payment, PaymentStatus

DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="Set TEST_DATABASE_URL to run PostgreSQL integration checks",
)


def test_postgres_can_create_and_read_payment():
    engine = create_engine(DATABASE_URL)
    try:
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        reference = f"PG-{uuid.uuid4().hex[:12]}"
        with Session.begin() as session:
            payment = Payment(
                customer_reference=reference,
                amount_minor=12500,
                currency="RUB",
                status=PaymentStatus.pending.value,
            )
            session.add(payment)
            session.flush()
            payment_id = payment.id

        with Session() as session:
            saved = session.scalar(select(Payment).where(Payment.id == payment_id))
            assert saved is not None
            assert saved.customer_reference == reference
            assert saved.amount_minor == 12500
            assert saved.status == PaymentStatus.pending.value
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
