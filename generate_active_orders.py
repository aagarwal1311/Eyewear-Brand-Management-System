import pandas as pd
import random
from faker import Faker

fake = Faker()

NUM_ACTIVE = 100

LENS_TYPES = [
    "Single Vision",
    "Bifocal",
    "Progressive"
]

SLA_MAP = {
    "Single Vision": 24,
    "Bifocal": 48,
    "Progressive": 72
}

COATINGS = [
    "None",
    "Anti-Reflective",
    "Blue Light",
    "Transitions"
]

STORES = [
    "Downtown",
    "Northside",
    "East Mall",
    "Online Store"
]

STAGES = [
    "Prescription Verification",
    "Lens Allocation",
    "Lab Processing",
    "QC",
    "Packaging",
    "Shipped"
]

active_orders = []

for _ in range(NUM_ACTIVE):

    lens_type = random.choice(LENS_TYPES)

    inventory_available = random.random() < 0.8
    qc_failed = random.random() < 0.15

    active_orders.append({
        "order_id": fake.uuid4()[:8],
        "store_location": random.choice(STORES),
        "lens_type": lens_type,
        "coating": random.choice(COATINGS),
        "prescription_power": round(random.uniform(-6, 6), 2),
        "inventory_available": inventory_available,
        "qc_failed": qc_failed,
        "current_stage": random.choice(STAGES),
        "time_in_stage": random.randint(1, 24),
        "sla_hours": SLA_MAP[lens_type]
    })

pd.DataFrame(active_orders).to_csv(
    "data/active_orders.csv",
    index=False
)

print("Active orders generated.")