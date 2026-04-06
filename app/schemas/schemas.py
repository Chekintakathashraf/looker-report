"""Pydantic v2 response schemas for all API endpoints."""

from typing import List, Optional

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Sales schemas
# ---------------------------------------------------------------------------


class SalesSummary(BaseModel):
    """Aggregate sales KPIs for a given date range."""

    total_orders: int
    total_revenue: float
    total_profit: float
    average_order_value: float
    cancelled_orders: int
    delivered_orders: int


class DailySales(BaseModel):
    """Revenue and profit for a single day."""

    date: str
    revenue: float
    profit: float
    orders: int


class FunnelStep(BaseModel):
    """Order count and percentage share for a single status."""

    status: str
    order_count: int
    percentage: float


# ---------------------------------------------------------------------------
# Product schemas
# ---------------------------------------------------------------------------


class TopProduct(BaseModel):
    """Product ranked by revenue."""

    product_id: int
    product_name: str
    category: str
    total_revenue: float
    total_profit: float
    units_sold: int


class CategoryRevenue(BaseModel):
    """Revenue contribution of a product category."""

    category: str
    total_revenue: float
    percentage: float
    order_count: int


class LowStockProduct(BaseModel):
    """Product whose stock is at or below the requested threshold."""

    product_id: int
    product_name: str
    sku: str
    category: str
    stock: int
    price: float


# ---------------------------------------------------------------------------
# Customer schemas
# ---------------------------------------------------------------------------


class CustomerSegment(BaseModel):
    """Aggregate metrics for a customer spending segment."""

    segment: str
    customer_count: int
    total_revenue: float
    average_order_value: float


class TopCustomer(BaseModel):
    """Customer ranked by lifetime value."""

    customer_id: int
    name: str
    email: str
    city: Optional[str]
    state: Optional[str]
    total_spent: float
    total_orders: int


class MonthlyRetention(BaseModel):
    """New vs returning customer counts for a single month."""

    month: str
    new_customers: int
    returning_customers: int


# ---------------------------------------------------------------------------
# Revenue schemas
# ---------------------------------------------------------------------------


class RevenueTrend(BaseModel):
    """Monthly revenue, profit, and growth metrics."""

    month: str
    revenue: float
    profit: float
    order_count: int
    mom_growth_rate: Optional[float]


class RevenueByState(BaseModel):
    """Revenue aggregated by Indian state."""

    state: str
    total_revenue: float
    total_orders: int
    total_customers: int
