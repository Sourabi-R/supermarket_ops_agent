from decimal import Decimal
import sqlite3

from app.database.db import get_connection


class ProductRepository:
    def search_products(self, query: str):
        q = f"%{query.strip()}%"
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT sku, product_name, brand, category, pack_size, unit, selling_price, cost_price, mrp,
                       gst_rate_pct, hsn_code, current_stock, reorder_level
                FROM products
                WHERE LOWER(product_name) LIKE LOWER(?)
                   OR LOWER(brand) LIKE LOWER(?)
                   OR LOWER(sku) LIKE LOWER(?)
                ORDER BY product_name
                LIMIT 20
                """,
                (q, q, q),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_by_sku(self, sku: str):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE sku = ?",
                (sku,),
            ).fetchone()
            return dict(row) if row else None

    def get_by_name(self, name: str):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE LOWER(product_name) = LOWER(?)",
                (name,),
            ).fetchone()
            return dict(row) if row else None

    def get_low_stock(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM products WHERE current_stock <= reorder_level ORDER BY current_stock ASC"
            ).fetchall()
            return [dict(r) for r in rows]

    def update_stock(self, sku: str, delta: int, reason: str = None, bill_id: str = None):
        with get_connection() as conn:
            conn.execute(
                "UPDATE products SET current_stock = current_stock + ?, updated_at = datetime('now') WHERE sku = ?",
                (delta, sku),
            )
            conn.execute(
                "INSERT INTO stock_transactions (sku, delta, reason, bill_id, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
                (sku, delta, reason, bill_id),
            )
            conn.commit()

    def create_product(self, payload: dict):
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products (
                    sku, product_name, brand, category, pack_size, unit,
                    selling_price, cost_price, mrp, gst_rate_pct, hsn_code,
                    current_stock, reorder_level, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (
                    payload["sku"],
                    payload["product_name"],
                    payload.get("brand", ""),
                    payload.get("category", ""),
                    payload.get("pack_size", ""),
                    payload.get("unit", ""),
                    str(payload.get("selling_price", "0")),
                    str(payload.get("cost_price", "0")),
                    str(payload.get("mrp", "0")),
                    float(payload.get("gst_rate_pct", 0) or 0),
                    payload.get("hsn_code", ""),
                    int(payload.get("current_stock", 0) or 0),
                    int(payload.get("reorder_level", 0) or 0),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def list_all(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM products ORDER BY product_name").fetchall()
            return [dict(r) for r in rows]
