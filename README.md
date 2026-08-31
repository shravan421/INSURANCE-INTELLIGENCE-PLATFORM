# Risk & Pricing Dashboard

An enterprise-grade, data-driven **Risk & Pricing Dashboard** built with **Python**, **Streamlit**, **Snowflake**, and **Plotly**. Designed for underwriters, risk managers, actuarial analysts, and insurance executives to perform real-time risk assessment, loss ratio monitoring, claims analysis, and interactive pricing simulation.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Directory Structure](#project-directory-structure)
4. [Prerequisites](#prerequisites)
5. [Setup & Installation](#setup--installation)
6. [Environment Configuration](#environment-configuration)
7. [Snowflake Configuration](#snowflake-configuration)
8. [Run Application](#run-application)
9. [Testing](#testing)
10. [Team Git Workflow](#team-git-workflow)
11. [VS Code Team Quickstart](#vs-code-team-quickstart)
12. [Security Best Practices](#security-best-practices)

---

## 🎯 Project Overview

The **Risk & Pricing Dashboard** provides live intelligence and analytical decision-support for enterprise insurance operations. Key capabilities include:

- **Executive KPI Suite**: Live tracking of Gross Written Premium (GWP), Claims Paid, Loss Ratio (%), and Total Active Policies.
- **Underwriting & Risk Workbench**: Scoring policy risks, reviewing plan tiers, and monitoring high-risk portfolios.
- **Claims & Fraud Monitoring**: Tracking claims adjudication, anomaly scores, and detailed investigation notes.
- **Actuarial Rate Modeling**: Interactive rate adjustments and loss ratio scenario planning.
- **Snowflake Cortex AI Assistant**: Natural language querying for policy analytical inquiries.

---

## 🛠️ Technology Stack

- **Core Runtime**: Python 3.9+
- **Web Application Framework**: [Streamlit](https://streamlit.io/) (v1.30.0+)
- **Data Platform**: [Snowflake Data Cloud](https://www.snowflake.com/) (`snowflake-connector-python`)
- **Data Analytics & Processing**: [Pandas](https://pandas.pydata.org/)
- **Data Visualization**: [Plotly](https://plotly.com/) (Express & Graph Objects)
- **Environment Management**: `python-dotenv`

---

## 📁 Project Directory Structure

```text
risk-pricing-dashboard/
│
├── .streamlit/
│   └── config.toml                  # Streamlit layout theme and visual settings
│
├── app.py                           # Main Streamlit application and dashboard UI
├── snowflake_utils.py               # Snowflake connection manager & live SQL query functions
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
cd risk-pricing-dashboard
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
- `feature/risk-dashboard`
- `feature/pricing-dashboard`
- `feature/snowflake-integration`
- `bugfix/dashboard-filter`
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
5. **Create Pull Request**: Open a PR on GitHub targetting `main` for code review.

---

## 💻 VS Code Team Quickstart

For teammates opening this project in VS Code:

1. Clone and open project:
   ```bash
   git clone https://github.com/shravan421/INSURANCE-INTELLIGENCE-PLATFORM.git
   cd risk-pricing-dashboard
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
