import html
import json
import logging
import os
from decimal import Decimal

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters

from app.config.settings import TELEGRAM_BOT_TOKEN
from app.database.db import mark_update_processed, was_update_processed
from app.agent.tooling import ToolCallingAgent
from app.services.analytics_service import AnalyticsService
from app.services.store_service import StoreService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

store_service = StoreService()
analytics = AnalyticsService()
agent = ToolCallingAgent()


def _format_money(value):
    return f"₹{Decimal(str(value)).quantize(Decimal('0.01')):,.2f}"


def _contains_any(text: str, *keywords: str) -> bool:
    return any(keyword in text for keyword in keywords)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Sri Lakshmi Stores. Ask me anything about stock, billing, khata, or sales.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message is None:
        return
    update_id = str(update.update_id)
    if was_update_processed(update_id):
        return
    mark_update_processed(update_id)

    message = update.effective_message.text or ""
    text = message.strip()
    if not text:
        return

    lower = text.lower()
    if "good morning" in lower or "morning brief" in lower:
        brief = analytics.get_morning_brief()
        response = [
            "*Morning store brief*",
            f"Revenue: {_format_money(brief['revenue'])}",
            f"Bills: {brief['bill_count']}",
            f"Average bill value: {_format_money(brief['avg_bill_value'])}",
            "Top products:",
        ]
        for item in brief['top_products'][:3]:
            response.append(f"- {item['product_name']}: {item['qty']} sold")
        response.append("Low stock:")
        for item in brief['low_stock'][:3]:
            response.append(f"- {item['product_name']}: {item['current_stock']} left")
        await update.message.reply_text("\n".join(response), parse_mode="Markdown")
        return

    if "what needs my attention" in lower or "needs my attention" in lower:
        attention = analytics.get_store_attention_report()
        if not attention:
            await update.message.reply_text("Nothing urgent is showing in the data right now.")
            return
        lines = ["*What needs my attention?*"]
        for item in attention[:5]:
            lines.append(f"- {item['product_name']}: {item['current_stock']} left, reorder level {item['reorder_level']}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if any(phrase in lower for phrase in ["sold out", "out of stock", "which products are sold out", "which item is sold out"]):
        sold_out = [p for p in store_service.products.list_all() if int(p.get("current_stock", 0) or 0) <= 0]
        if not sold_out:
            await update.message.reply_text("No products are sold out right now.")
            return
        lines = ["*Sold out items*"]
        for item in sold_out[:10]:
            lines.append(f"- {item['product_name']}: 0 left")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if any(phrase in lower for phrase in ["what's low in stock", "low in stock", "low stock", "which products are low", "low inventory"]):
        low = analytics.get_low_stock()
        if not low:
            await update.message.reply_text("No products are currently low in stock.")
            return
        lines = ["*Low stock report*"]
        for row in low[:10]:
            lines.append(f"- {row['product_name']}: {row['current_stock']} left (reorder level {row['reorder_level']})")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if any(phrase in lower for phrase in ["what are the stock", "what are the stocks", "stock available", "stocks available", "available stock", "what stock do i have", "all available stock", "all stock", "show all products"]) :
        products = [p for p in store_service.products.list_all() if int(p.get("current_stock", 0) or 0) > 0]
        if not products:
            await update.message.reply_text("No products are available in the store right now.")
            return
        lines = ["*Available stock*"]
        for item in products[:10]:
            lines.append(f"- {item['product_name']}: {item['current_stock']} units")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if any(phrase in lower for phrase in ["how much stock is left", "how many units left", "remaining quantity", "remaining stock", "units left", "left in stock"]):
        product_query = text
        for phrase in ["how much stock is left", "how many units left", "remaining quantity", "remaining stock", "units left", "left in stock", "for "]:
            if phrase in lower:
                if phrase == "for ":
                    product_query = text.split("for", 1)[1] if "for" in text.lower() else text
                else:
                    product_query = text.lower().replace(phrase, "", 1)
                break
        product_query = product_query.strip().strip("?").strip()
        if not product_query:
            await update.message.reply_text("Tell me which product you want the remaining quantity for.")
            return
        matches = store_service.search_products(product_query)
        if not matches:
            await update.message.reply_text(f"I couldn’t find any product matching '{product_query}' in the inventory.")
            return
        product = matches[0]
        await update.message.reply_text(f"{product['product_name']} has {product['current_stock']} units remaining in stock.")
        return

    if "reorder" in lower and "which products" in lower:
        reorder = analytics.get_reorder_report()
        if not reorder:
            await update.message.reply_text("No reorder suggestions right now.")
            return
        lines = ["*Suggested reorder list*"]
        for row in reorder[:10]:
            lines.append(f"- {row['product_name']}: stock {row['current_stock']} | reorder level {row['reorder_level']} | suggested qty {max(0, row.get('suggested_qty') or 0)}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if "today's sales" in lower or "todays sales" in lower or "give me today's sales" in lower or "sales summary" in lower:
        summary = analytics.get_sales_summary()
        response = (
            "*Today’s sales summary*\n"
            f"Revenue: {_format_money(summary['total_revenue'])}\n"
            f"Bills: {summary['bill_count']}\n"
            f"Average bill value: {_format_money(summary['avg_bill_value'])}\n"
            f"Cash sales: {_format_money(summary['cash_sales'])}\n"
            f"UPI sales: {_format_money(summary['upi_sales'])}\n"
            f"Card sales: {_format_money(summary['card_sales'])}"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    if _contains_any(lower,
                    "what are the stock",
                    "what are the stocks",
                    "stock available",
                    "stocks available",
                    "available stock",
                    "what stock do i have",
                    "how much stock"):
        products = store_service.products.list_all()
        if not products:
            await update.message.reply_text("No products are available in the store right now.")
            return
        lines = ["*Available stock*"]
        for item in products[:10]:
            lines.append(f"- {item['product_name']}: {item['current_stock']} units")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if _contains_any(lower, "how much", "how many") and _contains_any(lower, "have", "left", "stock"):
        query = text
        for token in ["how much", "how many", "do i have", "do I have", "left", "stock"]:
            query = query.replace(token, "")
        query = query.strip()
        if not query:
            query = ""
        results = store_service.search_products(query) if query else store_service.products.list_all()
        if not results:
            await update.message.reply_text("I couldn't find that product in the inventory.")
            return
        if len(results) > 1 and query:
            lines = ["I found multiple matching products:"]
            for i, item in enumerate(results[:5], 1):
                lines.append(f"{i}. {item['product_name']} ({item['sku']})")
            lines.append("Which one do you mean?")
            await update.message.reply_text("\n".join(lines))
            return
        if query:
            product = results[0]
            await update.message.reply_text(f"{product['product_name']} has {product['current_stock']} units in stock.")
        else:
            lines = ["*Current stock overview*"]
            for item in results[:10]:
                lines.append(f"- {item['product_name']}: {item['current_stock']} units")
            await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if "make a bill" in lower or "bill for" in lower:
        customer_name = "Walk-in"
        customer_id = None
        if "for " in lower:
            name = text.split("for", 1)[1].strip()
            if name:
                customer_name = name.title()
        customer = store_service.search_customers(customer_name)
        if customer:
            customer_id = customer[0]["customer_id"]
        draft = store_service.create_draft_bill(customer_id, customer_name)
        await update.message.reply_text(f"I created a draft bill for {customer_name}. What would you like to add?")
        context.user_data["draft_id"] = draft["draft_id"]
        return

    if "show bill" in lower:
        draft_id = context.user_data.get("draft_id")
        if not draft_id:
            await update.message.reply_text("There is no active draft bill.")
            return
        draft = store_service.billing.get_draft(draft_id)
        if not draft or not draft["items"]:
            await update.message.reply_text("The draft bill is empty.")
            return
        total = store_service.calculate_draft_bill(draft_id)
        lines = ["*Draft bill*"]
        for item in draft["items"]:
            lines.append(f"- {item['product_name']} x{item['quantity']} @ {item['unit_price']} = {item['line_total']}")
        lines.append(f"Subtotal: {_format_money(total['subtotal'])}")
        lines.append(f"CGST: {_format_money(total['cgst_total'])}")
        lines.append(f"SGST: {_format_money(total['sgst_total'])}")
        lines.append(f"Grand Total: {_format_money(total['grand_total'])}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    if "finalize" in lower or "finalise" in lower:
        draft_id = context.user_data.get("draft_id")
        if not draft_id:
            await update.message.reply_text("There is no active draft bill to finalize.")
            return
        result = store_service.finalize_bill(draft_id)
        await update.message.reply_text(f"Bill finalized: {result['bill_id']} | Total: {_format_money(result['amount'])}")
        context.user_data.pop("draft_id", None)
        return

    if "paid by" in lower or "paid" in lower:
        draft_id = context.user_data.get("draft_id")
        if draft_id:
            mode = "UPI" if "upi" in lower else "CARD" if "card" in lower else "CASH"
            payment = store_service.record_payment(draft_id, mode, Decimal("0"), "")
            await update.message.reply_text(f"Payment recorded as {mode}.")
            return

    if _contains_any(lower, "payment done today", "payment today", "what is the payment", "how much payment", "payments received", "what are the payments"):
        summary = analytics.get_sales_summary()
        response = (
            "*Payment summary today*\n"
            f"Cash: {_format_money(summary['cash_sales'])}\n"
            f"UPI: {_format_money(summary['upi_sales'])}\n"
            f"Card: {_format_money(summary['card_sales'])}"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    if _contains_any(lower, "sold today", "is any product got sold", "did we sell", "how much did i sell today", "how much sold today"):
        summary = analytics.get_sales_summary()
        await update.message.reply_text(
            f"Today’s sales: {_format_money(summary['total_revenue'])} from {summary['bill_count']} bills."
        )
        return

    if "ramesh" in lower and "owe" in lower:
        customer = store_service.search_customers("Ramesh")
        if not customer:
            await update.message.reply_text("I couldn't find a customer named Ramesh.")
            return
        balance = store_service.get_khata_balance(customer[0]["customer_id"])
        await update.message.reply_text(f"Ramesh owes {_format_money(balance)}.")
        return

    if "credit" in lower:
        name = text.lower().replace("put", "").replace("on", "").replace("credit", "").replace("₹", "").replace("rs", "").strip()
        try:
            amount = Decimal(name.split()[0])
        except Exception:
            amount = Decimal("0")
        customer = store_service.search_customers("Ramesh")
        if not customer:
            await update.message.reply_text("Customer not found.")
            return
        tx = store_service.add_khata_transaction(customer[0]["customer_id"], "CREDIT", amount, "Telegram")
        await update.message.reply_text(f"Added ₹{amount} to {customer[0]['name']}'s credit ledger.")
        return

    if "add " in lower and "draft_id" in context.user_data:
        draft_id = context.user_data["draft_id"]
        product_text = text.lower().replace("add", "", 1).strip()
        qty_match = product_text.split()[0]
        try:
            qty = int(qty_match)
        except ValueError:
            await update.message.reply_text("I couldn't parse the quantity. Please try again with a number first.")
            return
        remaining = product_text.split(None, 1)[1] if len(product_text.split(None, 1)) > 1 else ""
        search_query = remaining.strip()
        matches = store_service.search_products(search_query)
        if not matches:
            await update.message.reply_text("I couldn't find that product.")
            return
        product = matches[0]
        result = store_service.add_draft_item(draft_id, product["sku"], qty)
        await update.message.reply_text(f"Added {qty} × {product['product_name']}. Anything else?")
        return

    if "how much did i sell today" in lower or "give me today's sales" in lower:
        summary = analytics.get_sales_summary()
        await update.message.reply_text(f"Today’s revenue is {_format_money(summary['total_revenue'])} across {summary['bill_count']} bills.")
        return

    if "generate today's invoice" in lower or "generate todays invoice" in lower:
        from app.services.documents_service import generate_invoice_pdf
        path = generate_invoice_pdf(store_service, output_path=os.path.join(os.getcwd(), 'sample_outputs', 'sample_invoice.pdf'))
        await update.message.reply_document(document=open(path, 'rb'))
        return

    if "create the sales analysis deck" in lower or "sales analysis deck" in lower:
        from app.services.documents_service import generate_analysis_pptx
        path = generate_analysis_pptx(store_service, output_path=os.path.join(os.getcwd(), 'sample_outputs', 'sample_analysis_deck.pptx'))
        await update.message.reply_document(document=open(path, 'rb'))
        return

    if "close today's shop" in lower or "close today" in lower:
        summary = analytics.get_sales_summary()
        await update.message.reply_text(f"Today’s shop close: revenue {_format_money(summary['total_revenue'])}, bills {summary['bill_count']}, average {_format_money(summary['avg_bill_value'])}.")
        return

    fallback = agent.answer(text)
    await update.message.reply_text(fallback)
    return


def run_bot():
    try:
        import fcntl
        lock_file = open(os.path.join(os.getcwd(), ".telegram_bot.lock"), "w")
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Telegram bot is already running on this machine. Exiting to avoid duplicate polling.")
        return
    except Exception:
        lock_file = None

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Starting Telegram bot...")
    try:
        app.run_polling()
    finally:
        if lock_file is not None:
            try:
                lock_file.close()
            except Exception:
                pass
