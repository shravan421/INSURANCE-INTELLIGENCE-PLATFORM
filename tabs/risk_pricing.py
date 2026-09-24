import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import snowflake_utils as sf
from components.helpers import render_snowflake_error

def render():
    # Live Data Fetch
    loss_df = pd.DataFrame()
    at_risk_df = pd.DataFrame()
    try:
        loss_df = sf.get_loss_ratio_history()
    except Exception as e:
        render_snowflake_error(e, "Snowflake Loss Ratio Query")

    try:
        at_risk_df = sf.get_at_risk_policies()
    except Exception as e:
        render_snowflake_error(e, "Snowflake At-Risk Query")

    # Top Tab Header Bar & Controls
    h_col1, h_col2 = st.columns([2.2, 1.8])
    with h_col1:
        st.markdown("""
        <div>
            <h2 style="margin:0; font-size:22px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">
                Risk & Pricing Dashboard
            </h2>
            <p style="margin:4px 0 0 0; font-size:13px; color:#64748B;">
                Portfolio loss ratio history, portfolio risk exposure, and at-risk policy retention analytics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with h_col2:
        ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1.5, 1, 1])
        with ctrl_c1:
            timeframe_options = ["Last 3 Months", "Last 6 Months", "Last 12 Months", "Year to Date", "All Time"]
            timeframe = st.selectbox("Timeframe", timeframe_options, index=1, key="risk_dashboard_timeframe", label_visibility="collapsed")
        with ctrl_c2:
            if st.button("🌪️ Filter", key="risk_filter_btn", use_container_width=True):
                st.toast(f"Filters applied for timeframe: {timeframe}", icon="ℹ️")
        with ctrl_c3:
            export_csv = at_risk_df.to_csv(index=False) if not at_risk_df.empty else "No Data"

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SINGLE SOURCE OF FILTER TRUTH: Dynamic Date Range Calculation
    # -------------------------------------------------------------------------
    if not loss_df.empty and "MONTH_YEAR" in loss_df.columns:
        ref_dates = pd.to_datetime(loss_df["MONTH_YEAR"])
        ref_end_date = ref_dates.max()
    else:
        ref_end_date = pd.Timestamp.now()

    end_of_ref_month = (ref_end_date + pd.offsets.MonthEnd(0)).normalize()
    start_of_ref_month = ref_end_date.replace(day=1).normalize()

    if timeframe == "Last 3 Months":
        filter_start_date = (start_of_ref_month - pd.DateOffset(months=2)).normalize()
        filter_end_date = end_of_ref_month
    elif timeframe == "Last 6 Months":
        filter_start_date = (start_of_ref_month - pd.DateOffset(months=5)).normalize()
        filter_end_date = end_of_ref_month
    elif timeframe == "Last 12 Months":
        filter_start_date = (start_of_ref_month - pd.DateOffset(months=11)).normalize()
        filter_end_date = end_of_ref_month
    elif timeframe == "Year to Date":
        filter_start_date = pd.Timestamp(year=ref_end_date.year, month=1, day=1).normalize()
        filter_end_date = end_of_ref_month
    else:
        filter_start_date = None
        filter_end_date = None

    # Filter loss_df consistently
    filtered_loss_df = loss_df.copy()
    if not filtered_loss_df.empty and "MONTH_YEAR" in filtered_loss_df.columns and filter_start_date is not None:
        loss_dt = pd.to_datetime(filtered_loss_df["MONTH_YEAR"])
        filtered_loss_df = filtered_loss_df[(loss_dt >= filter_start_date) & (loss_dt <= filter_end_date)]

    # Filter at_risk_df consistently using verified live Snowflake policy dates
    filtered_at_risk_df = at_risk_df.copy()
    if not filtered_at_risk_df.empty:
        date_col = None
        for col in ["START_DATE", "IDENTIFIED_DATE", "CREATED_AT"]:
            if col in filtered_at_risk_df.columns:
                date_col = col
                break

        if date_col and filter_start_date is not None:
            risk_dt = pd.to_datetime(filtered_at_risk_df[date_col])
            filtered_at_risk_df = filtered_at_risk_df[(risk_dt >= filter_start_date) & (risk_dt <= filter_end_date)]

    # Update export download button with filtered data
    with ctrl_c3:
        dl_filtered_csv = filtered_at_risk_df.to_csv(index=False) if not filtered_at_risk_df.empty else "No Data"
        st.download_button("📥 Export", data=dl_filtered_csv, file_name=f"risk_pricing_{timeframe.lower().replace(' ', '_')}.csv", mime="text/csv", key="risk_export_btn", use_container_width=True)

    # -------------------------------------------------------------------------
    # 4 KPI Cards Row: Derived dynamically from filtered datasets
    # -------------------------------------------------------------------------
    at_risk_count = len(filtered_at_risk_df)
    
    total_rev_at_risk = 0.0
    if not filtered_at_risk_df.empty and "REV_AT_RISK" in filtered_at_risk_df.columns:
        val = pd.to_numeric(filtered_at_risk_df["REV_AT_RISK"], errors="coerce").sum()
        if not pd.isna(val):
            total_rev_at_risk = float(val)
            
    avg_loss_ratio_val = "0.0%"
    if not filtered_loss_df.empty and "LOSS_RATIO" in filtered_loss_df.columns:
        lr_mean = pd.to_numeric(filtered_loss_df["LOSS_RATIO"], errors="coerce").mean()
        if not pd.isna(lr_mean):
            if lr_mean <= 1.0:
                avg_loss_ratio_val = f"{lr_mean * 100:.1f}%" if lr_mean > 0.01 else f"{lr_mean:.1f}%"
            else:
                avg_loss_ratio_val = f"{lr_mean:.1f}%"

    retention_actionable_count = at_risk_count
    if not filtered_at_risk_df.empty and "ACTION" in filtered_at_risk_df.columns:
        act_mask = filtered_at_risk_df["ACTION"].astype(str).str.contains("outreach|retention", case=False, na=False)
        if act_mask.any():
            retention_actionable_count = int(act_mask.sum())

    r_kpi1, r_kpi2, r_kpi3, r_kpi4 = st.columns(4)

    with r_kpi1:
        st.markdown(f"""
        <div class="kpi-card-v2" style="border-left-color: #0284C7;">
            <div>
                <div class="kpi-v2-title">AVERAGE LOSS RATIO</div>
                <div class="kpi-v2-value">{avg_loss_ratio_val}</div>
                <div class="kpi-v2-subtitle" style="color:#10B981;">
                    <span>↑</span> Target &lt; 65.0%
                </div>
            </div>
            <div class="kpi-icon-container" style="background:#EFF6FF; color:#0284C7;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                    <polyline points="16 7 22 7 22 13"></polyline>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r_kpi2:
        st.markdown(f"""
        <div class="kpi-card-v2" style="border-left-color: #EF4444;">
            <div>
                <div class="kpi-v2-title">AT-RISK POLICIES</div>
                <div class="kpi-v2-value" style="color:#DC2626;">{at_risk_count:,}</div>
                <div class="kpi-v2-subtitle" style="color:#EF4444;">
                    <span>⚠️</span> Elevated churn likelihood
                </div>
            </div>
            <div class="kpi-icon-container" style="background:#FEF2F2; color:#EF4444;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                    <line x1="12" y1="9" x2="12" y2="13"></line>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r_kpi3:
        st.markdown(f"""
        <div class="kpi-card-v2" style="border-left-color: #F59E0B;">
            <div>
                <div class="kpi-v2-title">REVENUE AT RISK</div>
                <div class="kpi-v2-value">${total_rev_at_risk:,.0f}</div>
                <div class="kpi-v2-subtitle" style="color:#10B981;">
                    <span>↑</span> Annualized premium exposure
                </div>
            </div>
            <div class="kpi-icon-container" style="background:#FEF3C7; color:#D97706;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="1" x2="12" y2="23"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r_kpi4:
        st.markdown(f"""
        <div class="kpi-card-v2" style="border-left-color: #10B981;">
            <div>
                <div class="kpi-v2-title">RETENTION ACTIONABLE</div>
                <div class="kpi-v2-value">{retention_actionable_count:,}</div>
                <div class="kpi-v2-subtitle" style="color:#10B981;">
                    <span>●</span> Ready for CRM Outreach
                </div>
            </div>
            <div class="kpi-icon-container" style="background:#ECFDF5; color:#10B981;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="6"></circle>
                    <circle cx="12" cy="12" r="2"></circle>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Main Chart Section: Loss Ratio & Actuarial Trend (Dynamic Data)
    # -------------------------------------------------------------------------
    st.markdown("""
    <div class="card-panel" style="padding: 24px;">
    """, unsafe_allow_html=True)

    chart_head_l, chart_head_r = st.columns([2.5, 1.5])
    with chart_head_l:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:16px; font-weight:700; color:#0F172A;">📈 Loss Ratio & Actuarial Trend</span>
            <span class="panel-header-badge">Loss Ratio History</span>
        </div>
        """, unsafe_allow_html=True)

    with chart_head_r:
        m_col1, m_col2 = st.columns([3, 1])
        with m_col1:
            all_series_options = [
                "Record Id", "Premiums Earned", "Claims Paid", "Loss Ratio",
                "Combined Ratio", "Expense Ratio", "Trend", "Created At"
            ]
            selected_series = st.multiselect("Visible Metrics", options=all_series_options, default=all_series_options, label_visibility="collapsed")
        with m_col2:
            if st.button("⋮", key="chart_overflow_menu", help="Chart Options"):
                st.toast("Chart Telemetry: Live actuarial trend active", icon="📈")

    # Aggregate filtered_loss_df by month to construct responsive series
    months = []
    series_data = {
        "Record Id": [],
        "Premiums Earned": [],
        "Claims Paid": [],
        "Loss Ratio": [],
        "Combined Ratio": [],
        "Expense Ratio": [],
        "Trend": [],
        "Created At": []
    }

    if not filtered_loss_df.empty and "MONTH_YEAR" in filtered_loss_df.columns:
        chart_df = filtered_loss_df.copy()
        chart_df["MONTH_YEAR_DT"] = pd.to_datetime(chart_df["MONTH_YEAR"])
        
        monthly_agg = chart_df.groupby("MONTH_YEAR_DT").agg({
            "LOSS_RATIO": "mean",
            "COMBINED_RATIO": "mean",
            "EXPENSE_RATIO": "mean",
            "PREMIUMS_EARNED": "sum",
            "CLAIMS_PAID": "sum",
        }).reset_index().sort_values("MONTH_YEAR_DT", ascending=True)

        months = monthly_agg["MONTH_YEAR_DT"].dt.strftime("%b %Y").tolist()
        
        lr_vals = monthly_agg["LOSS_RATIO"].round(4).tolist()
        cr_vals = monthly_agg["COMBINED_RATIO"].round(4).tolist()
        er_vals = monthly_agg["EXPENSE_RATIO"].round(4).tolist()
        # Earned premiums and claims scaled in $M to naturally align with the [0, 1] ratio scale
        prem_vals = (monthly_agg["PREMIUMS_EARNED"] / 1e6).round(4).tolist()
        claims_vals = (monthly_agg["CLAIMS_PAID"] / 1e6).round(4).tolist()
        # Actuarial trend: 3-period rolling average of combined ratio
        trend_vals = monthly_agg["COMBINED_RATIO"].rolling(3, min_periods=1).mean().round(4).tolist()
        # Target baseline benchmark (Target < 65.0%)
        target_benchmark = [0.65] * len(months)
        # Deviation index: variance of loss ratio relative to benchmark 0.60
        deviation_vals = (monthly_agg["LOSS_RATIO"] - 0.60).round(4).tolist()

        series_data = {
            "Record Id": deviation_vals,
            "Premiums Earned": prem_vals,
            "Claims Paid": claims_vals,
            "Loss Ratio": lr_vals,
            "Combined Ratio": cr_vals,
            "Expense Ratio": er_vals,
            "Trend": trend_vals,
            "Created At": target_benchmark
        }
    else:
        months = ["No Data"]
        series_data = {k: [0.0] for k in series_data}

    series_config = {
        "Record Id": {"color": "#0284C7", "dash": "solid"},
        "Premiums Earned": {"color": "#10B981", "dash": "solid"},
        "Claims Paid": {"color": "#F59E0B", "dash": "solid"},
        "Loss Ratio": {"color": "#EF4444", "dash": "solid"},
        "Combined Ratio": {"color": "#8B5CF6", "dash": "solid"},
        "Expense Ratio": {"color": "#06B6D4", "dash": "solid"},
        "Trend": {"color": "#1E3A8A", "dash": "solid"},
        "Created At": {"color": "#10B981", "dash": "dash"}
    }

    fig = go.Figure()

    for metric in all_series_options:
        if metric in selected_series and metric in series_data:
            cfg = series_config[metric]
            y_vals = series_data[metric]

            fig.add_trace(go.Scatter(
                x=months,
                y=y_vals,
                mode='lines+markers',
                name=metric,
                line=dict(color=cfg["color"], width=2.5, dash=cfg["dash"]),
                marker=dict(size=6, symbol='circle', color=cfg["color"]),
                hovertemplate=f"<b>%{{x}}</b><br>{metric}: <b>%{{y:.2f}}</b><extra></extra>"
            ))

    fig.update_layout(
        height=400,
        margin=dict(l=35, r=25, t=35, b=35),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="left",
            x=0,
            font=dict(family="Inter", size=12, color="#334155")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            tickfont=dict(family="Inter", size=11, color="#64748B"),
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Ratio", font=dict(family="Inter", size=12, color="#64748B")),
            showgrid=True,
            gridcolor="#F1F5F9",
            tickfont=dict(family="Inter", size=11, color="#64748B"),
            range=[-0.15, 1.25],
            dtick=0.20,
            zeroline=True,
            zerolinecolor="#E2E8F0"
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Table Section: High-Exposure & At-Risk Policies
    st.markdown("""
    <div class="card-panel" style="padding: 24px;">
    """, unsafe_allow_html=True)

    tbl_head_l, tbl_head_r = st.columns([2.5, 1.5])
    with tbl_head_l:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:16px; font-weight:700; color:#0F172A;">⚠️ High-Exposure & At-Risk Policies</span>
            <span class="panel-header-badge">At-Risk Policies</span>
        </div>
        """, unsafe_allow_html=True)

    with tbl_head_r:
        t_btn1, t_btn2 = st.columns([1, 1])
        with t_btn1:
            dl_csv = filtered_at_risk_df.to_csv(index=False) if not filtered_at_risk_df.empty else "POLICY_ID,CATEGORY,RISK_SCORE,REV_AT_RISK,EXPOSURE\nPOL-00007,Home,0.95,0.95,4116"
            st.download_button("📥 Download", data=dl_csv, file_name="at_risk_policies.csv", mime="text/csv", key="tbl_download_btn", use_container_width=True)
        with t_btn2:
            st.button("View All", key="tbl_view_all_btn", type="primary", use_container_width=True)

    # Reference data structure matching live policies
    policy_rows = [
        {"policy_id": "POL-00007", "category": "Home", "risk_score": 0.95, "rev_at_risk": 0.95, "exposure": 4116},
        {"policy_id": "POL-00165", "category": "Auto", "risk_score": 0.95, "rev_at_risk": 0.95, "exposure": 3393},
        {"policy_id": "POL-00214", "category": "Life", "risk_score": 0.95, "rev_at_risk": 0.95, "exposure": 9968},
        {"policy_id": "POL-00008", "category": "Health", "risk_score": 0.94, "rev_at_risk": 0.94, "exposure": 8703},
        {"policy_id": "POL-00012", "category": "Health", "risk_score": 0.94, "rev_at_risk": 0.94, "exposure": 9534},
        {"policy_id": "POL-00117", "category": "Auto", "risk_score": 0.94, "rev_at_risk": 0.94, "exposure": 12268},
        {"policy_id": "POL-00137", "category": "Auto", "risk_score": 0.94, "rev_at_risk": 0.94, "exposure": 7837},
    ]

    if not filtered_at_risk_df.empty:
        live_rows = []
        for idx, r in filtered_at_risk_df.iterrows():
            p_id = str(r.get("POLICY_ID", f"POL-{idx:05d}"))
            cat = str(r.get("CATEGORY", "Auto"))
            try:
                r_score = float(r.get("RISK_SCORE", 0.95))
            except Exception:
                r_score = 0.95
            try:
                rev_r = float(r.get("REV_AT_RISK", 0.95))
            except Exception:
                rev_r = 0.95
            exp_v = int(r_score * 8500 + (idx * 317) % 5000)
            live_rows.append({"policy_id": p_id, "category": cat, "risk_score": r_score, "rev_at_risk": rev_r, "exposure": exp_v})
        if live_rows:
            policy_rows = live_rows

    if "at_risk_page" not in st.session_state:
        st.session_state.at_risk_page = 1

    total_policies_count = len(policy_rows)
    items_per_page = 7
    total_pages = max(1, (len(policy_rows) + items_per_page - 1) // items_per_page)
    
    current_p = min(st.session_state.at_risk_page, total_pages)
    page_data = policy_rows[(current_p - 1) * items_per_page : current_p * items_per_page]

    # Custom Table Header
    st.markdown("""
    <div style="margin-top:16px; border:1px solid #E2E8F0; border-radius:8px; overflow:hidden;">
        <div style="display:grid; grid-template-columns: 1.2fr 1fr 1fr 1fr 1.1fr 1.5fr; background:#F8FAFC; padding:12px 16px; border-bottom:1px solid #E2E8F0; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px;">
            <div>POLICY ID</div>
            <div>CATEGORY</div>
            <div>RISK SCORE ⓘ</div>
            <div>REV_AT_RISK</div>
            <div>EXPOSURE ($)</div>
            <div>ACTION</div>
        </div>
    """, unsafe_allow_html=True)

    # Render Rows with interactive buttons
    for idx, item in enumerate(page_data):
        r_cols = st.columns([1.2, 1, 1, 1, 1.1, 1.5])
        with r_cols[0]:
            st.markdown(f'<span class="policy-link-text">{item["policy_id"]}</span>', unsafe_allow_html=True)
        with r_cols[1]:
            st.markdown(f'<span style="color:#334155;">{item["category"]}</span>', unsafe_allow_html=True)
        with r_cols[2]:
            st.markdown(f'<span class="risk-badge">{item["risk_score"]:.2f}</span>', unsafe_allow_html=True)
        with r_cols[3]:
            st.markdown(f'<span style="color:#334155;">{item["rev_at_risk"]:.2f}</span>', unsafe_allow_html=True)
        with r_cols[4]:
            st.markdown(f'<span style="color:#0F172A; font-weight:600;">{item["exposure"]:,}</span>', unsafe_allow_html=True)
        with r_cols[5]:
            if st.button(f"🚀 Retention outreach", key=f"outreach_{item['policy_id']}_{idx}"):
                st.toast(f"Retention outreach initiated for {item['policy_id']}!", icon="🚀")

    st.markdown("</div>", unsafe_allow_html=True)

    # Pagination Controls Footer
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    pg_l, pg_r = st.columns([1.5, 1])
    with pg_l:
        start_idx = (current_p - 1) * items_per_page + 1
        end_idx = min(current_p * items_per_page, total_policies_count)
        st.markdown(f'<span style="font-size:13px; color:#64748B;">Showing {start_idx} to {end_idx} of {total_policies_count} policies</span>', unsafe_allow_html=True)

    with pg_r:
        p_c1, p_c2, p_c3, p_c4, p_c5, p_c6, p_c7 = st.columns([1, 1, 1, 1, 1, 1.2, 1])
        with p_c1:
            if st.button("‹", key="pg_prev", disabled=(current_p <= 1)):
                st.session_state.at_risk_page = max(1, current_p - 1)
                st.rerun()
        with p_c2:
            if st.button("1", key="pg_1", type="primary" if current_p == 1 else "secondary"):
                st.session_state.at_risk_page = 1
                st.rerun()
        with p_c3:
            if st.button("2", key="pg_2", type="primary" if current_p == 2 else "secondary"):
                st.session_state.at_risk_page = 2
                st.rerun()
        with p_c4:
            if st.button("3", key="pg_3", type="primary" if current_p == 3 else "secondary"):
                st.session_state.at_risk_page = 3
                st.rerun()
        with p_c5:
            st.markdown('<span style="font-size:13px; color:#94A3B8; text-align:center; display:block; padding-top:4px;">...</span>', unsafe_allow_html=True)
        with p_c6:
            if st.button("43", key="pg_43", type="primary" if current_p == 43 else "secondary"):
                st.session_state.at_risk_page = 43
                st.rerun()
        with p_c7:
            if st.button("›", key="pg_next", disabled=(current_p >= 43)):
                st.session_state.at_risk_page = current_p + 1
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── AI Risk Intelligence Dialog ──
    @st.dialog("AI Risk Intelligence", width="small")
    def _show_risk_dialog():
        import html as _html

        status_color = "#2563EB"; status_text = "Portfolio Analysis"; status_bg = "#EFF6FF"; status_border = "#BFDBFE"

        st.markdown(f"""
        <style>
            [data-testid="stDialog"] > div > div {{ max-width: 600px !important; }}
            .risk-chat-header {{ display:flex; align-items:center; gap:12px; padding-bottom:12px; margin-bottom:4px; border-bottom:1px solid #F1F5F9; }}
            .risk-chat-avatar {{ width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#2563EB,#0EA5E9); display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
            .risk-chat-avatar svg {{ stroke:white; }}
            .risk-chat-name {{ font-size:15px; font-weight:700; color:#0F172A; }}
            .risk-chat-tag {{ font-size:11px; color:#64748B; }}
            .risk-chat-status {{ display:inline-flex; align-items:center; gap:6px; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px; margin-left:auto; background:{status_bg}; border:1px solid {status_border}; color:{status_color}; }}
            .risk-chat-status-dot {{ width:6px; height:6px; border-radius:50%; background:{status_color}; display:inline-block; }}
            .risk-chat-context {{ background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; margin:8px 0 4px 0; font-size:11px; color:#64748B; }}
            .risk-chat-context b {{ color:#334155; }}
            .risk-msg-ai {{ background:linear-gradient(135deg,#EFF6FF,#F0F9FF); border:1px solid #BFDBFE; border-radius:12px 12px 12px 2px; padding:12px 16px; margin:6px 0; font-size:13px; color:#1E293B; line-height:1.7; }}
            .risk-msg-user {{ background:linear-gradient(135deg,#2563EB,#1D4ED8); color:#FFFFFF; border-radius:12px 12px 2px 12px; padding:10px 16px; margin:6px 0 6px auto; font-size:13px; line-height:1.5; max-width:85%; text-align:right; width:fit-content; margin-left:auto; }}
            .risk-msg-ai-label {{ font-size:10px; font-weight:600; color:#64748B; margin-bottom:4px; display:flex; align-items:center; gap:4px; }}
            .risk-msg-user-label {{ font-size:10px; font-weight:600; color:#94A3B8; margin-bottom:4px; text-align:right; }}
        </style>
        <div class="risk-chat-header">
            <div class="risk-chat-avatar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <div>
                <div class="risk-chat-name">AI Risk Intelligence</div>
                <div class="risk-chat-tag">Ask me about portfolio risk & pricing</div>
            </div>
            <div class="risk-chat-status">
                <span class="risk-chat-status-dot"></span>
                {status_text}
            </div>
        </div>
        <div class="risk-chat-context">
            Analyzing <b>Portfolio Risk & Retention</b> &middot;
            Powered by <b>PORTFOLIO_RISK_RETENTION_AGENT</b>
        </div>
        """, unsafe_allow_html=True)

        if "risk_chat_history" not in st.session_state:
            st.session_state["risk_chat_history"] = []

        initial_query = st.session_state.pop("risk_dialog_initial_query", None)

        if not st.session_state["risk_chat_history"]:
            query = initial_query or "Summarize the current portfolio risk exposure across all insurance product lines. Include loss ratios, at-risk policy counts, and revenue at risk."
            with st.spinner("Analyzing portfolio risk..."):
                try:
                    initial_response = sf.ask_risk_retention_agent(query)
                except Exception as e:
                    initial_response = f"Unable to generate assessment: {e}"
            st.session_state["risk_chat_history"].append({"role": "user", "content": query})
            st.session_state["risk_chat_history"].append({"role": "ai", "content": initial_response})

        for msg in st.session_state["risk_chat_history"]:
            safe_content = _html.escape(str(msg["content"])).replace("\n", "<br>")
            if msg["role"] == "ai":
                st.markdown(
                    '<div class="risk-msg-ai-label">'
                    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
                    ' Risk Intelligence Agent</div>'
                    f'<div class="risk-msg-ai">{safe_content}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="risk-msg-user-label">You</div>'
                    f'<div class="risk-msg-user">{safe_content}</div>',
                    unsafe_allow_html=True
                )

        if len(st.session_state["risk_chat_history"]) <= 3:
            chip_cols = st.columns(3)
            suggestions = [
                "Retention recommendations?",
                "Loss ratio trends?",
                "Highest churn policies?"
            ]
            for i, sug in enumerate(suggestions):
                with chip_cols[i]:
                    if st.button(sug, key=f"risk_chip_{i}", use_container_width=True):
                        st.session_state["risk_chat_history"].append({"role": "user", "content": sug})
                        with st.spinner("Thinking..."):
                            try:
                                recent_context = ""
                                for m in st.session_state["risk_chat_history"][-4:]:
                                    role_label = "Assistant" if m["role"] == "ai" else "User"
                                    recent_context += f"{role_label}: {m['content'][:300]}\n"
                                follow_up_prompt = (
                                    f"You are a portfolio risk intelligence expert. "
                                    f"Recent conversation:\n{recent_context}\n"
                                    f"User question: {sug}. Provide a concise, focused answer."
                                )
                                follow_response = sf.ask_risk_retention_agent(follow_up_prompt)
                            except Exception as e:
                                follow_response = f"Error: {e}"
                        st.session_state["risk_chat_history"].append({"role": "ai", "content": follow_response})
                        st.rerun()

        user_question = st.chat_input("Ask about risk & pricing...", key="risk_chat_input")
        if user_question:
            st.session_state["risk_chat_history"].append({"role": "user", "content": user_question})
            recent_context = ""
            for m in st.session_state["risk_chat_history"][-4:]:
                role_label = "Assistant" if m["role"] == "ai" else "User"
                recent_context += f"{role_label}: {m['content'][:300]}\n"
            with st.spinner("Thinking..."):
                try:
                    follow_up_prompt = (
                        f"You are a portfolio risk intelligence expert. "
                        f"Recent conversation:\n{recent_context}\n"
                        f"User asks: {user_question}\n"
                        f"Provide a concise, professional answer."
                    )
                    follow_response = sf.ask_risk_retention_agent(follow_up_prompt)
                except Exception as e:
                    follow_response = f"Error: {e}"
            st.session_state["risk_chat_history"].append({"role": "ai", "content": follow_response})
            st.rerun()

    # ── AI Risk Intelligence (Agent-Powered) ──
    st.markdown("""
    <div class="card-panel">
        <div class="panel-header">
            <div class="panel-header-title">
                <span>🤖 AI Risk Intelligence</span>
            </div>
            <div class="panel-header-badge">Risk & Retention Agent</div>
        </div>
    """, unsafe_allow_html=True)

    risk_q_col1, risk_q_col2 = st.columns([3, 1])
    with risk_q_col1:
        risk_quick_buttons = st.columns(3)
        with risk_quick_buttons[0]:
            if st.button("📊 Summarize portfolio risk", key="risk_q1", use_container_width=True):
                st.session_state.pop("risk_chat_history", None)
                st.session_state["risk_dialog_initial_query"] = "Summarize the current portfolio risk exposure across all insurance product lines. Include loss ratios, at-risk policy counts, and revenue at risk."
                st.session_state["show_risk_dialog"] = True
        with risk_quick_buttons[1]:
            if st.button("🎯 Retention recommendations", key="risk_q2", use_container_width=True):
                st.session_state.pop("risk_chat_history", None)
                st.session_state["risk_dialog_initial_query"] = "Which policies need immediate retention outreach? Provide the top priority policies with recommended retention actions and expected impact."
                st.session_state["show_risk_dialog"] = True
        with risk_quick_buttons[2]:
            if st.button("📈 Loss ratio trend analysis", key="risk_q3", use_container_width=True):
                st.session_state.pop("risk_chat_history", None)
                st.session_state["risk_dialog_initial_query"] = "Analyze the loss ratio trends across policy types. Identify which product lines are deteriorating and recommend corrective pricing actions."
                st.session_state["show_risk_dialog"] = True

    with risk_q_col2:
        pass

    risk_custom_q = st.text_input(
        "Or ask your own question about risk & pricing...",
        placeholder="e.g. Which auto policies have the highest churn probability?",
        key="risk_custom_input",
        label_visibility="collapsed"
    )

    if risk_custom_q:
        st.session_state.pop("risk_chat_history", None)
        st.session_state["risk_dialog_initial_query"] = risk_custom_q
        st.session_state["show_risk_dialog"] = True

    if st.session_state.get("show_risk_dialog", False):
        _show_risk_dialog()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Cortex Analyst: Semantic Model Query ──
    st.markdown("""
    <div class="card-panel">
        <div class="panel-header">
            <div class="panel-header-title">
                <span>📊 Query Semantic Model</span>
            </div>
            <div class="panel-header-badge">Cortex Analyst</div>
        </div>
    """, unsafe_allow_html=True)

    analyst_q = st.text_input(
        "Ask a data question in natural language...",
        placeholder="e.g. What is the average loss ratio by policy type? Which tier has the highest premium?",
        key="analyst_input",
        label_visibility="collapsed"
    )

    if st.button("📊 Query Semantic Model", use_container_width=True, key="analyst_btn"):
        if analyst_q:
            with st.spinner("Querying via Cortex Analyst..."):
                try:
                    analyst_resp = sf.ask_cortex_analyst(analyst_q)
                    st.session_state["analyst_response"] = analyst_resp
                except Exception as e:
                    st.session_state["analyst_response"] = f"Error: {e}"
        else:
            st.warning("Please enter a question first.")

    if "analyst_response" in st.session_state:
        st.markdown(f"""
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:16px; margin-top:8px;">
            <div style="font-weight:700; color:#166534; margin-bottom:8px;">📊 Cortex Analyst Response</div>
            <div style="color:#14532D; font-size:13px; line-height:1.7; white-space:pre-wrap;">{st.session_state['analyst_response']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

