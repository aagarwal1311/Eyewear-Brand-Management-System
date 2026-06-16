# backend/seed_data.py

import pandas as pd

from database import SessionLocal
from models import Order

db = SessionLocal()

df = pd.read_csv("data/active_orders.csv")

for _, row in df.iterrows():

    order = Order(
        order_id=row["order_id"],
        store_location=row["store_location"],
        lens_type=row["lens_type"],
        coating=row["coating"],
        prescription_power=row["prescription_power"],
        current_stage=row["current_stage"],
        time_in_stage=row["time_in_stage"],
        inventory_available=bool(row["inventory_available"]),
        qc_failed=bool(row["qc_failed"]),
        sla_hours=row["sla_hours"]
    )

    db.add(order)

db.commit()
db.close()

print("Orders loaded successfully!")