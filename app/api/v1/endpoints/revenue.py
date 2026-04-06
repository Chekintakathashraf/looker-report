"""Revenue analytics endpoints for Looker Studio dashboards."""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import RevenueByState, RevenueTrend
from app.services.revenue_service import RevenueService

router = APIRouter(prefix="/revenue", tags=["Revenue"])


@router.get("/trend", response_model=List[RevenueTrend])
def get_revenue_trend(
    months: int = Query(default=12, ge=1, le=60),
    db: Session = Depends(get_db),
) -> List[RevenueTrend]:
    """
    Return monthly revenue, profit, order count, and month-over-month growth rate.

    **Looker Studio chart**: Combo chart — bars for revenue/profit and a line
    overlay for MoM growth rate. Use the months param to control lookback window.
    """
    return RevenueService(db).get_trend(months)


@router.get("/by-state", response_model=List[RevenueByState])
def get_revenue_by_state(db: Session = Depends(get_db)) -> List[RevenueByState]:
    """
    Return total revenue, orders, and unique customers grouped by Indian state.

    **Looker Studio chart**: Geo map (India) with state as geo dimension and
    total_revenue as colour-coded metric. Pair with a sortable table for exact values.
    """
    return RevenueService(db).get_by_state()
