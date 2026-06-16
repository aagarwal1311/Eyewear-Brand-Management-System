import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# --------------------------
# CONFIG
# --------------------------

NUM_ORDERS = 5000

LENS_TYPES = {
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
    "Shipped",
    "Delivered"
]

orders = []

# --------------------------
# DATA GENERATION
# --------------------------

for _ in range(NUM_ORDERS):

    lens_type = random.choice(list(LENS_TYPES.keys()))
    coating = random.choice(COATINGS)
    store = random.choice(STORES)

    power = round(random.uniform(-6.0, 6.0), 2)

    sla_hours = LENS_TYPES[lens_type]

    order_placed = fake.date_time_between(
        start_date="-90d",
        end_date="now"
    )

    # --------------------------
    # Inventory availability
    # --------------------------

    inventory_available = random.random() < 0.80

    # --------------------------
    # QC failure
    # --------------------------

    qc_failed = random.random() < 0.15

    # --------------------------
    # Current stage
    # --------------------------

    current_stage = random.choice(STAGES[:-1])

    time_in_stage = random.randint(1, 24)

    # --------------------------
    # Breach probability
    # --------------------------

    breach_score = 0

    if lens_type == "Progressive":
        breach_score += 3

    if coating == "Transitions":
        breach_score += 2

    if store == "Online Store":
        breach_score += 1

    if abs(power) > 4:
        breach_score += 2

    if not inventory_available:
        breach_score += 3

    if qc_failed:
        breach_score += 4

    breach_probability = min(
        0.05 + breach_score * 0.06,
        0.90
    )

    will_breach = random.random() < breach_probability

    # --------------------------
    # Processing time
    # --------------------------

    processing_hours = random.randint(
        int(sla_hours * 0.4),
        int(sla_hours * 0.9)
    )

    if not inventory_available:
        processing_hours += random.randint(12, 48)

    if qc_failed:
        processing_hours += random.randint(12, 36)

    if will_breach:
        processing_hours += random.randint(5, 48)

    order_completed = (
        order_placed +
        timedelta(hours=processing_hours)
    )

    orders.append({
        "order_id": fake.uuid4()[:8],
        "store_location": store,
        "lens_type": lens_type,
        "coating": coating,
        "prescription_power": power,
        "inventory_available": int(inventory_available),
        "qc_failed": int(qc_failed),
        "current_stage": current_stage,
        "time_in_stage": time_in_stage,
        "order_placed": order_placed,
        "order_completed": order_completed,
        "sla_hours": sla_hours,
        "actual_hours": processing_hours,
        "is_breached": int(processing_hours > sla_hours)
    })

# --------------------------
# SAVE
# --------------------------

df = pd.DataFrame(orders)

df.to_csv(
    "data/historical_orders.csv",
    index=False
)

print(
    f"Generated {len(df)} orders."
)

print(
    f"Breach Rate: "
    f"{round(df['is_breached'].mean()*100,2)}%"
)