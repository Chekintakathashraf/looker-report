"""Service layer for sales-related analytics queries."""

from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.schemas import DailySales, FunnelStep, SalesSummary


class SalesService:
    """Handles all sales analytics queries using raw SQL with CTEs."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_summary(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> SalesSummary:
        """Return aggregate KPIs: total orders, revenue, profit, AOV, cancelled, delivered."""
        filters = self._date_filters(start_date, end_date)
        params = self._date_params(start_date, end_date)

        sql = text(
            f"""
            WITH order_profits AS (
                SELECT
                    o.id,
                    o.status,
                    o.total_amount,
                    SUM((oi.unit_price - p.cost_price) * oi.quantity) AS profit
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.id
                JOIN products p ON p.id = oi.product_id
                {filters}
                GROUP BY o.id, o.status, o.total_amount
            )
            SELECT
                COUNT(*) AS total_orders,
                ROUND(SUM(total_amount), 2) AS total_revenue,
                ROUND(SUM(profit), 2) AS total_profit,
                ROUND(AVG(total_amount), 2) AS average_order_value,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
                SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders
            FROM order_profits
            """
        )

        row = self.db.execute(sql, params).fetchone()
        return SalesSummary(
            total_orders=row.total_orders or 0,
            total_revenue=row.total_revenue or 0.0,
            total_profit=row.total_profit or 0.0,
            average_order_value=row.average_order_value or 0.0,
            cancelled_orders=row.cancelled_orders or 0,
            delivered_orders=row.delivered_orders or 0,
        )

    def get_daily(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[DailySales]:
        """Return day-by-day revenue and profit for the requested date range."""
        filters = self._date_filters(start_date, end_date)
        params = self._date_params(start_date, end_date)

        sql = text(
            f"""
            WITH daily AS (
                SELECT
                    DATE(o.created_at) AS sale_date,
                    o.total_amount,
                    SUM((oi.unit_price - p.cost_price) * oi.quantity) AS profit
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.id
                JOIN products p ON p.id = oi.product_id
                {filters}
                GROUP BY o.id, DATE(o.created_at), o.total_amount
            )
            SELECT
                sale_date AS date,
                ROUND(SUM(total_amount), 2) AS revenue,
                ROUND(SUM(profit), 2) AS profit,
                COUNT(*) AS orders
            FROM daily
            GROUP BY sale_date
            ORDER BY sale_date
            """
        )

        rows = self.db.execute(sql, params).fetchall()
        return [
            DailySales(
                date=str(row.date),
                revenue=row.revenue or 0.0,
                profit=row.profit or 0.0,
                orders=row.orders or 0,
            )
            for row in rows
        ]

    def get_funnel(self) -> List[FunnelStep]:
        """Return order count and percentage share for every order status."""
        sql = text(
            """
            WITH status_counts AS (
                SELECT status, COUNT(*) AS order_count
                FROM orders
                GROUP BY status
            ),
            total AS (
                SELECT SUM(order_count) AS grand_total FROM status_counts
            )
            SELECT
                s.status,
                s.order_count,
                ROUND(CAST(s.order_count AS FLOAT) / t.grand_total * 100, 2) AS percentage
            FROM status_counts s, total t
            ORDER BY s.order_count DESC
            """
        )

        rows = self.db.execute(sql).fetchall()
        return [
            FunnelStep(
                status=row.status,
                order_count=row.order_count,
                percentage=row.percentage or 0.0,
            )
            for row in rows
        ]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _date_filters(start_date: Optional[str], end_date: Optional[str]) -> str:
        """Build a WHERE clause fragment for date range filtering on orders."""
        clauses = []
        if start_date:
            clauses.append("DATE(o.created_at) >= :start_date")
        if end_date:
            clauses.append("DATE(o.created_at) <= :end_date")
        return "WHERE " + " AND ".join(clauses) if clauses else ""

    @staticmethod
    def _date_params(start_date: Optional[str], end_date: Optional[str]) -> dict:
        """Build the parameter dict matching _date_filters."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return params
