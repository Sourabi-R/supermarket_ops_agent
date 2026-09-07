# 🛒 Supermarket Ops Agent — StoreMate AI

### AI-Powered Telegram Assistant for Kirana Store Operations

**StoreMate AI** is a lightweight, agent-first Telegram-powered supermarket/kirana store operations system built with **Python, SQLite, Excel-backed seed data, and a local Large Language Model (LLM)**.

The system provides intelligent support for **inventory, billing, payments, khata management, sales analytics, and business reporting** through a Telegram interface.

---

## 📸 Screenshots

### 🤖 StoreMate AI — Telegram Bot

<p align="center">
  <img src="docs/screenshots/telegram-inventory.png" alt="StoreMate AI Inventory" width="700">
</p>

### 🧾 StoreMate AI — Billing

<p align="center">
  <img src="docs/screenshots/telegram-billing.png" alt="StoreMate AI Billing" width="700">
</p>

> **Note:** Add additional screenshots to `docs/screenshots/` and reference them in this section.

---

# 🚀 Overview

The application loads the provided Excel dataset into SQLite and exposes a tool-rich backend for supermarket operations.

### Core Operations

- 📦 Inventory management
- 🔎 Product lookup and search
- 🧾 Billing and invoice management
- 💰 Payment recording
- 📒 Khata / credit management
- 📊 Sales analytics
- 📉 Stock monitoring
- 🔄 Reorder recommendations
- 📑 Business reports
- 📄 PDF invoice generation
- 📊 PPTX sales analysis

The AI agent dynamically selects the appropriate tools and reasons over their results instead of relying on a fixed keyword-based switchboard.

---

# 🤖 Bot Name

## **StoreMate AI**

**StoreMate AI** is the Telegram-based AI assistant that acts as a digital operator for supermarket and kirana store activities.

Users can interact with the bot using natural-language commands.

### Example Commands

```text
Good morning
What's low in stock?
Make a bill for Ramesh
Add 2 atta
Show bill
Finalize it
Ramesh paid by UPI
Give me today's sales
Which products should I reorder?
Generate today's invoice
Create the sales analysis deck
🧠 AI Model Used

The project uses the Qwen3:4b Large Language Model locally through Ollama.

Model Stack
Component	Technology
🧠 LLM	Qwen3:4b
🦙 LLM Runtime	Ollama
💻 AI Execution	Local Machine
🔧 Agent Framework	Custom Python Tool-Calling Agent
🗄️ Database	SQLite
📊 Seed Data	Excel
📱 Interface	Telegram Bot
Why Qwen3:4b?

Qwen3:4b provides a lightweight local language model suitable for:

Natural-language understanding
Tool selection
Structured responses
Local AI execution
Low-resource environments

The model runs locally through Ollama, so the application does not require a cloud LLM API for its AI processing.

🌐 Internet Requirement

One of the key features of this project is local AI execution.

The Qwen3:4b model runs locally through Ollama, while the database and core business logic also run locally.

Offline Capabilities
Component	Internet Required?
🧠 Qwen3:4b AI inference	❌ No
🦙 Ollama	❌ No
🗄️ SQLite database	❌ No
📦 Inventory operations	❌ No
🧾 Billing calculations	❌ No
📊 Analytics	❌ No
🔧 Business logic	❌ No
📱 Telegram messaging	✅ Yes

The AI model and core supermarket operations can run without internet access because they are executed locally.

However, Telegram messaging requires an internet connection because the bot communicates with Telegram's servers.

Therefore, the project does not depend on cloud AI services for its core AI processing.

⏳ Response Time

StoreMate AI performs multiple operations before generating a response:

User Request
     ↓
Understand Request
     ↓
Select Appropriate Tool
     ↓
Query Database
     ↓
Perform Business Calculations
     ↓
Process Tool Results
     ↓
Generate Final Response
⚠️ Please wait a few seconds after sending a request.

Some operations, especially:

Analytics
Billing
Reports
Multi-step requests
Document generation

may take a few seconds to complete.

Do not send the same request repeatedly while the previous request is being processed.

🏗️ System Architecture
                    ┌──────────────────────┐
                    │    Telegram User     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   StoreMate AI Bot   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    AI Agent Layer    │
                    │                      │
                    │   Qwen3:4b + Ollama  │
                    └──────────┬───────────┘
                               │
                         Tool Selection
                               │
                               ▼
        ┌──────────────────────────────────────────┐
        │              Business Tools              │
        ├────────────┬────────────┬────────────────┤
        │ Inventory  │  Billing   │     Khata      │
        │ Analytics  │  Payments  │    Reports     │
        └────────────┴────────────┴────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      SQLite DB       │
                    └──────────┬───────────┘
                               ▲
                               │
                    ┌──────────┴───────────┐
                    │    Excel Dataset     │
                    └──────────────────────┘
🔄 Agent Workflow
                 User Query
                     ↓
        Natural Language Understanding
                     ↓
              Intent Identification
                     ↓
               Tool Selection
                     ↓
        Database / Business Logic
                     ↓
                Tool Result
                     ↓
                AI Reasoning
                     ↓
              Final Response

The agent dynamically selects tools based on the user's request and uses the returned results to generate the final response.

📁 Project Structure
supermarket_ops_agent/
│
├── app/
│   │
│   ├── agent/
│   │   └── tooling.py
│   │
│   ├── bot/
│   │   └── telegram_bot.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── ...
│   │   └── database initialization
│   │
│   ├── models/
│   │   └── product.py
│   │
│   ├── repositories/
│   │   ├── billing_repository.py
│   │   ├── customer_repository.py
│   │   ├── khata_repository.py
│   │   └── product_repository.py
│   │
│   └── services/
│       ├── analytics_service.py
│       ├── documents_service.py
│       └── store_service.py
│
├── data/
│   └── raw/
│       └── kirana_supermarket_demo_dataset.xlsx
│
├── docs/
│   └── screenshots/
│       ├── telegram-inventory.png
│       └── telegram-billing.png
│
├── sample_outputs/
│
├── scripts/
│
├── tests/
│   └── test_core.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
🛠️ Technology Stack
Layer	Technology
💻 Programming Language	Python 3.11+
🧠 AI Model	Qwen3:4b
🦙 Local LLM Runtime	Ollama
🗄️ Database	SQLite
📊 Dataset	Microsoft Excel
📱 Bot Interface	Telegram
🔗 ORM / Database Layer	SQLAlchemy
🐼 Data Processing	Pandas
📄 Document Generation	ReportLab
📊 Presentation Generation	python-pptx
🧪 Testing	Pytest
📊 Dataset

The system uses the provided Excel workbook as the seed data source.

data/raw/kirana_supermarket_demo_dataset.xlsx

The application imports the Excel data into SQLite and uses the database as the operational source of truth.

The project does not hardcode product or sales data into the application logic.

Data Flow
Excel Dataset
      ↓
Data Import
      ↓
SQLite Database
      ↓
Repositories
      ↓
Business Services
      ↓
AI Agent Tools
      ↓
StoreMate AI
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Sourabi-R/supermarket_ops_agent.git
cd supermarket_ops_agent
2. Create a Virtual Environment
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Windows
python -m venv .venv
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
🦙 Install Ollama

StoreMate AI uses Ollama to run the Qwen3:4b model locally.

Install Ollama and make sure it is running.

Then download the required model:

ollama pull qwen3:4b

Verify that the model is installed:

ollama list

You should see:

qwen3:4b

The application communicates with the local Ollama server.

Default Ollama Endpoint
http://localhost:11434
🔐 Environment Variables

Copy the example environment file:

macOS / Linux
cp .env.example .env
Windows
copy .env.example .env

Configure the required Telegram bot token and local application settings.

Example:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MODEL=qwen3:4b
DB_PATH=data/supermarket.db
DATASET_PATH=data/raw/kirana_supermarket_demo_dataset.xlsx

⚠️ Never commit your .env file or Telegram bot token to GitHub.

🗄️ Database Initialization

Initialize the SQLite database using the provided dataset:

python -m app.database.init_db

This creates the local SQLite database and imports the Excel seed data into structured tables.

▶️ Run the Bot

Make sure Ollama is running and that the qwen3:4b model is available.

Then start the Telegram bot:

python main.py

Open Telegram and start interacting with:

StoreMate AI
⏳ Important

After sending a message, wait a few seconds for StoreMate AI to process the request and return the result.

🤖 Agent Capabilities
📦 Inventory Management
Product lookup
Product search
Stock availability
Stock movement history
Low-stock detection
Reorder recommendations
🧾 Billing
Draft bills
Add products to bills
GST calculations
Bill finalization
Payment recording
Automatic stock deduction
💰 Payments
Cash payments
UPI payments
Payment tracking
Billing status
📒 Khata Management
Customer credit tracking
Outstanding balances
Credit payments
Customer account history
📈 Analytics
Sales summaries
Revenue analysis
Product performance
Inventory intelligence
Morning brief
Attention reports
📄 Document Generation
PDF invoice generation
Sales analysis reports
PPTX business presentation generation
🧾 Example Billing Flow
User:
Make a bill for Ramesh

        ↓

Create Draft Bill

        ↓

User:
Add 2 atta

        ↓

Update Bill

        ↓

User:
Show bill

        ↓

Display Bill

        ↓

User:
Finalize it

        ↓

Finalize Bill

        ↓

User:
Ramesh paid by UPI

        ↓

Record Payment
        +
Deduct Stock
🛡️ Safety & Guardrails

The system implements several operational safeguards:

❌ No negative stock
❌ No overselling
🔒 Atomic database transactions
🔄 Idempotent handling of duplicate Telegram updates
💰 Financial calculations using Decimal
🗄️ Database-backed ground truth
📦 Controlled inventory updates
🧾 Structured billing workflow

These safeguards help maintain consistency between inventory, billing, payments, and customer accounts.

🧪 Testing

Run the automated tests using:

pytest -q
📑 Generate Sample Outputs

To generate sample documents:

python scripts/generate_samples.py

Generated outputs may include:

PDF invoices
Sales reports
PPTX business decks
Example Markdown outputs
💬 Demo Prompts

Try the following commands with StoreMate AI.

General
Good morning
Inventory
What's low in stock?
Which products should I reorder?
Billing
Make a bill for Ramesh
Add 2 atta
Show bill
Finalize it
Payments
Ramesh paid by UPI
Analytics
Give me today's sales
Documents
Generate today's invoice
Create the sales analysis deck
🔒 Security

Sensitive configuration should remain outside Git.

The following files and directories should never be committed:

.env
*.db
.venv/
__pycache__/
*.pyc
.DS_Store

Use .env.example as the template for required environment variables.

⭐ Key Highlights
Feature	Description
🤖 Local AI	Qwen3:4b running through Ollama
📱 Telegram Bot	Natural-language supermarket assistant
📦 Inventory	Product and stock management
🧾 Billing	AI-assisted billing and GST calculations
💰 Payments	Cash and UPI payment tracking
📒 Khata	Customer credit management
📊 Analytics	Sales and inventory intelligence
📄 PDF	Automated invoice generation
📊 PPTX	Automated sales analysis presentation
🗄️ SQLite	Local database-backed operations
🌐 Offline AI	Local AI inference without cloud LLM dependency
🛡️ Guardrails	Transaction-safe business operations
🔮 Future Enhancements

Potential future improvements include:

PostgreSQL support
Redis-based task processing
Advanced demand forecasting
Multi-store management
Voice-based commands
Barcode integration
Automated daily reports
Advanced business intelligence dashboards
Role-based access control
Mobile application
🎯 Project Highlights

StoreMate AI combines:

Local LLM
   +
Tool Calling
   +
SQLite
   +
Excel Dataset
   +
Business Logic
   +
Telegram
   +
Analytics
   +
Document Generation

into a single AI-powered supermarket operations platform.

The goal is to provide a practical AI digital operator for kirana and supermarket businesses while keeping the AI processing local and the operational data database-driven.
