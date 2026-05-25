from sqlalchemy import Column, String, Float
from pydantic import BaseModel
from app.database import Base
import uuid


# SQLAlchemy model
class PaymentDB(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    customer_email = Column(String, nullable=False)
    status = Column(String, default="paid")
    transaction_ref = Column(String, nullable=False)


# Pydantic models
class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    customer_email: str

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    amount: float
    customer_email: str
    status: str
    transaction_ref: str

    class Config:
        from_attributes = True