# Eyewear Order Management System

## Overview

The Eyewear Order Management System is an operational dashboard designed to manage eyewear orders, monitor inventory availability, track SLA compliance, and proactively identify orders that are at risk of missing delivery commitments.

The solution combines a FastAPI backend, SQLite database, Streamlit dashboard, and a Machine Learning model to provide end-to-end visibility into the eyewear fulfillment workflow.

---

## Features

### 1. Order Management

* View all active orders
* Filter orders by:

  * Current Stage
  * Lens Type
  * Store Location
* Update order status through the dashboard
* Track order progress across the fulfillment workflow

### 2. SLA Monitoring

* Calculate remaining SLA hours for each order
* Highlight breached orders
* Provide real-time visibility into operational delays

### 3. Inventory Management

* View inventory availability
* Track stock counts by:

  * Lens Type
  * Prescription Power
  * Coating Type
* Support inventory availability checks before order fulfillment

### 4. Inventory Availability Check

Users can verify whether a required lens configuration is available in stock by selecting:

* Lens Type
* Prescription Power
* Coating

The system returns inventory availability and stock count information.

### 5. AI-Powered Risk Prediction

A Machine Learning model predicts the probability of SLA breach for each order.

The system evaluates operational factors such as:

* Store location
* Lens type
* Coating
* Prescription power
* Inventory availability
* Quality control failures
* Current workflow stage
* Time spent in stage

High-risk orders are surfaced in the Alerts dashboard for proactive intervention.

### 6. Operational Dashboard

The Streamlit dashboard provides:

* Order visibility
* Inventory visibility
* SLA tracking
* Risk monitoring
* Workflow updates
* Operational analytics

---

## Data Generation

As no production eyewear order dataset was available, a synthetic dataset was created to simulate real-world order fulfillment operations.

The generated dataset includes:

* Order information
* Store locations
* Lens types
* Coating options
* Prescription powers
* Inventory availability status
* Quality control outcomes
* Workflow stages
* SLA commitments
* Actual fulfillment times
* SLA breach indicators

The synthetic data was generated using realistic business rules to model operational scenarios such as inventory shortages, quality control failures, processing delays, and SLA breaches.

This dataset was then used to train and evaluate the machine learning model responsible for SLA breach prediction.


### Training Dataset

The Random Forest model was trained on a synthetically generated historical order dataset containing simulated eyewear fulfillment records.

The dataset was designed to reflect realistic operational workflows and included both successful and breached orders to enable supervised learning.


## System Architecture

```
                    ┌─────────────────┐
                    │   Streamlit UI  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │   REST APIs     │
                    └────────┬────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    ┌─────────────────┐             ┌─────────────────┐
    │ SQLite Database │             │ Random Forest   │
    │ Orders/Inventory│             │ ML Model        │
    └─────────────────┘             └─────────────────┘
```

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### Database

* SQLite
* SQLAlchemy ORM

### Machine Learning

* Scikit-Learn
* Random Forest Classifier
* LabelEncoder

### Supporting Libraries

* Pandas
* Joblib
* Requests
* Uvicorn

---

## Database Schema

### Orders

Stores order-related information including:

* Order ID
* Store Location
* Lens Type
* Coating
* Prescription Power
* Current Stage
* SLA Hours
* Delay Reason
* Order Timestamps

### Inventory

Stores inventory information including:

* Lens Type
* Prescription Power
* Coating
* Stock Count

### Alerts

Stores generated risk alerts including:

* Order ID
* Risk Score
* Alert Message
* Resolution Status

---

## Machine Learning Model

### Model Type

Random Forest Classifier

### Prediction Objective

Predict whether an order is likely to breach its SLA.

### Features Used

* Store Location
* Lens Type
* Coating
* Prescription Power
* Inventory Availability
* QC Failure Status
* Current Stage
* Time In Stage

### Output

* Risk Score
* Prediction Category:

  * On Track
  * Likely Breach

### Why Random Forest?

Random Forest was selected because:

* Performs well on structured tabular datasets
* Handles both categorical and numerical features
* Requires minimal feature engineering
* Produces reliable probability estimates
* Provides strong baseline predictive performance

---

## Project Structure

```text
EYEWEAR_BRAND_MANAGEMENT_SYSTEM

├── backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── eyewear_system.db
│
├── frontend
│   └── app.py
│
├── ml
│   ├── train_model.py
│   ├── breach_model.pkl
│   └── encoders.pkl
│
├── data
│   ├── historical_orders.csv
│   ├── generate_data.py
│   └── seed_database.py
│
├── requirements.txt
└── README.md
```

---

## Running the Application

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend will be available at:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit Dashboard

```bash
cd frontend
streamlit run app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## Future Improvements

* Cloud deployment
* Authentication and role-based access control
* Automated alert notifications
* Real-time order tracking
* Advanced forecasting models
* Inventory replenishment recommendations
* Historical analytics dashboards

---

## Author

Developed as part of an Eyewear Order Management and SLA Prediction assignment demonstrating full-stack application development, database management, and machine learning integration.
