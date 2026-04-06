"""Service layer for customer-related analytics queries."""

from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.schemas import CustomerSegment, MonthlyRetention, TopCustomer


class CustomerService:
    """Handles all customer analytics queries using raw SQL with CTEs."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_segments(self) -> List[CustomerSegment]:
        """
        Group customers into:
        - VIP       : lifetime spend >= 10000
        - Regular   : lifetime spend >= 3000
        - New       : has orders but spend < 3000
        - Inactive  : no orders at all
        Returns count, total revenue, and AOV per segment.
        """
        sql = text(
            """
            WITH customer_spend AS (
                SELECT
                    c.id AS customer_id,
                    COALESCE(SUM(CASE WHEN o.status != 'cancelled' THEN o.total_amount ELSE 0 END), 0) AS lifetime_spend,
                    COUNT(CASE WHEN o.status != 'cancelled' THEN 1 END) AS order_count
                FROM customers c
                LEFT JOIN orders o ON o.customer_id = c.id
                GROUP BY c.id
            ),
            segmented AS (
                SELECT
                    customer_id,
                    lifetime_spend,
                    order_count,
                    CASE
                        WHEN order_count = 0 THEN 'Inactive'
                        WHEN lifetime_spend >= 10000 THEN 'VIP'
                        WHEN lifetime_spend >= 3000 THEN 'Regular'
                        ELSE 'New'
                    END AS segment
                FROM customer_spend
            )
            SELECT
                segment,
                COUNT(*) AS customer_count,
                ROUND(SUM(lifetime_spend), 2) AS total_revenue,
                ROUND(
                    CASE
                        WHEN SUM(order_count) > 0
                        THEN SUM(lifetime_spend) / SUM(order_count)
                        ELSE 0
                    END, 2
                ) AS average_order_value
            FROM segmented
            GROUP BY segment
            ORDER BY total_revenue DESC
            """
        )

        rows = self.db.execute(sql).fetchall()
        return [
            CustomerSegment(
                segment=row.segment,
                customer_count=row.customer_count,
                total_revenue=row.total_revenue or 0.0,
                average_order_value=row.average_order_value or 0.0,
            )
            for row in rows
        ]

    def get_top_customers(self, limit: int = 10) -> List[TopCustomer]:
        """Return customers ranked by lifetime value (total spend on non-cancelled orders)."""
        sql = text(
            """
            SELECT
                c.id AS customer_id,
                c.name,
                c.email,
                c.city,
                c.state,
                ROUND(SUM(o.total_amount), 2) AS total_spent,
                COUNT(o.id) AS total_orders
            FROM customers c
            JOIN orders o ON o.customer_id = c.id
            WHERE o.status != 'cancelled'
            GROUP BY c.id, c.name, c.email, c.city, c.state
            ORDER BY total_spent DESC
            LIMIT :limit
            """
        )

        rows = self.db.execute(sql, {"limit": limit}).fetchall()
        return [
            TopCustomer(
                customer_id=row.customer_id,
                name=row.name,
                email=row.email,
                city=row.city,
                state=row.state,
                total_spent=row.total_spent or 0.0,
                total_orders=row.total_orders or 0,
            )
            for row in rows
        ]

    def get_retention(self) -> List[MonthlyRetention]:
        """Return new vs returning customer counts per month for the last 12 months."""
        sql = text(
            """
            WITH customer_first_order AS (
                SELECT
                    customer_id,
                    MIN(DATE(created_at)) AS first_order_date
                FROM orders
                GROUP BY customer_id
            ),
            monthly_orders AS (
                SELECT
                    o.customer_id,
                    STRFTIME('%Y-%m', o.created_at) AS month,
                    cfo.first_order_date
                FROM orders o
                JOIN customer_first_order cfo ON cfo.customer_id = o.customer_id
                WHERE o.created_at >= DATE('now', '-12 months')
                GROUP BY o.customer_id, month
            )
            SELECT
                month,
                SUM(CASE WHEN STRFTIME('%Y-%m', first_order_date) = month THEN 1 ELSE 0 END) AS new_customers,
                SUM(CASE WHEN STRFTIME('%Y-%m', first_order_date) != month THEN 1 ELSE 0 END) AS returning_customers
            FROM monthly_orders
            GROUP BY month
            ORDER BY month
            """
        )

        rows = self.db.execute(sql).fetchall()
        return [
            MonthlyRetention(
                month=row.month,
                new_customers=row.new_customers or 0,
                returning_customers=row.returning_customers or 0,
            )
            for row in rows
        ]
