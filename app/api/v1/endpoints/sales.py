"""Sales analytics endpoints for Looker Studio dashboards."""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import DailySales, FunnelStep, SalesSummary
from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/summary", response_model=SalesSummary)
def get_sales_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
) -> SalesSummary:
    """
    Return aggregate sales KPIs for a date range.

    **Looker Studio chart**: Scorecard widgets for total revenue, profit,
    AOV, and order counts. Filter controls can pass start_date / end_date.
    """
    return SalesService(db).get_summary(start_date, end_date)


@router.get("/daily", response_model=List[DailySales])
def get_daily_sales(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[DailySales]:
    """
    Return day-by-day revenue and profit.

    **Looker Studio chart**: Time series line/area chart with date on X-axis,
    revenue and profit as dual Y-axis series.
    """
    return SalesService(db).get_daily(start_date, end_date)


@router.get("/funnel", response_model=List[FunnelStep])
def get_sales_funnel(db: Session = Depends(get_db)) -> List[FunnelStep]:
    """
    Return order count and percentage share for every order status.

    **Looker Studio chart**: Funnel chart or donut/pie chart showing
    the distribution of order statuses (pending, processing, delivered, cancelled).
    """
    return SalesService(db).get_funnel()
