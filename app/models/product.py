from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    sku: str
    product_name: str
    brand: str
    category: str
    pack_size: str
    unit: str
    selling_price: Decimal
    cost_price: Decimal
    mrp: Decimal
    gst_rate_pct: Decimal
    hsn_code: str
    current_stock: int
    reorder_level: int
