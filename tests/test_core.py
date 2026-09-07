from decimal import Decimal

import os

from app.database.init_db import initialize_database
from app.services.store_service import StoreService
from app.services.analytics_service import AnalyticsService
from app.services.documents_service import generate_invoice_pdf, generate_analysis_pptx
from app.database.db import mark_update_processed, was_update_processed
from app.agent.tooling import ToolCallingAgent


DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "kirana_supermarket_demo_dataset.xlsx")


def setup_module():
    initialize_database(force_recreate=True, dataset_path=DATASET_PATH)


def test_database_initialization_and_products():
    service = StoreService()
    products = service.search_products("atta")
    assert len(products) >= 1
    assert any("Aashirvaad" in p["product_name"] for p in products)


def test_stock_lookup_and_receive():
    service = StoreService()
    stock = service.get_stock("SKU002")
    assert stock["current_stock"] >= 0
    item = service.receive_stock("SKU002", 12)
    assert item["current_stock"] >= stock["current_stock"]


def test_insufficient_stock_prevented():
    service = StoreService()
    product = service.get_product("SKU002")
    qty = int(product["current_stock"]) + 5
    try:
        service.validate_sell_quantity("SKU002", qty)
        assert False, "Oversell validation should have failed"
    except ValueError:
        pass


def test_bill_calculation_and_gst():
    service = StoreService()
    draft = service.create_draft_bill("C001", "Ramesh")
    quoted = service.add_draft_item(draft["id"], "SKU002", 2)
    assert quoted["quantity"] == 2
    bill = service.calculate_draft_bill(draft["id"])
    assert Decimal(str(bill["subtotal"])) > 0
    assert Decimal(str(bill["grand_total"])) >= Decimal(str(bill["subtotal"]))


def test_bill_finalization_and_payment_recording():
    service = StoreService()
    draft = service.create_draft_bill("C001", "Ramesh")
    service.add_draft_item(draft["id"], "SKU002", 1)
    final = service.finalize_bill(draft["id"], "UPI", "REF-123")
    assert final["status"] == "finalized"
    assert final["outstanding_amount"] >= 0
    payment = service.record_payment(final["bill_id"], "UPI", Decimal("30"), "REF-123")
    assert payment["amount"] == "30.00"


def test_khata_credit_payment_balance():
    service = StoreService()
    tx = service.add_khata_transaction("C001", "CREDIT", Decimal("500"), "test-credit")
    payment = service.add_khata_transaction("C001", "PAYMENT", Decimal("200"), "test-payment")
    assert tx["amount"] == "500.00"
    assert payment["amount"] == "200.00"
    balance = service.get_khata_balance("C001")
    assert Decimal(str(balance)) >= Decimal("0")


def test_duplicate_update_idempotency():
    assert not was_update_processed("telegram-test-1")
    mark_update_processed("telegram-test-1")
    assert was_update_processed("telegram-test-1")


def test_invoice_and_pptx_generation():
    service = StoreService()
    invoice_path = generate_invoice_pdf(service, output_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_outputs", "sample_invoice.pdf"))
    deck_path = generate_analysis_pptx(service, output_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_outputs", "sample_analysis_deck.pptx"))
    assert os.path.exists(invoice_path)
    assert os.path.exists(deck_path)


def test_analytics_and_reorder_report():
    analytics = AnalyticsService()
    sales_summary = analytics.get_sales_summary()
    reorder = analytics.get_reorder_report()
    attention = analytics.get_store_attention_report()
    assert sales_summary["total_revenue"] >= 0
    assert isinstance(reorder, list)
    assert isinstance(attention, list)


def test_agent_fallback_answer_generation():
    agent = ToolCallingAgent()
    result = agent.handle("what's low in stock?")
    response = agent.answer("what's low in stock?")
    assert isinstance(result, list)
    assert "stock" in response.lower() or "low" in response.lower()


def test_agent_stock_queries_for_low_and_sold_out_items():
    agent = ToolCallingAgent()
    sold_out = agent.answer("which products are sold out?")
    remaining = agent.answer("how much stock is left for atta?")
    assert "sold out" in sold_out.lower() or "out of stock" in sold_out.lower()
    assert "atta" in remaining.lower() or "units" in remaining.lower() or "left" in remaining.lower()


def test_agent_natural_language_stock_queries():
    agent = ToolCallingAgent()
    available = agent.answer("what is the available quantity of maggi?")
    in_stock = agent.answer("what's in stock?")
    assert "maggi" in available.lower() or "units" in available.lower() or "available" in available.lower()
    assert "stock" in in_stock.lower() or "available" in in_stock.lower() or "units" in in_stock.lower()
