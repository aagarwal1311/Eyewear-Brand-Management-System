import joblib
import pandas as pd

from pathlib import Path

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas import OrderUpdate
from models import Order, Inventory
from database import get_db

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR / "ml" / "breach_model.pkl"
)

encoders = joblib.load(
    BASE_DIR / "ml" / "encoders.pkl"
)


def safe_encode(encoder, value):
    value = str(value)

    if value not in encoder.classes_:
        return 0

    return encoder.transform([value])[0]


@app.get("/")
def home():
    return {
        "message": "Eyewear Order Management System"
    }


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.put("/orders/{order_id}")
def update_order(
    order_id: str,
    update: OrderUpdate,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        return {"error": "Order not found"}

    order.current_stage = update.current_stage
    order.delay_reason = update.delay_reason

    db.commit()

    return {"message": "Order updated"}


@app.get("/inventory")
def get_inventory(
    db: Session = Depends(get_db)
):
    return db.query(Inventory).all()


@app.get("/inventory/check")
def check_inventory(
    lens_type: str,
    power: float,
    coating: str,
    db: Session = Depends(get_db)
):

    item = (
        db.query(Inventory)
        .filter(
            Inventory.lens_type == lens_type,
            Inventory.prescription_power == power,
            Inventory.coating == coating,
            Inventory.stock_count > 0
        )
        .first()
    )

    if item:
        return {
            "available": True,
            "stock": item.stock_count
        }

    return {
        "available": False,
        "stock": 0
    }


@app.get("/predict/{order_id}")
def predict_order_risk(
    order_id: str,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        return {"error": "Order not found"}

    X = pd.DataFrame({
        "store_location": [
            safe_encode(
                encoders["store_location"],
                order.store_location
            )
        ],
        "lens_type": [
            safe_encode(
                encoders["lens_type"],
                order.lens_type
            )
        ],
        "coating": [
            safe_encode(
                encoders["coating"],
                order.coating
            )
        ],
        "prescription_power": [
            order.prescription_power
        ],
        "inventory_available": [
            int(order.inventory_available)
        ],
        "qc_failed": [
            int(order.qc_failed)
        ],
        "current_stage": [
            safe_encode(
                encoders["current_stage"],
                order.current_stage
            )
        ],
        "time_in_stage": [
            order.time_in_stage
        ]
    })

    risk = model.predict_proba(X)[0][1]

    return {
        "order_id": order_id,
        "risk_score": round(float(risk), 2),
        "prediction":
            "Likely Breach"
            if risk > 0.5
            else "On Track"
    }