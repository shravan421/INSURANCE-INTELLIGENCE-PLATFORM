import streamlit as st
import pandas as pd
import snowflake_utils as sf
from components.helpers import render_snowflake_error

def render():
    st.markdown("### 🔍 Claims & Fraud Console")
    st.caption("AI-powered claims triage, fraud risk scoring, and Snowflake Cortex semantic investigation analysis.")

    # Live Data Fetch
    claims_df = pd.DataFrame()
    try:
        claims_df = sf.get_claims_data()
    except Exception as e:
        render_snowflake_error(e, "Snowflake Claims Query")

    def is_siu_required(row) -> bool:
        """Centralized single source of truth for SIU Escalation decision."""
        try:
            score = float(row.get("FRAUD_SCORE", row.get("CONFIDENCE_SCORE", 0.0)) or 0.0)
        except Exception:
            score = 0.0

        try:
            ml_pred = float(row.get("ML_PREDICTION", row.get("ML_FRAUD_PREDICTION", 0.0)) or 0.0)
        except Exception:
            ml_pred = 0.0

        notes = str(row.get("INVESTIGATION_NOTES", row.get("FRAUD_REASON", ""))).lower()
        status = str(row.get("ALERT_WORKFLOW_STATUS", row.get("ALERT_STATUS", row.get("STATUS", row.get("CLAIM_STATUS", ""))))).lower()
        
        if score >= 0.70 or ml_pred >= 0.70:
            return True
        if any(k in notes for k in ["duplicate", "escalate", "arson", "staged", "phantom", "inconsistent", "flagged"]):
            return True
        if "escalat" in status or "investigat" in status:
            return True
        return False

    # Top KPI Metrics Row
    if not claims_df.empty:
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        total_claims = len(claims_df)
        
        # Calculate High Risk Count from live data
        high_risk_count = 0
        if "FRAUD_SCORE" in claims_df.columns:
            high_risk_count = len(claims_df[claims_df.apply(is_siu_required, axis=1)])
            avg_fraud_score = pd.to_numeric(claims_df["FRAUD_SCORE"], errors="coerce").mean()
        else:
            avg_fraud_score = 0.0

        # Calculate Total Claim Amount
        if "AMOUNT" in claims_df.columns:
            total_claim_amt = pd.to_numeric(claims_df["AMOUNT"], errors="coerce").sum()
        else:
            total_claim_amt = 0.0

        with c_kpi1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Claims Analyzed</div>
                <div class="kpi-value">{total_claims:,}</div>
                <div class="kpi-subtitle"><span>● 100%</span> live coverage</div>
            </div>
            """, unsafe_allow_html=True)

        with c_kpi2:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #EF4444;">
                <div class="kpi-title">High Fraud Alerts</div>
                <div class="kpi-value" style="color:#DC2626;">{high_risk_count}</div>
                <div class="kpi-subtitle danger"><span>⚠️ Requires</span> SIU Review</div>
            </div>
            """, unsafe_allow_html=True)

        with c_kpi3:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #F59E0B;">
                <div class="kpi-title">Total Claim Exposure</div>
                <div class="kpi-value">${total_claim_amt:,.0f}</div>
                <div class="kpi-subtitle"><span>● Active</span> claimed value</div>
            </div>
            """, unsafe_allow_html=True)

        with c_kpi4:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #8B5CF6;">
                <div class="kpi-title">Avg Fraud Risk Score</div>
                <div class="kpi-value">{avg_fraud_score:.2f}</div>
                <div class="kpi-subtitle"><span>● ML Confidence</span> index</div>
            </div>
            """, unsafe_allow_html=True)

    c_left, c_right = st.columns([1.1, 0.9])

    with c_left:
        st.markdown("""
        <div class="card-panel">
            <div class="panel-header">
                <div class="panel-header-title">
                    <span>📑 Claims Ranked by Fraud Score</span>
                </div>
                <div class="panel-header-badge">Fraud Predictions</div>
            </div>
        """, unsafe_allow_html=True)

        selected_claim_id = None
        if not claims_df.empty and "CLAIM_ID" in claims_df.columns:
            claim_ids = claims_df["CLAIM_ID"].astype(str).tolist()
            
            if "selected_claim_id" not in st.session_state or st.session_state["selected_claim_id"] not in claim_ids:
                st.session_state["selected_claim_id"] = claim_ids[0]

            if "claim_dropdown_select" not in st.session_state or st.session_state["claim_dropdown_select"] not in claim_ids:
                st.session_state["claim_dropdown_select"] = st.session_state["selected_claim_id"]

            search_not_found = None

            def on_search_submit():
                q = st.session_state.get("claim_search_input", "").strip()
                if q:
                    # 1. Exact match
                    exact = [cid for cid in claim_ids if cid.upper() == q.upper()]
                    if exact:
                        target = exact[0]
                    else:
                        # 2. Partial match
                        partial = [cid for cid in claim_ids if q.upper() in cid.upper()]
                        target = partial[0] if partial else None

                    if target:
                        st.session_state["selected_claim_id"] = target
                        st.session_state["claim_dropdown_select"] = target
                    else:
                        st.session_state["search_error_notice"] = f"No claim found for: '{q}'"

            def on_dropdown_change():
                st.session_state["selected_claim_id"] = st.session_state["claim_dropdown_select"]

            # Keep dropdown widget state synchronized
            if st.session_state["claim_dropdown_select"] != st.session_state["selected_claim_id"]:
                st.session_state["claim_dropdown_select"] = st.session_state["selected_claim_id"]

            f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
            with f_col1:
                st.text_input("🔎 Search Claim ID:", value="", placeholder="e.g. CLM-00044", key="claim_search_input", on_change=on_search_submit)

            with f_col2:
                st.selectbox("📋 Select Claim:", claim_ids, key="claim_dropdown_select", on_change=on_dropdown_change)

            with f_col3:
                status_list = ["All Statuses"] + list(claims_df["STATUS"].dropna().unique()) if "STATUS" in claims_df.columns else ["All Statuses"]
                selected_status = st.selectbox("Filter Status", status_list)

            if "search_error_notice" in st.session_state and st.session_state["search_error_notice"]:
                st.warning(st.session_state.pop("search_error_notice"))

            selected_claim_id = st.session_state["selected_claim_id"]

            display_claims = claims_df.copy()
            display_claims["SIU"] = display_claims.apply(lambda r: "🔴 SIU" if is_siu_required(r) else "—", axis=1)

            if selected_status != "All Statuses" and "STATUS" in display_claims.columns:
                display_claims = display_claims[display_claims["STATUS"] == selected_status]

            cols_order = [c for c in ["CLAIM_ID", "TYPE", "AMOUNT", "FRAUD_SCORE", "STATUS", "SIU"] if c in display_claims.columns]

            st.dataframe(
                display_claims[cols_order],
                use_container_width=True,
                height=340,
                hide_index=True
            )

            if selected_claim_id:
                st.markdown(f"**Inspecting Claim Record:** `{selected_claim_id}` | *Displaying all {len(display_claims)} live claims from Snowflake*")
        else:
            st.warning("No live claims data retrieved from Snowflake.")

        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("""
        <div class="card-panel">
            <div class="panel-header">
                <div class="panel-header-title">
                    <span>🔬 Cortex Semantic Investigation</span>
                </div>
                <div class="panel-header-badge">Cortex Search</div>
            </div>
        """, unsafe_allow_html=True)

        if selected_claim_id:
            try:
                detail_df = sf.get_claim_detail(selected_claim_id)
                if detail_df is not None and not detail_df.empty:
                    row = detail_df.iloc[0]
                    notes = row.get("INVESTIGATION_NOTES", "No notes recorded.")
                    f_type = row.get("FRAUD_TYPE", "Standard Risk")
                    
                    try:
                        conf = float(row.get("FRAUD_SCORE", 0.0))
                    except Exception:
                        conf = 0.0
                        
                    status = row.get("ALERT_STATUS", row.get("CLAIM_STATUS", "Open"))

                    st.markdown("**📝 Adjuster & Semantic Search Notes:**")
                    st.info(f'"{notes}"')

                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:6px; margin-top:10px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13px;">
                            <span style="color:#64748B;">Fraud Category:</span>
                            <span style="font-weight:600; color:#0F172A;">{f_type}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13px;">
                            <span style="color:#64748B;">Confidence Score:</span>
                            <span style="font-weight:700; color:#0284C7; font-family:'JetBrains Mono';">{conf:.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:13px;">
                            <span style="color:#64748B;">Alert Workflow Status:</span>
                            <span style="font-weight:600; color:#475569;">{status}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if is_siu_required(row):
                        st.markdown("""
                        <div class="recommendation-danger">
                            <span style="font-size:20px;">⚠️</span>
                            <div>
                                <div style="font-weight:700;">Action Required: Escalate to Special Investigation Unit (SIU)</div>
                                <div style="font-size:12px; font-weight:400; opacity:0.9;">High risk threshold exceeded or anomaly patterns detected.</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="recommendation-success">
                            <span style="font-size:20px;">✅</span>
                            <div>
                                <div style="font-weight:700;">Standard Procedure: Proceed with Standard Settlement</div>
                                <div style="font-size:12px; font-weight:400; opacity:0.9;">Low anomaly confidence. Routine adjudication recommended.</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No detail record found for `{selected_claim_id}`.")
            except Exception as e:
                render_snowflake_error(e, "Claim Detail Query")
        else:
            st.info("Select a valid claim from the table to inspect details.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Cortex Search & Claims Intelligence ──
    # ── Top Compact Header ──
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:2px;">
            <span style="font-size:24px;">🔎</span>
            <span style="font-size:22px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">Search Claims Intelligence</span>
        </div>
        <div style="font-size:13px; color:#64748B; margin-bottom:12px;">
            Search claims data and use AI-powered fraud intelligence to investigate claims.
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        is_connected = st.session_state.get("sf_connected", True)
        status_label = "Cortex Search Connected" if is_connected else "Offline"
        status_bg = "#F0FDF4" if is_connected else "#FEF2F2"
        status_border = "#BBF7D0" if is_connected else "#FCA5A5"
        status_text = "#15803D" if is_connected else "#991B1B"
        dot_color = "#22C55E" if is_connected else "#EF4444"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:4px;">
            <span style="background:{status_bg}; border:1px solid {status_border}; color:{status_text}; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; display:inline-flex; align-items:center; gap:6px;">
                <span style="width:7px; height:7px; background-color:{dot_color}; border-radius:50%; display:inline-block;"></span> ● {status_label}
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Search Bar Component
    search_col1, search_col2 = st.columns([3.5, 1])
    with search_col1:
        search_query = st.text_input(
            "Search Claim ID, policy number, or claim details...",
            placeholder="e.g. CLM-00177, suspicious auto claims, duplicate billing, staged accident",
            key="claims_search_input",
            label_visibility="collapsed"
        )
    with search_col2:
        search_clicked = st.button("Search ➜", use_container_width=True, key="claims_search_btn")

    # Quick Suggestion Chips for Search
    st.markdown("<div style='font-size:11px; font-weight:600; color:#94A3B8; margin-top:4px; margin-bottom:6px;'>Quick Search Suggestions:</div>", unsafe_allow_html=True)
    sugg_cols = st.columns(4)
    sample_searches = [
        "CLM-00177",
        "Suspicious auto claims",
        "Duplicate billing",
        "Staged accident"
    ]
    for idx, s_term in enumerate(sample_searches):
        with sugg_cols[idx]:
            if st.button(f"🔍 {s_term}", key=f"claim_sugg_{idx}", use_container_width=True):
                st.session_state["claims_pending_search"] = s_term
                st.rerun()

    active_search_query = None
    if search_clicked and search_query:
        active_search_query = search_query
    elif st.session_state.get("claims_pending_search"):
        active_search_query = st.session_state.pop("claims_pending_search")

    if active_search_query:
        with st.spinner("🔎 Searching claim data via Cortex Search..."):
            try:
                search_results = sf.search_claims(active_search_query)
                st.session_state["claims_search_results"] = search_results
                st.session_state["claims_search_query"] = active_search_query
            except Exception as e:
                print(f"[SECURITY REDACTED LOG] Search error: {str(e)}")
                st.warning("⚠️ Unable to retrieve claim information. Please check the claim query and try again.")

    if "claims_search_results" in st.session_state and not st.session_state["claims_search_results"].empty:
        sr = st.session_state["claims_search_results"]
        st.markdown(f"<div style='margin-top:12px; margin-bottom:8px; font-size:13px; font-weight:600; color:#334155;'>Found <span style='color:#2563EB;'>{len(sr)}</span> results for: <i>\"{st.session_state.get('claims_search_query', '')}\"</i></div>", unsafe_allow_html=True)
        display_cols = [c for c in ["CLAIM_ID", "FRAUD_TYPE", "CLAIM_TYPE", "CLAIM_AMOUNT", "ALERT_STATUS", "INVESTIGATION_NOTES"] if c in sr.columns]
        st.dataframe(sr[display_cols] if display_cols else sr, use_container_width=True, height=200, hide_index=True)
    elif active_search_query:
        st.info("No matching claims found.")

    st.markdown("<hr style='margin:24px 0; border:0; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)

    # ── AI FRAUD TRIAGE ASSISTANT (CONVERSATIONAL UX) ──
    f_hdr1, f_hdr2 = st.columns([3, 1])
    with f_hdr1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:2px;">
            <span style="font-size:24px;">🛡️</span>
            <span style="font-size:20px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">AI Fraud Triage Assistant</span>
        </div>
        <div style="font-size:13px; color:#64748B; margin-bottom:12px;">
            Analyze claims for potential fraud indicators and explain risk factors identified in available claim data.
        </div>
        """, unsafe_allow_html=True)
    with f_hdr2:
        if st.session_state.get("fraud_chat_history"):
            if st.button("🔄 Reset Assistant", key="reset_fraud_chat", use_container_width=True):
                st.session_state.pop("fraud_chat_history", None)
                st.session_state.pop("fraud_dialog_claim_id", None)
                st.session_state.pop("fraud_dialog_claim_row", None)
                st.rerun()

    # Determine Active Claim Context
    active_claim_id = selected_claim_id or st.session_state.get("fraud_dialog_claim_id", "")
    active_claim_row = st.session_state.get("fraud_dialog_claim_row", {})
    
    if selected_claim_id and selected_claim_id != st.session_state.get("fraud_dialog_claim_id"):
        try:
            detail_df = sf.get_claim_detail(selected_claim_id)
            if detail_df is not None and not detail_df.empty:
                active_claim_row = detail_df.iloc[0].to_dict()
                st.session_state["fraud_dialog_claim_id"] = selected_claim_id
                st.session_state["fraud_dialog_claim_row"] = active_claim_row
            else:
                st.session_state["fraud_dialog_claim_id"] = selected_claim_id
                st.session_state["fraud_dialog_claim_row"] = {}
        except Exception:
            pass

    # Context Header Badge if a claim is active
    if active_claim_id:
        fraud_score = float(active_claim_row.get("FRAUD_SCORE", active_claim_row.get("CONFIDENCE_SCORE", 0)) or 0)
        risk_label = "High Risk" if fraud_score >= 0.70 else ("Moderate Risk" if fraud_score >= 0.40 else "Low Risk")
        risk_color = "#DC2626" if fraud_score >= 0.70 else ("#D97706" if fraud_score >= 0.40 else "#059669")
        risk_bg = "#FEF2F2" if fraud_score >= 0.70 else ("#FFFBEB" if fraud_score >= 0.40 else "#F0FDF4")
        
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:12px 16px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:13px; font-weight:600; color:#334155;">
                <span style="color:#64748B;">Active Claim Context:</span> <b>{active_claim_id}</b> 
                <span style="color:#94A3B8; margin:0 6px;">|</span> {active_claim_row.get('CLAIM_TYPE','Claim')}
                <span style="color:#94A3B8; margin:0 6px;">|</span> Amount: <b>${float(active_claim_row.get('CLAIM_AMOUNT',0) or 0):,.0f}</b>
            </div>
            <span style="background:{risk_bg}; border:1px solid #E2E8F0; color:{risk_color}; font-size:11px; font-weight:700; padding:4px 10px; border-radius:12px;">
                {risk_label} ({fraud_score:.2f})
            </span>
        </div>
        """, unsafe_allow_html=True)

    if "fraud_chat_history" not in st.session_state:
        st.session_state["fraud_chat_history"] = []

    # ── EMPTY STATE OR CONVERSATION ──
    if not st.session_state["fraud_chat_history"]:
        if not active_claim_id:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:32px 24px; text-align:center; margin:10px 0 24px 0; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-size:42px; margin-bottom:12px;">🛡️</div>
                <div style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:6px;">Claims Intelligence Assistant</div>
                <div style="font-size:14px; font-weight:600; color:#3B82F6; margin-bottom:10px;">Select or search a claim to investigate details & run AI fraud triage.</div>
                <div style="font-size:13px; color:#64748B; max-width:540px; margin:0 auto 24px auto; line-height:1.5;">
                    Select a claim from the table above or use Cortex Search to evaluate risk factors, red flags, and SIU recommendations.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='font-size:12px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;'>Try analyzing a sample claim:</div>", unsafe_allow_html=True)
            chip_cols = st.columns(3)
            sample_claims = ["CLM-00177", "CLM-00044", "CLM-00035"]
            for idx, c_sample in enumerate(sample_claims):
                with chip_cols[idx]:
                    if st.button(f"🔍 Analyze {c_sample}", key=f"sample_claim_btn_{idx}", use_container_width=True):
                        st.session_state["fraud_dialog_claim_id"] = c_sample
                        try:
                            detail_df = sf.get_claim_detail(c_sample)
                            if detail_df is not None and not detail_df.empty:
                                st.session_state["fraud_dialog_claim_row"] = detail_df.iloc[0].to_dict()
                        except Exception:
                            pass
                        st.rerun()
        else:
            # Show triage button instead of auto-running
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:32px 24px; text-align:center; margin:10px 0 24px 0; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-size:42px; margin-bottom:12px;">🛡️</div>
                <div style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:6px;">Ready to Analyze</div>
                <div style="font-size:13px; color:#64748B; max-width:540px; margin:0 auto 16px auto; line-height:1.5;">
                    Click below to run AI fraud triage on the selected claim, or type a custom question.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🛡️ Run Fraud Triage Assessment", key="run_fraud_triage_btn", use_container_width=True, type="primary"):
                claim_context = (
                    f"Claim ID: {active_claim_id}, Type: {active_claim_row.get('CLAIM_TYPE', 'N/A')}, "
                    f"Amount: ${float(active_claim_row.get('CLAIM_AMOUNT', 0) or 0):,.0f}, "
                    f"Status: {active_claim_row.get('CLAIM_STATUS', 'N/A')}, "
                    f"Fraud Type: {active_claim_row.get('FRAUD_TYPE', 'N/A')}, "
                    f"Investigation Notes: {active_claim_row.get('INVESTIGATION_NOTES', 'None')}"
                )
                with st.spinner("🛡️ Analyzing claim for fraud indicators & risk factors..."):
                    try:
                        initial_prompt = (
                            f"Perform a detailed fraud triage assessment for this insurance claim. "
                            f"{claim_context}. "
                            f"Provide: 1) Fraud risk level (High/Medium/Low), "
                            f"2) Red flags identified, "
                            f"3) Recommended next steps for the adjuster, "
                            f"4) Whether SIU escalation is warranted and why. Keep it concise."
                        )
                        initial_response = sf.ask_claims_fraud_agent(initial_prompt)
                    except Exception as e:
                        print(f"[SECURITY REDACTED LOG] Fraud agent error: {str(e)}")
                        initial_response = "⚠️ Unable to complete the fraud assessment. Please try again."
                st.session_state["fraud_chat_history"].append({"role": "assistant", "content": initial_response})
                st.rerun()
    else:
        # Render Chat History
        for msg in st.session_state["fraud_chat_history"]:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🛡️"):
                    st.markdown(msg["content"])

    # Suggested Question Chips during active conversation
    if st.session_state["fraud_chat_history"] and active_claim_id:
        st.markdown("<div style='font-size:11px; font-weight:600; color:#94A3B8; margin-top:16px; margin-bottom:4px;'>Suggested investigation questions:</div>", unsafe_allow_html=True)
        fc_cols = st.columns(3)
        fraud_suggs = ["What are the red flags?", "Should this go to SIU?", "What evidence is needed?"]
        for idx, f_sug in enumerate(fraud_suggs):
            with fc_cols[idx]:
                if st.button(f_sug, key=f"fraud_conv_chip_{idx}", use_container_width=True):
                    st.session_state["fraud_pending_question"] = f_sug
                    st.rerun()

    # Chat Input for Follow-up Questions
    prompt_to_run = None
    chat_input_val = st.chat_input("Ask about this claim or fraud assessment...", key="claims_fraud_chat_input_box")
    
    if chat_input_val:
        prompt_to_run = chat_input_val
    elif st.session_state.get("fraud_pending_question"):
        prompt_to_run = st.session_state.pop("fraud_pending_question")

    if prompt_to_run and active_claim_id:
        st.session_state["fraud_chat_history"].append({"role": "user", "content": prompt_to_run})
        
        with st.chat_message("user"):
            st.markdown(prompt_to_run)
            
        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner("🛡️ Evaluating claim details & generating insights..."):
                try:
                    claim_context = (
                        f"Claim ID: {active_claim_id}, Type: {active_claim_row.get('CLAIM_TYPE', 'N/A')}, "
                        f"Amount: ${float(active_claim_row.get('CLAIM_AMOUNT', 0) or 0):,.0f}, "
                        f"Status: {active_claim_row.get('CLAIM_STATUS', 'N/A')}, "
                        f"Fraud Type: {active_claim_row.get('FRAUD_TYPE', 'N/A')}, "
                        f"Investigation Notes: {active_claim_row.get('INVESTIGATION_NOTES', 'None')}"
                    )
                    recent_context = ""
                    for m in st.session_state["fraud_chat_history"][-4:]:
                        role_label = "Assistant" if m["role"] == "assistant" else "User"
                        recent_context += f"{role_label}: {m['content'][:300]}\n"
                        
                    follow_up_prompt = (
                        f"You are an AI fraud investigation expert. Claim context: {claim_context}. "
                        f"Recent conversation:\n{recent_context}\n"
                        f"User asks: {prompt_to_run}\n"
                        f"Provide a concise, professional answer focused on this claim."
                    )
                    follow_response = sf.ask_claims_fraud_agent(follow_up_prompt)
                except Exception as e:
                    print(f"[SECURITY REDACTED LOG] Fraud follow-up error: {str(e)}")
                    follow_response = "⚠️ Unable to complete the fraud assessment. Please try again."
            st.markdown(follow_response)
            st.session_state["fraud_chat_history"].append({"role": "assistant", "content": follow_response})
        st.rerun()

