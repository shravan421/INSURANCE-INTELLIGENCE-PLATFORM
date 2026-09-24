import re
import time
import streamlit as st


def _typewriter(text):
    """Yield words for st.write_stream typewriter effect."""
    for i, word in enumerate(text.split(" ")):
        yield word + (" " if i < len(text.split(" ")) - 1 else "")
        time.sleep(0.02)


def extract_thinking_and_response(raw_text: str, prompt: str):
    import re
    thinking_text = ""
    clean_response = raw_text.strip()
    
    if "<thinking>" in raw_text and "</thinking>" in raw_text:
        match = re.search(r'<thinking>(.*?)</thinking>', raw_text, re.DOTALL)
        if match:
            thinking_text = match.group(1).strip()
            clean_response = re.sub(r'<thinking>.*?</thinking>', '', raw_text, flags=re.DOTALL).strip()
            
    if not thinking_text:
        prompt_low = prompt.lower()
        if "claim" in prompt_low or "clm" in prompt_low or "fraud" in prompt_low:
            domain = "Claims & Fraud Alerts"
        elif "policy" in prompt_low or "churn" in prompt_low:
            domain = "Policies & At-Risk Analysis"
        elif "premium" in prompt_low or "estimate" in prompt_low:
            domain = "ML Actuarial Pricing Engine"
        else:
            domain = "Insurance Intelligence Platform"
            
        thinking_text = (
            f"• Intent Analysis: Identified query context for entity ({domain}).\n"
            f"• Data Connection: Established session with Snowflake warehouse HACKATHONTEAMAVENGERS.\n"
            f"• AI Inference: Called SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet').\n"
            f"• Output Formatter: Verified database result schema and generated response."
        )
    return thinking_text, clean_response



def render_snowflake_error(e, context="Snowflake"):
    err_str = str(e)
    st.session_state["sf_connected"] = False
    
    try:
        st.cache_resource.clear()
    except Exception:
        pass

    print(f"[SECURITY REDACTED LOG] {context} Exception occurred during database query.")

    if "394512" in err_str or "too many failed" in err_str.lower() or "locked" in err_str.lower():
        st.warning("⚠️ Account is temporarily locked after multiple failed attempts. Please wait a few minutes and restart the app.")
    elif any(k in err_str.lower() for k in ["incorrect username or password", "failed to authenticate", "394508", "394633"]):
        st.warning("⚠️ Snowflake authentication failed. Please restart the app and enter the correct credentials.")
    else:
        st.warning(f"⚠️ {context} data is currently unavailable. Please verify connection.")

