from app.database.db import get_connection


class KhataRepository:
    def get_balance(self, customer_id: str) -> float:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(CASE WHEN type='CREDIT' THEN CAST(amount AS REAL) ELSE -CAST(amount AS REAL) END), 0) AS balance FROM khata_transactions WHERE customer_id = ?",
                (customer_id,),
            ).fetchone()
            return float(row["balance"] or 0)

    def get_history(self, customer_id: str):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM khata_transactions WHERE customer_id = ? ORDER BY date DESC, id DESC",
                (customer_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def add_transaction(self, customer_id: str, transaction_type: str, amount: str, reference: str):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO khata_transactions (customer_id, date, type, amount, reference, created_at) VALUES (?, date('now'), ?, ?, ?, datetime('now'))",
                (customer_id, transaction_type.upper(), str(amount), reference),
            )
            conn.commit()
            return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, tx_id: int):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM khata_transactions WHERE id = ?", (tx_id,)).fetchone()
            return dict(row) if row else None

    def get_outstanding(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT customer_id, SUM(CASE WHEN type='CREDIT' THEN CAST(amount AS REAL) ELSE -CAST(amount AS REAL) END) AS balance FROM khata_transactions GROUP BY customer_id HAVING balance > 0 ORDER BY balance DESC"
            ).fetchall()
            return [dict(r) for r in rows]
