# Demo Guide

This walkthrough is optimized for a 4–5 minute Telegram demo of the agent-first kirana store system.

## 1. Morning brief

Type:

- Good morning

Expected result:

- A concise summary with yesterday’s revenue, bill count, average bill value, top products, payment mix, GST summary, low stock and reorder priorities.

## 2. Inventory awareness

Type:

- What’s low in stock?

Expected result:

- A database-grounded list of low and critical stock items with current quantity and reorder suggestions.

## 3. Attention report

Type:

- What needs my attention?

Expected result:

- An actionable report covering critical inventory, high-velocity low-stock items, outstanding khata, and other data-backed issues.

## 4. Product lookup

Type:

- How much atta do I have?

Expected result:

- The agent searches the products table and returns the exact stock for the matching atta product(s), asking for clarification if needed.

## 5. Multi-turn billing

Type:

- Make a bill for Ramesh

Then continue:

- Add 2 atta
- Add 3 salt
- Show bill
- Finalize it

Expected result:

- The agent uses product search, creates a draft bill, applies GST logic, and finalizes it only after confirmation. Stock is decremented at finalization, not at draft creation.

## 6. Payment and khata

Type:

- Ramesh paid by UPI

Then:

- How much does Ramesh owe?

Expected result:

- Payment is recorded against the bill, khata is updated, and the current outstanding balance is returned from the database.

## 7. Sales and analytics

Type:

- Give me today’s sales

Then:

- Which products should I reorder?

Expected result:

- Real summaries generated from SQLite, not hardcoded metrics.

## 8. Documents

Type:

- Generate today’s invoice
- Create the sales analysis deck

Expected result:

- A real PDF invoice and real PowerPoint deck are generated in sample_outputs using live data.

## Why this demo matters

The experience is agent-first: the model decides which tools to call, inspects the results, and answers naturally. Every result is database-grounded and business logic is enforced in the backend for stock, billing, GST, and khata correctness.
