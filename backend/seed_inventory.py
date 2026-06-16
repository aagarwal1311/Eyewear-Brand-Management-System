import pandas as pd

from database import SessionLocal
from models import Inventory

db = SessionLocal()

df = pd.read_csv("data/inventory.csv")

for _, row in df.iterrows():

    item = Inventory(
        lens_type=row["lens_type"],
        prescription_power=row["prescription_power"],
        coating=row["coating"],
        stock_count=row["stock_count"]
    )

    db.add(item)

db.commit()
db.close()

print("Inventory loaded successfully")
