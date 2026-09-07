import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from app.config.settings import DATASET_PATH, DB_PATH
from app.database.db import get_connection
from app.database.schema import create_schema


def clean_string(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def normalize_product_name(value: str) -> str:
    return " ".join(clean_string(value).split())


def normalize_unit(value: str) -> str:
    v = clean_string(value).lower()
    mapping = {
        "kilogram": "kg",
        "kg": "kg",
        "gram": "g",
        "gm": "g",
        "g": "g",
        "litre": "ltr",
        "liter": "ltr",
        "ltr": "ltr",
        "l": "ltr",
        "ml": "ml",
        "packet": "packet",
        "dozen": "dozen",
        "piece": "piece",
    }
    return mapping.get(v, v)


def normalize_pack_size(value: Any) -> str:
    return normalize_product_name(str(value)) if value is not None else ""


def normalize_customer_name(value: Any) -> str:
    name = clean_string(value)
    return name.title() if name else ""


def load_raw_excel(dataset_path: Optional[Union[str, os.PathLike]] = None) -> Dict[str, pd.DataFrame]:
    path = Path(dataset_path or DATASET_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Excel dataset not found: {path}")
    xl = pd.ExcelFile(path)
    sheets = {}
    for sheet in xl.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        df = df.rename(columns=lambda c: str(c).strip().lower().replace(" ", "_"))
        df.columns = [str(c).strip() for c in df.columns]
        sheets[sheet] = df
    return sheets


def initialize_database(force_recreate: bool = False, dataset_path: Optional[Union[str, os.PathLike]] = None) -> Path:
    path = Path(dataset_path or DATASET_PATH)
    if force_recreate and DB_PATH.exists():
        DB_PATH.unlink()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    create_schema()
    if not path.exists():
        raise FileNotFoundError(f"Dataset missing at {path}")

    sheets = load_raw_excel(path)

    with get_connection() as conn:
        conn.execute("DELETE FROM payments")
        conn.execute("DELETE FROM bill_items")
        conn.execute("DELETE FROM bills")
        conn.execute("DELETE FROM stock_transactions")
        conn.execute("DELETE FROM khata_transactions")
        conn.execute("DELETE FROM draft_bill_items")
        conn.execute("DELETE FROM draft_bills")
        conn.execute("DELETE FROM sales_history")
        conn.execute("DELETE FROM products")
        conn.execute("DELETE FROM customers")
        conn.execute("DELETE FROM preferences")
        conn.execute("DELETE FROM idempotency")

        products_df = sheets.get("products").copy()
        products_df.columns = [str(c).strip().lower().replace(" ", "_") for c in products_df.columns]
        for _, row in products_df.iterrows():
            name = normalize_product_name(row.get("product_name", ""))
            sku = clean_string(row.get("sku", ""))
            if not sku:
                continue
            conn.execute(
                """
                INSERT INTO products (
                    sku, product_name, brand, category, pack_size, unit,
                    selling_price, cost_price, mrp, gst_rate_pct, hsn_code,
                    current_stock, reorder_level, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (
                    sku,
                    name,
                    clean_string(row.get("brand", "")),
                    clean_string(row.get("category", "")),
                    normalize_pack_size(row.get("pack_size", "")),
                    normalize_unit(str(row.get("unit", ""))),
                    str(row.get("selling_price", "0")),
                    str(row.get("cost_price", "0")),
                    str(row.get("mrp", "0")),
                    float(row.get("gst_rate_pct", 0) or 0),
                    clean_string(row.get("hsn_code", "")),
                    int(row.get("opening_stock", 0) or 0),
                    int(row.get("reorder_level", 0) or 0),
                ),
            )

        customers_df = sheets.get("customers", pd.DataFrame()).copy()
        for _, row in customers_df.iterrows():
            customer_id = clean_string(row.get("customer_id", ""))
            if not customer_id:
                continue
            conn.execute(
                "INSERT INTO customers (customer_id, name, phone, created_at) VALUES (?, ?, ?, datetime('now'))",
                (customer_id, normalize_customer_name(row.get("name", "")), clean_string(row.get("phone", ""))),
            )

        sales_df = sheets.get("sales_history", pd.DataFrame()).copy()
        for _, row in sales_df.iterrows():
            conn.execute(
                "INSERT INTO sales_history (sale_date, invoice_no, sku, product_name, customer, quantity, unit_price, gst_rate_pct, payment_mode, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
                (
                    str(row.get("sale_date", "")),
                    clean_string(row.get("invoice_no", "")),
                    clean_string(row.get("sku", "")),
                    normalize_product_name(str(row.get("product_name", ""))),
                    clean_string(row.get("customer", "")),
                    int(row.get("quantity", 0) or 0),
                    str(row.get("unit_price", "0")),
                    float(row.get("gst_rate_pct", 0) or 0),
                    clean_string(row.get("payment_mode", "")),
                ),
            )

        khata_df = sheets.get("khata_transactions", pd.DataFrame()).copy()
        for _, row in khata_df.iterrows():
            customer_id = clean_string(row.get("customer_id", ""))
            if not customer_id:
                continue
            conn.execute(
                "INSERT INTO khata_transactions (customer_id, date, type, amount, reference, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                (
                    customer_id,
                    str(row.get("date", "")),
                    str(row.get("type", "")).upper(),
                    str(row.get("amount", "0")),
                    clean_string(row.get("reference", "")),
                ),
            )

        preferences_df = sheets.get("preferences", pd.DataFrame()).copy()
        for _, row in preferences_df.iterrows():
            owner_id = clean_string(row.get("owner_id", "owner_001"))
            key = clean_string(row.get("key", ""))
            if not key:
                continue
            conn.execute(
                "INSERT OR REPLACE INTO preferences (owner_id, key, value, created_at) VALUES (?, ?, ?, datetime('now'))",
                (owner_id, key, clean_string(row.get("value", ""))),
            )

    return DB_PATH


if __name__ == "__main__":
    initialize_database(force_recreate=True)
    print(f"Initialized {DB_PATH}")
