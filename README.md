# 🛠️ The Toolbench: Multi-Server Model Context Protocol (MCP) Ecosystem

An interactive **Agentic AI Toolbench** built with **Streamlit**, **LangChain**, and **FastMCP**. This platform seamlessly orchestrates multiple Model Context Protocol (MCP) servers—enabling LLMs like **Llama 3.3 (via Groq)** and **Gemini 2.5 Flash** to perform structured real-world tasks such as mathematical computations, SQLite-backed expense tracking, and dynamic animation creation via Manim.


## 🌟 Key Features

* **🔌 Multi-Server MCP Architecture:** Built using `langchain-mcp-adapters` to connect and communicate with multiple local MCP servers (`stdio` transport) simultaneously.
* **🤖 Dual LLM Provider Support:** Switch effortlessly between **Groq (`llama-3.3-70b-versatile`)** and **Google Gemini (`gemini-2.5-flash`)**.
* **💰 SQLite-Backed Expense Tracker MCP:**
  * Record transactions with dates, categories, subcategories, and notes.
  * Retrieve date-range filtered transactions.
  * Generate aggregate spending summaries with breakdown by categories.
  * Access structured category taxonomy resources (`expense://categories`).
* **🧮 Async Math Calculator MCP:**
  * Perform exact arithmetic calculations (`add`, `subtract`, `multiply`, `divide`) with error handlings (e.g., zero-division safeguards).
* **🎬 Manim Animation Server MCP Integration:**
  * Support for rendering mathematical animations on-the-fly using Manim.
* **🖥️ Interactive Cyberpunk/Dark-Mode Dashboard:**
  * Real-time tool rack monitoring with live connection status indicators (LEDs).
  * Detailed tool-call trace logs (tool arguments, raw JSON returns, and final LLM responses).

---

## 📁 Repository Structure

```text
.
├── client2.py           # Streamlit Web UI & Multi-Server MCP Orchestrator
├── Expense_Tracker.py   # FastMCP Server for SQLite Expense Management
├── math.py              # FastMCP Server for Async Math Calculations
├── categories.json      # Structured Category & Subcategory Taxonomy
├── expenses.db          # SQLite Database (Auto-generated on launch)
└── README.md            # Project Documentation

```

---

## 🏗️ Architecture Overview

```
                        +-------------------------------------------------+
                        |              Streamlit Interface                |
                        |                 (client2.py)                    |
                        +------------------------+------------------------+
                                                 |
                                     MultiServerMCPClient
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                       |                                       |
         v                                       v                                       v
+------------------+                   +-------------------+                   +-------------------+
|  Math MCP Server |                   | Expense MCP Server|                   | Manim MCP Server  |
|    (math.py)     |                   |(Expense_Tracker.py|                   |  (manim_server)   |
+------------------+                   +-------------------+                   +-------------------+
         |                                       |                                       |
    [FastMCP]                               [FastMCP]                                [FastMCP]
         |                                       |                                       |
 Pure Python Logic                      SQLite (`expenses.db`)                  Manim Engine
                                        & `categories.json`

```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites

Ensure you have the following installed on your system:

* **Python 3.10+**
* **`uv` Package Manager** (or standard virtual environment)
* **Manim Community Edition** (Optional, for rendering animations)

### 2. Environment Setup

Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/himanshub0810/mcp---project.git](https://github.com/himanshub0810/mcp---project.git)
cd mcp---project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install streamlit langchain langchain-groq langchain-google-genai langchain-mcp-adapters fastmcp python-dotenv

```

### 3. Configure API Keys

Create a `.env` file in the root directory and add your LLM API keys:

```env
GROQ_API_KEY="your_groq_api_key_here"
GOOGLE_API_KEY="your_gemini_api_key_here"

```

### 4. Update File Paths in `client2.py`

Before running the dashboard, update the absolute paths inside `client2.py` under `SERVERS` dictionary to point to your local setup:

```python
SERVERS = {
    "maths": {
        "transport": "stdio",
        "command": "uv",
        "args": ["run", "fastmcp", "run", "/path/to/math.py"]
    },
    "expense": {
        "transport": "stdio",
        "command": "uv",
        "args": ["run", "fastmcp", "run", "/path/to/Expense_Tracker.py"]
    },
    "manim-server": {
        "transport": "stdio",
        "command": "/path/to/venv/bin/python",
        "args": ["/path/to/manim_server.py"],
        "env": {
            "MANIM_EXECUTABLE": "/path/to/venv/bin/manim"
        }
    }
}

```

---

## 🏃 Running the Application

Launch the Streamlit web dashboard:

```bash
streamlit run client2.py

```

Navigate to `http://localhost:8501` in your browser.

---

## 🛠️ MCP Servers & Available Tools

### 1. Expense Tracker MCP (`Expense_Tracker.py`)

Provides tools for persistent expense logging and aggregation into an SQLite database (`expenses.db`).

| Tool / Resource | Type | Description |
| --- | --- | --- |
| `add_expense` | Tool | Inserts date, amount, category, subcategory, and notes into DB. |
| `list_expenses` | Tool | Retrieves transactions within an inclusive date range (`start_date` to `end_date`). |
| `summarize_expenses` | Tool | Calculates total expenditure, transaction counts, and category totals. |
| `expense://categories` | Resource | Exposes JSON data taxonomy from `categories.json`. |

### 2. Async Math Calculator MCP (`math.py`)

Performs standard high-precision mathematical operations asynchronously.

| Tool | Parameters | Description |
| --- | --- | --- |
| `add` | `a: float, b: float` | Returns the sum of two numbers. |
| `subtract` | `a: float, b: float` | Subtracts `b` from `a`. |
| `multiply` | `a: float, b: float` | Multiplies `a` by `b`. |
| `divide` | `a: float, b: float` | Divides `a` by `b` (Includes zero division check). |

---

## 💡 Usage Examples

### 📥 Expense Management Prompt

> **User Prompt:** `"Add an expense of Rs 4500 for groceries on 2026-07-20 under food category"`
> **Tool Execution:** `add_expense(date="2026-07-20", amount=4500, category="food", subcategory="groceries")`
> **Response:** `"Successfully logged expense ID #1 for Rs 4500 under food (groceries)."`

### 📊 Expense Summary Prompt

> **User Prompt:** `"Summarize all my spending from 2026-07-01 to 2026-07-31"`
> **Tool Execution:** `summarize_expenses(start_date="2026-07-01", end_date="2026-07-31")`

### 🔢 Mathematical Calculation Prompt

> **User Prompt:** `"What is 9872 divided by 16?"`
> **Tool Execution:** `divide(a=9872, b=16)`
> **Response:** `"9872 ÷ 16 = 617.0"`

---

## ⚙️ Tech Stack

* **Frameworks & UI:** Streamlit
* **Agentic AI & LLMs:** LangChain, LangChain MCP Adapters, Groq API (`llama-3.3-70b`), Google Gemini API (`gemini-2.5-flash`)
* **MCP Framework:** FastMCP
* **Database:** SQLite3
* **Environment & Package Management:** Python 3.10+, `uv`, `python-dotenv`
