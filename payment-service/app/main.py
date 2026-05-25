from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import PaymentDB, PaymentRequest, PaymentResponse
import uuid
import random

app = FastAPI(title="Payment Service", version="1.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-service"}

@app.post("/payments", response_model=PaymentResponse, status_code=201)
def process_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    # Simulate 90% success rate for testing
    success = random.random() > 0.1
    if not success:
        raise HTTPException(status_code=402, detail="Payment declined")

    db_payment = PaymentDB(
        id=str(uuid.uuid4()),
        order_id=payment.order_id,
        amount=payment.amount,
        customer_email=payment.customer_email,
        status="paid",
        transaction_ref=f"TXN-{uuid.uuid4().hex[:8].upper()}"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(PaymentDB).filter(PaymentDB.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.get("/payments/order/{order_id}", response_model=PaymentResponse)
def get_payment_by_order(order_id: str, db: Session = Depends(get_db)):
    payment = db.query(PaymentDB).filter(PaymentDB.order_id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    return payment