import streamlit as st
import snowflake_utils as sf


# =========================================================================
# SIDEBAR NAVIGATION COMPONENT
# =========================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-icon">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
            </div>
            <div class="sidebar-brand-text">
                Insurance Intelligence<br>Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected_page = st.radio(
            "Navigation",
            options=[
                "📑 Underwriting Workbench",
                "🛡️ Claims & Fraud Console",
                "📈 Risk & Pricing Dashboard",
                "📊 Customer 360",
                "🧠 Intelligence Hub",
                "💬 Chat Assistant"
            ],
            index=0,
            label_visibility="collapsed"
        )

        # Check direct connection status
        is_connected = st.session_state.get("sf_connected", False)
        if not is_connected:
            try:
                val_res = sf.validate_connection()
                if val_res.get("valid"):
                    is_connected = True
                    st.session_state["sf_connected"] = True
            except Exception:
                pass

        sf_status_label = "● Snowflake Connected" if is_connected else "⚙️ Snowflake Offline"
        sf_status_color = "#10B981" if is_connected else "#F59E0B"

        st.markdown(f"""
        <div class="sidebar-wave-container">
            <svg width="100%" height="90" viewBox="0 0 240 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M-10 50 C 40 15, 95 85, 155 35 C 190 10, 215 40, 250 25" stroke="#1D4ED8" stroke-width="1.8" stroke-opacity="0.45"/>
                <path d="M-10 65 C 50 25, 105 95, 165 45 C 200 20, 225 50, 250 35" stroke="#0284C7" stroke-width="1.4" stroke-opacity="0.4"/>
                <path d="M-10 35 C 30 5, 85 70, 145 20 C 185 5, 210 30, 250 15" stroke="#38BDF8" stroke-width="1" stroke-opacity="0.3"/>
            </svg>
        </div>
        
        <div class="sidebar-status-box">
            <div class="sidebar-status-header">Platform Status</div>
            <div class="sidebar-status-item" style="margin-bottom: 12px;">
                <span style="color:#FFFFFF; font-weight:600; font-size:13px; display:flex; align-items:center; gap:6px;">
                    <span style="color:#10B981;">🟢</span> All Systems Operational
                </span>
            </div>
            <div class="sidebar-status-item">
                <span>Data Source</span>
                <span class="sidebar-status-val">
                    <span style="color:{sf_status_color};">{sf_status_label}</span>
                </span>
            </div>
            <div class="sidebar-status-item">
                <span>Last Updated</span>
                <span class="sidebar-status-val">
                    <span style="color:#94A3B8;">🕒</span> Just now
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        return selected_page


# Helper to render clean authentication error prompt (redacts raw Snowflake errors)
