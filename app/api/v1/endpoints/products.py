"""Product analytics endpoints for Looker Studio dashboards."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import CategoryRevenue, LowStockProduct, TopProduct
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/top", response_model=List[TopProduct])
def get_top_products(
    limit: int = Query(default=10, ge=1, le=100),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[TopProduct]:
    """
    Return top products ranked by revenue with profit metrics.

    **Looker Studio chart**: Horizontal bar chart — product name on Y-axis,
    revenue and profit as side-by-side or stacked bars. Add category_id filter
    control to drill down per category.
    """
    return ProductService(db).get_top_products(limit, category_id)


@router.get("/categories", response_model=List[CategoryRevenue])
def get_category_revenue(db: Session = Depends(get_db)) -> List[CategoryRevenue]:
    """
    Return revenue and percentage contribution broken down by category.

    **Looker Studio chart**: Pie or donut chart using category as dimension
    and total_revenue as metric. Add a table beneath for exact figures.
    """
    return ProductService(db).get_category_revenue()


@router.get("/low-stock", response_model=List[LowStockProduct])
def get_low_stock(
    threshold: int = Query(default=10, ge=0),
    db: Session = Depends(get_db),
) -> List[LowStockProduct]:
    """
    Return products whose stock is at or below the requested threshold.

    **Looker Studio chart**: Table widget sorted by stock ascending, with
    conditional formatting to highlight critically low stock in red.
    """
    return ProductService(db).get_low_stock(threshold)
