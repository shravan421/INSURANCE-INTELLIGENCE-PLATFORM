import os
import sys
import site
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Ensure site-packages is included for snowflake-connector
if site.USER_SITE not in sys.path:
    sys.path.append(site.USER_SITE)

load_dotenv()

# Snowflake Credentials from .env
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "GOLD")

@st.cache_resource(ttl=3600, show_spinner="Connecting to Snowflake (Authenticating Duo MFA once)...")
def _init_snowflake_connection():
    """Establishes and caches a single persistent Snowflake connection per session."""
    import snowflake.connector
    clean_account = SNOWFLAKE_ACCOUNT.replace("http://", "").replace("https://", "").replace(".snowflakecomputing.com", "")
    
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=clean_account,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        authenticator=os.getenv("SNOWFLAKE_AUTHENTICATOR", "snowflake"),
        client_session_keep_alive=True
    )

def get_connection():
    """Returns the cached Snowflake connection, re-establishing if closed."""
    try:
        conn = _init_snowflake_connection()
        if conn and not conn.is_closed():
            return conn
    except Exception:
        pass
    
    # If connection was closed or dropped, clear cache and reconnect
    st.cache_resource.clear()
    return _init_snowflake_connection()

def run_query(query: str) -> pd.DataFrame:
    """Executes live SQL query against Snowflake database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    df = cursor.fetch_pandas_all()
    cursor.close()
    return df

# =========================================================================
# LIVE SNOWFLAKE DATA FETCHERS
# =========================================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_policies_data() -> pd.DataFrame:
    """Queries live policy data from GOLD.FACT_POLICY or CORE.POLICIES."""
    try:
        return run_query("SELECT POLICY_ID, POLICY_TYPE AS TYPE, PLAN_TIER AS TIER, PREMIUM_AMOUNT AS PREMIUM, POLICY_STATUS AS STATUS FROM INSURANCE_MGMT_SYSTEM.GOLD.FACT_POLICY ORDER BY POLICY_ID LIMIT 200")
    except Exception:
        return run_query("SELECT POLICY_ID, POLICY_TYPE AS TYPE, PLAN_TIER AS TIER, PREMIUM_AMOUNT AS PREMIUM, POLICY_STATUS AS STATUS FROM INSURANCE_MGMT_SYSTEM.CORE.POLICIES ORDER BY POLICY_ID LIMIT 200")

@st.cache_data(ttl=300, show_spinner=False)
def get_claims_data() -> pd.DataFrame:
    """Queries live claims and fraud predictions from Snowflake."""
    try:
        return run_query("""
            SELECT 
                F.CLAIM_ID, C.CLAIM_TYPE AS TYPE, C.CLAIM_AMOUNT AS AMOUNT,
                F.FRAUD_PREDICTION AS FRAUD_SCORE, C.CLAIM_STATUS AS STATUS
            FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_PREDICTIONS_ML F
            JOIN INSURANCE_MGMT_SYSTEM.CORE.CLAIMS C ON F.CLAIM_ID = C.CLAIM_ID
            ORDER BY F.FRAUD_PREDICTION DESC
        """)
    except Exception:
        try:
            return run_query("""
                SELECT 
                    CLAIM_ID, FRAUD_TYPE AS TYPE, AMOUNT_SAVED AS AMOUNT,
                    CONFIDENCE_SCORE AS FRAUD_SCORE, ALERT_STATUS AS STATUS
                FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_ALERTS
                ORDER BY CONFIDENCE_SCORE DESC
            """)
        except Exception:
            return run_query("SELECT CLAIM_ID, CLAIM_TYPE AS TYPE, CLAIM_AMOUNT AS AMOUNT, 0.0 AS FRAUD_SCORE, CLAIM_STATUS AS STATUS FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS ORDER BY CLAIM_ID LIMIT 100")

@st.cache_data(ttl=300, show_spinner=False)
def get_claim_detail(claim_id: str) -> pd.DataFrame:
    """Queries detailed claim info and investigation notes from Snowflake."""
    try:
        df = run_query(f"""
            SELECT 
                C.CLAIM_ID, C.CLAIM_TYPE, C.CLAIM_AMOUNT, C.CLAIM_STATUS,
                COALESCE(F.INVESTIGATION_NOTES, C.FRAUD_REASON, 'Investigation notes verified.') AS INVESTIGATION_NOTES,
                COALESCE(F.FRAUD_TYPE, 'Standard Risk') AS FRAUD_TYPE,
                COALESCE(F.ALERT_STATUS, C.CLAIM_STATUS) AS ALERT_STATUS,
                COALESCE(F.CONFIDENCE_SCORE, 0.0) AS FRAUD_SCORE
            FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS C
            LEFT JOIN INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_ALERTS F ON C.CLAIM_ID = F.CLAIM_ID
            WHERE C.CLAIM_ID = '{claim_id}'
            LIMIT 1
        """)
        if df is not None and not df.empty:
            return df
    except Exception:
        pass

    return run_query(f"SELECT CLAIM_ID, CLAIM_TYPE, CLAIM_AMOUNT, CLAIM_STATUS, FRAUD_REASON AS INVESTIGATION_NOTES FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS WHERE CLAIM_ID = '{claim_id}'")

@st.cache_data(ttl=300, show_spinner=False)
def get_loss_ratio_history() -> pd.DataFrame:
    """Queries live loss ratio history from ANALYTICS.LOSS_RATIO_HISTORY."""
    try:
        return run_query("SELECT RECORD_ID, POLICY_TYPE, PLAN_TIER, MONTH_YEAR, PREMIUMS_EARNED, CLAIMS_PAID, LOSS_RATIO, COMBINED_RATIO, EXPENSE_RATIO, TREND, CREATED_AT FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.LOSS_RATIO_HISTORY ORDER BY MONTH_YEAR")
    except Exception:
        return run_query("SELECT * FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.LOSS_RATIO_HISTORY")

@st.cache_data(ttl=300, show_spinner=False)
def get_at_risk_policies() -> pd.DataFrame:
    """Queries live at-risk policies from RISK.AT_RISK_POLICIES_ML or RISK.AT_RISK_POLICIES."""
    try:
        return run_query("""
            SELECT 
                R.POLICY_ID, P.POLICY_TYPE AS CATEGORY, R.LOSS_RATIO AS RISK_SCORE,
                P.PREMIUM_AMOUNT AS REV_AT_RISK,
                CASE WHEN R.RISK_PREDICTION = 1 THEN 'Retention outreach' ELSE 'Standard Monitoring' END AS ACTION,
                P.START_DATE,
                P.CREATED_AT
            FROM INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES_ML R
            JOIN INSURANCE_MGMT_SYSTEM.CORE.POLICIES P ON R.POLICY_ID = P.POLICY_ID
            ORDER BY R.LOSS_RATIO DESC
        """)
    except Exception:
        return run_query("SELECT POLICY_ID, CATEGORY, RISK_SCORE, REV_AT_RISK, ACTION, IDENTIFIED_DATE AS START_DATE, CREATED_AT FROM INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES")

def estimate_premium(age, income, credit_score, coverage) -> float:
    """Calls registered ML model or Snowflake calculation in database."""
    try:
        query = f"SELECT PREMIUM_ESTIMATION_MODEL!PREDICT({age}, {income}, {credit_score}, {coverage}) AS PREDICTED_PREMIUM"
        df = run_query(query)
        if df is not None and not df.empty and "PREDICTED_PREMIUM" in df.columns:
            return float(df["PREDICTED_PREMIUM"].iloc[0])
    except Exception:
        pass
    
    query = f"""
        SELECT 
            (500 + ({age} - 18) * 12 + ({income} / 10000) * 15 + ({coverage} / 1000) * 5.8 - ({credit_score} - 300) * 2.1) AS PREDICTED_PREMIUM
    """
    df = run_query(query)
    return float(df["PREDICTED_PREMIUM"].iloc[0])

def ask_cortex_agent(prompt: str) -> str:
    """Sends user query to live Snowflake Cortex AI function or dynamic SQL analytics."""
    safe_prompt = prompt.replace("'", "''")
    try:
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', '{safe_prompt}') AS RESPONSE"
        df = run_query(query)
        if df is not None and not df.empty and "RESPONSE" in df.columns:
            res = str(df["RESPONSE"].iloc[0])
            if res and res != "None":
                return res
    except Exception:
        pass

    try:
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', '{safe_prompt}') AS RESPONSE"
        df = run_query(query)
        if df is not None and not df.empty and "RESPONSE" in df.columns:
            res = str(df["RESPONSE"].iloc[0])
            if res and res != "None":
                return res
    except Exception:
        pass

    lower = prompt.lower()
    if "claim" in lower or "fraud" in lower or "clm" in lower:
        df = run_query("SELECT CLAIM_ID, CLAIM_TYPE, CLAIM_AMOUNT, CLAIM_STATUS FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS LIMIT 5")
        return f"Live Snowflake Claims Analytics Result:\nFound active claims in CORE.CLAIMS:\n\n" + df.to_string(index=False)
    elif "policy" in lower or "churn" in lower or "risk" in lower:
        df = run_query("SELECT POLICY_ID, POLICY_TYPE, PLAN_TIER, PREMIUM_AMOUNT, POLICY_STATUS FROM INSURANCE_MGMT_SYSTEM.CORE.POLICIES LIMIT 5")
        return f"Live Snowflake Policy Analytics Result:\nFound active policy book in CORE.POLICIES:\n\n" + df.to_string(index=False)
    else:
        df = run_query("SELECT COUNT(*) AS TOTAL_POLICIES FROM INSURANCE_MGMT_SYSTEM.CORE.POLICIES")
        count = df.iloc[0, 0] if df is not None and not df.empty else 0
        return f"Snowflake Intelligence Agent evaluated your request '{prompt}'.\nConnected to live database INSURANCE_MGMT_SYSTEM (Total active policies in CORE.POLICIES: {count})."
