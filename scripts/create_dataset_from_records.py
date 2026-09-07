from __future__ import annotations

from pathlib import Path

import pandas as pd

def normalize_sku(value):
    text = str(value or "").strip().upper()
    if text.startswith("SKU"):
        return text
    if text.startswith("P") and text[1:].isdigit():
        return f"SKU{text[1:]}"
    return text


PRODUCTS = [
    {"sku": "P001", "product_name": "Aashirvaad Atta 5kg", "brand": "Aashirvaad", "category": "Staples", "pack_size": "5kg", "unit": "packet", "cost_price": 220, "selling_price": 245, "mrp": 260, "gst_rate_pct": 5, "hsn_code": "11010000", "opening_stock": 25, "reorder_level": 10},
    {"sku": "P002", "product_name": "Tata Salt 1kg", "brand": "Tata", "category": "Staples", "pack_size": "1kg", "unit": "packet", "cost_price": 24, "selling_price": 28, "mrp": 30, "gst_rate_pct": 5, "hsn_code": "25010010", "opening_stock": 40, "reorder_level": 15},
    {"sku": "P003", "product_name": "Amul Butter 100g", "brand": "Amul", "category": "Dairy", "pack_size": "100g", "unit": "packet", "cost_price": 52, "selling_price": 58, "mrp": 62, "gst_rate_pct": 12, "hsn_code": "04051000", "opening_stock": 18, "reorder_level": 8},
    {"sku": "P004", "product_name": "Fortune Sunflower Oil 1L", "brand": "Fortune", "category": "Cooking Oil", "pack_size": "1L", "unit": "litre", "cost_price": 105, "selling_price": 118, "mrp": 125, "gst_rate_pct": 5, "hsn_code": "15121910", "opening_stock": 20, "reorder_level": 8},
    {"sku": "P005", "product_name": "Maggi 70g", "brand": "Nestle", "category": "Instant Food", "pack_size": "70g", "unit": "packet", "cost_price": 11, "selling_price": 13, "mrp": 14, "gst_rate_pct": 12, "hsn_code": "19023000", "opening_stock": 50, "reorder_level": 15},
    {"sku": "P006", "product_name": "Parle-G 800g", "brand": "Parle", "category": "Biscuits", "pack_size": "800g", "unit": "packet", "cost_price": 38, "selling_price": 45, "mrp": 50, "gst_rate_pct": 12, "hsn_code": "19053100", "opening_stock": 30, "reorder_level": 10},
    {"sku": "P007", "product_name": "Surf Excel 1kg", "brand": "Surf Excel", "category": "Home Care", "pack_size": "1kg", "unit": "packet", "cost_price": 105, "selling_price": 125, "mrp": 140, "gst_rate_pct": 18, "hsn_code": "34022010", "opening_stock": 12, "reorder_level": 5},
    {"sku": "P008", "product_name": "Colgate 100g", "brand": "Colgate", "category": "Personal Care", "pack_size": "100g", "unit": "packet", "cost_price": 48, "selling_price": 58, "mrp": 65, "gst_rate_pct": 18, "hsn_code": "33061010", "opening_stock": 15, "reorder_level": 5},
    {"sku": "P009", "product_name": "Sugar", "brand": "Loose Staples", "category": "Staples", "pack_size": "1kg", "unit": "kg", "cost_price": 40, "selling_price": 45, "mrp": 45, "gst_rate_pct": 0, "hsn_code": "17019990", "opening_stock": 60, "reorder_level": 20},
    {"sku": "P010", "product_name": "Rice", "brand": "Loose Staples", "category": "Staples", "pack_size": "1kg", "unit": "kg", "cost_price": 48, "selling_price": 55, "mrp": 55, "gst_rate_pct": 0, "hsn_code": "10063090", "opening_stock": 75, "reorder_level": 25},
    {"sku": "P011", "product_name": "Toor Dal", "brand": "Loose Staples", "category": "Pulses", "pack_size": "1kg", "unit": "kg", "cost_price": 110, "selling_price": 125, "mrp": 125, "gst_rate_pct": 0, "hsn_code": "07136000", "opening_stock": 25, "reorder_level": 10},
    {"sku": "P012", "product_name": "Moong Dal", "brand": "Loose Staples", "category": "Pulses", "pack_size": "1kg", "unit": "kg", "cost_price": 105, "selling_price": 120, "mrp": 120, "gst_rate_pct": 0, "hsn_code": "07133100", "opening_stock": 18, "reorder_level": 8},
    {"sku": "P013", "product_name": "Amul Milk 500ml", "brand": "Amul", "category": "Dairy", "pack_size": "500ml", "unit": "packet", "cost_price": 27, "selling_price": 30, "mrp": 30, "gst_rate_pct": 0, "hsn_code": "04011000", "opening_stock": 35, "reorder_level": 12},
    {"sku": "P014", "product_name": "Cadbury Dairy Milk 50g", "brand": "Cadbury", "category": "Chocolate", "pack_size": "50g", "unit": "packet", "cost_price": 35, "selling_price": 45, "mrp": 50, "gst_rate_pct": 18, "hsn_code": "18063100", "opening_stock": 10, "reorder_level": 5},
    {"sku": "P015", "product_name": "Lifebuoy Soap 100g", "brand": "Lifebuoy", "category": "Personal Care", "pack_size": "100g", "unit": "piece", "cost_price": 28, "selling_price": 35, "mrp": 40, "gst_rate_pct": 18, "hsn_code": "34011190", "opening_stock": 0, "reorder_level": 5},
]
PRODUCTS = [{**p, "sku": normalize_sku(p["sku"])} for p in PRODUCTS]

CUSTOMERS = [
    {"customer_id": "C001", "name": "Ramesh", "phone": ""},
    {"customer_id": "C002", "name": "Suresh", "phone": ""},
    {"customer_id": "C003", "name": "Priya", "phone": ""},
    {"customer_id": "C004", "name": "Anitha", "phone": ""},
    {"customer_id": "C005", "name": "Karthik", "phone": ""},
]

SALES_HISTORY = [
    {"sale_date": "2026-09-01", "invoice_no": "B001", "sku": "P009", "product_name": "Sugar", "customer": "", "quantity": 2, "unit_price": 45, "gst_rate_pct": 0, "payment_mode": "UPI"},
    {"sale_date": "2026-09-01", "invoice_no": "B001", "sku": "P005", "product_name": "Maggi 70g", "customer": "", "quantity": 4, "unit_price": 13, "gst_rate_pct": 12, "payment_mode": "UPI"},
    {"sale_date": "2026-09-01", "invoice_no": "B001", "sku": "P002", "product_name": "Tata Salt 1kg", "customer": "", "quantity": 3, "unit_price": 28, "gst_rate_pct": 5, "payment_mode": "UPI"},
    {"sale_date": "2026-09-01", "invoice_no": "B002", "sku": "P001", "product_name": "Aashirvaad Atta 5kg", "customer": "Ramesh", "quantity": 1, "unit_price": 245, "gst_rate_pct": 5, "payment_mode": "Cash"},
    {"sale_date": "2026-09-01", "invoice_no": "B002", "sku": "P006", "product_name": "Parle-G 800g", "customer": "Ramesh", "quantity": 1, "unit_price": 45, "gst_rate_pct": 12, "payment_mode": "Cash"},
    {"sale_date": "2026-09-01", "invoice_no": "B002", "sku": "P009", "product_name": "Sugar", "customer": "Ramesh", "quantity": 1, "unit_price": 45, "gst_rate_pct": 0, "payment_mode": "Cash"},
    {"sale_date": "2026-09-02", "invoice_no": "B003", "sku": "P004", "product_name": "Fortune Sunflower Oil 1L", "customer": "", "quantity": 2, "unit_price": 118, "gst_rate_pct": 5, "payment_mode": "Card"},
    {"sale_date": "2026-09-02", "invoice_no": "B003", "sku": "P007", "product_name": "Surf Excel 1kg", "customer": "", "quantity": 1, "unit_price": 125, "gst_rate_pct": 18, "payment_mode": "Card"},
    {"sale_date": "2026-09-02", "invoice_no": "B003", "sku": "P010", "product_name": "Rice", "customer": "", "quantity": 5, "unit_price": 55, "gst_rate_pct": 0, "payment_mode": "Card"},
    {"sale_date": "2026-09-02", "invoice_no": "B004", "sku": "P003", "product_name": "Amul Butter 100g", "customer": "Suresh", "quantity": 2, "unit_price": 58, "gst_rate_pct": 12, "payment_mode": "UPI"},
    {"sale_date": "2026-09-02", "invoice_no": "B004", "sku": "P005", "product_name": "Maggi 70g", "customer": "Suresh", "quantity": 6, "unit_price": 13, "gst_rate_pct": 12, "payment_mode": "UPI"},
    {"sale_date": "2026-09-02", "invoice_no": "B004", "sku": "P009", "product_name": "Sugar", "customer": "Suresh", "quantity": 4, "unit_price": 45, "gst_rate_pct": 0, "payment_mode": "UPI"},
]

KHATA = [
    {"transaction_id": "K001", "customer_id": "C001", "date": "2026-09-01", "type": "CREDIT", "amount": 500, "reference": "Initial credit"},
    {"transaction_id": "K002", "customer_id": "C001", "date": "2026-09-03", "type": "PAYMENT", "amount": 300, "reference": "UPI"},
    {"transaction_id": "K003", "customer_id": "C002", "date": "2026-09-02", "type": "CREDIT", "amount": 400, "reference": "Initial credit"},
    {"transaction_id": "K004", "customer_id": "C002", "date": "2026-09-04", "type": "PAYMENT", "amount": 200, "reference": "UPI"},
    {"transaction_id": "K005", "customer_id": "C003", "date": "2026-09-03", "type": "CREDIT", "amount": 750, "reference": "Open account"},
    {"transaction_id": "K006", "customer_id": "C004", "date": "2026-09-04", "type": "CREDIT", "amount": 300, "reference": "Open account"},
    {"transaction_id": "K007", "customer_id": "C005", "date": "2026-09-05", "type": "CREDIT", "amount": 500, "reference": "Open account"},
    {"transaction_id": "K008", "customer_id": "C005", "date": "2026-09-06", "type": "PAYMENT", "amount": 250, "reference": "Cash"},
]

PREFERENCES = [
    {"owner_id": "owner_001", "key": "default_payment", "value": "UPI"},
    {"owner_id": "owner_001", "key": "default_atta", "value": "Aashirvaad Atta 5kg"},
    {"owner_id": "owner_001", "key": "shop_name", "value": "Sri Lakshmi Stores"},
]


def build_datasets():
    products_df = pd.DataFrame(PRODUCTS)
    products_df = products_df[["sku", "product_name", "brand", "category", "pack_size", "unit", "selling_price", "cost_price", "mrp", "gst_rate_pct", "hsn_code", "opening_stock", "reorder_level"]]

    customers_df = pd.DataFrame(CUSTOMERS)
    customers_df = customers_df[["customer_id", "name", "phone"]]

    sales_df = pd.DataFrame(SALES_HISTORY)
    sales_df["sku"] = sales_df["sku"].map(normalize_sku)
    sales_df = sales_df[["sale_date", "invoice_no", "sku", "product_name", "customer", "quantity", "unit_price", "gst_rate_pct", "payment_mode"]]

    khata_df = pd.DataFrame(KHATA)
    khata_df = khata_df[["transaction_id", "customer_id", "date", "type", "amount", "reference"]]

    preferences_df = pd.DataFrame(PREFERENCES)
    preferences_df = preferences_df[["owner_id", "key", "value"]]

    return {
        "products": products_df,
        "customers": customers_df,
        "sales_history": sales_df,
        "khata_transactions": khata_df,
        "preferences": preferences_df,
    }


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "kirana_supermarket_demo_dataset.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    datasets = build_datasets()
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in datasets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Generated dataset: {output_path}")
    for name, df in datasets.items():
        print(name, df.shape)
