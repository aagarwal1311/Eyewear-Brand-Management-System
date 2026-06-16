from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean
)

from database import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    # Primary Key
    order_id = Column(String, primary_key=True, index=True)

    # Order Details
    store_location = Column(String, index=True)
    lens_type = Column(String, index=True)
    coating = Column(String)
    prescription_power = Column(Float)

    # Workflow Tracking
    current_stage = Column(String, index=True)
    time_in_stage = Column(Integer)

    # Operational Features
    inventory_available = Column(Boolean, default=True)
    qc_failed = Column(Boolean, default=False)

    # SLA Tracking
    sla_hours = Column(Integer)

    # Delay Information
    delay_reason = Column(String, nullable=True)

    # Timestamps
    order_placed = Column(
        DateTime,
        default=datetime.utcnow
    )

    order_completed = Column(
        DateTime,
        nullable=True
    )

    # Historical Metrics
    actual_hours = Column(
        Integer,
        nullable=True
    )

    is_breached = Column(
        Boolean,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    lens_type = Column(String, index=True)

    prescription_power = Column(Float)

    coating = Column(String)

    stock_count = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(String, index=True)

    risk_score = Column(Float)

    message = Column(String)

    is_resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )