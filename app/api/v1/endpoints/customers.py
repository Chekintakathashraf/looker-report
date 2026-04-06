"""Customer analytics endpoints for Looker Studio dashboards."""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import CustomerSegment, MonthlyRetention, TopCustomer
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/segments", response_model=List[CustomerSegment])
def get_customer_segments(db: Session = Depends(get_db)) -> List[CustomerSegment]:
    """
    Group customers into VIP (≥₹10000), Regular (≥₹3000), New, and Inactive segments.

    **Looker Studio chart**: Stacked bar or grouped bar chart comparing customer
    count and revenue per segment. Scorecard widgets showing VIP vs New ratio.
    """
    return CustomerService(db).get_segments()


@router.get("/top", response_model=List[TopCustomer])
def get_top_customers(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[TopCustomer]:
    """
    Return top customers ranked by lifetime value (total spend on delivered orders).

    **Looker Studio chart**: Table widget with customer name, city, state,
    total spent, and order count — sortable columns for analyst drill-down.
    """
    return CustomerService(db).get_top_customers(limit)


@router.get("/retention", response_model=List[MonthlyRetention])
def get_customer_retention(db: Session = Depends(get_db)) -> List[MonthlyRetention]:
    """
    Return new vs returning customer counts per month for the last 12 months.

    **Looker Studio chart**: Stacked area or grouped bar chart with month on X-axis,
    new_customers and returning_customers as separate series to visualise retention trends.
    """
    return CustomerService(db).get_retention()
