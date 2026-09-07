from app.database.db import get_connection


class CustomerRepository:
    def get_by_id(self, customer_id: str):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
            return dict(row) if row else None

    def search(self, query: str):
        q = f"%{query}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM customers WHERE LOWER(name) LIKE LOWER(?) OR LOWER(customer_id) LIKE LOWER(?) ORDER BY name LIMIT 20",
                (q, q),
            ).fetchall()
            return [dict(r) for r in rows]

    def create(self, customer_id: str, name: str, phone: str = None):
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO customers (customer_id, name, phone, created_at) VALUES (?, ?, ?, datetime('now'))",
                (customer_id, name, phone),
            )
            conn.commit()
            return self.get_by_id(customer_id)
