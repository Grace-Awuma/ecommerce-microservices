from sqlalchemy import Column, String, Float, JSON
from pydantic import BaseModel
from app.database import Base
from typing import List
import uuid


# SQLAlchemy model
class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_email = Column(String, nullable=False)
    items = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")


# Pydantic models
class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    customer_email: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str
    customer_email: str
    items: List[OrderItem]
    total_price: float
    status: str

    class Config:
        from_attributes = True