# Insurance Intelligence Platform

An enterprise-grade, data-driven **Insurance Intelligence Platform** built with **Python**, **Streamlit**, **Snowflake (Cortex AI, Cortex Search & Data Cloud)**, **Pandas**, and **Plotly**.

Designed for underwriters, claims adjusters, risk managers, actuarial analysts, and insurance executives to perform real-time policy underwriting, AI-powered claims triage with visual damage inspection, market trend detection, actuarial rate modeling, and conversational AI product & pricing optimization.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Platform Capabilities](#-key-platform-capabilities)
3. [Authentication & Connection Flow](#-authentication--connection-flow)
4. [Technology Stack](#-technology-stack)
5. [Project Directory Structure](#-project-directory-structure)
6. [Application Modules](#-application-modules)
7. [Snowflake Architecture & Data Integration](#-snowflake-architecture--data-integration)
8. [Prerequisites](#-prerequisites)
9. [Setup & Installation](#-setup--installation)
10. [Environment Configuration](#-environment-configuration)
11. [Testing & Verification](#-testing--verification)
12. [Team Git Workflow](#-team-git-workflow)
13. [Security Best Practices](#-security-best-practices)

---

## 🎯 Project Overview

The **Insurance Intelligence Platform** provides live intelligence and decision-support for enterprise insurance operations across underwriting, claims investigation, actuarial modeling, customer 360 analytics, and conversational AI assistance.

Key capabilities include:
- **Direct Automatic Snowflake Connection**: Establishes live Snowflake session on application load with automated connection health validation (`SELECT CURRENT_USER(), CURRENT_ACCOUNT();`).
- **Conversational AI Experience**: ChatGPT-inspired enterprise assistant interfaces with quick prompt chips, structured Markdown responses, multi-turn history, and floating message composers across AI modules.
- **Visual Claim Triage**: Multi-modal chat assistant with inline image upload for evaluating vehicle and property damage claims.
- **Cortex Natural Language Search**: Vectorized search over claim investigation notes and alert histories.

---

## ⚡ Key Platform Capabilities

### 💬 Modern Conversational AI Interface
- **ChatGPT-Style UX**: Modern responsive interface with persistent conversation history, avatar badges, suggestion prompt chips, and clean floating message bars.
- **Interactive Assistance**: Dedicated AI modules for **Product Matching**, **Market Intelligence**, **Competitive Pricing**, and **Claims Fraud Triage**.
- **Multi-Modal Image Analysis**: Upload vehicle damage photos or property claim documents directly inside the Chat Assistant for visual severity estimation.

### 🛡️ Direct & Audited Snowflake Data Integration
- **Live Query Execution**: Queries 300 live policy records in `INSURANCE_MGMT_SYSTEM.GOLD.FACT_POLICY` or `CORE.POLICIES`.
- **Real-Time KPI Auditing**:
  - **Total Policies**: `300`
  - **Active Book**: `180`
  - **Total Premium Volume**: `$2,320,783`
  - **Average Premium**: `$7,735.94`
- **Cortex Search Engine**: High-speed search over `ANALYTICS.CLAIM_NOTES_SEARCH` using `SNOWFLAKE.CORTEX.SEARCH_PREVIEW`.

---

## 🔐 Authentication & Connection Flow

The platform utilizes a **Direct Automatic Snowflake Connection**:

1. **Startup**: When Streamlit starts, credentials are loaded directly from the local environment (`.env`).
2. **Authentication**: Connects securely via `snowflake-connector-python` using `SNOWFLAKE_AUTHENTICATOR=snowflake` (default username + password authentication).
3. **Passkey / MFA Flow Removed**: The application no longer prompts for terminal passkeys or Duo MFA codes on process startup.
4. **Automated Validation**: Executes a lightweight validation query upon connection (`SELECT CURRENT_USER(), CURRENT_ACCOUNT();`) and displays a live connection status indicator (`● Snowflake Connected`) in the sidebar.

```text
Streamlit Starts ➔ Load Credentials (.env) ➔ Connect to Snowflake ➔ Validate Connection ➔ Load Platform
```

---

## 🛠️ Technology Stack

- **Frontend / Presentation**: [Streamlit](https://streamlit.io/) (v1.30.0+) with custom enterprise CSS components.
- **Data Engine**: [Snowflake Data Cloud](https://www.snowflake.com/) (`snowflake-connector-python` v3.6.0+)
- **AI & Cortex Services**:
  - Snowflake Cortex Agent REST API (`SNOWFLAKE.CORTEX.DATA_AGENT_RUN`)
  - Snowflake Cortex Search (`SNOWFLAKE.CORTEX.SEARCH_PREVIEW`)
- **Data Analytics & Processing**: [Pandas](https://pandas.pydata.org/) (v2.0.0+)
- **Data Visualization**: [Plotly](https://plotly.com/) (Express & Graph Objects v5.18.0+)
- **Document Processing**: `fpdf2` (v2.7.0+)
- **Environment Management**: `python-dotenv` (v1.0.0+)

---

## 📁 Project Directory Structure

```text
INSURANCE-INTELLIGENCE-PLATFORM/
│
├── .env                              # Local environment variables (Snowflake credentials, ignored by Git)
├── .env.example                      # Template configuration file for environment variables
├── .gitignore                        # Git ignore rules for secrets, virtualenv, and Python caches
│
├── .streamlit/
│   └── config.toml                   # Streamlit layout theme and UI configuration
│
├── app.py                            # Main Streamlit web application & 8 enterprise intelligence modules
├── snowflake_utils.py                # Snowflake connection manager, Cortex Search, Cortex Agents & SQL fetchers
├── test_env.py                       # Environment & connection validation script
│
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation and setup guide
```

---

## 📑 Application Modules

The application consists of 8 core enterprise modules accessible from the sidebar:

### 1. 📑 Underwriting Workbench
- **Purpose**: Real-time policy book management, actuarial rate modeling, and dynamic ML premium quoting.
- **Features**:
  - Live policy book overview with policy status filtering (Active, Expired, Cancelled, Pending).
  - Dynamic predictive ML premium calculator with actuarial rate drivers (Age, Credit Score, Coverage Exposure).
  - Rate driver sensitivity controls and policy tier selection (Bronze, Silver, Gold, Platinum).
- **Data**: Queries `GOLD.FACT_POLICY` and `CORE.POLICIES`.

### 2. 🛡️ Claims & Fraud Console
- **Purpose**: AI-powered claims triage, fraud risk assessment, and claims data search.
- **Features**:
  - **Search Claims Intelligence**: Natural language search over investigation notes using Snowflake Cortex Search Service (`ANALYTICS.CLAIM_NOTES_SEARCH`).
  - **Conversational AI Fraud Triage Assistant**: Inline ChatGPT-style chat workspace evaluating red flags, fraud scores, and SIU (Special Investigation Unit) escalation recommendations using `CLAIMS_FRAUD_TRIAGE_AGENT`.
  - Claim details inspection and anomaly score indicators.
- **Data/AI**: Snowflake Cortex Search Service & `CLAIMS_FRAUD_TRIAGE_AGENT`.

### 3. 📈 Risk & Pricing Dashboard
- **Purpose**: Portfolio loss ratio history, risk retention analytics, and portfolio risk exposure.
- **Features**:
  - Combined ratio scenario modeling and portfolio loss ratio trends across policy types.
  - At-risk policy retention scoring and risk distribution analysis.
- **Data**: Queries `ANALYTICS.LOSS_RATIO_HISTORY` and `ANALYTICS.PORTFOLIO_RISK`.

### 4. 📊 Customer 360
- **Purpose**: Single view of customer profile, lifetime value, and policy portfolios.
- **Features**:
  - Customer overview KPIs: total policies, lifetime premium, claims count, and risk tier.
  - Policyholder search and cross-sell opportunity identification.
- **Data**: Queries `ANALYTICS.CUSTOMER_360_VIEW` and `GOLD.FACT_POLICY`.

### 5. 🎯 Product Matching
- **Purpose**: Multi-strategy insurance product recommendation assistant.
- **Features**:
  - **ChatGPT-Style Conversational Interface**: Clean enterprise AI layout with welcome empty state, quick scenario chips, and floating message bar.
  - Multi-strategy analysis across 4 pillars: `Needs-Based`, `Profile-Based`, `Risk-Adjusted`, and `Value Optimized`.
- **Data/AI**: Snowflake Cortex Agent (`PRODUCT_MATCHING_AGENT`).

### 6. 📊 Market Intelligence
- **Purpose**: Strategic market trend detection and competitive intelligence across insurance lines.
- **Features**:
  - **ChatGPT-Style Conversational Interface**: Interactive assistant with live market KPI cards for Health, Auto, Life, and Home lines.
  - Revenue tracking, growth rate indicators (`↑ 4.6% growth`), and retention rates.
- **Data/AI**: `ANALYTICS.POLICY_TRENDS` and `INSURANCE_INTELLIGENCE_AGENT`.

### 7. 💰 Competitive Pricing & Optimization
- **Purpose**: Actuarial premium benchmarking and loss ratio optimization.
- **Features**:
  - **ChatGPT-Style Conversational Interface**: Conversational workspace with compact Loss Ratio Snapshot KPI cards.
  - Premium optimization insights, loss ratio breakdown (`LR 64%`), and combined ratio analysis.
- **Data/AI**: `ANALYTICS.LOSS_RATIO_HISTORY` and `INSURANCE_INTELLIGENCE_AGENT`.

### 8. 💬 Chat Assistant
- **Purpose**: Universal enterprise insurance assistant powered by Snowflake Cortex AI.
- **Features**:
  - Multi-modal conversation with inline vehicle/property damage image attachments.
  - Built-in suggested inquiries, persistent chat history, and structured Markdown responses.
- **Data/AI**: `INSURANCE_INTELLIGENCE_ASSISTANT` (Cortex Agent REST API).

---

## ❄️ Snowflake Architecture & Data Integration

The platform integrates directly with the Snowflake Data Cloud using the following schema objects and services:

| Object Type | Name / FQN | Purpose |
| :--- | :--- | :--- |
| **Database** | `INSURANCE_MGMT_SYSTEM` | Central data repository |
| **Table** | `GOLD.FACT_POLICY` | Verified policy dataset (300 live records) |
| **Table** | `CORE.POLICIES` | Fallback policy master table |
| **Table** | `CORE.CLAIMS` | Master claims record table |
| **Table** | `ANALYTICS.FRAUD_PREDICTIONS_ML` | ML fraud scores and alert classifications |
| **Table** | `ANALYTICS.POLICY_TRENDS` | Segment market trends, revenue, growth & retention |
| **Table** | `ANALYTICS.LOSS_RATIO_HISTORY` | Actuarial loss ratios and combined ratios |
| **Table** | `ANALYTICS.CUSTOMER_360_VIEW` | Aggregated customer profiles |
| **Cortex Search** | `ANALYTICS.CLAIM_NOTES_SEARCH` | Vectorized natural language search over investigation notes |
| **Cortex Agent** | `ANALYTICS.INSURANCE_INTELLIGENCE_ASSISTANT` | Universal Insurance Intelligence Assistant |
| **Cortex Agent** | `ANALYTICS.CLAIMS_FRAUD_TRIAGE_AGENT` | Claims Fraud Triage Agent |
| **Cortex Agent** | `GOLD.PRODUCT_MATCHING_AGENT` | Multi-strategy Product Recommendation Agent |

---

## ⚙️ Prerequisites

- **Python**: Version 3.9 or higher installed.
- **Git**: Installed and available in terminal.
- **Snowflake Account**: User access with permissions to `INSURANCE_MGMT_SYSTEM` database.

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shravan421/INSURANCE-INTELLIGENCE-PLATFORM.git
cd INSURANCE-INTELLIGENCE-PLATFORM
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

1. Copy `.env.example` to create your local `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and configure your Snowflake credentials:
   ```env
   SNOWFLAKE_USER=your_snowflake_username
   SNOWFLAKE_PASSWORD=your_snowflake_password
   SNOWFLAKE_ACCOUNT=your_snowflake_account_identifier
   SNOWFLAKE_WAREHOUSE=INSURANCE_WH
   SNOWFLAKE_DATABASE=INSURANCE_MGMT_SYSTEM
   SNOWFLAKE_SCHEMA=GOLD
   SNOWFLAKE_AUTHENTICATOR=snowflake
   ```

3. **Security Note**: Never commit your `.env` file to Git. It is automatically ignored by `.gitignore`.

---

## 🧪 Testing & Verification

To verify your environment configuration and direct Snowflake connection:

```bash
python test_env.py
```

To test connection validation and live query execution directly:
```bash
python -c "import snowflake_utils as sf; print(sf.validate_connection()); print(sf.get_policies_data().head())"
```

Expected output:
```text
{'valid': True, 'user': 'YOUR_USER', 'account': 'YOUR_ACCOUNT'}
   POLICY_ID    TYPE      TIER  PREMIUM     STATUS
0  POL-00000  Health    Bronze   6287.0     Active
```

---

## 💻 Run Application

To start the Streamlit application:

```bash
streamlit run app.py
```

The application will start locally and open in your default browser at `http://localhost:8501`.

---

## 🔀 Team Git Workflow

We follow a branch-based Git workflow. Direct commits to `main` are restricted.

1. **Pull latest `main`**:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push -u origin feature/your-feature-name
   ```
4. **Create Pull Request**: Open a PR on GitHub targeting `main`.

---

## 🛡️ Security Best Practices

- `.env`, `.venv/`, `__pycache__/`, and `.streamlit/secrets.toml` are strictly ignored in `.gitignore`.
- Direct automatic connection uses secure environment variables without prompting for passkeys or exposing secrets in code or logs.
- All raw database errors are intercepted and sanitized before rendering in the UI.
