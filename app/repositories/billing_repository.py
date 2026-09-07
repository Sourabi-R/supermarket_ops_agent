from decimal import Decimal
from typing import Any

from app.database.db import get_connection


class BillingRepository:
    def create_draft_bill(self, customer_id: str, customer_name: str, draft_id: str):
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO draft_bills (draft_id, customer_id, customer_name, created_at, updated_at, status) VALUES (?, ?, ?, datetime('now'), datetime('now'), 'open')",
                (draft_id, customer_id, customer_name),
            )
            conn.commit()
            return self.get_draft(draft_id)

    def get_draft(self, draft_id: str):
        with get_connection() as conn:
            draft = conn.execute("SELECT * FROM draft_bills WHERE draft_id = ?", (draft_id,)).fetchone()
            if not draft:
                return None
            items = conn.execute("SELECT * FROM draft_bill_items WHERE draft_id = ? ORDER BY id", (draft_id,)).fetchall()
            return {**dict(draft), "items": [dict(item) for item in items]}

    def add_item(self, draft_id: str, sku: str, product_name: str, quantity: int, unit_price: str, gst_rate_pct: float, hsn_code: str):
        with get_connection() as conn:
            existing = conn.execute(
                "SELECT * FROM draft_bill_items WHERE draft_id = ? AND sku = ?",
                (draft_id, sku),
            ).fetchone()
            if existing:
                new_qty = int(existing["quantity"]) + quantity
                conn.execute(
                    "UPDATE draft_bill_items SET quantity = ?, taxable_amount = ?, cgst = ?, sgst = ?, line_total = ? WHERE id = ?",
                    (
                        new_qty,
                        str(Decimal(str(existing["unit_price"])) * new_qty),
                        str((Decimal(str(existing["unit_price"])) * new_qty * Decimal(str(existing["gst_rate_pct"])) / Decimal("100")) / Decimal("2")),
                        str((Decimal(str(existing["unit_price"])) * new_qty * Decimal(str(existing["gst_rate_pct"])) / Decimal("100")) / Decimal("2")),
                        str((Decimal(str(existing["unit_price"])) * new_qty) + ((Decimal(str(existing["unit_price"])) * new_qty * Decimal(str(existing["gst_rate_pct"])) / Decimal("100")))),
                        existing["id"],
                    ),
                )
            else:
                taxable = Decimal(str(unit_price)) * quantity
                gst_total = taxable * Decimal(str(gst_rate_pct)) / Decimal("100")
                cgst = gst_total / Decimal("2")
                sgst = gst_total / Decimal("2")
                line_total = taxable + gst_total
                conn.execute(
                    "INSERT INTO draft_bill_items (draft_id, sku, product_name, quantity, unit_price, gst_rate_pct, taxable_amount, cgst, sgst, line_total, hsn_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        draft_id,
                        sku,
                        product_name,
                        quantity,
                        str(unit_price),
                        float(gst_rate_pct),
                        str(taxable),
                        str(cgst),
                        str(sgst),
                        str(line_total),
                        hsn_code,
                    ),
                )
            conn.commit()
            return self.get_draft(draft_id)

    def remove_item(self, draft_id: str, item_id: int):
        with get_connection() as conn:
            conn.execute("DELETE FROM draft_bill_items WHERE draft_id = ? AND id = ?", (draft_id, item_id))
            conn.commit()
            return self.get_draft(draft_id)

    def upsert_bill(self, bill_id: str, customer_id: str, customer_name: str, subtotal: str, cgst_total: str, sgst_total: str, grand_total: str, payment_mode: str = None):
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO bills (bill_id, customer_id, customer_name, bill_date, subtotal, cgst_total, sgst_total, grand_total, payment_mode, status, finalized_at)
                VALUES (?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, 'finalized', datetime('now'))
                ON CONFLICT(bill_id) DO UPDATE SET
                    customer_id=excluded.customer_id,
                    customer_name=excluded.customer_name,
                    subtotal=excluded.subtotal,
                    cgst_total=excluded.cgst_total,
                    sgst_total=excluded.sgst_total,
                    grand_total=excluded.grand_total,
                    payment_mode=excluded.payment_mode,
                    status='finalized',
                    finalized_at=datetime('now')
                """,
                (bill_id, customer_id, customer_name, subtotal, cgst_total, sgst_total, grand_total, payment_mode),
            )
            conn.commit()
            return self.get_bill(bill_id)

    def get_bill(self, bill_id: str):
        with get_connection() as conn:
            bill = conn.execute("SELECT * FROM bills WHERE bill_id = ?", (bill_id,)).fetchone()
            if not bill:
                return None
            items = conn.execute("SELECT * FROM bill_items WHERE bill_id = ? ORDER BY id", (bill_id,)).fetchall()
            return {**dict(bill), "items": [dict(item) for item in items]}

    def set_bill_items(self, bill_id: str, items):
        with get_connection() as conn:
            for item in items:
                conn.execute(
                    "INSERT INTO bill_items (bill_id, sku, product_name, quantity, unit_price, gst_rate_pct, taxable_amount, cgst, sgst, line_total, hsn_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        bill_id,
                        item["sku"],
                        item["product_name"],
                        int(item["quantity"]),
                        str(item["unit_price"]),
                        float(item.get("gst_rate_pct", 0) or 0),
                        str(item["taxable_amount"]),
                        str(item["cgst"]),
                        str(item["sgst"]),
                        str(item["line_total"]),
                        item.get("hsn_code", ""),
                    ),
                )
            conn.commit()

    def get_open_drafts(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM draft_bills WHERE status = 'open' ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]
