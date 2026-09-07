from decimal import Decimal
import uuid
from typing import Optional, Union

from app.database.db import get_connection
from app.repositories.billing_repository import BillingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.khata_repository import KhataRepository
from app.repositories.product_repository import ProductRepository


class StoreService:
    def __init__(self):
        self.products = ProductRepository()
        self.customers = CustomerRepository()
        self.billing = BillingRepository()
        self.khata = KhataRepository()

    def search_products(self, query: str):
        return self.products.search_products(query)

    def get_product(self, sku_or_name: str):
        exact = self.products.get_by_sku(sku_or_name)
        if exact:
            return exact
        return self.products.get_by_name(sku_or_name)

    def get_stock(self, sku: str):
        product = self.get_product(sku)
        if not product:
            raise ValueError("Product not found.")
        return {"sku": product["sku"], "product_name": product["product_name"], "current_stock": int(product["current_stock"]) }

    def receive_stock(self, sku: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        product = self.get_product(sku)
        if not product:
            raise ValueError("Product not found.")
        with get_connection() as conn:
            conn.execute("UPDATE products SET current_stock = current_stock + ?, updated_at = datetime('now') WHERE sku = ?", (int(quantity), sku))
            conn.execute("INSERT INTO stock_transactions (sku, delta, reason, created_at) VALUES (?, ?, ?, datetime('now'))", (sku, int(quantity), "receive_stock"))
            conn.commit()
        return self.get_stock(sku)

    def validate_sell_quantity(self, sku: str, quantity: int):
        product = self.get_product(sku)
        if not product:
            raise ValueError("Product not found.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if int(product["current_stock"]) < quantity:
            raise ValueError(f"Only {product['current_stock']} units are available. I can't sell {quantity}.")

    def create_draft_bill(self, customer_id: Optional[str] = None, customer_name: Optional[str] = None):
        draft_id = f"DRAFT-{uuid.uuid4().hex[:8]}"
        self.billing.create_draft_bill(customer_id, customer_name, draft_id)
        draft = self.billing.get_draft(draft_id)
        draft["id"] = draft["draft_id"]
        return draft

    def add_draft_item(self, draft_id: str, sku_or_name: str, quantity: int):
        product = self.get_product(sku_or_name)
        if not product:
            raise ValueError("Product not found.")
        self.validate_sell_quantity(product["sku"], quantity)
        draft = self.billing.get_draft(draft_id)
        if not draft:
            raise ValueError("Draft bill not found.")
        qty = int(quantity)
        self.billing.add_item(
            draft_id,
            product["sku"],
            product["product_name"],
            qty,
            product["selling_price"],
            float(product["gst_rate_pct"] or 0),
            product["hsn_code"],
        )
        draft = self.billing.get_draft(draft_id)
        draft["id"] = draft["draft_id"]
        draft["quantity"] = qty
        draft["product_name"] = product["product_name"]
        return draft

    def calculate_draft_bill(self, draft_id: str):
        draft = self.billing.get_draft(draft_id)
        if not draft:
            raise ValueError("Draft bill not found.")
        subtotal = Decimal("0")
        cgst_total = Decimal("0")
        sgst_total = Decimal("0")
        for item in draft["items"]:
            qty = Decimal(str(item["quantity"]))
            price = Decimal(str(item["unit_price"]))
            gst = Decimal(str(item["gst_rate_pct"] or "0"))
            taxable = qty * price
            tax_total = taxable * gst / Decimal("100")
            subtotal += taxable
            cgst_total += tax_total / Decimal("2")
            sgst_total += tax_total / Decimal("2")
        grand_total = subtotal + cgst_total + sgst_total
        return {
            "draft_id": draft_id,
            "subtotal": str(subtotal.quantize(Decimal("0.01"))),
            "cgst_total": str(cgst_total.quantize(Decimal("0.01"))),
            "sgst_total": str(sgst_total.quantize(Decimal("0.01"))),
            "grand_total": str(grand_total.quantize(Decimal("0.01"))),
            "items": draft["items"],
        }

    def finalize_bill(self, draft_id: str, payment_mode: Optional[str] = None, payment_reference: Optional[str] = None):
        draft = self.billing.get_draft(draft_id)
        if not draft or not draft["items"]:
            raise ValueError("Draft bill is empty.")
        calc = self.calculate_draft_bill(draft_id)
        subtotal = Decimal(str(calc["subtotal"]))
        cgst = Decimal(str(calc["cgst_total"]))
        sgst = Decimal(str(calc["sgst_total"]))
        grand_total = Decimal(str(calc["grand_total"]))

        with get_connection() as conn:
            customer_id = draft.get("customer_id")
            customer_name = draft.get("customer_name")
            bill_id = f"INV-{uuid.uuid4().hex[:8]}"
            conn.execute(
                "INSERT INTO bills (bill_id, customer_id, customer_name, bill_date, subtotal, cgst_total, sgst_total, grand_total, payment_mode, status, finalized_at) VALUES (?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, 'finalized', datetime('now'))",
                (bill_id, customer_id, customer_name, str(subtotal), str(cgst), str(sgst), str(grand_total), payment_mode or "CASH"),
            )
            for item in draft["items"]:
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
                self.validate_sell_quantity(item["sku"], int(item["quantity"]))
                conn.execute(
                    "UPDATE products SET current_stock = current_stock - ? WHERE sku = ?",
                    (int(item["quantity"]), item["sku"]),
                )
                conn.execute(
                    "INSERT INTO stock_transactions (sku, delta, reason, bill_id, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
                    (item["sku"], -int(item["quantity"]), "bill_finalization", bill_id),
                )
            conn.execute("UPDATE draft_bills SET status = 'closed', updated_at = datetime('now') WHERE draft_id = ?", (draft_id,))
            conn.execute("DELETE FROM draft_bill_items WHERE draft_id = ?", (draft_id,))
            conn.commit()
        payment = self.record_payment(bill_id, payment_mode or "CASH", grand_total, payment_reference or "")
        return {"bill_id": bill_id, "status": "finalized", "amount": str(grand_total), "outstanding_amount": Decimal("0.00"), "payment": payment}

    def record_payment(self, bill_id: str, payment_mode: str, amount: Union[Decimal, str], reference: Optional[str] = None):
        with get_connection() as conn:
            bill = conn.execute("SELECT * FROM bills WHERE bill_id = ?", (bill_id,)).fetchone()
            if not bill:
                raise ValueError("Bill not found.")
            payment_amount = Decimal(str(amount))
            if payment_amount <= 0:
                raise ValueError("Payment amount must be positive.")
            payment_id = f"PAY-{uuid.uuid4().hex[:8]}"
            conn.execute(
                "INSERT INTO payments (payment_id, bill_id, customer_id, amount, mode, reference, created_at) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
                (payment_id, bill_id, bill["customer_id"], str(payment_amount), payment_mode, reference or ""),
            )
            conn.commit()
            return {"payment_id": payment_id, "bill_id": bill_id, "amount": str(payment_amount.quantize(Decimal("0.01"))), "mode": payment_mode, "reference": reference or ""}

    def add_khata_transaction(self, customer_id: str, tx_type: str, amount: Union[Decimal, str], reference: str = ""):
        customer = self.customers.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found.")
        amount_decimal = Decimal(str(amount))
        if amount_decimal <= 0:
            raise ValueError("Khata amount must be positive.")
        tx = self.khata.add_transaction(customer_id, tx_type, str(amount_decimal.quantize(Decimal("0.01"))), reference)
        return tx

    def get_khata_balance(self, customer_id: str):
        customer = self.customers.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found.")
        return self.khata.get_balance(customer_id)

    def get_customer(self, customer_id: str):
        return self.customers.get_by_id(customer_id)

    def search_customers(self, query: str):
        return self.customers.search(query)

    def create_customer(self, customer_id: str, name: str, phone: Optional[str] = None):
        return self.customers.create(customer_id, name, phone)

    def set_preference(self, key: str, value: str, owner_id: str = "owner_001"):
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO preferences (owner_id, key, value, created_at) VALUES (?, ?, ?, datetime('now')) ON CONFLICT(owner_id, key) DO UPDATE SET value=excluded.value",
                (owner_id, key, value),
            )
            conn.commit()
        return {"owner_id": owner_id, "key": key, "value": value}

    def get_preference(self, key: str, owner_id: str = "owner_001"):
        with get_connection() as conn:
            row = conn.execute("SELECT value FROM preferences WHERE owner_id = ? AND key = ?", (owner_id, key)).fetchone()
            return row["value"] if row else None

    def get_outstanding_khata(self):
        return self.khata.get_outstanding()
