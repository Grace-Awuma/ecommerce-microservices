from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from app.database import Base
import uuid

# SQLAlchemy model (database table)
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)


# Pydantic models (API request/response shapes)
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int