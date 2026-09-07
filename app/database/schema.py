from app.database.db import get_connection


CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        product_name TEXT NOT NULL,
        brand TEXT,
        category TEXT,
        pack_size TEXT,
        unit TEXT,
        selling_price TEXT,
        cost_price TEXT,
        mrp TEXT,
        gst_rate_pct REAL,
        hsn_code TEXT,
        current_stock INTEGER DEFAULT 0,
        reorder_level INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sales_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date TEXT,
        invoice_no TEXT,
        sku TEXT,
        product_name TEXT,
        customer TEXT,
        quantity INTEGER,
        unit_price TEXT,
        gst_rate_pct REAL,
        payment_mode TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bills (
        bill_id TEXT PRIMARY KEY,
        customer_id TEXT,
        customer_name TEXT,
        bill_date TEXT,
        subtotal TEXT,
        cgst_total TEXT,
        sgst_total TEXT,
        grand_total TEXT,
        payment_mode TEXT,
        status TEXT DEFAULT 'draft',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        finalized_at TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id TEXT NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price TEXT NOT NULL,
        gst_rate_pct REAL,
        taxable_amount TEXT,
        cgst TEXT,
        sgst TEXT,
        line_total TEXT,
        hsn_code TEXT,
        FOREIGN KEY(bill_id) REFERENCES bills(bill_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        delta INTEGER NOT NULL,
        reason TEXT,
        bill_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sku) REFERENCES products(sku)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS payments (
        payment_id TEXT PRIMARY KEY,
        bill_id TEXT,
        customer_id TEXT,
        amount TEXT,
        mode TEXT,
        reference TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(bill_id) REFERENCES bills(bill_id),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS khata_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT NOT NULL,
        date TEXT,
        type TEXT CHECK(type IN ('CREDIT','PAYMENT')),
        amount TEXT,
        reference TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id TEXT,
        key TEXT,
        value TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(owner_id, key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS idempotency (
        update_id TEXT PRIMARY KEY,
        processed_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS draft_bills (
        draft_id TEXT PRIMARY KEY,
        customer_id TEXT,
        customer_name TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'open',
        note TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS draft_bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        draft_id TEXT NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price TEXT NOT NULL,
        gst_rate_pct REAL,
        taxable_amount TEXT,
        cgst TEXT,
        sgst TEXT,
        line_total TEXT,
        hsn_code TEXT,
        FOREIGN KEY(draft_id) REFERENCES draft_bills(draft_id)
    )
    """,
]


def create_schema() -> None:
    with get_connection() as conn:
        for stmt in CREATE_TABLES_SQL:
            conn.execute(stmt)
        conn.commit()
