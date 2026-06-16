import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Eyewear Order Management",
    layout="wide"
)

st.title("👓 Eyewear Order Management Dashboard")

COLUMN_NAMES = {
    "order_id": "Order ID",
    "store_location": "Store Location",
    "lens_type": "Lens Type",
    "coating": "Coating",
    "prescription_power": "Prescription Power",
    "current_stage": "Current Stage",
    "time_in_stage": "Hours in Current Stage",
    "sla_hours": "SLA Hours",
    "sla_remaining": "SLA Remaining",
    "sla_status": "SLA Status",
    "inventory_available": "Inventory Available",
    "qc_failed": "QC Failed",
    "delay_reason": "Delay Reason",
    "stock_count": "Available Stock",
    "risk_score": "Risk Score",
    "prediction": "Prediction"
}

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Orders",
        "Inventory",
        "Alerts",
        "Inventory Check"
    ]
)

with tab1:

    orders = requests.get(
        "http://127.0.0.1:8000/orders"
    ).json()

    df = pd.DataFrame(orders)


    st.metric(
        "Total Active Orders",
        len(df)
    )
    st.subheader("Orders by Stage")
    st.bar_chart(df["current_stage"].value_counts())    


    df["sla_remaining"] = (
        df["sla_hours"] - df["time_in_stage"]
    )

    df["sla_status"] = df["sla_remaining"].apply(
        lambda x: "BREACHED" if x < 0 else f"{x} hrs remaining"
    )


    # Filters
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["current_stage"].unique().tolist())
    )

    lens_filter = st.selectbox(
        "Lens Type",
        ["All"] + sorted(df["lens_type"].unique().tolist())
    )

    store_filter = st.selectbox(
        "Store Location",
        ["All"] + sorted(df["store_location"].unique().tolist())
    )

    filtered_df = df.copy()

    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["current_stage"] == status_filter
        ]

    if lens_filter != "All":
        filtered_df = filtered_df[
            filtered_df["lens_type"] == lens_filter
        ]

    if store_filter != "All":
        filtered_df = filtered_df[
            filtered_df["store_location"] == store_filter
        ]

    display_df = filtered_df[
        [
            "order_id",
            "store_location",
            "lens_type",
            "coating",
            "current_stage",
            "time_in_stage",
            "sla_remaining",
            "sla_status",
            "delay_reason"
        ]
    ]

    display_df = display_df.rename(columns=COLUMN_NAMES)

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.subheader("Update Order Status")

    selected_order = st.selectbox(
        "Select Order",
        df["order_id"].tolist()
    )

    new_status = st.selectbox(
        "New Status",
        [
            "Prescription Verification",
            "Lens Allocation",
            "Lab Processing",
            "Quality Check",
            "Dispatch",
            "Delivered"
        ]
    )

    delay_reason = st.text_input(
        "Delay Reason (optional)"
    )

    if st.button("Update Status"):

        payload = {
            "current_stage": new_status,
            "delay_reason": delay_reason
        }

        response = requests.put(
            f"http://127.0.0.1:8000/orders/{selected_order}",
            json=payload
        )

        if response.status_code == 200:
            st.success("Order updated successfully")
        else:
            st.error("Failed to update order")



with tab2:

    inventory = requests.get(
        "http://127.0.0.1:8000/inventory"
    ).json()

    inv_df = pd.DataFrame(inventory)

    st.metric(
        "Inventory Items",
        len(inv_df)
    )

    inventory_display = inv_df[
        [
            "lens_type",
            "prescription_power",
            "coating",
            "stock_count"
        ]
    ].rename(columns=COLUMN_NAMES)

    st.dataframe(
        inventory_display,
        use_container_width=True
)

with tab3:

    st.header("SLA Breach Alerts")

    orders = requests.get(
        "http://127.0.0.1:8000/orders"
    ).json()

    high_risk_orders = []

    for order in orders:

        order_id = order["order_id"]

        response = requests.get(
            f"http://127.0.0.1:8000/predict/{order_id}"
        )

        if response.status_code != 200:
            st.write(f"Failed for order {order_id}")
            st.write(response.text)
            continue

        result = response.json()

        if result["risk_score"] > 0.7:

            high_risk_orders.append({
                "order_id": order_id,
                "risk_score": result["risk_score"],
                "prediction": result["prediction"]
            })

    if len(high_risk_orders) == 0:

        st.success(
            "No high-risk orders found."
        )

    else:

        st.error(
            f"{len(high_risk_orders)} high-risk orders detected"
        )

        high_risk_display = pd.DataFrame(high_risk_orders).rename(columns=COLUMN_NAMES)

        st.dataframe(
            high_risk_display,
            use_container_width=True
        )


with tab4:

    st.header("Inventory Availability Check")

    lens_type = st.selectbox(
        "Lens Type",
        [
            "Single Vision",
            "Bifocal",
            "Progressive"
        ]
    )

    power = st.number_input(
        "Prescription Power",
        value=0.0
    )

    coating = st.selectbox(
        "Coating",
        [
            "Anti-Reflective",
            "Blue Light",
            "Transitions",
            "None"
        ]
    )

    if st.button("Check Inventory"):

        response = requests.get(
            "http://127.0.0.1:8000/inventory/check",
            params={
                "lens_type": lens_type,
                "power": power,
                "coating": coating
            }
        )

        result = response.json()

        if result["available"]:
            st.success(
                f"In Stock | Available Units: {result['stock']}"
            )
        else:
            st.error(
                "Not Available In Inventory"
            )