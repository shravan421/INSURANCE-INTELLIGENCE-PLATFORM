import streamlit as st
import snowflake_utils as sf

def render():

    st.markdown("""
    <style>
    .ih-tile-card {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: box-shadow 0.3s, transform 0.3s;
    }
    .ih-tile-card:hover { box-shadow: 0 8px 28px rgba(0,0,0,0.10); transform: translateY(-3px); }
    .ih-tile-card-body { padding: 20px 22px 18px 22px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; }
    .ih-tile-card-title { font-size: 15px; font-weight: 700; color: #0F172A; display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
    .ih-tile-card-desc { font-size: 13px; color: #64748B; line-height: 1.6; margin-bottom: 14px; min-height: 62px; }
    .ih-tile-card-features { display: flex; flex-wrap: wrap; gap: 6px; }
    .ih-tile-card-chip {
        font-size: 11px; font-weight: 600; color: #475569;
        background: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 3px 10px; border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
        <div style="font-size:28px; background:linear-gradient(135deg,#2563EB,#7C3AED); border-radius:10px; width:42px; height:42px; display:flex; align-items:center; justify-content:center; color:#FFF;">🧠</div>
        <div>
            <div style="font-size:20px; font-weight:800; color:#0F172A;">Intelligence Hub</div>
            <div style="font-size:12px; color:#64748B;">AI-powered product matching, market analysis, and competitive pricing intelligence.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sub-page Navigation State ──
    if "ih_subpage" not in st.session_state:
        st.session_state["ih_subpage"] = "landing"

    # ── Back button when inside a sub-page ──
    if st.session_state["ih_subpage"] != "landing":
        if st.button("← Back to Intelligence Hub", key="ih_back_btn"):
            st.session_state["ih_subpage"] = "landing"
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # LANDING PAGE — Capability Tiles
    # ══════════════════════════════════════════════════════════════════════
    if st.session_state["ih_subpage"] == "landing":
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; font-size:22px; font-weight:800; color:#0F172A; margin-bottom:6px;">Intelligence Capabilities</div>
        <div style="text-align:center; font-size:13px; color:#64748B; margin-bottom:24px;">
            Product recommendations, market trends, and pricing optimization — all in one place.
        </div>
        """, unsafe_allow_html=True)

        tile_col1, tile_col2, tile_col3 = st.columns(3, gap="large")

        with tile_col1:
            st.markdown("""
            <div class="ih-tile-card">
                <div style="width:100%; height:110px; background: linear-gradient(135deg, #0D9488 0%, #14B8A6 40%, #2DD4BF 100%); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>
                    <div style="position:absolute; bottom:-20px; left:-20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.05);"></div>
                    <div style="text-align:center; position:relative; z-index:1;">
                        <div style="font-size:32px; margin-bottom:4px;">🎯</div>
                        <div style="font-size:11px; font-weight:700; color:#FFFFFF; letter-spacing:1px; text-transform:uppercase;">Product Matching</div>
                    </div>
                </div>
                <div class="ih-tile-card-body">
                    <div class="ih-tile-card-title">
                        <span>🎯</span> Smart Product Matching
                    </div>
                    <div class="ih-tile-card-desc">
                        AI-powered insurance product recommendations based on customer needs, profile, risk factors, and value optimization.
                    </div>
                    <div class="ih-tile-card-features">
                        <span class="ih-tile-card-chip">Needs-Based</span>
                        <span class="ih-tile-card-chip">Profile-Based</span>
                        <span class="ih-tile-card-chip">Risk-Adjusted</span>
                        <span class="ih-tile-card-chip">Value Optimized</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch Product Matching", use_container_width=True, type="primary", key="ih_launch_pm"):
                st.session_state["ih_subpage"] = "product_matching"
                st.rerun()

        with tile_col2:
            st.markdown("""
            <div class="ih-tile-card">
                <div style="width:100%; height:110px; background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 40%, #60A5FA 100%); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>
                    <div style="position:absolute; bottom:-20px; left:-20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.05);"></div>
                    <div style="text-align:center; position:relative; z-index:1;">
                        <div style="font-size:32px; margin-bottom:4px;">📊</div>
                        <div style="font-size:11px; font-weight:700; color:#FFFFFF; letter-spacing:1px; text-transform:uppercase;">Market Intelligence</div>
                    </div>
                </div>
                <div class="ih-tile-card-body">
                    <div class="ih-tile-card-title">
                        <span>📊</span> Market Trend Analysis
                    </div>
                    <div class="ih-tile-card-desc">
                        AI-powered market trend analysis and strategic insights across all insurance segments and product lines.
                    </div>
                    <div class="ih-tile-card-features">
                        <span class="ih-tile-card-chip">Trend Detection</span>
                        <span class="ih-tile-card-chip">Segment Analysis</span>
                        <span class="ih-tile-card-chip">Growth Metrics</span>
                        <span class="ih-tile-card-chip">Revenue Insights</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch Market Intelligence", use_container_width=True, type="primary", key="ih_launch_mi"):
                st.session_state["ih_subpage"] = "market_intelligence"
                st.rerun()

        with tile_col3:
            st.markdown("""
            <div class="ih-tile-card">
                <div style="width:100%; height:110px; background: linear-gradient(135deg, #D97706 0%, #F59E0B 40%, #FBBF24 100%); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>
                    <div style="position:absolute; bottom:-20px; left:-20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.05);"></div>
                    <div style="text-align:center; position:relative; z-index:1;">
                        <div style="font-size:32px; margin-bottom:4px;">💰</div>
                        <div style="font-size:11px; font-weight:700; color:#FFFFFF; letter-spacing:1px; text-transform:uppercase;">Competitive Pricing</div>
                    </div>
                </div>
                <div class="ih-tile-card-body">
                    <div class="ih-tile-card-title">
                        <span>💰</span> Pricing & Optimization
                    </div>
                    <div class="ih-tile-card-desc">
                        AI-powered pricing analysis, loss-ratio insights, and competitive benchmarking across all product tiers.
                    </div>
                    <div class="ih-tile-card-features">
                        <span class="ih-tile-card-chip">Loss Ratio Analysis</span>
                        <span class="ih-tile-card-chip">Pricing Optimization</span>
                        <span class="ih-tile-card-chip">Benchmarking</span>
                        <span class="ih-tile-card-chip">Profitability Insights</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch Competitive Pricing", use_container_width=True, type="primary", key="ih_launch_cp"):
                st.session_state["ih_subpage"] = "competitive_pricing"
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUB-PAGE: PRODUCT MATCHING
    # ══════════════════════════════════════════════════════════════════════
    elif st.session_state["ih_subpage"] == "product_matching":

        # ── Top Compact Header ──
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom: 2px;">
                <span style="font-size:24px;">🎯</span>
                <span style="font-size:22px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">Product Matching Agent</span>
            </div>
            <div style="font-size:13px; color:#64748B; margin-bottom:8px;">
                AI-powered insurance product recommendations based on your needs, profile, risk, and value.
            </div>
            """, unsafe_allow_html=True)
        with h_col2:
            is_connected = st.session_state.get("sf_connected", True)
            status_label = "Connected" if is_connected else "Offline"
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

        # ── Recommendation Factors / Strategy Pills & Clear Button ──
        s_col1, s_col2 = st.columns([4, 1])
        with s_col1:
            st.markdown("""
            <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; align-items:center;">
                <span style="font-size:12px; font-weight:600; color:#64748B; margin-right:4px;">Analyzing across:</span>
                <span style="background:#EFF6FF; border:1px solid #BFDBFE; color:#1D4ED8; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px;">
                    Needs-Based
                </span>
                <span style="background:#F0FDF4; border:1px solid #BBF7D0; color:#15803D; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px;">
                    Profile-Based
                </span>
                <span style="background:#FFF7ED; border:1px solid #FED7AA; color:#C2410C; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px;">
                    Risk-Adjusted
                </span>
                <span style="background:#FAF5FF; border:1px solid #E9D5FF; color:#7E22CE; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px;">
                    Value Optimized
                </span>
            </div>
            """, unsafe_allow_html=True)
        with s_col2:
            if st.session_state.get("pm_chat_history"):
                if st.button("🔄 New Search", key="pm_clear_chat", use_container_width=True):
                    st.session_state["pm_chat_history"] = []
                    st.rerun()

        # Session State for Chat History
        if "pm_chat_history" not in st.session_state:
            st.session_state["pm_chat_history"] = []

        pm_sample_prompts = [
            "I'm a 35-year-old married engineer with 2 kids earning $150K. What insurance should I get?",
            "What's the best health plan for a young healthy individual on a budget?",
            "Compare Gold vs Platinum auto insurance plans",
            "Recommend home insurance for a family in a high-risk flood zone",
            "I have high claims history — what Life insurance tier should I consider?",
        ]

        # ── EMPTY STATE or CHAT CONVERSATION ──
        if not st.session_state["pm_chat_history"]:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:32px 24px; text-align:center; margin:10px 0 24px 0; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-size:42px; margin-bottom:12px;">🎯</div>
                <div style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:6px;">Product Matching Agent</div>
                <div style="font-size:14px; font-weight:600; color:#3B82F6; margin-bottom:10px;">Find insurance products that fit your needs.</div>
                <div style="font-size:13px; color:#64748B; max-width:540px; margin:0 auto 24px auto; line-height:1.5;">
                    Tell me about yourself, your coverage requirements, budget, family situation, or risk profile to receive tailored recommendations.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='font-size:12px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;'>Try asking:</div>", unsafe_allow_html=True)
            chip_cols = st.columns(2)
            for i, p in enumerate(pm_sample_prompts[:4]):
                with chip_cols[i % 2]:
                    if st.button(f"💡 {p}", key=f"pm_empty_chip_{i}", use_container_width=True):
                        st.session_state["pm_pending_prompt"] = p
                        st.rerun()
        else:
            # Render Chat History
            for msg in st.session_state["pm_chat_history"]:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🎯"):
                        st.markdown(msg["content"])

        # ── Compact Prompt Suggestions above input during conversation ──
        if st.session_state["pm_chat_history"]:
            st.markdown("<div style='font-size:11px; font-weight:600; color:#94A3B8; margin-top:16px; margin-bottom:4px;'>Suggested prompts:</div>", unsafe_allow_html=True)
            q_cols = st.columns(3)
            for idx, prompt_text in enumerate(pm_sample_prompts[:3]):
                with q_cols[idx]:
                    short_text = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
                    if st.button(short_text, key=f"pm_conv_chip_{idx}", use_container_width=True):
                        st.session_state["pm_pending_prompt"] = prompt_text
                        st.rerun()

        # ── Chat Input ──
        prompt_to_run = None
        chat_input_val = st.chat_input("Describe your insurance needs or customer profile...", key="pm_chat_input_box")
        
        if chat_input_val:
            prompt_to_run = chat_input_val
        elif st.session_state.get("pm_pending_prompt"):
            prompt_to_run = st.session_state.pop("pm_pending_prompt")

        if prompt_to_run:
            st.session_state["pm_chat_history"].append({"role": "user", "content": prompt_to_run})
            
            with st.chat_message("user"):
                st.markdown(prompt_to_run)
                
            with st.chat_message("assistant", avatar="🎯"):
                with st.spinner("Analyzing your profile across needs, risk, and value..."):
                    try:
                        response = sf.ask_product_matching_agent(prompt_to_run)
                    except Exception as e:
                        print(f"[SECURITY REDACTED LOG] Exception in Product Matching Agent: {str(e)}")
                        response = "⚠️ Something went wrong while generating your recommendations. Please try again."
                st.markdown(response)
                st.session_state["pm_chat_history"].append({"role": "assistant", "content": response})
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUB-PAGE: MARKET INTELLIGENCE
    # ══════════════════════════════════════════════════════════════════════
    elif st.session_state["ih_subpage"] == "market_intelligence":

        # ── Top Compact Header ──
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:2px;">
                <span style="font-size:24px;">📊</span>
                <span style="font-size:22px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">Market Intelligence Agent</span>
            </div>
            <div style="font-size:13px; color:#64748B; margin-bottom:12px;">
                AI-powered market trend analysis and strategic insights across insurance segments.
            </div>
            """, unsafe_allow_html=True)
        with h_col2:
            is_connected = st.session_state.get("sf_connected", True)
            status_label = "Ready" if is_connected else "Offline"
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

        # ── Redesigned Compact Market KPI Summary Cards ──
        try:
            trend_df = sf.run_query("""
                SELECT POLICY_TYPE,
                       SUM(NEW_POLICIES) AS NEW_POL,
                       SUM(CANCELLED_POLICIES) AS CANCEL_POL,
                       AVG(RETENTION_RATE) AS AVG_RET,
                       AVG(GROWTH_RATE) AS AVG_GROWTH,
                       SUM(TOTAL_PREMIUM_REVENUE) AS TOTAL_REV
                FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.POLICY_TRENDS
                GROUP BY POLICY_TYPE ORDER BY TOTAL_REV DESC
            """)
            if trend_df is not None and not trend_df.empty:
                mi_cols = st.columns(len(trend_df))
                for idx, row in trend_df.iterrows():
                    with mi_cols[idx]:
                        growth = float(row.get("AVG_GROWTH", 0) or 0)
                        growth_color = "#059669" if growth >= 0 else "#DC2626"
                        growth_arrow = "↑" if growth >= 0 else "↓"
                        st.markdown(f"""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 16px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                            <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase;">{row['POLICY_TYPE']}</div>
                            <div style="font-size:20px; font-weight:800; color:#0F172A; margin:4px 0 2px 0;">${float(row.get('TOTAL_REV',0) or 0):,.0f}</div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
                                <span style="font-size:12px; color:{growth_color}; font-weight:600;">{growth_arrow} {growth:.1f}% growth</span>
                                <span style="font-size:11px; color:#64748B; font-weight:500;">Retention {float(row.get('AVG_RET',0) or 0):.0f}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception:
            pass

        # ── Action Row (Clear Chat & Context) ──
        s_col1, s_col2 = st.columns([4, 1])
        with s_col2:
            if st.session_state.get("mi_chat_history"):
                if st.button("🔄 New Analysis", key="mi_clear_chat", use_container_width=True):
                    st.session_state["mi_chat_history"] = []
                    st.rerun()

        # Session State for Market Intelligence Chat History
        if "mi_chat_history" not in st.session_state:
            st.session_state["mi_chat_history"] = []

        mi_sample_prompts = [
            "What are the key market trends in Health insurance over the last 6 months?",
            "Which product lines are growing and which are declining?",
            "Show me retention rate trends across all insurance types",
            "What market signals indicate we should adjust our Auto insurance strategy?",
            "Analyze the relationship between premium growth and loss ratios",
        ]

        # ── EMPTY STATE or CONVERSATION ──
        if not st.session_state["mi_chat_history"]:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:32px 24px; text-align:center; margin:16px 0 24px 0; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-size:42px; margin-bottom:12px;">📊</div>
                <div style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:6px;">Market Intelligence Assistant</div>
                <div style="font-size:14px; font-weight:600; color:#3B82F6; margin-bottom:10px;">Strategic market analysis & trend detection</div>
                <div style="font-size:13px; color:#64748B; max-width:540px; margin:0 auto 24px auto; line-height:1.5;">
                    Ask me about market trends, growth patterns, retention, product performance, or competitive dynamics across insurance lines.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size:12px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;'>Suggested Questions:</div>", unsafe_allow_html=True)
            chip_cols = st.columns(2)
            for i, p in enumerate(mi_sample_prompts[:4]):
                with chip_cols[i % 2]:
                    if st.button(f"📈 {p}", key=f"mi_empty_chip_{i}", use_container_width=True):
                        st.session_state["mi_pending_prompt"] = p
                        st.rerun()
        else:
            # Render Chat History
            for msg in st.session_state["mi_chat_history"]:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="📊"):
                        st.markdown(msg["content"])

        # ── Suggested prompts bar during conversation ──
        if st.session_state["mi_chat_history"]:
            st.markdown("<div style='font-size:11px; font-weight:600; color:#94A3B8; margin-top:16px; margin-bottom:4px;'>Suggested questions:</div>", unsafe_allow_html=True)
            q_cols = st.columns(3)
            for idx, prompt_text in enumerate(mi_sample_prompts[:3]):
                with q_cols[idx]:
                    short_text = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
                    if st.button(short_text, key=f"mi_conv_chip_{idx}", use_container_width=True):
                        st.session_state["mi_pending_prompt"] = prompt_text
                        st.rerun()

        # ── Chat Input ──
        prompt_to_run = None
        chat_input_val = st.chat_input("Ask about market trends, growth patterns, or retention...", key="mi_chat_input_box")
        
        if chat_input_val:
            prompt_to_run = chat_input_val
        elif st.session_state.get("mi_pending_prompt"):
            prompt_to_run = st.session_state.pop("mi_pending_prompt")

        if prompt_to_run:
            st.session_state["mi_chat_history"].append({"role": "user", "content": prompt_to_run})
            
            with st.chat_message("user"):
                st.markdown(prompt_to_run)
                
            with st.chat_message("assistant", avatar="📊"):
                with st.spinner("Analyzing market data across Health, Auto, Life, and Home insurance segments..."):
                    try:
                        response = sf.ask_market_intelligence_agent(prompt_to_run)
                    except Exception as e:
                        print(f"[SECURITY REDACTED LOG] Exception in Market Intelligence Agent: {str(e)}")
                        response = "⚠️ Unable to analyze the market right now. Please try again."
                st.markdown(response)
                st.session_state["mi_chat_history"].append({"role": "assistant", "content": response})
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUB-PAGE: COMPETITIVE PRICING
    # ══════════════════════════════════════════════════════════════════════
    elif st.session_state["ih_subpage"] == "competitive_pricing":

        # ── Top Compact Header ──
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:2px;">
                <span style="font-size:24px;">💰</span>
                <span style="font-size:22px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">Competitive Pricing & Optimization</span>
            </div>
            <div style="font-size:13px; color:#64748B; margin-bottom:12px;">
                AI-powered pricing analysis, loss-ratio insights, and competitive benchmarking.
            </div>
            """, unsafe_allow_html=True)
        with h_col2:
            is_connected = st.session_state.get("sf_connected", True)
            status_label = "Ready" if is_connected else "Offline"
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

        # ── Redesigned Loss Ratio Snapshot KPI Cards ──
        try:
            lr_df = sf.run_query("""
                SELECT POLICY_TYPE, PLAN_TIER,
                       AVG(LOSS_RATIO) AS AVG_LR,
                       AVG(COMBINED_RATIO) AS AVG_CR,
                       SUM(PREMIUMS_EARNED) AS TOTAL_PREM,
                       SUM(CLAIMS_PAID) AS TOTAL_CLAIMS
                FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.LOSS_RATIO_HISTORY
                GROUP BY POLICY_TYPE, PLAN_TIER
                ORDER BY AVG_LR DESC
                LIMIT 8
            """)
            if lr_df is not None and not lr_df.empty:
                st.markdown("<div style='font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;'>Loss Ratio Snapshot (Higher = Less Profitable)</div>", unsafe_allow_html=True)
                cp_cols = st.columns(4)
                for idx, row in lr_df.head(4).iterrows():
                    with cp_cols[idx]:
                        lr_val = float(row.get("AVG_LR", 0) or 0)
                        lr_color = "#DC2626" if lr_val > 0.7 else ("#D97706" if lr_val > 0.5 else "#059669")
                        lr_bg_accent = "#FEF2F2" if lr_val > 0.7 else ("#FFFBEB" if lr_val > 0.5 else "#F0FDF4")
                        st.markdown(f"""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-size:11px; color:#475569; font-weight:700; text-transform:uppercase;">{row['POLICY_TYPE']} — {row['PLAN_TIER']}</span>
                                <span style="font-size:10px; background:{lr_bg_accent}; color:{lr_color}; font-weight:700; padding:2px 6px; border-radius:6px;">LR {lr_val:.0%}</span>
                            </div>
                            <div style="font-size:22px; font-weight:800; color:{lr_color}; margin:6px 0 4px 0;">{lr_val:.0%}</div>
                            <div style="display:flex; justify-content:space-between; font-size:11px; color:#64748B;">
                                <span>Combined: {float(row.get('AVG_CR',0) or 0):.0%}</span>
                                <span>Premiums: ${float(row.get('TOTAL_PREM',0) or 0):,.0f}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception:
            pass

        # ── Action Row (Clear Chat & Context) ──
        s_col1, s_col2 = st.columns([4, 1])
        with s_col2:
            if st.session_state.get("cp_chat_history"):
                if st.button("🔄 New Analysis", key="cp_clear_chat", use_container_width=True):
                    st.session_state["cp_chat_history"] = []
                    st.rerun()

        # Session State for Competitive Pricing Chat History
        if "cp_chat_history" not in st.session_state:
            st.session_state["cp_chat_history"] = []

        cp_sample_prompts = [
            "Are our Health Gold premiums competitive? Should we adjust pricing?",
            "Which product lines have loss ratios above 70% and need premium increases?",
            "Optimize pricing across Auto tiers to improve profitability",
            "What's the optimal premium for Home Silver based on claims and market data?",
            "Show me a pricing comparison across all products and tiers",
        ]

        # ── EMPTY STATE or CONVERSATION ──
        if not st.session_state["cp_chat_history"]:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:32px 24px; text-align:center; margin:16px 0 24px 0; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                <div style="font-size:42px; margin-bottom:12px;">💰</div>
                <div style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:6px;">Pricing Optimization Assistant</div>
                <div style="font-size:14px; font-weight:600; color:#3B82F6; margin-bottom:10px;">Actuarial pricing, loss ratio analysis & benchmarking</div>
                <div style="font-size:13px; color:#64748B; max-width:540px; margin:0 auto 24px auto; line-height:1.5;">
                    Ask me about pricing competitiveness, loss ratios, premium adjustments, profitability, or tier-level pricing recommendations.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size:12px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;'>Suggested Pricing Queries:</div>", unsafe_allow_html=True)
            chip_cols = st.columns(2)
            for i, p in enumerate(cp_sample_prompts[:4]):
                with chip_cols[i % 2]:
                    if st.button(f"💡 {p}", key=f"cp_empty_chip_{i}", use_container_width=True):
                        st.session_state["cp_pending_prompt"] = p
                        st.rerun()
        else:
            # Render Chat History
            for msg in st.session_state["cp_chat_history"]:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="💰"):
                        st.markdown(msg["content"])

        # ── Suggested prompts bar during conversation ──
        if st.session_state["cp_chat_history"]:
            st.markdown("<div style='font-size:11px; font-weight:600; color:#94A3B8; margin-top:16px; margin-bottom:4px;'>Suggested pricing queries:</div>", unsafe_allow_html=True)
            q_cols = st.columns(3)
            for idx, prompt_text in enumerate(cp_sample_prompts[:3]):
                with q_cols[idx]:
                    short_text = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
                    if st.button(short_text, key=f"cp_conv_chip_{idx}", use_container_width=True):
                        st.session_state["cp_pending_prompt"] = prompt_text
                        st.rerun()

        # ── Chat Input ──
        prompt_to_run = None
        chat_input_val = st.chat_input("Ask about pricing strategy, loss ratios, or competitive benchmarking...", key="cp_chat_input_box")
        
        if chat_input_val:
            prompt_to_run = chat_input_val
        elif st.session_state.get("cp_pending_prompt"):
            prompt_to_run = st.session_state.pop("cp_pending_prompt")

        if prompt_to_run:
            st.session_state["cp_chat_history"].append({"role": "user", "content": prompt_to_run})
            
            with st.chat_message("user"):
                st.markdown(prompt_to_run)
                
            with st.chat_message("assistant", avatar="💰"):
                with st.spinner("Price Optimization Agent evaluating loss ratios, combined ratios, and pricing competitiveness..."):
                    try:
                        response = sf.ask_price_optimization_agent(prompt_to_run)
                    except Exception as e:
                        print(f"[SECURITY REDACTED LOG] Exception in Price Optimization Agent: {str(e)}")
                        response = "⚠️ Unable to complete the pricing analysis. Please try again."
                st.markdown(response)
                st.session_state["cp_chat_history"].append({"role": "assistant", "content": response})
            st.rerun()
