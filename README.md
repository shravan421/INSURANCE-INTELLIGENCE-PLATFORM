# Insurance Intelligence Platform

An enterprise-grade, data-driven **Insurance Intelligence Platform** built with **Python**, **Streamlit**, **Snowflake (Cortex AI & Data Cloud)**, and **Plotly**. Designed for underwriters, risk managers, actuarial analysts, and insurance executives to perform real-time policy book underwriting, AI-powered claims triage with visual damage image analysis, loss ratio monitoring, and dynamic predictive pricing simulation.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Platform Capabilities & Recent Updates](#-key-platform-capabilities--recent-updates)
3. [Technology Stack](#-technology-stack)
4. [Project Directory Structure](#-project-directory-structure)
5. [Prerequisites](#-prerequisites)
6. [Setup & Installation](#-setup--installation)
7. [Environment Configuration](#-environment-configuration)
8. [Snowflake Configuration](#-snowflake-configuration)
9. [Run Application](#-run-application)
10. [Testing](#-testing)
11. [Team Git Workflow](#-team-git-workflow)
12. [VS Code Team Quickstart](#-vs-code-team-quickstart)
13. [Security Best Practices](#-security-best-practices)

---

## 🎯 Project Overview

The **Insurance Intelligence Platform** provides live intelligence and analytical decision-support for enterprise insurance operations across underwriting, claims investigation, actuarial modeling, and conversational AI assistance.

Key modules include:
- **Underwriting Workbench**: Real-time policy book management, live Snowflake policy dataset auditing (300 live records), dynamic predictive ML premium quoting, and interactive actuarial rate driver calculations.
- **Claims & Fraud Console**: AI-powered claims triage, fraud risk scoring, automated SIU escalation workflows, and Cortex semantic search over investigation notes.
- **AI Chat Assistant (Cortex Powered)**: ChatGPT-style conversational assistant with inline image/damage file attachments, persistent chat history, and live Cortex Agent (`INSURANCE_MASTER_AGENT`) execution.
- **Actuarial Rate Modeling**: Interactive rate adjustments, combined ratio scenario planning, and loss ratio trend monitoring.

---

## ⚡ Key Platform Capabilities & Recent Updates

### 🖼️ AI Chat Assistant with Visual Damage & Document Uploads
- **Inline Image & File Attachments**: Underwriters and claims adjusters can upload vehicle damage photos, structural property damage images, or claim PDFs directly inside the chat console.
- **Visual Claim Triage**: Attach damage images alongside prompt inquiries to evaluate claim context, estimate repair severity, and trigger automated fraud risk assessments.
- **ChatGPT-Style UX**: Modern responsive interface with persistent conversation history, model thinking process drawer, and smooth streaming responses.

### 🛡️ Audited Live Snowflake Data Integration
- **Verified Policy Book**: 100% verified live query execution against `INSURANCE_MGMT_SYSTEM.GOLD.FACT_POLICY` (300 live policy rows).
- **Accurate Real-Time KPIs**:
  - **Total Policies**: `300`
  - **Active Book**: `180`
  - **Total Premium Volume**: `$2,320,783`
  - **Average Premium**: `$7,735.94`
- **Dynamic Predictive ML Quoting**: Dynamic premium valuation computed in real time via Snowflake SQL predictive algorithms with reactive actuarial rate multipliers (Credit Score, Age, Coverage Exposure).

---

## 🛠️ Technology Stack

- **Core Runtime**: Python 3.9+
- **Web Application Framework**: [Streamlit](https://streamlit.io/) (v1.30.0+)
- **Data Platform**: [Snowflake Data Cloud](https://www.snowflake.com/) (`snowflake-connector-python`)
- **AI & Data Agents**: Snowflake Cortex AI (`SNOWFLAKE.CORTEX.DATA_AGENT_RUN`)
- **Data Analytics & Processing**: [Pandas](https://pandas.pydata.org/)
- **Data Visualization**: [Plotly](https://plotly.com/) (Express & Graph Objects)
- **Environment Management**: `python-dotenv`

---

## 📁 Project Directory Structure

```text
INSURANCE-INTELLIGENCE-PLATFORM/
│
├── .streamlit/
│   └── config.toml                  # Streamlit layout theme and visual settings
│
├── app.py                           # Main Streamlit application and platform UI
├── snowflake_utils.py               # Snowflake connection manager, Cortex agent, & live SQL queries
├── test_env.py                      # Environment variable & Snowflake connection validation script
│
├── requirements.txt                 # Project Python package dependencies
├── README.md                        # Project documentation and setup guide
├── .gitignore                       # Git ignore rules for credentials, caches, and venv
└── .env.example                     # Template file for environment variable setup
```

---

## ⚙️ Prerequisites

- **Python**: Version 3.9 or higher installed.
- **Git**: Installed and available in terminal.
- **Snowflake Account**: User access with permissions to `INSURANCE_MGMT_SYSTEM` database (or local `.env` configured).

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shravan421/INSURANCE-INTELLIGENCE-PLATFORM.git
cd INSURANCE-INTELLIGENCE-PLATFORM
```

### 2. Create Virtual Environment

**Windows:**
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
2. Open `.env` and fill in your Snowflake credentials and database configuration:
   ```env
   SNOWFLAKE_USER=your_snowflake_username
   SNOWFLAKE_PASSWORD=your_snowflake_password
   SNOWFLAKE_ACCOUNT=your_snowflake_account_identifier
   SNOWFLAKE_WAREHOUSE=HACKATHONTEAMAVENGERS
   SNOWFLAKE_DATABASE=INSURANCE_MGMT_SYSTEM
   SNOWFLAKE_SCHEMA=GOLD
   SNOWFLAKE_AUTHENTICATOR=snowflake
   ```
3. **NEVER** commit your `.env` file to Git. It is automatically ignored by `.gitignore`.

---

## ❄️ Snowflake Configuration

The application authenticates securely to Snowflake using parameters loaded via environment variables in `snowflake_utils.py`:

- Connection settings are dynamically read using `os.getenv()`.
- Credentials remain strictly local to your machine.
- All policy, claims, loss ratio, and analytics queries run strictly live against your Snowflake Data Cloud tables.
- Conversational queries invoke Snowflake Cortex Data Agent (`INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_MASTER_AGENT`).

---

## 💻 Run Application

To launch the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will start locally and open in your default browser at `http://localhost:8501`.

---

## 🧪 Testing

To test and verify your local environment configuration and Snowflake connection:

```bash
python test_env.py
```

If configured correctly, it will print confirmation that environment variables were successfully loaded.

---

## 🔀 Team Git Workflow

We follow a branch-based Git workflow. Direct commits to `main` are restricted.

### Branch Naming Conventions
- `feature/insurance-intelligence`
- `feature/damage-image-attachments`
- `feature/underwriting-workbench`
- `feature/snowflake-integration`
- `feature/<developer-name>`

### Standard Development Workflow

1. **Pull latest `main`**:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "Add description of your changes"
   ```
4. **Push branch to GitHub**:
   ```bash
   git push -u origin feature/your-feature-name
   ```
5. **Create Pull Request**: Open a PR on GitHub targeting `main` for code review.

---

## 💻 VS Code Team Quickstart

For teammates opening this project in VS Code:

1. Clone and open project:
   ```bash
   git clone https://github.com/shravan421/INSURANCE-INTELLIGENCE-PLATFORM.git
   cd INSURANCE-INTELLIGENCE-PLATFORM
   code .
   ```
2. Create and activate virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure `.env`:
   - Copy `.env.example` -> `.env`
   - Enter your Snowflake credentials.
5. Launch app:
   ```powershell
   streamlit run app.py
   ```

---

## 🛡️ Security Best Practices

- `.env`, `*.pyc`, `__pycache__/`, `.venv/`, and `.streamlit/secrets.toml` are strictly ignored in `.gitignore`.
- Always inspect `git status` before committing to ensure no credentials or secret keys are staged.
