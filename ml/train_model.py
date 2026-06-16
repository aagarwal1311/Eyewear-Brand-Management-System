import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv("data/historical_orders.csv")

# Encode categorical columns
encoders = {}

for col in [
    "store_location",
    "lens_type",
    "coating",
    "current_stage"
]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# Features
X = df[
    [
        "store_location",
        "lens_type",
        "coating",
        "prescription_power",
        "inventory_available",
        "qc_failed",
        "current_stage",
        "time_in_stage"
    ]
]

# Target
y = df["is_breached"]

# Train
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save
joblib.dump(model, "ml/breach_model.pkl")
joblib.dump(encoders, "ml/encoders.pkl")

print("Model trained and saved.")