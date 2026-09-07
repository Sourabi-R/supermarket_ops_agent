# Supermarket Ops Agent

A lightweight, agent-first Telegram-powered kirana store system built on SQLite, Excel-backed seed data, and a tool-calling Python agent.

## Overview

The application loads the provided Excel dataset into SQLite, exposes a tool-rich backend for inventory, billing, payments, khata, and analytics, and exposes it through a Telegram bot. The agent selects tools dynamically and reasons over their results instead of relying on a fixed keyword switchboard.

## Project structure

- app/agent/: tool-calling agent and tool layer
- app/bot/: Telegram bot handlers
- app/config/: configuration and environment settings
- app/database/: database connection and schema bootstrap
- app/models/: typed data models
- app/repositories/: CRUD and query repositories
- app/services/: business logic for inventory, billing, khata, analytics
- app/tools/: exported agent tools
- app/analytics/: sales and intelligence summaries
- data/raw/: seed Excel dataset and generated SQLite DB
- sample_outputs/: generated PDF/PPTX/example markdown outputs
- tests/: automated tests
- main.py: bootstraps the app

## Python version

Python 3.11+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` to `.env` and fill values:

```env
TELEGRAM_BOT_TOKEN=
LLM_API_KEY=
MODEL=gpt-4o-mini
DB_PATH=data/supermarket.db
DATASET_PATH=data/raw/kirana_supermarket_demo_dataset.xlsx
```

## Dataset import and database initialization

```bash
python -m app.database.init_db
```

This creates the SQLite database and imports data from the Excel workbook into structured tables.

## Run Telegram bot

```bash
python main.py
```

## Run tests

```bash
pytest -q
```

## Generate sample outputs

```bash
python scripts/generate_samples.py
```

## Agent capabilities

- product lookup and search
- stock check and stock movement history
- low stock and reorder recommendations
- draft billing with GST
- finalization, payment recording, and stock deduction
- khata credit/payment tracking
- sales summary and analytics
- morning brief and attention report
- PDF invoice generation
- PPTX business deck generation

## Safety and guardrails

- no negative stock
- no overselling
- atomic database transactions
- duplicate Telegram updates are idempotent
- financial calculations use Decimal
- database-backed ground truth only

## Demo instructions

Use the Telegram bot with prompts such as:

- Good morning
- What’s low in stock?
- Make a bill for Ramesh
- Add 2 atta
- Show bill
- Finalize it
- Ramesh paid by UPI
- Give me today’s sales
- Which products should I reorder?
- Generate today’s invoice
- Create the sales analysis deck

## Notes

This project uses the provided workbook in Downloads as the seed source and does not hardcode product or sales data.
