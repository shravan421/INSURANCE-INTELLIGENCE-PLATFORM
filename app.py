import streamlit as st
from dotenv import load_dotenv

import snowflake_utils as sf
from styles.global_css import inject_global_css
from components.header import render_header
from components.sidebar import render_sidebar
from tabs import underwriting, claims_fraud, risk_pricing, customer_360, intelligence_hub, chat_assistant

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Insurance Intelligence Platform | Capgemini & Snowflake",
    page_icon="\U0001f6e1\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject global CSS
inject_global_css()

# Render header and sidebar
render_header()
if "sf_connected" not in st.session_state:
    val_init = sf.validate_connection()
    st.session_state["sf_connected"] = val_init.get("valid", False)
selected_tab = render_sidebar()

# Route to the selected tab
if "Underwriting Workbench" in selected_tab:
    underwriting.render()
elif "Claims & Fraud Console" in selected_tab:
    claims_fraud.render()
elif "Risk & Pricing Dashboard" in selected_tab:
    risk_pricing.render()
elif "Customer 360" in selected_tab:
    customer_360.render()
elif "Intelligence Hub" in selected_tab:
    intelligence_hub.render()
elif "Chat Assistant" in selected_tab:
    chat_assistant.render()
