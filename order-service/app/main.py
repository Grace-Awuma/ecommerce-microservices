from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import OrderDB, OrderCreate, OrderResponse, OrderItem
from app.config import settings
from typing import List
import httpx
import uuid

app = FastAPI(title="Order Service", version="1.0.0")


@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database connection failed on startup: {e}")
        print("App will continue running - retrying on first request")


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    total_price = 0.0
    items_data = []

    async with httpx.AsyncClient() as client:
        for item in order.items:
            resp = await client.get(
                f"{settings.PRODUCT_SERVICE_URL}/products/{item.product_id}"
            )
            if resp.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )

            product = resp.json()

            if product["stock"] < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {product['name']}"
                )

            total_price += product["price"] * item.quantity
            items_data.append(
                {"product_id": item.product_id, "quantity": item.quantity})

            await client.patch(
                f"{settings.PRODUCT_SERVICE_URL}/products/{item.product_id}/stock",
                json={"quantity": item.quantity}
            )

        order_id = str(uuid.uuid4())
        payment_resp = await client.post(
            f"{settings.PAYMENT_SERVICE_URL}/payments",
            json={
                "order_id": order_id,
                "amount": total_price,
                "customer_email": order.customer_email
            }
        )

        if payment_resp.status_code != 201:
            raise HTTPException(
                status_code=502,
                detail="Payment processing failed")

        payment = payment_resp.json()

    db_order = OrderDB(
        id=order_id,
        customer_email=order.customer_email,
        items=items_data,
        total_price=total_price,
        status=payment["status"]
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return OrderResponse(
        id=db_order.id,
        customer_email=db_order.customer_email,
        items=[OrderItem(**i) for i in db_order.items],
        total_price=db_order.total_price,
        status=db_order.status
    )


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(
        id=order.id,
        customer_email=order.customer_email,
        items=[OrderItem(**i) for i in order.items],
        total_price=order.total_price,
        status=order.status
    )


@app.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return [
        OrderResponse(
            id=o.id,
            customer_email=o.customer_email,
            items=[OrderItem(**i) for i in o.items],
            total_price=o.total_price,
            status=o.status
        ) for o in orders
    ]
