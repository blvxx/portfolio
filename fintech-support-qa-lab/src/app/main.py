import os
from datetime import datetime, timezone
from enum import Enum
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fintech_lab.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_reference: Mapped[str] = mapped_column(String(64), index=True)
    amount_minor: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    status: Mapped[str] = mapped_column(String(16), default=PaymentStatus.pending.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


Base.metadata.create_all(bind=engine)


class PaymentCreate(BaseModel):
    customer_reference: str = Field(min_length=3, max_length=64)
    amount_minor: int = Field(gt=0, le=100_000_000)
    currency: str = Field(default="RUB", pattern="^[A-Z]{3}$")


class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_reference: str
    amount_minor: int
    currency: str
    status: PaymentStatus
    created_at: datetime


app = FastAPI(title="Fintech Support & QA Lab API", version="0.1.0")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/payments", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)) -> Payment:
    payment = Payment(**payload.model_dump(), status=PaymentStatus.pending.value)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)) -> Payment:
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.patch("/payments/{payment_id}/status", response_model=PaymentOut)
def update_payment_status(
    payment_id: int,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db),
) -> Payment:
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    allowed = {
        PaymentStatus.pending.value: {PaymentStatus.paid.value, PaymentStatus.failed.value},
        PaymentStatus.paid.value: set(),
        PaymentStatus.failed.value: set(),
    }
    if payload.status.value not in allowed[payment.status]:
        raise HTTPException(
            status_code=409,
            detail=f"Invalid payment status transition: {payment.status} -> {payload.status.value}",
        )

    payment.status = payload.status.value
    db.commit()
    db.refresh(payment)
    return payment
