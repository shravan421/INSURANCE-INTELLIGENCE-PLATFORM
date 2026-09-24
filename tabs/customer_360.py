import streamlit as st
import pandas as pd
import snowflake_utils as sf

def render():
    def run_360_sql(query_str):
        try:
            from snowflake.snowpark.context import get_active_session
            sess = get_active_session()
            return sess.sql(query_str).to_pandas()
        except Exception:
            return sf.run_query(query_str)

    # ── Section 1: Customer Search Header ──
    try:
        customers = run_360_sql("""
            SELECT CUSTOMER_ID, CUSTOMER_NAME 
            FROM INSURANCE_MGMT_SYSTEM.GOLD.CUSTOMER_360
            ORDER BY CUSTOMER_NAME
        """)
    except Exception:
        customers = pd.DataFrame()

    if customers is None or customers.empty or "CUSTOMER_ID" not in customers.columns:
        try:
            customers = run_360_sql("""
                SELECT CUSTOMER_ID, CUSTOMER_NAME 
                FROM INSURANCE_MGMT_SYSTEM.CORE.CUSTOMERS
                ORDER BY CUSTOMER_NAME
            """)
        except Exception:
            customers = pd.DataFrame()

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:16px 20px; margin-bottom:16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <h3 style="margin:0; font-size:20px; font-weight:800; color:#0F172A; display:flex; align-items:center; gap:8px;">
                    <span>📊</span> Customer 360 Profile
                </h3>
                <div style="font-size:13px; color:#64748B; margin-top:2px;">
                    Unified customer view for policies, claims, risk, engagement, and AI insights.
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Live Database View</span>
                <span class="risk-badge" style="background:#E0F2FE; color:#0369A1; border-color:#BAE6FD;">Customer 360 View</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_sel1, c_sel2 = st.columns([3, 1])
    with c_sel1:
        if not customers.empty and "CUSTOMER_ID" in customers.columns and "CUSTOMER_NAME" in customers.columns:
            options_list = customers["CUSTOMER_ID"].tolist()
            selected = st.selectbox(
                "Search or select a customer",
                options=options_list,
                format_func=lambda x: f"{customers[customers['CUSTOMER_ID']==x]['CUSTOMER_NAME'].values[0]} ({x})",
                label_visibility="collapsed"
            )
        else:
            st.warning("⚠️ No customer records found in database.")
            selected = None

    if selected:
        # ── Load 360 data for this customer ──
        try:
            row_df = run_360_sql(f"""
                SELECT * FROM INSURANCE_MGMT_SYSTEM.GOLD.CUSTOMER_360
                WHERE CUSTOMER_ID = '{selected}'
            """)
            row = row_df.iloc[0] if not row_df.empty else None
        except Exception:
            row = None

        if row is not None:
            # ──────────────────────────────────────────────────
            # Section 2: Compact Customer Identity Card
            # ──────────────────────────────────────────────────
            cust_name = row.get('CUSTOMER_NAME', 'Unknown Customer')
            name_parts = str(cust_name).split()
            initials = "".join([p[0].upper() for p in name_parts[:2]]) if name_parts else "CU"
            
            cust_id = row.get('CUSTOMER_ID', selected)
            age = row.get('AGE', 'N/A')
            gender = row.get('GENDER', 'N/A')
            state = row.get('STATE', 'N/A')
            city = row.get('CITY', 'N/A')
            marital = row.get('MARITAL_STATUS', 'N/A')
            occ = row.get('OCCUPATION', 'N/A')
            income = row.get('ANNUAL_INCOME', None)
            credit = row.get('CREDIT_SCORE', 'N/A')
            bmi = row.get('BMI', None)
            smoker = row.get('SMOKING_STATUS', 'N/A')
            since = row.get('CUSTOMER_SINCE', 'N/A')
            tenure = row.get('TENURE_YEARS', 0)

            inc_str = f"${income:,.0f}" if pd.notnull(income) and isinstance(income, (int, float)) else "N/A"
            bmi_str = f"{float(bmi):.1f}" if pd.notnull(bmi) and isinstance(bmi, (int, float)) else "N/A"
            loc_str = f"{state}, {city}" if pd.notnull(state) and pd.notnull(city) else f"{state}"

            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px 22px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #F1F5F9; padding-bottom: 14px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #1E3A8A, #0284C7); color: #FFFFFF; font-weight: 800; font-size: 18px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25);">
                            {initials}
                        </div>
                        <div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #0F172A;">{cust_name}</h4>
                                <span style="background: #F1F5F9; color: #475569; font-weight: 700; font-size: 12px; padding: 2px 8px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; border: 1px solid #E2E8F0;">{cust_id}</span>
                            </div>
                            <div style="font-size: 12px; color: #64748B; margin-top: 3px; display: flex; align-items: center; gap: 12px;">
                                <span>📅 Customer since <strong>{since}</strong> ({tenure} yrs tenure)</span>
                                <span>•</span>
                                <span style="color: #10B981; font-weight: 600;">● Active Record</span>
                            </div>
                        </div>
                    </div>
                    <div>
                        <span class="risk-badge" style="background:#EFF6FF; color:#1D4ED8; border-color:#BFDBFE; font-size:12px; padding:6px 12px;">
                            Verified 360 Record
                        </span>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 14px;">
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Age / Gender</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{age} yrs | {gender}</div>
                    </div>
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Location</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{loc_str}</div>
                    </div>
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Occupation</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{occ} ({marital})</div>
                    </div>
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Annual Income</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{inc_str}</div>
                    </div>
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Credit Score</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{credit}</div>
                    </div>
                    <div style="background:#F8FAFC; border:1px solid #F1F5F9; padding:10px 14px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">BMI & Smoker</div>
                        <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:2px;">{bmi_str} | Smoker: {smoker}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ──────────────────────────────────────────────────
            # Section 3: Portfolio KPI Cards Row (6 Cards)
            # ──────────────────────────────────────────────────
            policy_cnt = int(row.get('POLICY_COUNT', 0)) if pd.notnull(row.get('POLICY_COUNT')) else 0
            active_policies = int(row.get('ACTIVE_POLICIES', 0)) if pd.notnull(row.get('ACTIVE_POLICIES')) else 0
            tot_premium = float(row.get('TOTAL_PREMIUM', 0)) if pd.notnull(row.get('TOTAL_PREMIUM')) else 0.0
            tot_claimed = float(row.get('TOTAL_CLAIMED', 0)) if pd.notnull(row.get('TOTAL_CLAIMED')) and row.get('TOTAL_CLAIMED') else 0.0
            loss_ratio = float(row.get('LOSS_RATIO', 0)) if pd.notnull(row.get('LOSS_RATIO')) else 0.0
            
            churn_pct = row.get('MAX_CHURN_PROBABILITY', None)
            if pd.isnull(churn_pct):
                churn_pct = row.get('CHURN_PROBABILITY', None)

            if churn_pct is not None and pd.notnull(churn_pct):
                c_val = float(churn_pct)
                c_fmt = f"{c_val:.0%}"
                if c_val >= 0.70:
                    c_sub = "⚠️ Critical churn risk"
                    c_color = "#DC2626"
                    c_border = "#EF4444"
                elif c_val >= 0.40:
                    c_sub = "⚡ Moderate Risk"
                    c_color = "#D97706"
                    c_border = "#F59E0B"
                else:
                    c_sub = "✓ Healthy retention"
                    c_color = "#059669"
                    c_border = "#10B981"
            else:
                c_fmt = "N/A"
                c_sub = "No model prediction"
                c_color = "#64748B"
                c_border = "#CBD5E1"

            k1, k2, k3, k4, k5, k6 = st.columns(6)
            
            with k1:
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: #0284C7;">
                    <div>
                        <div class="kpi-v2-title">Policies</div>
                        <div class="kpi-v2-value">{policy_cnt}</div>
                        <div class="kpi-v2-subtitle" style="color:#0284C7;"><span>● {active_policies} active</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: #0284C7;">
                    <div>
                        <div class="kpi-v2-title">Total Premium</div>
                        <div class="kpi-v2-value">${tot_premium:,.0f}</div>
                        <div class="kpi-v2-subtitle" style="color:#64748B;"><span>Annual portfolio</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: #64748B;">
                    <div>
                        <div class="kpi-v2-title">Total Claimed</div>
                        <div class="kpi-v2-value">${tot_claimed:,.0f}</div>
                        <div class="kpi-v2-subtitle" style="color:#64748B;"><span>Claims exposure</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with k4:
                lr_color = "#DC2626" if loss_ratio > 1.0 else "#10B981"
                lr_sub = "⚠️ High ratio" if loss_ratio > 1.0 else ("✓ Normal ratio" if tot_claimed > 0 else "No claims")
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: {lr_color};">
                    <div>
                        <div class="kpi-v2-title">Loss Ratio</div>
                        <div class="kpi-v2-value" style="color:{lr_color};">{loss_ratio:.2f}x</div>
                        <div class="kpi-v2-subtitle" style="color:{lr_color};"><span>{lr_sub}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with k5:
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: {c_border};">
                    <div>
                        <div class="kpi-v2-title">Churn Risk</div>
                        <div class="kpi-v2-value" style="color:{c_color};">{c_fmt}</div>
                        <div class="kpi-v2-subtitle" style="color:{c_color};"><span>{c_sub}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with k6:
                fraud_cnt = int(row.get('FRAUD_ALERT_COUNT', 0)) if pd.notnull(row.get('FRAUD_ALERT_COUNT')) else 0
                fr_color = "#DC2626" if fraud_cnt > 0 else "#10B981"
                fr_sub = f"🚨 {fraud_cnt} Alerts" if fraud_cnt > 0 else "✓ Clean record"
                st.markdown(f"""
                <div class="kpi-card-v2" style="border-left-color: {fr_color};">
                    <div>
                        <div class="kpi-v2-title">Fraud Status</div>
                        <div class="kpi-v2-value" style="color:{fr_color};">{fraud_cnt}</div>
                        <div class="kpi-v2-subtitle" style="color:{fr_color};"><span>{fr_sub}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ──────────────────────────────────────────────────
            # Section 4: AI Insight Structured Analysis Card
            # ──────────────────────────────────────────────────
            top_risk = row.get('TOP_RISK_FACTOR') or 'None'
            ret_offer = row.get('RETENTION_OFFER') or 'None'
            
            if policy_cnt == 0:
                insight_context = f"{cust_name} currently holds no active policy portfolio (0 policies, $0 premium). Churn risk is estimated at {c_fmt} with top factor '{top_risk}'. Recommended action: {ret_offer}."
                prompt = f"""You are an insurance analyst. Customer {cust_name} currently holds NO active policies ($0 total premium, 0 claims). Churn model probability is {c_fmt}, top risk factor is '{top_risk}', and retention offer is '{ret_offer}'. Provide a concise 2-sentence executive summary explaining their status and recommended engagement strategy."""
            else:
                insight_context = f"{cust_name} holds {policy_cnt} policies (${tot_premium:,.0f} premium) with loss ratio {loss_ratio:.2f}x. Churn risk is {c_fmt} driven by '{top_risk}'. Recommended action: {ret_offer}."
                prompt = f"""You are an insurance analyst. Given profile: Name {cust_name}, Policies {policy_cnt}, Premium ${tot_premium:,.0f}, Claims ${tot_claimed:,.0f}, Loss Ratio {loss_ratio:.2f}x, Churn Prob {c_fmt}, Risk Factor '{top_risk}', Retention Offer '{ret_offer}'. Provide a direct 2-sentence executive assessment summarizing value, key concern, and recommended action."""

            try:
                insight_df = run_360_sql(f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', $${prompt}$$) AS INSIGHT
                """)
                if not insight_df.empty and pd.notnull(insight_df.iloc[0][0]):
                    insight_text = str(insight_df.iloc[0][0]).strip()
                else:
                    insight_text = insight_context
            except Exception:
                insight_text = insight_context

            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:18px 22px; margin-top:16px; margin-bottom:20px; box-shadow:0 1px 3px rgba(0,0,0,0.03); border-top: 4px solid #1D4ED8;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #F1F5F9; padding-bottom:10px;">
                    <div style="font-size:14px; font-weight:800; color:#0F172A; display:flex; align-items:center; gap:8px;">
                        <span style="font-size:18px;">🤖</span> Executive AI Insight & Risk Assessment
                    </div>
                    <span style="background:#EFF6FF; color:#1D4ED8; font-size:11px; font-weight:700; padding:3px 10px; border-radius:12px; border:1px solid #BFDBFE;">
                        Snowflake Cortex • mistral-large2
                    </span>
                </div>
                <div style="font-size:14px; color:#1E293B; line-height:1.6; margin-bottom:16px; background:#F8FAFC; padding:14px 16px; border-radius:8px; border-left:3px solid #3B82F6;">
                    {insight_text}
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
                    <div style="background:#F0FDF4; border:1px solid #DCFCE7; padding:12px 16px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#166534; text-transform:uppercase; letter-spacing:0.5px;">Recommended Retention Action</div>
                        <div style="font-size:13px; font-weight:700; color:#14532D; margin-top:3px;">🎯 {ret_offer}</div>
                    </div>
                    <div style="background:#FEF2F2; border:1px solid #FEE2E2; padding:12px 16px; border-radius:8px;">
                        <div style="font-size:11px; font-weight:700; color:#991B1B; text-transform:uppercase; letter-spacing:0.5px;">Key Risk Drivers</div>
                        <div style="font-size:13px; font-weight:700; color:#7F1D1D; margin-top:3px;">⚡ Top: {top_risk} | 2nd: {row.get('SECOND_RISK_FACTOR', 'None')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ──────────────────────────────────────────────────
            # Section 5 & 6: Policies Book & Claims History Grid
            # ──────────────────────────────────────────────────
            col_policies, col_claims = st.columns(2)
            
            with col_policies:
                st.markdown("""
                <div style="font-size:15px; font-weight:800; color:#0F172A; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                    <span>📋</span> Policy Book Overview
                </div>
                """, unsafe_allow_html=True)
                try:
                    policies_df = run_360_sql(f"""
                        SELECT POLICY_ID, POLICY_TYPE, PLAN_TIER, POLICY_STATUS,
                               PREMIUM_AMOUNT, COVERAGE_AMOUNT, DEDUCTIBLE,
                               LOSS_RATIO, START_DATE, END_DATE
                        FROM INSURANCE_MGMT_SYSTEM.CORE.POLICIES
                        WHERE CUSTOMER_ID = '{selected}'
                        ORDER BY START_DATE DESC
                    """)
                    if not policies_df.empty:
                        st.dataframe(policies_df, use_container_width=True, hide_index=True)
                    else:
                        st.markdown("""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                            <div style="font-size:28px; margin-bottom:6px;">📄</div>
                            <div style="font-weight:700; color:#334155; font-size:14px;">No Policy Records Found</div>
                            <div style="font-size:12px; margin-top:2px;">This customer currently has no policy records in Snowflake CORE.POLICIES.</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    st.markdown("""
                    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                        <div style="font-size:28px; margin-bottom:6px;">📄</div>
                        <div style="font-weight:700; color:#334155; font-size:14px;">No Policy Records Found</div>
                        <div style="font-size:12px; margin-top:2px;">This customer currently has no policy records in Snowflake CORE.POLICIES.</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_claims:
                st.markdown("""
                <div style="font-size:15px; font-weight:800; color:#0F172A; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                    <span>🚨</span> Claims Ledger History
                </div>
                """, unsafe_allow_html=True)
                try:
                    claims_df = run_360_sql(f"""
                        SELECT CLAIM_ID, CLAIM_TYPE, CLAIM_STATUS, CLAIM_AMOUNT,
                               APPROVED_AMOUNT, FRAUD_FLAG, FRAUD_SCORE,
                               DAYS_TO_RESOLVE, CLAIM_DATE
                        FROM INSURANCE_MGMT_SYSTEM.CORE.CLAIMS
                        WHERE CUSTOMER_ID = '{selected}'
                        ORDER BY CLAIM_DATE DESC
                    """)
                    if not claims_df.empty:
                        st.dataframe(claims_df, use_container_width=True, hide_index=True)
                    else:
                        st.markdown("""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                            <div style="font-size:28px; margin-bottom:6px;">📂</div>
                            <div style="font-weight:700; color:#334155; font-size:14px;">No Claims Filed</div>
                            <div style="font-size:12px; margin-top:2px;">No claim history records are associated with this customer in CORE.CLAIMS.</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    st.markdown("""
                    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                        <div style="font-size:28px; margin-bottom:6px;">📂</div>
                        <div style="font-weight:700; color:#334155; font-size:14px;">No Claims Filed</div>
                        <div style="font-size:12px; margin-top:2px;">No claim history records are associated with this customer in CORE.CLAIMS.</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ──────────────────────────────────────────────────
            # Section 7 & 8: Premium Risk Factors & Risk Engagement Grid
            # ──────────────────────────────────────────────────
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            col_factors, col_risk = st.columns(2)
            
            with col_factors:
                st.markdown("""
                <div style="font-size:15px; font-weight:800; color:#0F172A; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                    <span>📈</span> Premium Risk Multipliers
                </div>
                """, unsafe_allow_html=True)
                try:
                    factors_df = run_360_sql(f"""
                        SELECT POLICY_TYPE, PLAN_TIER,
                               BASE_PREMIUM, AGE_FACTOR, LOCATION_FACTOR,
                               HEALTH_FACTOR, LIFESTYLE_FACTOR, CLAIMS_HISTORY_FACTOR,
                               FINAL_PREMIUM, DISCOUNT_APPLIED
                        FROM INSURANCE_MGMT_SYSTEM.PREMIUM.PREMIUM_CALCULATIONS
                        WHERE CUSTOMER_ID = '{selected}'
                        ORDER BY CALC_DATE DESC
                    """)
                    if not factors_df.empty:
                        latest = factors_df.iloc[0]
                        chart_data = pd.DataFrame({
                            "Factor": ["Age", "Location", "Health", "Lifestyle", "Claims History"],
                            "Multiplier": [
                                float(latest.get("AGE_FACTOR", 1.0)) if pd.notnull(latest.get("AGE_FACTOR")) else 1.0,
                                float(latest.get("LOCATION_FACTOR", 1.0)) if pd.notnull(latest.get("LOCATION_FACTOR")) else 1.0,
                                float(latest.get("HEALTH_FACTOR", 1.0)) if pd.notnull(latest.get("HEALTH_FACTOR")) else 1.0,
                                float(latest.get("LIFESTYLE_FACTOR", 1.0)) if pd.notnull(latest.get("LIFESTYLE_FACTOR")) else 1.0,
                                float(latest.get("CLAIMS_HISTORY_FACTOR", 1.0)) if pd.notnull(latest.get("CLAIMS_HISTORY_FACTOR")) else 1.0
                            ]
                        }).set_index("Factor")
                        st.bar_chart(chart_data)
                        base_p = float(latest.get('BASE_PREMIUM', 0)) if pd.notnull(latest.get('BASE_PREMIUM')) else 0.0
                        final_p = float(latest.get('FINAL_PREMIUM', 0)) if pd.notnull(latest.get('FINAL_PREMIUM')) else 0.0
                        disc_p = float(latest.get('DISCOUNT_APPLIED', 0)) if pd.notnull(latest.get('DISCOUNT_APPLIED')) else 0.0
                        st.caption(f"Base Premium: ${base_p:,.0f} → Final Quoted: ${final_p:,.0f} (Discount Applied: ${disc_p:,.0f})")
                    else:
                        st.markdown("""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                            <div style="font-size:28px; margin-bottom:6px;">📊</div>
                            <div style="font-weight:700; color:#334155; font-size:14px;">No Premium Risk Calculations</div>
                            <div style="font-size:12px; margin-top:2px;">Risk analytics will populate automatically when policy premium calculations are generated.</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    st.markdown("""
                    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:32px; text-align:center; color:#64748B;">
                        <div style="font-size:28px; margin-bottom:6px;">📊</div>
                        <div style="font-weight:700; color:#334155; font-size:14px;">No Premium Risk Calculations</div>
                        <div style="font-size:12px; margin-top:2px;">Risk analytics will populate automatically when policy premium calculations are generated.</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_risk:
                st.markdown("""
                <div style="font-size:15px; font-weight:800; color:#0F172A; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                    <span>🛡️</span> Risk & Policy Engagement
                </div>
                """, unsafe_allow_html=True)
                try:
                    risk_df = run_360_sql(f"""
                        SELECT POLICY_ID, POLICY_TYPE, RISK_CATEGORY, RISK_SCORE,
                               REVENUE_AT_RISK, CHURN_PROBABILITY, RISK_DRIVERS,
                               COMPLAINTS_COUNT, MISSED_PAYMENTS, DAYS_SINCE_CONTACT,
                               RECOMMENDED_ACTION, PRIORITY
                        FROM INSURANCE_MGMT_SYSTEM.RISK.AT_RISK_POLICIES
                        WHERE CUSTOMER_ID = '{selected}'
                        ORDER BY RISK_SCORE DESC
                    """)
                    if not risk_df.empty:
                        for _, r in risk_df.iterrows():
                            p_id = r.get('POLICY_ID', 'N/A')
                            r_cat = r.get('RISK_CATEGORY', 'General')
                            r_score = float(r.get('RISK_SCORE', 0.0)) if pd.notnull(r.get('RISK_SCORE')) else 0.0
                            rev_risk = float(r.get('REVENUE_AT_RISK', 0.0)) if pd.notnull(r.get('REVENUE_AT_RISK')) else 0.0
                            drivers = r.get('RISK_DRIVERS', 'N/A')
                            complaints = r.get('COMPLAINTS_COUNT', 0)
                            missed = r.get('MISSED_PAYMENTS', 0)
                            days_cnt = r.get('DAYS_SINCE_CONTACT', 0)
                            rec_act = r.get('RECOMMENDED_ACTION', 'N/A')
                            prio = r.get('PRIORITY', 'Normal')

                            with st.expander(f"{p_id} — {r_cat} (Risk Score: {r_score:.2f})"):
                                st.markdown(f"""
                                **Revenue at Risk:** ${rev_risk:,.0f}  
                                **Risk Drivers:** {drivers}  
                                **Complaints Count:** {complaints} | **Missed Payments:** {missed}  
                                **Days Since Last Contact:** {days_cnt}  
                                **Recommended Action:** {rec_act}  
                                **Action Priority:** {prio}
                                """)
                    else:
                        st.markdown("""
                        <div style="background:#F0FDF4; border:1px solid #DCFCE7; border-radius:8px; padding:20px; text-align:center; color:#166534;">
                            <div style="font-size:24px; margin-bottom:4px;">✓</div>
                            <div style="font-weight:700; font-size:14px;">No At-Risk Policies Identified</div>
                            <div style="font-size:12px; color:#15803D; margin-top:2px;">All active customer policies maintain standard risk monitoring metrics.</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    st.markdown("""
                    <div style="background:#F0FDF4; border:1px solid #DCFCE7; border-radius:8px; padding:20px; text-align:center; color:#166534;">
                        <div style="font-size:24px; margin-bottom:4px;">✓</div>
                        <div style="font-weight:700; font-size:14px;">No At-Risk Policies Identified</div>
                        <div style="font-size:12px; color:#15803D; margin-top:2px;">All active customer policies maintain standard risk monitoring metrics.</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ──────────────────────────────────────────────────
            # Section 9: Fraud Alert Details
            # ──────────────────────────────────────────────────
            if fraud_cnt > 0:
                st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div style="font-size:15px; font-weight:800; color:#0F172A; margin-bottom:10px; display:flex; align-items:center; gap:6px;">
                    <span>🚨</span> Fraud Investigation Alert Details
                </div>
                """, unsafe_allow_html=True)
                try:
                    fraud_df = run_360_sql(f"""
                        SELECT ALERT_ID, CLAIM_ID, FRAUD_TYPE, CONFIDENCE_SCORE,
                               ALERT_STATUS, INVESTIGATION_NOTES, RESOLUTION,
                               AMOUNT_SAVED, ALERT_DATE
                        FROM INSURANCE_MGMT_SYSTEM.ANALYTICS.FRAUD_ALERTS
                        WHERE CUSTOMER_ID = '{selected}'
                        ORDER BY ALERT_DATE DESC
                    """)
                    if not fraud_df.empty:
                        st.dataframe(fraud_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No detailed fraud alert records found.")
                except Exception:
                    st.info("No detailed fraud alert records found.")

            # ──────────────────────────────────────────────────
            # Section 10: AI Retention Strategy (Agent-Powered)
            # ──────────────────────────────────────────────────
            # ── Retention Strategy Dialog ──
            @st.dialog("AI Retention Strategy", width="small")
            def _show_retention_dialog():
                import html as _html

                cust_data = st.session_state.get("retention_dialog_customer", {})
                cust_name = cust_data.get("CUSTOMER_NAME", "Unknown")
                if not cust_data:
                    st.warning("Select a customer first.")
                    return

                churn_prob = cust_data.get('MAX_CHURN_PROBABILITY', 0)
                try:
                    churn_val = float(churn_prob) if churn_prob != 'N/A' else 0
                except Exception:
                    churn_val = 0
                if churn_val >= 0.70:
                    status_color = "#DC2626"; status_text = "High Churn Risk"; status_bg = "#FEF2F2"; status_border = "#FECACA"
                elif churn_val >= 0.40:
                    status_color = "#D97706"; status_text = "Moderate Risk"; status_bg = "#FFFBEB"; status_border = "#FDE68A"
                else:
                    status_color = "#059669"; status_text = "Low Risk"; status_bg = "#ECFDF5"; status_border = "#A7F3D0"

                _safe_income = float(cust_data.get('ANNUAL_INCOME', 0) or 0)
                _safe_premium = float(cust_data.get('TOTAL_PREMIUM', 0) or 0)
                _safe_rev_risk = float(cust_data.get('TOTAL_REVENUE_AT_RISK', 0) or 0)

                customer_context = (
                    f"Customer: {cust_name}, Age: {cust_data.get('AGE', 'N/A')}, "
                    f"Tenure: {cust_data.get('TENURE_YEARS', 'N/A')} years, "
                    f"Annual Income: ${_safe_income:,.0f}, Total Premium: ${_safe_premium:,.0f}, "
                    f"Churn Probability: {churn_prob}, Risk Score: {cust_data.get('MAX_RISK_SCORE', 'N/A')}, "
                    f"Revenue at Risk: ${_safe_rev_risk:,.0f}, "
                    f"Top Risk Factor: {cust_data.get('TOP_RISK_FACTOR', 'N/A')}, "
                    f"Claims Filed: {cust_data.get('CLAIM_COUNT', 0)}, "
                    f"Retention Offer: {cust_data.get('RETENTION_OFFER', 'N/A')}"
                )

                st.markdown(f"""
                <style>
                    [data-testid="stDialog"] > div > div {{ max-width: 600px !important; }}
                    .ret-chat-header {{ display:flex; align-items:center; gap:12px; padding-bottom:12px; margin-bottom:4px; border-bottom:1px solid #F1F5F9; }}
                    .ret-chat-avatar {{ width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#7C3AED,#A855F7); display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
                    .ret-chat-avatar svg {{ stroke:white; }}
                    .ret-chat-name {{ font-size:15px; font-weight:700; color:#0F172A; }}
                    .ret-chat-tag {{ font-size:11px; color:#64748B; }}
                    .ret-chat-status {{ display:inline-flex; align-items:center; gap:6px; font-size:11px; font-weight:600; padding:3px 10px; border-radius:12px; margin-left:auto; background:{status_bg}; border:1px solid {status_border}; color:{status_color}; }}
                    .ret-chat-status-dot {{ width:6px; height:6px; border-radius:50%; background:{status_color}; display:inline-block; }}
                    .ret-chat-context {{ background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; margin:8px 0 4px 0; font-size:11px; color:#64748B; }}
                    .ret-chat-context b {{ color:#334155; }}
                    .ret-msg-ai {{ background:linear-gradient(135deg,#FDF4FF,#FAF5FF); border:1px solid #E9D5FF; border-radius:12px 12px 12px 2px; padding:12px 16px; margin:6px 0; font-size:13px; color:#1E293B; line-height:1.7; }}
                    .ret-msg-user {{ background:linear-gradient(135deg,#7C3AED,#6D28D9); color:#FFFFFF; border-radius:12px 12px 2px 12px; padding:10px 16px; margin:6px 0 6px auto; font-size:13px; line-height:1.5; max-width:85%; text-align:right; width:fit-content; margin-left:auto; }}
                    .ret-msg-ai-label {{ font-size:10px; font-weight:600; color:#64748B; margin-bottom:4px; display:flex; align-items:center; gap:4px; }}
                    .ret-msg-user-label {{ font-size:10px; font-weight:600; color:#94A3B8; margin-bottom:4px; text-align:right; }}
                </style>
                <div class="ret-chat-header">
                    <div class="ret-chat-avatar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    </div>
                    <div>
                        <div class="ret-chat-name">AI Retention Strategy</div>
                        <div class="ret-chat-tag">Personalized retention for {_html.escape(cust_name)}</div>
                    </div>
                    <div class="ret-chat-status">
                        <span class="ret-chat-status-dot"></span>
                        {status_text}
                    </div>
                </div>
                <div class="ret-chat-context">
                    Analyzing <b>{_html.escape(cust_name)}</b> &mdash;
                    Churn: <b>{churn_prob}</b> &middot;
                    Revenue at Risk: <b>${_safe_rev_risk:,.0f}</b> &middot;
                    Premium: <b>${_safe_premium:,.0f}</b>
                </div>
                """, unsafe_allow_html=True)

                if "retention_chat_history" not in st.session_state:
                    st.session_state["retention_chat_history"] = []

                if not st.session_state["retention_chat_history"]:
                    with st.spinner("Generating personalized retention strategy..."):
                        try:
                            initial_prompt = (
                                f"Generate a detailed, personalized retention strategy for this insurance customer. "
                                f"{customer_context}. "
                                f"Provide: 1) Risk assessment summary, "
                                f"2) Personalized retention actions ranked by priority, "
                                f"3) Recommended offer/discount strategy, "
                                f"4) Expected revenue impact if retained vs churned. Keep it concise."
                            )
                            initial_response = sf.ask_intelligence_agent(initial_prompt)
                        except Exception as e:
                            initial_response = f"Unable to generate strategy: {e}"
                    st.session_state["retention_chat_history"].append({"role": "ai", "content": initial_response})

                for msg in st.session_state["retention_chat_history"]:
                    safe_content = _html.escape(str(msg["content"])).replace("\n", "<br>")
                    if msg["role"] == "ai":
                        st.markdown(
                            '<div class="ret-msg-ai-label">'
                            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>'
                            ' Retention Strategist</div>'
                            f'<div class="ret-msg-ai">{safe_content}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="ret-msg-user-label">You</div>'
                            f'<div class="ret-msg-user">{safe_content}</div>',
                            unsafe_allow_html=True
                        )

                if len(st.session_state["retention_chat_history"]) <= 2:
                    chip_cols = st.columns(3)
                    suggestions = [
                        "What discount to offer?",
                        "Revenue impact analysis?",
                        "Compare to similar customers?"
                    ]
                    for i, sug in enumerate(suggestions):
                        with chip_cols[i]:
                            if st.button(sug, key=f"ret_chip_{i}", use_container_width=True):
                                st.session_state["retention_chat_history"].append({"role": "user", "content": sug})
                                with st.spinner("Thinking..."):
                                    try:
                                        follow_up_prompt = (
                                            f"Context: {customer_context}. "
                                            f"Previous conversation: {st.session_state['retention_chat_history'][-2]['content'][:300] if len(st.session_state['retention_chat_history']) >= 2 else 'Initial strategy'}. "
                                            f"User question: {sug}. Provide a concise, focused answer."
                                        )
                                        follow_response = sf.ask_intelligence_agent(follow_up_prompt)
                                    except Exception as e:
                                        follow_response = f"Error: {e}"
                                st.session_state["retention_chat_history"].append({"role": "ai", "content": follow_response})
                                st.rerun()

                user_question = st.chat_input("Ask about retention strategy...", key="ret_chat_input")
                if user_question:
                    st.session_state["retention_chat_history"].append({"role": "user", "content": user_question})
                    recent_context = ""
                    for m in st.session_state["retention_chat_history"][-4:]:
                        role_label = "Assistant" if m["role"] == "ai" else "User"
                        recent_context += f"{role_label}: {m['content'][:300]}\n"
                    with st.spinner("Thinking..."):
                        try:
                            follow_up_prompt = (
                                f"You are an AI customer retention expert. Customer context: {customer_context}. "
                                f"Recent conversation:\n{recent_context}\n"
                                f"User asks: {user_question}\n"
                                f"Provide a concise, professional answer focused on this customer's retention."
                            )
                            follow_response = sf.ask_intelligence_agent(follow_up_prompt)
                        except Exception as e:
                            follow_response = f"Error: {e}"
                    st.session_state["retention_chat_history"].append({"role": "ai", "content": follow_response})
                    st.rerun()

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="card-panel">
                <div class="panel-header">
                    <div class="panel-header-title">
                        <span>🤖 AI-Powered Retention Strategy</span>
                    </div>
                    <div class="panel-header-badge">Intelligence Assistant</div>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"🧠 Generate Retention Strategy for {row.get('CUSTOMER_NAME', selected)}", use_container_width=True, type="primary", key="retention_agent_btn"):
                cust_dict = row.to_dict() if hasattr(row, 'to_dict') else dict(row)
                st.session_state["retention_dialog_customer"] = cust_dict
                st.session_state.pop("retention_chat_history", None)
                st.session_state["show_retention_dialog"] = True

            if st.session_state.get("show_retention_dialog", False):
                _show_retention_dialog()

            st.markdown("</div>", unsafe_allow_html=True)

