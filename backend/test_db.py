# backend/test_db.py

from database import SessionLocal
from models import Order

db = SessionLocal()

orders = db.query(Order).all()

print(f"Total Orders: {len(orders)}")

for order in orders[:5]:
    print(order.order_id, order.current_stage)

db.close()