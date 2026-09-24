# Insurance Intelligence Platform

An enterprise-grade **AI-Powered Insurance Risk & Claims Management System** built on **Snowflake Cortex AI**, **Streamlit**, and **Plotly**. Designed for the Insurance & Financial Services industry to automate premium estimation, claims analysis, fraud detection, and policy risk prediction across Health, Auto, Life, and Home insurance products.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Platform Capabilities](#platform-capabilities)
3. [Architecture Overview](#architecture-overview)
4. [Technology Stack](#technology-stack)
5. [Snowflake Features Used](#snowflake-features-used)
6. [Project Structure](#project-structure)
7. [Application Modules](#application-modules)
8. [Snowflake Data Architecture](#snowflake-data-architecture)
9. [Cortex Agents](#cortex-agents)
10. [Prerequisites](#prerequisites)
11. [Setup & Installation](#setup--installation)
12. [Environment Configuration](#environment-configuration)
13. [Running the Application](#running-the-application)
14. [Testing & Verification](#testing--verification)
15. [Security](#security)

---

## Problem Statement

Insurers face challenges in manual underwriting, slow claims processing, reactive fraud detection, and fragmented customer views. This platform addresses these by providing:

- **Automated premium estimation** using ML models and actuarial rule engines
- **AI-powered claims triage** with fraud risk scoring and natural language investigation search
- **Proactive risk identification** of at-risk policies and churn-prone customers
- **Real-time analytics and predictive insights** for data-driven decision-making
- **Multi-modal claim assessment** with image-based damage estimation

---

## Platform Capabilities

### Underwriting Automation
- Live policy book with status filtering (Active, Expired, Cancelled, Pending)
- ML-powered premium calculator with actuarial rate driver sensitivity controls
- Explainable AI risk scoring across 8 weighted underwriting factors
- Automated underwriting decisions with downloadable policy binder PDFs

### Claims & Fraud Intelligence
- Natural language search over claim investigation notes via Cortex Search
- ML fraud prediction scores with anomaly indicators
- Conversational AI fraud triage with multi-turn investigation context
- Image upload and AI-powered visual damage assessment for claim evidence

### Risk & Portfolio Analytics
- Loss ratio and combined ratio trend analysis with interactive Plotly charts
- At-risk policy identification with ML-based retention scoring
- Churn prediction with risk factor decomposition
- Natural language queries against semantic models via Cortex Analyst

### Customer 360
- Unified customer profiles with lifetime premium, claims history, and risk tier
- Policy portfolio breakdown with cross-sell opportunity identification
- AI-generated retention strategies per customer

### Intelligence Hub
- **Product Matching Agent**: Multi-strategy product recommendations (Needs-Based, Profile-Based, Risk-Adjusted, Value Optimized)
- **Market Intelligence Agent**: Strategic trend detection across Health, Auto, Life, and Home segments with revenue tracking and growth indicators
- **Price Optimization Agent**: Competitive premium benchmarking, loss ratio optimization, and combined ratio analysis

### Universal AI Assistant
- Conversational interface powered by Snowflake Cortex Agents
- 9 quick-inquiry prompts covering policies, claims, fraud, risk, and image analysis
- Multi-modal support with inline image attachment for claim evidence photos
- AI reasoning trace visibility with dedicated thinking/execution tabs

---

## Architecture Overview

```
                        +-------------------+
                        |    Streamlit UI   |
                        |   (6 Modules)     |
                        +--------+----------+
                                 |
                    +------------+------------+
                    |                         |
            +-------+-------+       +--------+--------+
            | snowflake_utils|       |   components/   |
            | (Backend Core) |       | header, sidebar |
            +-------+-------+       |    helpers      |
                    |               +-----------------+
       +------------+------------+
       |            |            |
  +----+----+ +----+----+ +----+----+
  | Cortex  | | Cortex  | |  ML     |
  | Agents  | | Search  | | Models  |
  | (5+)    | | Service | | (UDFs)  |
  +---------+ +---------+ +---------+
       |            |            |
  +----+------------+------------+----+
  |     INSURANCE_MGMT_SYSTEM DB      |
  |  GOLD | CORE | ANALYTICS | RISK   |
  |              PREMIUM               |
  +------------------------------------+
```

---

## Technology Stack

| Layer | Technology | Version |
|:------|:-----------|:--------|
| Frontend | Streamlit with custom enterprise CSS design system | 1.30.0+ |
| AI/ML | Snowflake Cortex Agents, Cortex Search, Cortex Analyst, ML Model UDFs | - |
| Data Platform | Snowflake Data Cloud | - |
| Connector | snowflake-connector-python (with Snowpark session auto-detection) | 3.6.0+ |
| Visualization | Plotly Express & Graph Objects | 5.18.0+ |
| Data Processing | Pandas | 2.0.0+ |
| Document Generation | fpdf2 (policy binder PDFs) | 2.7.0+ |
| Environment | python-dotenv | 1.0.0+ |

---

## Snowflake Features Used

| Feature | How It's Used |
|:--------|:-------------|
| **Cortex Agents** (`DATA_AGENT_RUN`) | 5+ purpose-built agents for underwriting, claims triage, risk retention, product matching, and intelligence |
| **Cortex Search** (`SEARCH_PREVIEW`) | Natural language search over claim investigation notes and fraud alert histories |
| **Cortex Analyst** (Semantic Models) | Natural language queries against insurance semantic model for ad-hoc analytics |
| **ML Model UDFs** (`PREDICT()`) | Premium estimation model for real-time actuarial pricing |
| **Snowflake Stages** | Image upload/retrieval for multi-modal claim evidence analysis |
| **AI/SQL** | Embedded analytical SQL across all modules with ML-enriched result sets |
| **Snowpark Session Detection** | Auto-detects Streamlit-in-Snowflake (SiS) vs local environment for seamless deployment |

---

## Project Structure

```
INSURANCE-INTELLIGENCE-PLATFORM/
|
+-- app.py                    # Main Streamlit entry point and tab router
+-- snowflake_utils.py        # Backend: Snowflake connection, Cortex Agents, ML models, SQL queries
+-- requirements.txt          # Python dependencies
+-- test_env.py               # Environment and connection validation
|
+-- tabs/
|   +-- underwriting.py       # Underwriting Workbench (policy book, ML calculator, AI copilot)
|   +-- claims_fraud.py       # Claims & Fraud Console (Cortex Search, fraud triage chat)
|   +-- risk_pricing.py       # Risk & Pricing Dashboard (loss ratios, at-risk policies, Cortex Analyst)
|   +-- customer_360.py       # Customer 360 (unified profiles, retention strategy AI)
|   +-- intelligence_hub.py   # Intelligence Hub (product matching, market intel, competitive pricing)
|   +-- chat_assistant.py     # Universal AI Chat Assistant (multi-modal with image support)
|
+-- components/
|   +-- header.py             # Dual-brand enterprise header with live connection badge
|   +-- sidebar.py            # 6-tab navigation with connection status indicator
|   +-- helpers.py            # Response parsing, typewriter effects, error rendering
|
+-- styles/
|   +-- global_css.py         # Enterprise CSS design system (Inter font, card panels, KPI cards)
|
+-- .streamlit/
|   +-- config.toml           # Streamlit server configuration
|
+-- .env.example              # Template for Snowflake credentials
+-- .gitignore                # Ignores .env, .venv, __pycache__, IDE files
```

---

## Application Modules

### 1. Underwriting Workbench
Real-time policy book management with ML-powered premium estimation and AI underwriting copilot.
- Policy book overview with KPI cards and status filtering
- Interactive premium calculator with sliders for age, income, credit score, and coverage
- Explainable risk scoring engine (8 weighted factors) with color-coded decision banners
- AI-generated underwriting narrative via `UNDERWRITING_PREMIUM_AGENT`
- Downloadable policy binder PDF generation

### 2. Claims & Fraud Console
AI-powered claims investigation and fraud detection workspace.
- **Cortex Search Panel**: Natural language search over `CLAIM_NOTES_SEARCH` for instant investigation lookups
- **Fraud Triage Chat**: Select a claim, inspect details (fraud type, anomaly score, investigation notes), then run multi-turn conversational analysis via `CLAIMS_FRAUD_TRIAGE_AGENT`
- Fraud score indicators and SIU escalation recommendations

### 3. Risk & Pricing Dashboard
Portfolio-level risk analytics with actuarial modeling and semantic model querying.
- Loss ratio and combined ratio trend charts (Plotly)
- At-risk policy retention table with ML risk scores
- **Cortex Analyst Panel**: Natural language queries against `INSURANCE_INTELLIGENCE_MODEL` semantic model

### 4. Customer 360
Single-pane customer view with AI-driven retention strategies.
- Customer search and selection with profile KPI cards (lifetime premium, claims count, risk tier)
- Policy portfolio table with coverage breakdown
- AI retention strategy generation via `PORTFOLIO_RISK_RETENTION_AGENT` with dialog-style chat

### 5. Intelligence Hub
Strategic intelligence with three sub-tabs:
- **Product Matching**: Multi-strategy recommendation engine via `PRODUCT_MATCHING_AGENT` (Needs-Based, Profile-Based, Risk-Adjusted, Value Optimized)
- **Market Intelligence**: Market segment KPI cards (Health, Auto, Life, Home) with revenue, growth rates, and retention metrics. Conversational trend analysis via `MARKET_INTELLIGENCE_AGENT`
- **Competitive Pricing**: Loss ratio snapshot cards with competitive benchmarking chat via `PRICE_OPTIMIZATION_AGENT`

### 6. Chat Assistant
Universal enterprise AI assistant with multi-modal capabilities.
- 9 quick-inquiry buttons covering policy, claims, fraud, risk, and image-based analysis
- Inline image attachment for claim evidence photos (uploaded to Snowflake stage, analyzed by agent)
- AI reasoning trace visibility (Response tab + Thinking Process tab)
- Persistent multi-turn conversation history

---

## Snowflake Data Architecture

### Database: `INSURANCE_MGMT_SYSTEM`

| Schema | Object | Type | Purpose |
|:-------|:-------|:-----|:--------|
| `GOLD` | `FACT_POLICY` | Table | Curated policy dataset |
| `CORE` | `POLICIES` | Table | Policy master table |
| `CORE` | `CLAIMS` | Table | Claims records |
| `CORE` | `CUSTOMERS` | Table | Customer demographics and profiles |
| `ANALYTICS` | `FRAUD_PREDICTIONS_ML` | Table | ML fraud scores and classifications |
| `ANALYTICS` | `FRAUD_ALERTS` | Table | Fraud alerts with investigation notes |
| `ANALYTICS` | `LOSS_RATIO_HISTORY` | Table | Actuarial loss ratios and combined ratios |
| `ANALYTICS` | `POLICY_TRENDS` | Table | Market segment trends, revenue, growth |
| `ANALYTICS` | `CUSTOMER_360_VIEW` | Table | Aggregated customer profiles |
| `ANALYTICS` | `CLAIM_NOTES_SEARCH` | Cortex Search Service | NL search over investigation notes |
| `ANALYTICS` | `CLAIM_EVIDENCE` | Stage | Claim evidence image storage |
| `RISK` | `AT_RISK_POLICIES_ML` | Table | ML-predicted at-risk policies |
| `RISK` | `CHURN_PREDICTIONS` | Table | Churn probability and risk factors |
| `PREMIUM` | `PREMIUM_CALCULATIONS` | Table | Rule-based premium calculations |
| `PREMIUM` | `PREMIUM_CALCULATIONS_ML` | Table | ML premium predictions |

---

## Cortex Agents

| Agent | Schema | Purpose |
|:------|:-------|:--------|
| `INSURANCE_INTELLIGENCE_ASSISTANT` | GOLD | Universal insurance assistant for cross-domain queries |
| `UNDERWRITING_PREMIUM_AGENT` | GOLD | Underwriting narrative generation and premium analysis |
| `CLAIMS_FRAUD_TRIAGE_AGENT` | GOLD | Fraud investigation triage and SIU escalation recommendations |
| `PORTFOLIO_RISK_RETENTION_AGENT` | GOLD | Portfolio risk assessment and customer retention strategies |
| `PRODUCT_MATCHING_AGENT` | GOLD | Multi-strategy insurance product recommendations |
| `MARKET_INTELLIGENCE_AGENT` | GOLD | Market trend detection and competitive intelligence |
| `PRICE_OPTIMIZATION_AGENT` | GOLD | Competitive pricing analysis and premium optimization |

---

## Prerequisites

- **Python** 3.9+
- **Git** installed and available in terminal
- **Snowflake Account** with access to `INSURANCE_MGMT_SYSTEM` database
- Cortex Agents and Search Services provisioned in the target Snowflake account

---

## Setup & Installation

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

## Environment Configuration

1. Copy the template:
   ```bash
   cp .env.example .env
   ```

2. Configure your Snowflake credentials in `.env`:
   ```env
   SNOWFLAKE_USER=your_snowflake_username
   SNOWFLAKE_PASSWORD=your_snowflake_password
   SNOWFLAKE_ACCOUNT=your_snowflake_account_identifier
   SNOWFLAKE_WAREHOUSE=INSURANCE_WH
   SNOWFLAKE_DATABASE=INSURANCE_MGMT_SYSTEM
   SNOWFLAKE_SCHEMA=GOLD
   SNOWFLAKE_AUTHENTICATOR=snowflake
   ```

3. The `.env` file is excluded from version control via `.gitignore`.

---

## Running the Application

```bash
streamlit run app.py
```

The application starts at `http://localhost:8501`. The platform auto-detects the runtime environment (Streamlit-in-Snowflake or local) and establishes the appropriate Snowflake session.

---

## Testing & Verification

Validate environment configuration:

```bash
python test_env.py
```

Verify Snowflake connectivity and data access:

```bash
python -c "import snowflake_utils as sf; print(sf.validate_connection()); print(sf.get_policies_data().head())"
```

---

## Security

- Credentials are loaded from environment variables only; never hardcoded
- `.env`, `.venv/`, `__pycache__/`, and `.streamlit/secrets.toml` are excluded via `.gitignore`
- Database errors are intercepted and sanitized before rendering in the UI
- Error logs use `[SECURITY REDACTED LOG]` to prevent credential leakage in outputs
