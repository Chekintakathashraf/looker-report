"""Service layer for revenue trend and geo-distribution analytics."""

from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.schemas import RevenueByState, RevenueTrend


class RevenueService:
    """Handles revenue trend and geographic breakdown queries."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_trend(self, months: int = 12) -> List[RevenueTrend]:
        """
        Return monthly revenue, profit, order count, and month-over-month growth rate
        for the last N months using a window function LAG equivalent via subquery.
        """
        sql = text(
            """
            WITH monthly_raw AS (
                SELECT
                    STRFTIME('%Y-%m', o.created_at) AS month,
                    ROUND(SUM(o.total_amount), 2) AS revenue,
                    ROUND(SUM((oi.unit_price - p.cost_price) * oi.quantity), 2) AS profit,
                    COUNT(DISTINCT o.id) AS order_count
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.id
                JOIN products p ON p.id = oi.product_id
                WHERE o.status != 'cancelled'
                  AND o.created_at >= DATE('now', :months_offset)
                GROUP BY STRFTIME('%Y-%m', o.created_at)
            ),
            ranked AS (
                SELECT
                    month,
                    revenue,
                    profit,
                    order_count,
                    ROW_NUMBER() OVER (ORDER BY month) AS rn
                FROM monthly_raw
            ),
            with_prev AS (
                SELECT
                    r.month,
                    r.revenue,
                    r.profit,
                    r.order_count,
                    prev.revenue AS prev_revenue
                FROM ranked r
                LEFT JOIN ranked prev ON prev.rn = r.rn - 1
            )
            SELECT
                month,
                revenue,
                profit,
                order_count,
                CASE
                    WHEN prev_revenue IS NULL OR prev_revenue = 0 THEN NULL
                    ELSE ROUND((revenue - prev_revenue) / prev_revenue * 100, 2)
                END AS mom_growth_rate
            FROM with_prev
            ORDER BY month
            """
        )

        rows = self.db.execute(sql, {"months_offset": f"-{months} months"}).fetchall()
        return [
            RevenueTrend(
                month=row.month,
                revenue=row.revenue or 0.0,
                profit=row.profit or 0.0,
                order_count=row.order_count or 0,
                mom_growth_rate=row.mom_growth_rate,
            )
            for row in rows
        ]

    def get_by_state(self) -> List[RevenueByState]:
        """Return total revenue, orders, and unique customers grouped by Indian state."""
        sql = text(
            """
            SELECT
                c.state,
                ROUND(SUM(o.total_amount), 2) AS total_revenue,
                COUNT(DISTINCT o.id) AS total_orders,
                COUNT(DISTINCT c.id) AS total_customers
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            WHERE o.status != 'cancelled'
              AND c.state IS NOT NULL
            GROUP BY c.state
            ORDER BY total_revenue DESC
            """
        )

        rows = self.db.execute(sql).fetchall()
        return [
            RevenueByState(
                state=row.state,
                total_revenue=row.total_revenue or 0.0,
                total_orders=row.total_orders or 0,
                total_customers=row.total_customers or 0,
            )
            for row in rows
        ]
