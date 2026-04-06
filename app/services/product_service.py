"""Service layer for product-related analytics queries."""

from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.schemas import CategoryRevenue, LowStockProduct, TopProduct


class ProductService:
    """Handles all product analytics queries using raw SQL with CTEs."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_top_products(
        self, limit: int = 10, category_id: Optional[int] = None
    ) -> List[TopProduct]:
        """Return top products ranked by revenue, optionally filtered by category."""
        category_filter = "AND p.category_id = :category_id" if category_id else ""
        params: dict = {"limit": limit}
        if category_id:
            params["category_id"] = category_id

        sql = text(
            f"""
            WITH product_stats AS (
                SELECT
                    p.id AS product_id,
                    p.name AS product_name,
                    c.name AS category,
                    SUM(oi.total_price) AS total_revenue,
                    SUM((oi.unit_price - p.cost_price) * oi.quantity) AS total_profit,
                    SUM(oi.quantity) AS units_sold
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                JOIN categories c ON c.id = p.category_id
                JOIN orders o ON o.id = oi.order_id
                WHERE o.status != 'cancelled'
                {category_filter}
                GROUP BY p.id, p.name, c.name
            )
            SELECT
                product_id,
                product_name,
                category,
                ROUND(total_revenue, 2) AS total_revenue,
                ROUND(total_profit, 2) AS total_profit,
                units_sold
            FROM product_stats
            ORDER BY total_revenue DESC
            LIMIT :limit
            """
        )

        rows = self.db.execute(sql, params).fetchall()
        return [
            TopProduct(
                product_id=row.product_id,
                product_name=row.product_name,
                category=row.category,
                total_revenue=row.total_revenue or 0.0,
                total_profit=row.total_profit or 0.0,
                units_sold=row.units_sold or 0,
            )
            for row in rows
        ]

    def get_category_revenue(self) -> List[CategoryRevenue]:
        """Return revenue breakdown and percentage share per category."""
        sql = text(
            """
            WITH cat_stats AS (
                SELECT
                    c.name AS category,
                    SUM(oi.total_price) AS total_revenue,
                    COUNT(DISTINCT o.id) AS order_count
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                JOIN categories c ON c.id = p.category_id
                JOIN orders o ON o.id = oi.order_id
                WHERE o.status != 'cancelled'
                GROUP BY c.name
            ),
            grand AS (
                SELECT SUM(total_revenue) AS grand_total FROM cat_stats
            )
            SELECT
                cs.category,
                ROUND(cs.total_revenue, 2) AS total_revenue,
                ROUND(CAST(cs.total_revenue AS FLOAT) / g.grand_total * 100, 2) AS percentage,
                cs.order_count
            FROM cat_stats cs, grand g
            ORDER BY cs.total_revenue DESC
            """
        )

        rows = self.db.execute(sql).fetchall()
        return [
            CategoryRevenue(
                category=row.category,
                total_revenue=row.total_revenue or 0.0,
                percentage=row.percentage or 0.0,
                order_count=row.order_count or 0,
            )
            for row in rows
        ]

    def get_low_stock(self, threshold: int = 10) -> List[LowStockProduct]:
        """Return products whose current stock is at or below the given threshold."""
        sql = text(
            """
            SELECT
                p.id AS product_id,
                p.name AS product_name,
                p.sku,
                c.name AS category,
                p.stock,
                ROUND(p.price, 2) AS price
            FROM products p
            JOIN categories c ON c.id = p.category_id
            WHERE p.stock <= :threshold
            ORDER BY p.stock ASC
            """
        )

        rows = self.db.execute(sql, {"threshold": threshold}).fetchall()
        return [
            LowStockProduct(
                product_id=row.product_id,
                product_name=row.product_name,
                sku=row.sku,
                category=row.category,
                stock=row.stock,
                price=row.price,
            )
            for row in rows
        ]
