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
AGENT_NAME = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_INTELLIGENCE_ASSISTANT"
UNDERWRITING_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.UNDERWRITING_PREMIUM_AGENT"
CLAIMS_FRAUD_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.CLAIMS_FRAUD_TRIAGE_AGENT"
RISK_RETENTION_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.PORTFOLIO_RISK_RETENTION_AGENT"
INTELLIGENCE_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_INTELLIGENCE_ASSISTANT"
PRODUCT_MATCHING_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.PRODUCT_MATCHING_AGENT"
MARKET_INTELLIGENCE_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.MARKET_INTELLIGENCE_AGENT"
PRICE_OPTIMIZATION_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.PRICE_OPTIMIZATION_AGENT"
INSURANCE_INTELLIGENCE_AGENT = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_INTELLIGENCE_AGENT"
CLAIM_EVIDENCE_STAGE = "INSURANCE_MGMT_SYSTEM.ANALYTICS.CLAIM_EVIDENCE"
SEMANTIC_MODEL = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_SEMANTIC_MODEL"
INTELLIGENCE_SEMANTIC_MODEL = "INSURANCE_MGMT_SYSTEM.GOLD.INSURANCE_INTELLIGENCE_MODEL"
CORTEX_SEARCH_SERVICE = "INSURANCE_MGMT_SYSTEM.ANALYTICS.CLAIM_NOTES_SEARCH"

# Build REST API URL
_clean_account = SNOWFLAKE_ACCOUNT.replace("http://", "").replace("https://", "").replace(".snowflakecomputing.com", "")
SNOWFLAKE_BASE_URL = f"https://{_clean_account}.snowflakecomputing.com"
AGENT_API_URL = f"{SNOWFLAKE_BASE_URL}/api/v2/cortex/agent:run"

# =============================================================================
# SNOWFLAKE CONNECTION — Snowpark session first, connector fallback
# =============================================================================
_snowpark_session = None

def _get_snowpark_session():
    """Try to get Snowpark active session (works in Workspaces / SiS)."""
    global _snowpark_session
    if _snowpark_session is not None:
        return _snowpark_session
    try:
        from snowflake.snowpark.context import get_active_session
        _snowpark_session = get_active_session()
        return _snowpark_session
    except Exception:
        return None

@st.cache_resource(ttl=3600, show_spinner="Connecting to Snowflake...")
def _init_snowflake_connection():
    """Establishes and caches a single persistent Snowflake connection per session."""
    import snowflake.connector
    authenticator = os.getenv("SNOWFLAKE_AUTHENTICATOR", "snowflake")
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=_clean_account,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        authenticator=authenticator,
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

def validate_connection() -> dict:
    """Executes a lightweight query to validate the active Snowflake connection."""
    try:
        df = run_query("SELECT CURRENT_USER() AS USER_NAME, CURRENT_ACCOUNT() AS ACCOUNT_NAME;")
        if df is not None and not df.empty:
            row = df.iloc[0]
            return {
                "valid": True,
                "user": str(row.get("USER_NAME", "")),
                "account": str(row.get("ACCOUNT_NAME", ""))
            }
    except Exception as e:
        print(f"[SECURITY REDACTED LOG] Snowflake connection validation failed: {str(e)}")
        return {"valid": False, "error": str(e)}
    return {"valid": False, "error": "No validation data returned."}

def run_query(query: str) -> pd.DataFrame:
    """Executes live SQL query against Snowflake database.
    Uses Snowpark session if available (Workspaces), falls back to connector."""
    session = _get_snowpark_session()
    if session is not None:
        try:
            return session.sql(query).to_pandas()
        except Exception:
            pass
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
# CORTEX AGENT API (calls agents via SQL DATA_AGENT_RUN)
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

def _extract_text_from_content(content_val) -> list:
    """Safely extract text from a content field that may be a str, list of str, or list of dicts."""
    texts = []
    if isinstance(content_val, str):
        texts.append(content_val)
    elif isinstance(content_val, list):
        for item in content_val:
            if isinstance(item, str):
                texts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text", ""))
                elif item.get("type") == "tool_results":
                    texts.append(str(item.get("content", "")))
    return texts

def _parse_agent_response(content: str) -> str:
    """Parse Cortex Agent response — handles v2 schema JSON and SSE formats."""
    if not content:
        return "No response received from agent."

    # First try: parse as JSON (DATA_AGENT_RUN v2 schema format)
    try:
        parsed = json.loads(content)
        # Handle double-encoded JSON (string within string)
        if isinstance(parsed, str):
            try:
                parsed = json.loads(parsed)
            except (json.JSONDecodeError, TypeError):
                return parsed

        if isinstance(parsed, dict):
            # v2 schema: {"content": [{"text": "...", "type": "text"}], ...}
            if "content" in parsed:
                full_text = _extract_text_from_content(parsed["content"])
                if full_text:
                    return "\n".join(full_text)
            # Alternative: {"message": {"content": [...]}}
            if "message" in parsed:
                msg = parsed["message"]
                if isinstance(msg, str):
                    return msg
                if isinstance(msg, dict) and "content" in msg:
                    full_text = _extract_text_from_content(msg["content"])
                    if full_text:
                        return "\n".join(full_text)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass

    # Second try: SSE (Server-Sent Events) streaming format
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
            if isinstance(delta, dict) and "content" in delta:
                full_text.extend(_extract_text_from_content(delta["content"]))
            for choice in event_data.get("choices", []):
                d = choice.get("delta", {}) if isinstance(choice, dict) else {}
                if "content" in d:
                    full_text.extend(_extract_text_from_content(d["content"]))
        except (json.JSONDecodeError, TypeError, AttributeError):
            continue
    if full_text:
        return "".join(full_text)

    return content

def parse_agent_thinking(content: str) -> str:
    """
    Extract real thinking + tool execution traces from the agent response.
    Returns a formatted string showing which tools were called and their results.
    Used by hackaton.py / app.py for the 'Thinking Process' tab.
    """
    traces = []
    try:
        parsed = json.loads(content) if isinstance(content, str) else content
        if isinstance(parsed, str):
            try:
                parsed = json.loads(parsed)
            except (json.JSONDecodeError, TypeError):
                return ""
        items = parsed.get("content", []) if isinstance(parsed, dict) else []
        if not isinstance(items, list):
            return ""
        for item in items:
            if not isinstance(item, dict):
                continue
            item_type = item.get("type", "")
            if item_type == "thinking":
                thinking_val = item.get("thinking", {})
                text = thinking_val.get("text", "").strip() if isinstance(thinking_val, dict) else str(thinking_val).strip()
                if text:
                    traces.append(f"[THINKING] {text}")
            elif item_type == "tool_use":
                tool = item.get("tool_use", {})
                if isinstance(tool, dict):
                    name = tool.get("name", "unknown")
                    inp = tool.get("input", {})
                    traces.append(f"[TOOL CALL] {name}")
                    if isinstance(inp, dict):
                        for k, v in inp.items():
                            if k != "pruning_question":
                                traces.append(f"  Input: {k} = {v}")
            elif item_type == "tool_result":
                result = item.get("tool_result", {})
                if isinstance(result, dict):
                    name = result.get("name", "unknown")
                    status = result.get("status", "unknown")
                    traces.append(f"[TOOL RESULT] {name} -> {status}")
                    result_content = result.get("content", [])
                    if isinstance(result_content, list):
                        for c in result_content:
                            if isinstance(c, dict) and c.get("type") == "json":
                                j = c.get("json", {})
                                if isinstance(j, dict):
                                    if "sql" in j:
                                        traces.append(f"  SQL: {str(j['sql'])[:200]}...")
                                    if "error" in j:
                                        traces.append(f"  Error: {str(j['error'])[:200]}")
                                    if "result_set" in j:
                                        rs = j["result_set"]
                                        rows = rs.get("data", []) if isinstance(rs, dict) else []
                                        traces.append(f"  Rows returned: {len(rows)}")
        if traces:
            return "\n".join(traces)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass
    return ""

# =============================================================================
# IMAGE UPLOAD / STAGE FUNCTIONS (for image-based claim estimation)
# =============================================================================
def upload_image_to_stage(file_bytes: bytes, filename: str) -> bool:
    """Upload an image to the CLAIM_EVIDENCE stage. Returns True/False."""
    try:
        safe_filename = filename.replace(" ", "_")
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = os.path.join(temp_dir, safe_filename)
            with open(local_path, "wb") as f:
                f.write(file_bytes)
            local_path_normalized = local_path.replace("\\", "/")
            put_sql = f"PUT 'file://{local_path_normalized}' @{CLAIM_EVIDENCE_STAGE} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
            # Try Snowpark session first
            session = _get_snowpark_session()
            if session is not None:
                session.sql(put_sql).collect()
            else:
                conn = get_connection()
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

# =============================================================================
# TAB-SPECIFIC AGENT CALLS
# =============================================================================
def ask_specific_agent(agent_fqn: str, prompt: str) -> str:
    """Calls any Cortex Agent by fully qualified name via DATA_AGENT_RUN."""
    try:
        body = json.dumps({
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        })
        safe_body = body.replace("'", "''")
        query = f"""
            SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                '{agent_fqn}',
                '{safe_body}'
            ) AS RESPONSE
        """
        df = run_query(query)
        if df is not None and not df.empty and "RESPONSE" in df.columns:
            raw_response = str(df["RESPONSE"].iloc[0])
            return _parse_agent_response(raw_response)
        return "No response received from agent."
    except Exception as e:
        return f"Error calling agent: {str(e)}"

def stream_specific_agent(agent_fqn: str, prompt: str):
    """Calls agent via SQL and yields the response in chunks for st.write_stream."""
    import time
    result = ask_specific_agent(agent_fqn, prompt)
    if not result:
        yield "No response received from agent."
        return
    words = result.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.02)

def ask_underwriting_agent(prompt: str) -> str:
    return ask_specific_agent(UNDERWRITING_AGENT, prompt)

def stream_underwriting_agent(prompt: str):
    return stream_specific_agent(UNDERWRITING_AGENT, prompt)

def ask_claims_fraud_agent(prompt: str) -> str:
    return ask_specific_agent(CLAIMS_FRAUD_AGENT, prompt)

def stream_claims_fraud_agent(prompt: str):
    return stream_specific_agent(CLAIMS_FRAUD_AGENT, prompt)

def ask_risk_retention_agent(prompt: str) -> str:
    return ask_specific_agent(RISK_RETENTION_AGENT, prompt)

def stream_risk_retention_agent(prompt: str):
    return stream_specific_agent(RISK_RETENTION_AGENT, prompt)

def ask_intelligence_agent(prompt: str) -> str:
    return ask_specific_agent(INTELLIGENCE_AGENT, prompt)

# =============================================================================
# CORTEX SEARCH (CLAIM NOTES)
# =============================================================================
def search_claims(query: str, limit: int = 10) -> pd.DataFrame:
    """Searches claim notes using Cortex Search service."""
    try:
        safe_query = query.replace("'", "''")
        sql = f"""
            SELECT PARSE_JSON(
                SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    '{CORTEX_SEARCH_SERVICE}',
                    '{{"query": "{safe_query}", "columns": ["CLAIM_ID","FRAUD_TYPE","INVESTIGATION_NOTES","ALERT_STATUS","FRAUD_REASON","CLAIM_TYPE","CLAIM_AMOUNT"], "limit": {limit}}}'
                )
            )['results'] AS RESULTS
        """
        df = run_query(sql)
        if df is not None and not df.empty:
            results_json = df["RESULTS"].iloc[0]
            if isinstance(results_json, str):
                results_list = json.loads(results_json)
            else:
                results_list = results_json
            if results_list:
                return pd.DataFrame(results_list)
    except Exception as e:
        st.warning(f"Cortex Search error: {e}")
    return pd.DataFrame()

# =============================================================================
# CORTEX ANALYST (SEMANTIC VIEW)
# =============================================================================
# =============================================================================
# UNDERWRITING COPILOT -- Profile, Decisioning, PDF Binder
# =============================================================================
def get_underwriting_profile(customer_id: str) -> dict:
    """Fetches full underwriting profile by joining customer, premium calc, risk, and claims data."""
    try:
        df = run_query(f"""
            SELECT
                c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS FULL_NAME,
                c.AGE, c.GENDER, c.STATE, c.CITY, c.OCCUPATION,
                c.ANNUAL_INCOME, c.CREDIT_SCORE, c.SMOKING_STATUS, c.BMI,
                pc.POLICY_TYPE, pc.PLAN_TIER, pc.BASE_PREMIUM,
                pc.AGE_FACTOR, pc.LOCATION_FACTOR, pc.HEALTH_FACTOR,
                pc.LIFESTYLE_FACTOR, pc.CLAIMS_HISTORY_FACTOR,
                pc.FINAL_PREMIUM, pc.DISCOUNT_APPLIED, pc.FACTOR_BREAKDOWN,
                COALESCE(ml.PREDICTED_PREMIUM, pc.FINAL_PREMIUM) AS ML_PREDICTED_PREMIUM,
                COALESCE(ar.LOSS_RATIO, 0) AS LOSS_RATIO,
                COALESCE(ar.RISK_PREDICTION, 0) AS RISK_PREDICTION,
                COALESCE(ch.CHURN_PROBABILITY, 0) AS CHURN_PROBABILITY,
                ch.TOP_RISK_FACTOR,
                (SELECT COUNT(*) FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS cl
                 WHERE cl.CUSTOMER_ID = c.CUSTOMER_ID AND cl.FRAUD_FLAG = TRUE) AS FRAUD_CLAIM_COUNT,
                (SELECT COUNT(*) FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS cl
                 WHERE cl.CUSTOMER_ID = c.CUSTOMER_ID) AS TOTAL_CLAIMS
            FROM INSURANCE_MGMT_SYSTEM.CORE.CUSTOMERS c
            LEFT JOIN INSURANCE_MGMT_SYSTEM.PREMIUM.PREMIUM_CALCULATIONS pc
                ON c.CUSTOMER_ID = pc.CUSTOMER_ID
            LEFT JOIN INSURANCE_MGMT_SYSTEM.PREMIUM.PREMIUM_CALCULATIONS_ML ml
                ON c.CUSTOMER_ID = ml.CUSTOMER_ID AND pc.POLICY_TYPE = ml.POLICY_TYPE
            LEFT JOIN INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES_ML ar
                ON c.CUSTOMER_ID = ar.CUSTOMER_ID
            LEFT JOIN INSURANCE_MGMT_SYSTEM.RISK.CHURN_PREDICTIONS ch
                ON c.CUSTOMER_ID = ch.CUSTOMER_ID
            WHERE c.CUSTOMER_ID = '{customer_id}'
            ORDER BY pc.CALC_DATE DESC NULLS LAST
            LIMIT 1
        """)
        if df is not None and not df.empty:
            return df.iloc[0].to_dict()
    except Exception:
        pass
    return {}


def compute_underwriting_decision(profile: dict) -> dict:
    """Computes auto-decisioning: score + bucket + reasons from profile data."""
    score = 0.0
    reasons = []

    credit = float(profile.get("CREDIT_SCORE", 650) or 650)
    age = float(profile.get("AGE", 35) or 35)
    bmi = float(profile.get("BMI", 25) or 25)
    smoking = str(profile.get("SMOKING_STATUS", "No")).lower()
    income = float(profile.get("ANNUAL_INCOME", 50000) or 50000)
    loss_ratio = float(profile.get("LOSS_RATIO", 0) or 0)
    risk_pred = int(profile.get("RISK_PREDICTION", 0) or 0)
    churn_prob = float(profile.get("CHURN_PROBABILITY", 0) or 0)
    fraud_count = int(profile.get("FRAUD_CLAIM_COUNT", 0) or 0)
    total_claims = int(profile.get("TOTAL_CLAIMS", 0) or 0)

    age_factor = float(profile.get("AGE_FACTOR", 1.0) or 1.0)
    health_factor = float(profile.get("HEALTH_FACTOR", 1.0) or 1.0)
    lifestyle_factor = float(profile.get("LIFESTYLE_FACTOR", 1.0) or 1.0)
    claims_factor = float(profile.get("CLAIMS_HISTORY_FACTOR", 1.0) or 1.0)

    # Credit score (0-0.25)
    if credit >= 750:
        score += 0.0
        reasons.append(("Credit Score", credit, -0.05, "Excellent credit reduces risk"))
    elif credit >= 680:
        score += 0.08
        reasons.append(("Credit Score", credit, 0.08, "Good credit, minor uplift"))
    elif credit >= 620:
        score += 0.15
        reasons.append(("Credit Score", credit, 0.15, "Fair credit, moderate risk"))
    else:
        score += 0.25
        reasons.append(("Credit Score", credit, 0.25, "Poor credit, significant risk"))

    # Age risk (0-0.15)
    if age > 65:
        score += 0.15
        reasons.append(("Age Bracket", f"{age} yrs", 0.15, "Senior bracket, higher claim frequency"))
    elif age > 55:
        score += 0.10
        reasons.append(("Age Bracket", f"{age} yrs", 0.10, "Pre-senior, moderate risk uplift"))
    elif age < 25:
        score += 0.12
        reasons.append(("Age Bracket", f"{age} yrs", 0.12, "Young driver/policyholder risk"))
    else:
        score += 0.02
        reasons.append(("Age Bracket", f"{age} yrs", 0.02, "Prime age bracket"))

    # Health factors (0-0.20)
    health_score = 0.0
    if smoking == "yes":
        health_score += 0.10
        reasons.append(("Smoking Status", "Smoker", 0.10, "Tobacco use increases health/life risk"))
    if bmi > 35:
        health_score += 0.08
        reasons.append(("BMI", f"{bmi:.1f}", 0.08, "Obesity class II+ flagged"))
    elif bmi > 30:
        health_score += 0.04
        reasons.append(("BMI", f"{bmi:.1f}", 0.04, "Overweight, mild uplift"))
    else:
        reasons.append(("BMI", f"{bmi:.1f}", -0.02, "Healthy BMI range"))
    score += health_score

    # Loss ratio (0-0.15)
    if loss_ratio > 0.8:
        score += 0.15
        reasons.append(("Loss Ratio", f"{loss_ratio:.2f}", 0.15, "High loss ratio, unprofitable"))
    elif loss_ratio > 0.5:
        score += 0.08
        reasons.append(("Loss Ratio", f"{loss_ratio:.2f}", 0.08, "Elevated loss ratio"))
    elif loss_ratio > 0:
        score += 0.02
        reasons.append(("Loss Ratio", f"{loss_ratio:.2f}", 0.02, "Acceptable loss ratio"))

    # Fraud history (0-0.20)
    if fraud_count > 0:
        f_score = min(0.20, fraud_count * 0.10)
        score += f_score
        reasons.append(("Fraud History", f"{fraud_count} flagged", f_score, "Prior fraud flags detected"))

    # ML risk prediction
    if risk_pred == 1:
        score += 0.10
        reasons.append(("ML Risk Prediction", "HIGH", 0.10, "ML model predicts elevated risk"))

    # Factor multiplier penalties
    if claims_factor > 1.3:
        score += 0.08
        reasons.append(("Claims History Factor", f"{claims_factor:.2f}x", 0.08, "High claims history multiplier"))

    score = min(1.0, max(0.0, score))

    if score < 0.30:
        bucket = "AUTO_APPROVE"
        label = "Auto-Approve"
        color = "#10B981"
        icon = "🟢"
        action = "Low risk profile. Eligible for instant policy issuance."
    elif score < 0.60:
        bucket = "HUMAN_REVIEW"
        label = "Human Underwriter Review"
        color = "#F59E0B"
        icon = "🟡"
        action = "Borderline metrics detected. Route to senior underwriter for manual review."
    else:
        bucket = "DECLINE_ESCALATE"
        label = "Decline / Escalate to Fraud Unit"
        color = "#EF4444"
        icon = "🔴"
        action = "High risk signals. Recommend decline or SIU escalation."

    return {
        "score": score,
        "bucket": bucket,
        "label": label,
        "color": color,
        "icon": icon,
        "action": action,
        "reasons": reasons
    }


def _strip_emoji(text: str) -> str:
    """Remove emoji and other non-latin1 characters for PDF rendering."""
    import re
    emoji_pattern = re.compile(
        "[\U0001F000-\U0001FFFF"
        "\U00002700-\U000027BF"
        "\U0000FE00-\U0000FE0F"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "\U0000200D"
        "\U00002B50\U00002B55"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub("", text).strip()


def generate_binder_pdf(profile: dict, decision: dict, premium: float) -> bytes:
    """Generates a Policy Quote/Binder PDF and returns bytes."""
    from fpdf import FPDF
    from datetime import datetime

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 12, "INSURANCE INTELLIGENCE PLATFORM", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, "Policy Quote & Binder Document", ln=True, align="C")
    pdf.ln(4)

    # Reference line
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    ref_no = f"UW-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, f"Reference: {ref_no}  |  Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}  |  Status: QUOTE", ln=True)
    pdf.ln(6)

    # Decision Banner
    bucket = decision.get("bucket", "HUMAN_REVIEW")
    if bucket == "AUTO_APPROVE":
        r, g, b = 16, 185, 129
    elif bucket == "HUMAN_REVIEW":
        r, g, b = 245, 158, 11
    else:
        r, g, b = 239, 68, 68
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    bucket_label = _strip_emoji(decision.get('label', 'Review')).upper()
    pdf.cell(0, 12, f"  DECISION: {bucket_label}  (Score: {decision['score']:.2f})", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_text_color(15, 23, 42)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, decision.get("action", ""), ln=True)
    pdf.ln(6)

    # Section helper
    def section_header(title):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    def detail_row(label, value):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(70, 6, label)
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, str(value), ln=True)

    # Applicant Details
    section_header("1. APPLICANT DETAILS")
    detail_row("Full Name:", profile.get("FULL_NAME", "N/A"))
    detail_row("Age / Gender:", f"{profile.get('AGE', 'N/A')} / {profile.get('GENDER', 'N/A')}")
    detail_row("Location:", f"{profile.get('CITY', '')}, {profile.get('STATE', '')}")
    detail_row("Occupation:", profile.get("OCCUPATION", "N/A"))
    detail_row("Annual Income:", f"${float(profile.get('ANNUAL_INCOME', 0) or 0):,.0f}")
    detail_row("Credit Score:", str(profile.get("CREDIT_SCORE", "N/A")))
    detail_row("Smoking Status:", profile.get("SMOKING_STATUS", "N/A"))
    detail_row("BMI:", f"{float(profile.get('BMI', 0) or 0):.1f}")
    pdf.ln(4)

    # Coverage Details
    section_header("2. COVERAGE DETAILS")
    detail_row("Policy Type:", profile.get("POLICY_TYPE", "N/A"))
    detail_row("Plan Tier:", profile.get("PLAN_TIER", "N/A"))
    detail_row("Base Premium:", f"${float(profile.get('BASE_PREMIUM', 0) or 0):,.2f}")
    detail_row("Final Quoted Premium:", f"${premium:,.2f}")
    detail_row("ML Predicted Premium:", f"${float(profile.get('ML_PREDICTED_PREMIUM', 0) or 0):,.2f}")
    detail_row("Discount Applied:", f"${float(profile.get('DISCOUNT_APPLIED', 0) or 0):,.2f}")
    pdf.ln(4)

    # XAI Breakdown
    section_header("3. EXPLAINABLE AI (XAI) RISK FACTOR BREAKDOWN")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(55, 7, "RISK FACTOR", border=1, fill=True)
    pdf.cell(30, 7, "VALUE", border=1, fill=True, align="C")
    pdf.cell(30, 7, "IMPACT", border=1, fill=True, align="C")
    pdf.cell(75, 7, "EXPLANATION", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(15, 23, 42)
    for factor, value, impact, explanation in decision.get("reasons", []):
        if impact > 0.05:
            pdf.set_text_color(220, 38, 38)
            impact_str = f"+{impact:.0%}"
        elif impact < -0.01:
            pdf.set_text_color(16, 185, 129)
            impact_str = f"{impact:.0%}"
        else:
            pdf.set_text_color(100, 116, 139)
            impact_str = f"{impact:.0%}"
        pdf.cell(55, 6, str(factor), border=1)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(30, 6, str(value), border=1, align="C")
        pdf.cell(30, 6, impact_str, border=1, align="C")
        pdf.cell(75, 6, explanation[:40], border=1, ln=True)
    pdf.ln(2)

    factor_text = profile.get("FACTOR_BREAKDOWN", "")
    if factor_text:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, f"DB Factor Breakdown: {factor_text}", ln=True)
    pdf.ln(4)

    # Actuarial Multipliers
    section_header("4. ACTUARIAL PREMIUM MULTIPLIERS")
    for fname, fval in [
        ("Age Factor", profile.get("AGE_FACTOR", 1.0)),
        ("Location Factor", profile.get("LOCATION_FACTOR", 1.0)),
        ("Health Factor", profile.get("HEALTH_FACTOR", 1.0)),
        ("Lifestyle Factor", profile.get("LIFESTYLE_FACTOR", 1.0)),
        ("Claims History Factor", profile.get("CLAIMS_HISTORY_FACTOR", 1.0)),
    ]:
        v = float(fval or 1.0)
        detail_row(f"{fname}:", f"{v:.2f}x")
    pdf.ln(4)

    # Terms
    section_header("5. TERMS & CONDITIONS")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 4,
        "This document constitutes a preliminary policy quote generated by the Insurance Intelligence Platform. "
        "Final binding is subject to underwriter approval, verification of applicant information, and completion "
        "of all required documentation. Quote is valid for 30 days from generation date. Premium amounts are "
        "subject to adjustment based on final underwriting review. This quote does not constitute a contract of insurance."
    )
    pdf.ln(8)

    # Signature
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(90, 6, "________________________________")
    pdf.cell(90, 6, "________________________________", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(90, 5, "Underwriter Signature / Date")
    pdf.cell(90, 5, "Applicant Signature / Date", ln=True)

    return bytes(pdf.output())


def call_cortex_agent(agent_fqn: str, prompt: str) -> str:
    """Generic caller for any Cortex Agent via SQL DATA_AGENT_RUN."""
    try:
        body = json.dumps({
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        })
        safe_body = body.replace("'", "''")
        query = f"""
            SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                '{agent_fqn}',
                '{safe_body}',
                TRUE
            ) AS RESPONSE
        """
        df = run_query(query)
        if df is not None and not df.empty and "RESPONSE" in df.columns:
            raw_response = str(df["RESPONSE"].iloc[0])
            return _parse_agent_response(raw_response)
        return "No response received from agent."
    except Exception as e:
        return f"Error calling Cortex Agent: {str(e)}"


def ask_product_matching_agent(prompt: str) -> str:
    """Calls the Product Matching Agent for multi-strategy product recommendations."""
    return call_cortex_agent(PRODUCT_MATCHING_AGENT, prompt)


def ask_intelligence_agent(prompt: str) -> str:
    """Calls the unified Insurance Intelligence Hub (market trends, pricing, matching accuracy)."""
    return call_cortex_agent(INSURANCE_INTELLIGENCE_AGENT, prompt)


# Aliases — route market intelligence & pricing to the unified Intelligence Hub
ask_market_intelligence_agent = ask_intelligence_agent
ask_price_optimization_agent = ask_intelligence_agent


def ask_cortex_analyst(question: str) -> str:
    """Queries the Insurance Intelligence Model via Cortex Analyst semantic view."""
    return call_cortex_agent(INSURANCE_INTELLIGENCE_AGENT, question)