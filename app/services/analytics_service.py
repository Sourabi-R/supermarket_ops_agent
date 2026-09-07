from decimal import Decimal

from app.database.db import get_connection


class AnalyticsService:
    def get_sales_summary(self):
        with get_connection() as conn:
            result = conn.execute(
                """
                SELECT
                    COUNT(DISTINCT bill_id) AS bill_count,
                    COALESCE(SUM(CAST(grand_total AS REAL)), 0) AS total_revenue,
                    AVG(CAST(grand_total AS REAL)) AS avg_bill_value,
                    SUM(CASE WHEN payment_mode = 'CASH' THEN CAST(grand_total AS REAL) ELSE 0 END) AS cash_sales,
                    SUM(CASE WHEN payment_mode = 'UPI' THEN CAST(grand_total AS REAL) ELSE 0 END) AS upi_sales,
                    SUM(CASE WHEN payment_mode = 'CARD' THEN CAST(grand_total AS REAL) ELSE 0 END) AS card_sales
                FROM bills
                WHERE status = 'finalized'
                """
            ).fetchone()
            return {
                "bill_count": int(result["bill_count"] or 0),
                "total_revenue": float(result["total_revenue"] or 0),
                "avg_bill_value": float(result["avg_bill_value"] or 0),
                "cash_sales": float(result["cash_sales"] or 0),
                "upi_sales": float(result["upi_sales"] or 0),
                "card_sales": float(result["card_sales"] or 0),
            }

    def get_top_products(self, limit: int = 5):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT product_name, SUM(quantity) AS qty
                FROM bill_items
                GROUP BY product_name
                ORDER BY qty DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_reorder_report(self):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT p.product_name, p.current_stock, p.reorder_level, p.selling_price,
                       CASE WHEN p.current_stock <= 0 THEN 0 ELSE p.reorder_level - p.current_stock END AS suggested_qty
                FROM products p
                WHERE p.current_stock <= p.reorder_level
                ORDER BY p.current_stock ASC
                """
            ).fetchall()
            return [dict(r) for r in rows]

    def get_store_attention_report(self):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT product_name, current_stock, reorder_level
                FROM products
                WHERE current_stock <= reorder_level
                ORDER BY current_stock ASC
                LIMIT 10
                """
            ).fetchall()
            return [dict(r) for r in rows]

    def get_low_stock(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT product_name, current_stock, reorder_level FROM products WHERE current_stock <= reorder_level ORDER BY current_stock ASC"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_morning_brief(self):
        summary = self.get_sales_summary()
        top = self.get_top_products(5)
        low = self.get_low_stock()
        with get_connection() as conn:
            khata = conn.execute(
                "SELECT COALESCE(SUM(CASE WHEN type='CREDIT' THEN CAST(amount AS REAL) ELSE -CAST(amount AS REAL) END), 0) AS balance FROM khata_transactions"
            ).fetchone()
            pay = conn.execute(
                "SELECT mode, SUM(CAST(amount AS REAL)) AS total FROM payments GROUP BY mode"
            ).fetchall()
        return {
            "revenue": summary["total_revenue"],
            "bill_count": summary["bill_count"],
            "avg_bill_value": summary["avg_bill_value"],
            "top_products": top,
            "payment_mix": [dict(r) for r in pay],
            "low_stock": low,
            "outstanding_khata": float(khata["balance"] or 0),
        }
