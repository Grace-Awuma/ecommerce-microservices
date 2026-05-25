from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import ProductDB, ProductCreate, ProductResponse, StockUpdate
from typing import List

app = FastAPI(title="Product Service", version="1.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.patch("/products/{product_id}/stock")
def update_stock(product_id: str, update: StockUpdate, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < update.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    product.stock -= update.quantity
    db.commit()
    db.refresh(product)
    return {"product_id": product_id, "stock_remaining": product.stock}

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()