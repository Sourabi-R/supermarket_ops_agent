# 🛒 Supermarket Ops Agent — StoreMate AI

### AI-Powered Telegram Assistant for Kirana Store Operations

> **StoreMate AI** is an intelligent supermarket operations assistant designed for Indian kirana stores. It combines a local Large Language Model (LLM), structured business tools, SQLite database operations, analytics, billing, inventory management, customer management, and reporting into a single Telegram-based assistant.

---

## 📸 StoreMate AI — Telegram Demo

### 📦 Inventory Management

<img width="1470" height="956" alt="telegram-inventory" src="https://github.com/user-attachments/assets/19363e49-6a43-498d-9c19-89f9c78c6431" />

### 🧾 Billing & Invoice Generation

<img width="1470" height="956" alt="telegram-billing" src="https://github.com/user-attachments/assets/5687463f-4b56-4bc5-9089-bd18f604254b" />

---

## 🤖 Project Overview

StoreMate AI acts as a digital operations assistant for supermarket and kirana-store owners.

Instead of manually checking databases, calculating bills, searching products, checking stock, or generating reports, the user can simply send a natural-language request through Telegram.

The AI Agent understands the user's request, identifies the required operation, calls the appropriate business tool, retrieves or processes the required data, and returns a structured response.

### Example

**User:**
> How much rice stock is available?

**StoreMate AI:**
> Rice has 125 units currently available in inventory.

---

# ✨ Key Features

- 🤖 AI-powered natural language interaction
- 💬 Telegram-based conversational interface
- 🧠 Local LLM using Qwen3:4b
- ⚡ Ollama-based local AI inference
- 📦 Product and inventory management
- 🧾 Billing and invoice generation
- 👥 Customer management
- 💰 Khata / customer credit management
- 📊 Sales and business analytics
- 📈 Revenue analysis
- 🗄️ SQLite database
- 📄 PDF report generation
- 📊 PowerPoint report generation
- 🔎 Product search and stock lookup
- 🛡️ Agent guardrails and validation
- 🌐 Local AI processing without cloud LLM dependency

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      USER            │
                         │  Natural Language    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      TELEGRAM        │
                         │     INTERFACE        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    STOREMate AI      │
                         │    AI AGENT LAYER    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    QWEN3:4B LLM      │
                         │       OLLAMA         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    AGENT TOOLING     │
                         │   Tool Selection     │
                         │   Function Calling   │
                         └──────────┬───────────┘
                                    │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │  INVENTORY  │      │   BILLING   │      │  CUSTOMER   │
      │   TOOLS     │      │    TOOLS    │      │    TOOLS    │
      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │     SERVICES LAYER   │
                       │ Analytics / Store /  │
                       │ Document Services    │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    REPOSITORIES      │
                       │ Database Operations  │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │      SQLITE DB       │
                       │   Local Store Data   │
                       └──────────────────────┘
```

---

# 🔄 Agent Workflow

StoreMate AI follows an agent-based workflow to convert natural-language questions into business operations.

```text
┌──────────────────────────┐
│ 1. USER QUERY            │
│                          │
│ "Show low stock items"   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 2. TELEGRAM BOT          │
│                          │
│ Receives user message    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 3. AI AGENT              │
│                          │
│ Understands intent       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 4. QWEN3:4B + OLLAMA     │
│                          │
│ Local LLM reasoning      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 5. TOOL SELECTION        │
│                          │
│ Select required tool     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 6. BUSINESS LOGIC        │
│                          │
│ Inventory / Billing /    │
│ Customer / Analytics     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 7. DATABASE              │
│                          │
│ Query / Update SQLite    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 8. RESULT PROCESSING     │
│                          │
│ Format business result   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 9. AI RESPONSE           │
│                          │
│ Natural-language answer  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ 10. TELEGRAM RESPONSE    │
│                          │
│ Result sent to user      │
└──────────────────────────┘
```

---

# 🧠 AI Agent Architecture

The core of the system is an AI Agent that connects natural-language requests with deterministic business operations.

```text
                 USER
                   │
                   ▼
          Natural Language Query
                   │
                   ▼
          ┌─────────────────┐
          │   Qwen3:4b      │
          │     Ollama      │
          └────────┬────────┘
                   │
                   ▼
          Intent Understanding
                   │
                   ▼
             Tool Selection
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    Inventory    Billing    Customer
      Tools       Tools       Tools
        │          │          │
        └──────────┼──────────┘
                   │
                   ▼
            Business Logic
                   │
                   ▼
               Database
                   │
                   ▼
             Tool Result
                   │
                   ▼
            AI Response
                   │
                   ▼
                Telegram
```

---

# 🤖 Model Used

## Qwen3:4b

StoreMate AI uses **Qwen3:4b** as the local Large Language Model.

### Model Stack

| Component | Technology |
|---|---|
| LLM | Qwen3:4b |
| LLM Runtime | Ollama |
| AI Processing | Local |
| Interface | Telegram Bot |
| Database | SQLite |
| Backend | Python |
| Business Logic | Python Services |
| Data Processing | Pandas |
| Reports | ReportLab / python-pptx |

### Why Local AI?

The LLM runs locally through Ollama rather than depending on a cloud-based LLM API.

This provides:

- Local inference
- Reduced dependency on cloud AI APIs
- No cloud LLM API key required
- Better control over business data
- Ability to run AI processing locally

---

# 🌐 Internet Requirement

The AI and database components are designed for local execution.

| Component | Internet Required? |
|---|---|
| Qwen3:4b inference | ❌ No |
| Ollama | ❌ No |
| SQLite database | ❌ No |
| Inventory operations | ❌ No |
| Billing calculations | ❌ No |
| Analytics | ❌ No |
| PDF generation | ❌ No |
| PowerPoint generation | ❌ No |
| Telegram messaging | ✅ Yes |

> **Important:** The local AI, database, analytics, billing, and business logic can operate without internet. However, the Telegram Bot requires an internet connection because it communicates with Telegram's servers.

---

# ⏳ Response Time

Because the project uses a local LLM and tool-calling workflow, some requests may take a few seconds to process.

> **Please wait a few seconds after sending a request.**

The agent may need to:

1. Understand the request
2. Select the appropriate tool
3. Query the database
4. Process the result
5. Generate the final natural-language response

---

# 🛒 Core Business Modules

## 1. 📦 Inventory Management

StoreMate AI can help with:

- Product search
- Product availability
- Stock-level checking
- Low-stock identification
- Product information
- Inventory-related queries

### Example Prompts

```text
Show me all available products.

Which products are low in stock?

How many units of rice are available?

Show me the stock for biscuits.

Find products in the grocery category.
```

---

## 2. 🧾 Billing Management

The billing module supports supermarket billing operations.

### Billing Workflow

```text
Customer Request
       │
       ▼
Select Products
       │
       ▼
Check Product Availability
       │
       ▼
Calculate Quantity × Price
       │
       ▼
Calculate Subtotal
       │
       ▼
Apply Billing Logic
       │
       ▼
Generate Invoice
       │
       ▼
Return Billing Result
```

### Example

```text
Create a bill for:

2 Rice
3 Biscuits
1 Cooking Oil
```

The system processes the requested products and generates the billing result.

---

# 👥 Customer Management

The customer module manages customer-related information and operations.

Capabilities include:

- Customer lookup
- Customer records
- Customer-related transactions
- Customer history
- Customer account operations

---

# 💳 Khata / Credit Management

The system supports customer credit / khata-related operations.

The module is designed to help store owners track customer balances and credit transactions.

### Example Prompts

```text
Show customer khata.

Check the outstanding balance.

Show customer credit details.
```

---

# 📊 Analytics Engine

StoreMate AI includes analytics functionality for supermarket operations.

Analytics can be used for:

- Sales analysis
- Revenue analysis
- Product performance
- Business summaries
- Store-level insights

The analytics layer uses structured business data and Python-based data processing.

---

# 🗄️ Database Architecture

The application uses **SQLite** for local data storage.

```text
Application
     │
     ▼
Repositories
     │
     ▼
SQLite Database
     │
     ├── Products
     ├── Customers
     ├── Billing Data
     └── Store Information
```

SQLite makes the project lightweight and easy to run locally without requiring a separate database server.

---

# 📂 Project Structure

```text
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
│   │   └── ...
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
│   └── ...
│
├── scripts/
│   └── ...
│
├── tests/
│   └── test_core.py
│
├── .env.example
├── .gitignore
├── DEMO_GUIDE.md
├── main.py
├── README.md
└── requirements.txt
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| AI Model | Qwen3:4b |
| AI Runtime | Ollama |
| Interface | Telegram Bot |
| Database | SQLite |
| ORM / Database Layer | SQLAlchemy |
| Data Processing | Pandas |
| Spreadsheet Processing | OpenPyXL |
| PDF Generation | ReportLab |
| Presentation Generation | python-pptx |
| Environment Management | python-dotenv |
| Testing | Pytest |

---

# 📊 Dataset

The project includes a demo supermarket dataset.

### Dataset File

```text
data/raw/kirana_supermarket_demo_dataset.xlsx
```

The dataset is used to support supermarket business operations, analytics, inventory-related workflows, and demonstrations.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Sourabi-R/supermarket_ops_agent.git
cd supermarket_ops_agent
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

StoreMate AI uses Ollama to run Qwen3:4b locally.

## Install Ollama

Download and install Ollama for your operating system.

After installation, verify it:

```bash
ollama --version
```

---

## Download Qwen3:4b

Run:

```bash
ollama pull qwen3:4b
```

Verify the model:

```bash
ollama list
```

You should see:

```text
qwen3:4b
```

---

## Start Ollama

If required, start the Ollama service:

```bash
ollama serve
```

The application communicates with the local Ollama service.

Default local Ollama endpoint:

```text
http://localhost:11434
```

---

# 🔐 Environment Variables

Create your environment file:

```bash
cp .env.example .env
```

Configure the required environment variables.

Example:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:4b
```

> Never commit your real `.env` file or Telegram Bot Token to GitHub.

---

# 🗄️ Database Setup

The project uses SQLite for local database storage.

The application initializes the required database structures when the application starts.

The database is designed to store local supermarket operational data.

---

# 🚀 Running StoreMate AI

After installing the dependencies, configuring `.env`, and making sure Ollama is available, run:

```bash
python main.py
```

The Telegram bot will start and wait for incoming messages.

Open Telegram and send a message to your StoreMate AI bot.

---

# 💬 Example User Queries

## Inventory

```text
Show all products.

Which products are low in stock?

How many rice packets are available?

Check the stock of cooking oil.
```

## Billing

```text
Create a bill for 2 rice and 3 biscuits.

Generate an invoice for this customer.

Calculate the total for these products.
```

## Customer

```text
Find this customer.

Show customer details.

Show customer transaction history.
```

## Khata

```text
Show customer khata.

What is the outstanding balance?

Check the customer's credit.
```

## Analytics

```text
Give me a sales summary.

Show revenue information.

Which products are performing well?

Give me a business summary.
```

---

# 🔄 End-to-End Example

### User

```text
Create a bill for 2 rice and 1 cooking oil.
```

### StoreMate AI Workflow

```text
User Query
    ↓
Telegram Bot
    ↓
AI Agent
    ↓
Qwen3:4b
    ↓
Intent Understanding
    ↓
Billing Tool
    ↓
Product Repository
    ↓
SQLite Database
    ↓
Price & Stock Retrieval
    ↓
Billing Calculation
    ↓
Invoice / Result
    ↓
AI Response
    ↓
Telegram
```

---

# 🛡️ Agent Safety & Guardrails

The application separates natural-language understanding from deterministic business operations.

The LLM is responsible for understanding the user's request and selecting the required operation, while business tools handle structured operations.

This approach helps keep important operations such as:

- Product lookup
- Stock checks
- Billing calculations
- Customer operations
- Database operations

within controlled application logic.

---

# 🧪 Testing

The project includes tests under:

```text
tests/
└── test_core.py
```

Run the test suite using:

```bash
pytest
```

For coverage:

```bash
pytest --cov=app
```

---

# 📄 Sample Outputs

The project contains sample outputs under:

```text
sample_outputs/
```

These demonstrate generated business reports and document-generation capabilities.

---

# 🎯 Project Objectives

The main objectives of StoreMate AI are:

1. Reduce manual supermarket operations.
2. Provide natural-language access to store data.
3. Simplify inventory management.
4. Automate billing operations.
5. Support customer and khata management.
6. Provide business analytics.
7. Reduce dependency on cloud AI services.
8. Provide a simple Telegram-based interface.
9. Combine AI reasoning with deterministic business tools.

---

# 💡 Why StoreMate AI?

Traditional supermarket systems often require users to navigate multiple screens and manually perform different operations.

StoreMate AI provides a conversational interface where the user can simply ask what they need.

Instead of:

```text
Open Application
      ↓
Find Inventory Module
      ↓
Search Product
      ↓
Check Stock
      ↓
Read Result
```

The user can simply ask:

```text
"How many rice packets are available?"
```

StoreMate AI handles the underlying workflow.

---

# 🧩 AI + Business Tools

The key architectural principle is:

```text
             Natural Language
                    │
                    ▼
                 LLM
                    │
             Intent / Tool
                Selection
                    │
                    ▼
            Deterministic Tool
                    │
                    ▼
              Business Logic
                    │
                    ▼
                Database
                    │
                    ▼
                 Result
                    │
                    ▼
             Natural Language
```

This allows the system to combine the flexibility of an LLM with the reliability of structured application logic.

---

# 🔥 Key Highlights

### 🤖 Local AI

Qwen3:4b runs locally through Ollama.

### 💬 Conversational Interface

Users interact naturally through Telegram.

### 📦 Business Operations

Inventory, billing, customer, khata, and analytics operations are integrated into one system.

### 🗄️ Local Database

SQLite provides lightweight local data storage.

### 📊 Analytics

Business data can be processed to generate useful insights.

### 🔐 Data Control

The AI model can operate locally without sending business data to a cloud LLM provider.

---

# 📱 Bot Name

## StoreMate AI

StoreMate AI is the Telegram-based supermarket operations assistant used by this project.

---

# ⏱️ Important Usage Note

When you send a request to StoreMate AI:

> **Please wait a few seconds for the result.**

The response time depends on the local LLM inference and the number of database/tool operations required.

---

# 🔮 Future Enhancements

Potential future improvements include:

- 📱 Dedicated mobile application
- 📊 Advanced business dashboards
- 📈 Demand forecasting
- 🔔 Automated low-stock alerts
- 🧾 Advanced invoice templates
- 👤 Role-based access control
- ☁️ Optional cloud deployment
- 🗃️ PostgreSQL production database
- 📦 Supplier management
- 💳 Payment integration
- 📊 Advanced sales forecasting
- 🧠 More specialized AI agents
- 📩 Automated reports and notifications

---

# 👨‍💻 Project Information

**Project:** Supermarket Ops Agent

**Assistant:** StoreMate AI

**AI Model:** Qwen3:4b

**LLM Runtime:** Ollama

**Interface:** Telegram

**Database:** SQLite

**Language:** Python

---

# 📌 Quick Start

```bash
# Clone
git clone https://github.com/Sourabi-R/supermarket_ops_agent.git

# Enter project
cd supermarket_ops_agent

# Create environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull local AI model
ollama pull qwen3:4b

# Configure environment
cp .env.example .env

# Run application
python main.py
```

---

# 🏁 Conclusion

**StoreMate AI** demonstrates how a local Large Language Model can be integrated with real-world supermarket business operations.

The project combines:

```text
Telegram
   +
Qwen3:4b
   +
Ollama
   +
AI Agent
   +
Business Tools
   +
Python Services
   +
SQLite
   +
Analytics
   +
Document Generation
```

into a single intelligent supermarket operations platform.

The goal is to make everyday kirana-store operations simpler, faster, and more accessible through natural-language interaction.

---
