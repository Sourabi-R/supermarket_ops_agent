from app.services.analytics_service import AnalyticsService
from app.services.store_service import StoreService


class ToolCallingAgent:
    def __init__(self):
        self.store = StoreService()
        self.analytics = AnalyticsService()

    def _normalize(self, text: str) -> str:
        return " ".join((text or "").lower().split())

    def _find_product_name(self, message: str):
        lower = self._normalize(message)
        for keyword in ["for ", "about ", "of ", "on ", "the "]:
            if keyword in lower:
                suffix = lower.split(keyword, 1)[1]
                suffix = suffix.replace("?", "").strip()
                suffix = suffix.replace("remaining", "").replace("stock", "").replace("quantity", "").replace("left", "").replace("available", "").strip(" .:-_")
                if suffix:
                    return suffix
        for product in ["atta", "salt", "butter", "maggi", "milk", "soap", "oil", "dal", "parle"]:
            if product in lower:
                return product
        return ""

    def handle(self, message: str):
        lower = self._normalize(message)
        if not lower:
            return {"status": "assistant_ready"}

        if any(phrase in lower for phrase in ["sold out", "out of stock", "which products are sold out", "is sold out", "products sold out"]):
            return [p for p in self.store.products.list_all() if int(p.get("current_stock", 0) or 0) <= 0]
        if any(phrase in lower for phrase in ["low stock", "low in stock", "below reorder", "which products are low", "what is low", "what's low", "low inventory"]):
            return self.analytics.get_low_stock()
        if any(phrase in lower for phrase in [
            "what's in stock",
            "what is in stock",
            "which products are in stock",
            "which items are in stock",
            "show all stock",
            "all available stock",
            "available stock",
            "stock available",
            "available stocks",
            "what stock do i have",
            "what are the stock",
            "what are the stocks",
            "how much stock",
            "all products",
            "show stock",
            "available products",
        ]):
            return [p for p in self.store.products.list_all() if int(p.get("current_stock", 0) or 0) > 0]

        if any(phrase in lower for phrase in [
            "available quantity",
            "available qty",
            "how much stock is left",
            "how many units left",
            "how much quantity is left",
            "remaining quantity",
            "remaining stock",
            "left in stock",
            "current stock",
            "units left",
            "quantity left",
            "what is the stock of",
            "what is the available quantity of",
            "what's the stock of",
            "what is the current stock of",
        ]):
            query = self._find_product_name(message)
            if query:
                products = self.store.search_products(query)
                if products:
                    return products
            return [p for p in self.store.products.list_all() if int(p.get("current_stock", 0) or 0) > 0]

        if any(phrase in lower for phrase in ["remaining quantity", "left in stock", "how much stock is left", "units left", "how many units left", "remaining stock", "remaining qty"]):
            query = self._find_product_name(message)
            if query:
                products = self.store.search_products(query)
                if products:
                    return products
            return [p for p in self.store.products.list_all() if int(p.get("current_stock", 0) or 0) > 0]
        if "reorder" in lower:
            return self.analytics.get_reorder_report()
        if "sales" in lower and ("today" in lower or "summary" in lower):
            return self.analytics.get_sales_summary()
        if any(token in lower for token in ["atta", "salt", "butter", "milk", "soap", "maggi", "oil", "dal", "parle"]):
            product = self.store.search_products(lower)
            if product:
                return product
            return {"status": "not_found"}
        if "bill" in lower or "draft" in lower:
            return {"status": "billing_tooling_available"}
        if "credit" in lower or "khata" in lower or "owe" in lower:
            return {"status": "khata_tooling_available"}
        return {"status": "assistant_ready"}

    def answer(self, message: str) -> str:
        result = self.handle(message)
        lower = self._normalize(message)

        if isinstance(result, list):
            if not result:
                if any(phrase in lower for phrase in ["sold out", "out of stock", "which products are sold out"]):
                    return "No products are sold out right now."
                if any(phrase in lower for phrase in ["low stock", "low in stock", "which products are low"]):
                    return "Low stock check: no products are currently below their reorder levels."
                if any(phrase in lower for phrase in ["available stock", "stock available", "what are the stock", "what are the stocks", "all products", "what's in stock", "what is in stock"]):
                    return "There are no products currently available in stock."
                return "I checked the store data and there are no matching items right now."

            first = result[0]
            if "product_name" in first and "current_stock" in first:
                if any(phrase in lower for phrase in ["sold out", "out of stock"]):
                    items = [f"{row['product_name']}: sold out (0 left)" for row in result[:10]]
                    return "Sold out items:\n" + "\n".join(items)
                if any(phrase in lower for phrase in ["low stock", "low in stock", "which products are low", "what's low", "what is low"]):
                    items = [f"{row['product_name']}: {row['current_stock']} left (reorder level {row['reorder_level']})" for row in result[:10]]
                    return "Low stock alert:\n" + "\n".join(items)
                if any(phrase in lower for phrase in [
                    "available stock",
                    "stock available",
                    "what are the stock",
                    "what are the stocks",
                    "all products",
                    "what's in stock",
                    "what is in stock",
                    "available products",
                    "show all stock",
                ]):
                    items = [f"{row['product_name']}: {row['current_stock']} units" for row in result[:10]]
                    return "Available stock:\n" + "\n".join(items)
                if any(phrase in lower for phrase in [
                    "available quantity",
                    "available qty",
                    "how much stock is left",
                    "how many units left",
                    "remaining quantity",
                    "remaining stock",
                    "left in stock",
                    "units left",
                    "current stock",
                    "quantity left",
                    "what is the stock of",
                    "what is the available quantity of",
                    "what's the stock of",
                ]):
                    product = result[0]
                    return f"{product['product_name']} has {product['current_stock']} units remaining in stock."
                items = [f"{row['product_name']}: {row['current_stock']} left" for row in result[:5]]
                return "Inventory match:\n" + "\n".join(items)
            if "total_revenue" in first:
                return (
                    "Today’s sales summary: "
                    f"Revenue ₹{result.get('total_revenue', 0):,.2f}, "
                    f"Bills {result.get('bill_count', 0)}, "
                    f"Average bill ₹{result.get('avg_bill_value', 0):,.2f}."
                )
            return "I found matching records:\n" + "\n".join(
                f"- {item.get('product_name', item.get('sku', 'Item'))}" for item in result[:5]
            )

        if isinstance(result, dict):
            status = result.get("status")
            if status == "not_found":
                return "I could not find that item in the store inventory."
            if status in {"billing_tooling_available", "khata_tooling_available"}:
                return "I can help with billing, payment tracking, and khata records for this store."
            if status == "assistant_ready":
                return "I can help with stock checks, reorder suggestions, billing, payments, khata, and sales summaries."

        return "I’m ready to help with store operations, inventory, and sales questions."
