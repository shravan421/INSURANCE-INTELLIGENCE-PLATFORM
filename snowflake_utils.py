import os
import sys
import site
import json
import tempfile
import requests
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

# Agent Configuration
AGENT_NAME = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_MASTER_AGENT"
CLAIM_EVIDENCE_STAGE = "INSURANCE_MGMT_SYSTEM.ANALYTICS.CLAIM_EVIDENCE"

# Build REST API URL
_clean_account = SNOWFLAKE_ACCOUNT.replace("http://", "").replace("https://", "").replace(".snowflakecomputing.com", "")
SNOWFLAKE_BASE_URL = f"https://{_clean_account}.snowflakecomputing.com"
AGENT_API_URL = f"{SNOWFLAKE_BASE_URL}/api/v2/cortex/agent:run"

# =============================================================================
# SNOWFLAKE CONNECTION
# =============================================================================
@st.cache_resource(ttl=3600, show_spinner="Connecting to Snowflake (Authenticating Duo MFA once)...")
def _init_snowflake_connection():
    """Establishes and caches a single persistent Snowflake connection per session."""
    import snowflake.connector
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=_clean_account,
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

# =============================================================================
# LIVE SNOWFLAKE DATA FETCHERS
# =============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_policies_data() -> pd.DataFrame:
    """Queries live policy data from GOLD.FACT_POLICY or CORE.POLICIES."""
    try:
        return run_query("""
            SELECT POLICY_ID, POLICY_TYPE AS TYPE, PLAN_TIER AS TIER,
            PREMIUM_AMOUNT AS PREMIUM, POLICY_STATUS AS STATUS
            FROM INSURANCE_MGMT_SYSTEM.GOLD.FACT_POLICY
            ORDER BY POLICY_ID
        """)
    except Exception:
        return run_query("""
            SELECT POLICY_ID, POLICY_TYPE AS TYPE, PLAN_TIER AS TIER,
            PREMIUM_AMOUNT AS PREMIUM, POLICY_STATUS AS STATUS
            FROM INSURANCE_MGMT_SYSTEM.CORE.POLICIES
            ORDER BY POLICY_ID
        """)

@st.cache_data(ttl=300, show_spinner=False)
def get_claims_data() -> pd.DataFrame:
    """Queries live claims and fraud predictions from Snowflake."""
    try:
        return run_query("""
            SELECT F.CLAIM_ID, C.CLAIM_TYPE AS TYPE, C.CLAIM_AMOUNT AS AMOUNT,
            F.FRAUD_PREDICTION AS FRAUD_SCORE, C.CLAIM_STATUS AS STATUS
            FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_PREDICTIONS_ML F
            JOIN INSURANCE_MGMT_SYSTEM.CORE.CLAIMS C ON F.CLAIM_ID = C.CLAIM_ID
            ORDER BY F.FRAUD_PREDICTION DESC
        """)
    except Exception:
        try:
            return run_query("""
                SELECT CLAIM_ID, FRAUD_TYPE AS TYPE, AMOUNT_SAVED AS AMOUNT,
                CONFIDENCE_SCORE AS FRAUD_SCORE, ALERT_STATUS AS STATUS
                FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_ALERTS
                ORDER BY CONFIDENCE_SCORE DESC
            """)
        except Exception:
            return run_query("""
                SELECT CLAIM_ID, CLAIM_TYPE AS TYPE, CLAIM_AMOUNT AS AMOUNT,
                0.0 AS FRAUD_SCORE, CLAIM_STATUS AS STATUS
                FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS
                ORDER BY CLAIM_ID LIMIT 100
            """)

@st.cache_data(ttl=300, show_spinner=False)
def get_claim_detail(claim_id: str) -> pd.DataFrame:
    """Queries detailed claim info and investigation notes from Snowflake."""
    try:
        df = run_query(f"""
            SELECT C.CLAIM_ID, C.CLAIM_TYPE, C.CLAIM_AMOUNT, C.CLAIM_STATUS,
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
    return run_query(f"""
        SELECT CLAIM_ID, CLAIM_TYPE, CLAIM_AMOUNT, CLAIM_STATUS,
        FRAUD_REASON AS INVESTIGATION_NOTES
        FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS
        WHERE CLAIM_ID = '{claim_id}'
    """)

@st.cache_data(ttl=300, show_spinner=False)
def get_loss_ratio_history() -> pd.DataFrame:
    """Queries live loss ratio history."""
    try:
        return run_query("""
            SELECT RECORD_ID, POLICY_TYPE, PLAN_TIER, MONTH_YEAR, PREMIUMS_EARNED,
            CLAIMS_PAID, LOSS_RATIO, COMBINED_RATIO, EXPENSE_RATIO, TREND, CREATED_AT
            FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.LOSS_RATIO_HISTORY
            ORDER BY MONTH_YEAR
        """)
    except Exception:
        return run_query("SELECT * FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.LOSS_RATIO_HISTORY")

@st.cache_data(ttl=300, show_spinner=False)
def get_at_risk_policies() -> pd.DataFrame:
    """Queries live at-risk policies."""
    try:
        return run_query("""
            SELECT R.POLICY_ID, P.POLICY_TYPE AS CATEGORY, R.LOSS_RATIO AS RISK_SCORE,
            P.PREMIUM_AMOUNT AS REV_AT_RISK,
            CASE WHEN R.RISK_PREDICTION = 1 THEN 'Retention outreach' ELSE 'Standard Monitoring' END AS ACTION,
            P.START_DATE, P.CREATED_AT
            FROM INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES_ML R
            JOIN INSURANCE_MGMT_SYSTEM.CORE.POLICIES P ON R.POLICY_ID = P.POLICY_ID
            ORDER BY R.LOSS_RATIO DESC
        """)
    except Exception:
        return run_query("""
            SELECT POLICY_ID, CATEGORY, RISK_SCORE, REV_AT_RISK, ACTION,
            IDENTIFIED_DATE AS START_DATE, CREATED_AT
            FROM INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES
        """)

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
        SELECT (500 + ({age} - 18) * 12 + ({income} / 10000) * 15
        + ({coverage} / 1000) * 5.8 - ({credit_score} - 300) * 2.1) AS PREDICTED_PREMIUM
    """
    df = run_query(query)
    return float(df["PREDICTED_PREMIUM"].iloc[0])

# =============================================================================
# CORTEX AGENT API (NEW -- calls INSURANCE_MASTER_AGENT via REST / SQL)
# =============================================================================
def _get_auth_token():
    """Extract the session token from the active snowflake.connector connection."""
    conn = get_connection()
    return conn.rest._token

def ask_cortex_agent(prompt: str) -> str:
    """
    Calls INSURANCE_MASTER_AGENT via SQL DATA_AGENT_RUN.
    Uses json.dumps for proper escaping of special characters.
    """
    try:
        body = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        })
        safe_body = body.replace("'", "''")
        query = f"""
            SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                '{AGENT_NAME}',
                '{safe_body}'
            ) AS RESPONSE
        """
        df = run_query(query)
        if df is not None and not df.empty and "RESPONSE" in df.columns:
            raw_response = str(df["RESPONSE"].iloc[0])
            return _parse_agent_response(raw_response)
        return "No response received from agent."
    except Exception as e:
        return f"Error calling Cortex Agent: {str(e)}"

def _parse_agent_response(content: str) -> str:
    """Parse Cortex Agent SSE (Server-Sent Events) streaming response."""
    full_text = []
    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("data:"):
            continue
        data_str = line[5:].strip()
        if data_str == "[DONE]":
            continue
        try:
            event_data = json.loads(data_str)
            delta = event_data.get("delta", {})
            if "content" in delta:
                for item in delta["content"]:
                    if item.get("type") == "text":
                        full_text.append(item.get("text", ""))
                    elif item.get("type") == "tool_results":
                        full_text.append(str(item.get("content", "")))
            for choice in event_data.get("choices", []):
                d = choice.get("delta", {})
                if "content" in d:
                    full_text.append(d["content"])
        except (json.JSONDecodeError, TypeError):
            continue
    if full_text:
        return "".join(full_text)

    # Fallback: try parsing as single JSON (DATA_AGENT_RUN format)
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict) and "content" in parsed:
            for item in parsed["content"]:
                if item.get("type") == "text":
                    full_text.append(item.get("text", ""))
            if full_text:
                return "\n".join(full_text)
        if isinstance(parsed, dict) and "message" in parsed:
            for item in parsed["message"].get("content", []):
                if item.get("type") == "text":
                    full_text.append(item["text"])
            if full_text:
                return "\n".join(full_text)
    except (json.JSONDecodeError, TypeError):
        pass

    return content if content else "No response received from agent."

def parse_agent_thinking(content: str) -> str:
    """
    Extract real thinking + tool execution traces from the agent response.
    Returns a formatted string showing which tools were called and their results.
    Used by hackaton.py / app.py for the 'Thinking Process' tab.
    """
    traces = []
    try:
        parsed = json.loads(content) if isinstance(content, str) else content
        items = parsed.get("content", []) if isinstance(parsed, dict) else []
        for item in items:
            item_type = item.get("type", "")
            if item_type == "thinking":
                text = item.get("thinking", {}).get("text", "").strip()
                if text:
                    traces.append(f"[THINKING] {text}")
            elif item_type == "tool_use":
                tool = item.get("tool_use", {})
                name = tool.get("name", "unknown")
                inp = tool.get("input", {})
                traces.append(f"[TOOL CALL] {name}")
                if inp:
                    for k, v in inp.items():
                        if k != "pruning_question":
                            traces.append(f"  Input: {k} = {v}")
            elif item_type == "tool_result":
                result = item.get("tool_result", {})
                name = result.get("name", "unknown")
                status = result.get("status", "unknown")
                traces.append(f"[TOOL RESULT] {name} -> {status}")
                for c in result.get("content", []):
                    if c.get("type") == "json":
                        j = c.get("json", {})
                        if "sql" in j:
                            traces.append(f"  SQL: {j['sql'][:200]}...")
                        if "error" in j:
                            traces.append(f"  Error: {j['error'][:200]}")
                        if "result_set" in j:
                            rows = j["result_set"].get("data", [])
                            traces.append(f"  Rows returned: {len(rows)}")
        if traces:
            return "\n".join(traces)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass
    return ""

# =============================================================================
# IMAGE UPLOAD / STAGE FUNCTIONS (NEW -- for image-based claim estimation)
# =============================================================================
def upload_image_to_stage(file_bytes: bytes, filename: str) -> bool:
    """Upload an image to the CLAIM_EVIDENCE stage. Returns True/False."""
    try:
        conn = get_connection()
        safe_filename = filename.replace(" ", "_")
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = os.path.join(temp_dir, safe_filename)
            with open(local_path, "wb") as f:
                f.write(file_bytes)
            local_path_normalized = local_path.replace("\\", "/")
            put_sql = f"PUT 'file://{local_path_normalized}' @{CLAIM_EVIDENCE_STAGE} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
            conn.cursor().execute(put_sql)
        return True
    except Exception as e:
        st.error(f"Upload error detail: {e}")
        return False

def list_stage_files() -> list:
    """List all files in the CLAIM_EVIDENCE stage. Returns list of filenames."""
    try:
        df = run_query(f"LS @{CLAIM_EVIDENCE_STAGE}")
        if "name" in df.columns:
            return sorted([path.split('/')[-1] for path in df["name"].tolist()])
        return []
    except Exception:
        return []

def get_image_from_stage(filename: str) -> bytes:
    """Download an image from stage and return bytes."""
    try:
        conn = get_connection()
        with tempfile.TemporaryDirectory() as temp_dir:
            conn.cursor().execute(
                f"GET @{CLAIM_EVIDENCE_STAGE}/{filename} 'file://{temp_dir}'"
            )
            local_path = os.path.join(temp_dir, filename)
            with open(local_path, "rb") as f:
                return f.read()
    except Exception:
        return None
