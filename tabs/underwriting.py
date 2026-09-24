import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import snowflake_utils as sf
from components.helpers import _typewriter, render_snowflake_error

def render():

    # ── Underwriting-specific CSS ──
    st.markdown("""
    <style>
    .uw-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0EA5E9;
        border-radius: 10px;
        padding: 20px 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .uw-kpi-card:hover { box-shadow: 0 6px 20px rgba(14,165,233,0.14); transform: translateY(-2px); }
    .uw-kpi-label { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #0EA5E9; margin-bottom: 4px; }
    .uw-kpi-value { font-size: 28px; font-weight: 800; color: #0F172A; line-height: 1.2; }
    .uw-kpi-delta { font-size: 12px; font-weight: 600; margin-top: 6px; }
    .uw-kpi-delta.positive { color: #10B981; }
    .uw-kpi-delta.neutral { color: #0EA5E9; }

    .uw-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 26px;
        min-height: 100px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }
    .uw-tile:hover { box-shadow: 0 4px 18px rgba(0,0,0,0.09); }
    .uw-tile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 14px;
        margin-bottom: 16px;
        border-bottom: 1px solid #F1F5F9;
    }
    .uw-tile-title { font-size: 15px; font-weight: 700; color: #0F172A; display: flex; align-items: center; gap: 8px; }
    .uw-tile-badge {
        font-size: 11px; font-weight: 600; font-family: 'JetBrains Mono', monospace;
        background: #F1F5F9; color: #475569; padding: 4px 10px; border-radius: 6px;
        border: 1px solid #E2E8F0;
    }

    /* ── Enterprise Copilot Design System ── */
    @keyframes copilot-pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); } 50% { box-shadow: 0 0 0 8px rgba(16,185,129,0); } }
    @keyframes copilot-glow { 0%,100% { box-shadow: 0 4px 24px rgba(37,99,235,0.08); } 50% { box-shadow: 0 4px 32px rgba(37,99,235,0.18); } }
    @keyframes flow-dot { 0% { opacity:0.3; } 50% { opacity:1; } 100% { opacity:0.3; } }
    @keyframes fade-up { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
    @keyframes copilot-typing { 0%,80%,100% { opacity:.3; transform:scale(.7); } 40% { opacity:1; transform:scale(1); } }

    .cp-header-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFF 100%);
        border: 1px solid #E2E8F0; border-radius: 16px;
        padding: 28px 32px; margin-bottom: 20px;
        box-shadow: 0 2px 16px rgba(37,99,235,0.06);
        animation: copilot-glow 4s ease-in-out infinite;
    }
    .cp-header-top { display:flex; justify-content:space-between; align-items:center; }
    .cp-header-left { display:flex; align-items:center; gap:16px; }
    .cp-logo {
        width:48px; height:48px; border-radius:14px;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        display:flex; align-items:center; justify-content:center;
        box-shadow: 0 4px 12px rgba(37,99,235,0.25);
    }
    .cp-header-title { font-size:20px; font-weight:800; color:#0F172A; letter-spacing:-0.3px; }
    .cp-header-subtitle { font-size:13px; color:#64748B; margin-top:2px; }
    .cp-status-badge {
        display:flex; align-items:center; gap:8px;
        background:#ECFDF5; border:1px solid #A7F3D0; border-radius:20px;
        padding:6px 16px; font-size:12px; font-weight:600; color:#059669;
    }
    .cp-status-dot { width:8px; height:8px; border-radius:50%; background:#10B981; animation: copilot-pulse 2s infinite; }

    .cp-feature-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:20px; }
    .cp-feature-card {
        background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
        padding:20px; transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        cursor:default;
    }
    .cp-feature-card:hover { border-color:#2563EB; box-shadow:0 8px 24px rgba(37,99,235,0.12); transform:translateY(-3px); }
    .cp-feature-icon {
        width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center;
        margin-bottom:12px;
    }
    .cp-feature-icon.blue { background:#EFF6FF; }
    .cp-feature-icon.purple { background:#F5F3FF; }
    .cp-feature-icon.emerald { background:#ECFDF5; }
    .cp-feature-title { font-size:14px; font-weight:700; color:#0F172A; margin-bottom:4px; }
    .cp-feature-desc { font-size:12px; color:#64748B; line-height:1.6; }

    .cp-workflow-section { margin:24px 0; }
    .cp-section-title {
        font-size:16px; font-weight:700; color:#0F172A; margin-bottom:16px;
        display:flex; align-items:center; gap:10px;
    }
    .cp-workflow-bar {
        display:flex; align-items:center; justify-content:center; gap:0;
        background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px;
        padding:20px 24px;
    }
    .cp-flow-step {
        display:flex; flex-direction:column; align-items:center; gap:8px;
        min-width:140px; text-align:center;
    }
    .cp-flow-icon {
        width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center;
        border:2px solid #E2E8F0; background:#FFFFFF;
        transition: all 0.3s ease;
    }
    .cp-flow-icon.active { border-color:#2563EB; background:#EFF6FF; box-shadow:0 2px 8px rgba(37,99,235,0.15); }
    .cp-flow-label { font-size:11px; font-weight:600; color:#475569; }
    .cp-flow-connector { display:flex; align-items:center; gap:4px; padding:0 8px; }
    .cp-flow-dot { width:6px; height:6px; border-radius:50%; background:#CBD5E1; }
    .cp-flow-dot.d1 { animation: flow-dot 1.5s 0s infinite; }
    .cp-flow-dot.d2 { animation: flow-dot 1.5s 0.3s infinite; }
    .cp-flow-dot.d3 { animation: flow-dot 1.5s 0.6s infinite; }

    .cp-applicant-section {
        background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px;
        padding:24px 28px; margin-bottom:20px;
        box-shadow:0 2px 12px rgba(0,0,0,0.04);
    }
    .cp-details-card {
        background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px;
        padding:16px 20px; margin-top:12px;
    }
    .cp-detail-row {
        display:flex; justify-content:space-between; padding:8px 0;
        border-bottom:1px solid #F1F5F9; font-size:13px;
    }
    .cp-detail-row:last-child { border-bottom:none; }
    .cp-detail-label { color:#64748B; }
    .cp-detail-value { font-weight:700; color:#0F172A; font-family:'JetBrains Mono',monospace; font-size:12px; }
    .cp-cta-btn {
        display:flex; align-items:center; justify-content:center; gap:10px;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color:#FFFFFF; border:none; border-radius:14px;
        padding:18px 32px; font-size:15px; font-weight:700; letter-spacing:0.3px;
        cursor:pointer; width:100%;
        box-shadow: 0 4px 16px rgba(37,99,235,0.3);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    }
    .cp-cta-btn:hover { box-shadow:0 8px 24px rgba(37,99,235,0.4); transform:translateY(-2px); }

    .cp-results-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:20px 0; }
    .cp-metric-card {
        background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
        padding:20px; text-align:center;
        box-shadow:0 2px 8px rgba(0,0,0,0.04);
        animation: fade-up 0.5s ease-out;
    }
    .cp-metric-card.green { border-left:4px solid #10B981; }
    .cp-metric-card.amber { border-left:4px solid #F59E0B; }
    .cp-metric-card.red { border-left:4px solid #EF4444; }
    .cp-metric-card.blue { border-left:4px solid #2563EB; }
    .cp-metric-label { font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px; }
    .cp-metric-value { font-size:28px; font-weight:800; font-family:'JetBrains Mono',monospace; }
    .cp-metric-sub { font-size:11px; color:#94A3B8; margin-top:4px; }

    .cp-decision-banner {
        border-radius:16px; padding:28px 32px; margin:20px 0;
        display:flex; align-items:center; gap:24px;
        box-shadow:0 4px 20px rgba(0,0,0,0.06);
        animation: fade-up 0.6s ease-out;
    }
    .cp-decision-banner.approve { background:linear-gradient(135deg,#ECFDF5,#D1FAE5); border:2px solid #6EE7B7; }
    .cp-decision-banner.review { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border:2px solid #FCD34D; }
    .cp-decision-banner.decline { background:linear-gradient(135deg,#FEF2F2,#FECACA); border:2px solid #FCA5A5; }
    .cp-decision-indicator {
        width:64px; height:64px; border-radius:50%; display:flex; align-items:center; justify-content:center;
        flex-shrink:0;
    }
    .cp-decision-indicator.green { background:linear-gradient(135deg,#34D399,#059669); box-shadow:0 4px 16px rgba(5,150,105,0.3); }
    .cp-decision-indicator.yellow { background:linear-gradient(135deg,#FBBF24,#D97706); box-shadow:0 4px 16px rgba(217,119,6,0.3); }
    .cp-decision-indicator.red { background:linear-gradient(135deg,#F87171,#DC2626); box-shadow:0 4px 16px rgba(220,38,38,0.3); }
    .cp-decision-text { flex:1; }
    .cp-decision-title { font-size:20px; font-weight:800; letter-spacing:0.5px; }
    .cp-decision-action { font-size:13px; margin-top:4px; opacity:0.85; }
    .cp-decision-meta { font-size:12px; color:#64748B; margin-top:8px; display:flex; gap:16px; flex-wrap:wrap; }
    .cp-decision-meta b { color:#334155; }

    .cp-binder-card {
        background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px;
        padding:28px 32px; margin:20px 0;
        box-shadow:0 2px 16px rgba(0,0,0,0.04);
        animation: fade-up 0.7s ease-out;
    }
    .cp-binder-header {
        display:flex; align-items:center; justify-content:space-between;
        padding-bottom:16px; margin-bottom:20px; border-bottom:2px solid #F1F5F9;
    }
    .cp-binder-title { font-size:16px; font-weight:700; color:#0F172A; display:flex; align-items:center; gap:10px; }
    .cp-binder-badge {
        font-size:10px; font-weight:700; background:#EFF6FF; color:#2563EB;
        padding:4px 12px; border-radius:16px; letter-spacing:0.5px;
    }
    .cp-binder-section { margin-bottom:16px; }
    .cp-binder-section-title {
        font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase;
        letter-spacing:0.8px; margin-bottom:8px;
        padding-bottom:6px; border-bottom:1px solid #F1F5F9;
    }
    .cp-binder-row {
        display:flex; justify-content:space-between; padding:6px 0; font-size:13px;
    }
    .cp-binder-label { color:#64748B; }
    .cp-binder-value { font-weight:600; color:#0F172A; }

    .cp-copilot-panel {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFF 100%);
        border:1px solid #E2E8F0; border-radius:16px;
        padding:20px; margin:20px 0;
        box-shadow:0 2px 16px rgba(37,99,235,0.06);
    }
    .cp-copilot-header-bar {
        display:flex; align-items:center; gap:10px;
        padding-bottom:12px; margin-bottom:14px; border-bottom:1px solid #EFF6FF;
    }
    .cp-copilot-avatar {
        width:32px; height:32px; border-radius:10px;
        background:linear-gradient(135deg,#2563EB,#7C3AED);
        display:flex; align-items:center; justify-content:center;
    }
    .cp-copilot-name { font-size:14px; font-weight:700; color:#0F172A; }
    .cp-copilot-tag { font-size:10px; color:#64748B; }
    .cp-chat-bubble {
        background:#F0F4FF; border:1px solid #DBEAFE; border-radius:12px;
        padding:12px 16px; margin-bottom:10px; font-size:13px; color:#1E293B; line-height:1.6;
        animation: fade-up 0.4s ease-out;
    }
    .cp-chat-bubble.ai { border-left:3px solid #2563EB; }
    .cp-chat-action {
        display:inline-flex; align-items:center; gap:6px;
        background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px;
        padding:6px 14px; font-size:12px; font-weight:600; color:#2563EB;
        cursor:pointer; transition:all 0.2s;
        margin-right:8px; margin-top:6px;
    }
    .cp-chat-action:hover { background:#EFF6FF; border-color:#2563EB; }
    .cp-typing-indicator { display:flex; gap:4px; padding:8px 0; }
    .cp-typing-dot { width:6px; height:6px; border-radius:50%; background:#2563EB; }
    .cp-typing-dot:nth-child(1) { animation:copilot-typing 1.4s 0s infinite; }
    .cp-typing-dot:nth-child(2) { animation:copilot-typing 1.4s 0.2s infinite; }
    .cp-typing-dot:nth-child(3) { animation:copilot-typing 1.4s 0.4s infinite; }

    .uw-info-banner {
        background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px;
        padding: 14px 20px; margin-bottom: 16px; font-size: 13px; color: #1E40AF; line-height: 1.6;
    }
    .uw-info-banner b { color: #1D4ED8; }

    .uw-decision-card {
        border-radius: 16px; padding: 40px 24px; text-align: center; margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    .uw-decision-card.approve { background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border: 2px solid #6EE7B7; }
    .uw-decision-card.review { background: linear-gradient(135deg, #FFFBEB, #FEF3C7); border: 2px solid #FCD34D; }
    .uw-decision-card.decline { background: linear-gradient(135deg, #FEF2F2, #FECACA); border: 2px solid #FCA5A5; }
    .uw-decision-label { font-size: 18px; font-weight: 800; letter-spacing: 1.5px; margin-top: 14px; }
    .uw-decision-score { font-size: 34px; font-weight: 800; margin-top: 4px; }
    .uw-decision-action { font-size: 13px; margin-top: 10px; opacity: 0.85; }
    .uw-decision-meta { font-size: 12px; color: #64748B; margin-top: 12px; }

    .uw-sphere {
        width: 56px; height: 56px; border-radius: 50%; margin: 0 auto;
        box-shadow: inset -8px -8px 16px rgba(0,0,0,0.15), inset 6px 6px 12px rgba(255,255,255,0.6), 0 4px 12px rgba(0,0,0,0.10);
    }
    .uw-sphere.green { background: radial-gradient(circle at 35% 35%, #6EE7B7, #059669); }
    .uw-sphere.yellow { background: radial-gradient(circle at 35% 35%, #FDE68A, #D97706); }
    .uw-sphere.red { background: radial-gradient(circle at 35% 35%, #FCA5A5, #DC2626); }

    /* ── Landing Page Tile Cards ── */
    .uw-landing-title {
        font-size: 20px; font-weight: 800; color: #0F172A;
        text-align: center; margin-bottom: 2px;
    }
    .uw-landing-subtitle {
        font-size: 12px; color: #64748B; text-align: center;
        margin-bottom: 18px; max-width: 540px; margin-left: auto; margin-right: auto;
    }
    .uw-tile-card {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
    }
    .uw-tile-card:hover {
        box-shadow: 0 8px 28px rgba(14,165,233,0.15);
        transform: translateY(-3px);
        border-color: #0EA5E9;
    }
    .uw-tile-card-body {
        padding: 14px 18px 16px 18px;
    }
    .uw-tile-card-title {
        font-size: 14px; font-weight: 800; color: #0F172A;
        margin-bottom: 6px; display: flex; align-items: center; gap: 6px;
    }
    .uw-tile-card-desc {
        font-size: 11.5px; color: #475569; line-height: 1.6; margin-bottom: 10px;
    }
    .uw-tile-card-features {
        display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 0;
    }
    .uw-tile-card-chip {
        font-size: 10px; font-weight: 600; color: #0369A1; background: #E0F2FE;
        padding: 2px 8px; border-radius: 16px; white-space: nowrap;
    }

    .uw-xai-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 26px;
        margin-top: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .uw-xai-tile-header {
        display: flex; align-items: center; gap: 10px;
        padding-bottom: 12px; margin-bottom: 14px; border-bottom: 1px solid #F1F5F9;
    }

    .uw-multiplier-tile {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 26px;
        margin-top: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    .uw-agent-popup-header {
        font-weight: 700; font-size: 14px; color: #6B21A8;
        display: flex; align-items: center; gap: 8px; margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
        <div style="font-size:28px; background:linear-gradient(135deg,#0EA5E9,#0369A1); border-radius:10px; width:42px; height:42px; display:flex; align-items:center; justify-content:center; color:#FFF;">🛡️</div>
        <div>
            <div style="font-size:20px; font-weight:800; color:#0F172A;">Underwriting Workbench</div>
            <div style="font-size:12px; color:#64748B;">Real-time policy book management, risk scoring, and ML-powered automated premium quoting.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sub-page Navigation State ──
    if "uw_subpage" not in st.session_state:
        st.session_state["uw_subpage"] = "landing"

    # ── Back button when inside a sub-page ──
    if st.session_state["uw_subpage"] != "landing":
        if st.button("← Back to Underwriting Workbench", key="uw_back_btn"):
            st.session_state["uw_subpage"] = "landing"
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # LANDING PAGE — Capability Tiles
    # ══════════════════════════════════════════════════════════════════════
    if st.session_state["uw_subpage"] == "landing":
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="uw-landing-title">Underwriting Capabilities</div>
        <div class="uw-landing-subtitle">
            From idea to AI — design, test, and deploy on a single platform.
            Select a capability below to get started.
        </div>
        """, unsafe_allow_html=True)

        tile_col1, tile_col2 = st.columns(2, gap="large")

        with tile_col1:
            st.markdown("""
            <div class="uw-tile-card">
                <div style="width:100%; height:110px; background: linear-gradient(135deg, #0369A1 0%, #0EA5E9 40%, #38BDF8 100%); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>
                    <div style="position:absolute; bottom:-20px; left:-20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.05);"></div>
                    <div style="text-align:center; position:relative; z-index:1;">
                        <div style="font-size:32px; margin-bottom:4px;">📑</div>
                        <div style="font-size:11px; font-weight:700; color:#FFFFFF; letter-spacing:1px; text-transform:uppercase;">Policy Management</div>
                    </div>
                </div>
                <div class="uw-tile-card-body">
                    <div class="uw-tile-card-title">
                        <span>📋</span> Smart Policy Quotation
                    </div>
                    <div class="uw-tile-card-desc">
                        Generate insurance quotations using customer demographics, credit scores, income details,
                        coverage requirements, and underwriting parameters. Users can explore policy books,
                        compare policy tiers, and instantly estimate premiums through an intelligent pricing engine.
                    </div>
                    <div class="uw-tile-card-features">
                        <span class="uw-tile-card-chip">Policy Book Management</span>
                        <span class="uw-tile-card-chip">Policy Search & Filtering</span>
                        <span class="uw-tile-card-chip">Policy Catalog View</span>
                        <span class="uw-tile-card-chip">Premium Estimation</span>
                        <span class="uw-tile-card-chip">Coverage Analysis</span>
                        <span class="uw-tile-card-chip">Risk-Based Pricing</span>
                        <span class="uw-tile-card-chip">Quote Generation</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ Launch Smart Quote Engine", use_container_width=True, type="primary", key="launch_tile_quote"):
                st.session_state["uw_subpage"] = "smart_quote"
                st.rerun()

        with tile_col2:
            st.markdown("""
            <div class="uw-tile-card">
                <div style="width:100%; height:110px; background: linear-gradient(135deg, #6B21A8 0%, #9333EA 40%, #A855F7 100%); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.08);"></div>
                    <div style="position:absolute; bottom:-20px; left:-20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.05);"></div>
                    <div style="text-align:center; position:relative; z-index:1;">
                        <div style="font-size:32px; margin-bottom:4px;">🧠</div>
                        <div style="font-size:11px; font-weight:700; color:#FFFFFF; letter-spacing:1px; text-transform:uppercase;">AI Decisioning</div>
                    </div>
                </div>
                <div class="uw-tile-card-body">
                    <div class="uw-tile-card-title">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> AI Underwriting Copilot & Auto-Binder
                    </div>
                    <div class="uw-tile-card-desc">
                        Leverage AI-driven underwriting intelligence to automatically assess applicant risk,
                        generate underwriting recommendations, explain decisions, and route applications for
                        approval, review, or rejection through an autonomous decisioning engine.
                    </div>
                    <div class="uw-tile-card-features">
                        <span class="uw-tile-card-chip">AI Risk Scoring</span>
                        <span class="uw-tile-card-chip">Automated Decisioning</span>
                        <span class="uw-tile-card-chip">Auto Approval Engine</span>
                        <span class="uw-tile-card-chip">Applicant Risk Assessment</span>
                        <span class="uw-tile-card-chip">Policy Recommendation</span>
                        <span class="uw-tile-card-chip">Underwriting Automation</span>
                        <span class="uw-tile-card-chip">Intelligent Auto-Binding</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch AI Underwriting Copilot", use_container_width=True, type="primary", key="launch_tile_copilot"):
                st.session_state["uw_subpage"] = "ai_copilot"
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUB-PAGE 1: Smart Policy Quotation  &  SUB-PAGE 2: AI Copilot
    # ══════════════════════════════════════════════════════════════════════

    # ── Agent Opinion Dialog ──
    @st.dialog("AI Underwriting Assistant", width="small")
    def _show_agent_opinion_dialog():
        import html as _html

        profile = st.session_state.get("uw_copilot_profile", {})
        decision = st.session_state.get("uw_copilot_decision", {})
        if not profile:
            st.warning("Run the Underwriting Copilot first to load a customer profile.")
            return

        bucket = decision.get("bucket", "")
        score = decision.get("score", 0)
        if bucket == "AUTO_APPROVE":
            status_color = "#059669"; status_text = "Low Risk"; status_bg = "#ECFDF5"; status_border = "#A7F3D0"
        elif bucket == "HUMAN_REVIEW":
            status_color = "#D97706"; status_text = "Moderate Risk"; status_bg = "#FFFBEB"; status_border = "#FDE68A"
        else:
            status_color = "#DC2626"; status_text = "High Risk"; status_bg = "#FEF2F2"; status_border = "#FECACA"

        applicant_context = (
            f"Applicant: {profile.get('FULL_NAME','N/A')}, Age: {profile.get('AGE','N/A')}, "
            f"Credit Score: {profile.get('CREDIT_SCORE','N/A')}, "
            f"Annual Income: ${float(profile.get('ANNUAL_INCOME',0) or 0):,.0f}, "
            f"Policy Type: {profile.get('POLICY_TYPE','N/A')}, Plan Tier: {profile.get('PLAN_TIER','N/A')}, "
            f"Smoking: {profile.get('SMOKING_STATUS','No')}, BMI: {profile.get('BMI','N/A')}, "
            f"Risk Score: {score:.2f}, Decision Bucket: {bucket}, "
            f"Loss Ratio: {profile.get('LOSS_RATIO',0)}, "
            f"ML Predicted Premium: ${float(profile.get('ML_PREDICTED_PREMIUM',0) or 0):,.2f}, "
            f"Fraud Claims: {profile.get('FRAUD_CLAIM_COUNT',0)}, Total Claims: {profile.get('TOTAL_CLAIMS',0)}"
        )

        # CSS for chat UI
        st.markdown(f"""
        <style>
            [data-testid="stDialog"] > div > div {{ max-width: 600px !important; }}
            .chat-header {{
                display:flex; align-items:center; gap:12px;
                padding-bottom:12px; margin-bottom:4px; border-bottom:1px solid #F1F5F9;
            }}
            .chat-avatar {{
                width:36px; height:36px; border-radius:10px;
                background:linear-gradient(135deg,#2563EB,#7C3AED);
                display:flex; align-items:center; justify-content:center; flex-shrink:0;
            }}
            .chat-avatar svg {{ stroke:white; }}
            .chat-name {{ font-size:15px; font-weight:700; color:#0F172A; }}
            .chat-tag {{ font-size:11px; color:#64748B; }}
            .chat-status {{
                display:inline-flex; align-items:center; gap:6px;
                font-size:11px; font-weight:600; padding:3px 10px;
                border-radius:12px; margin-left:auto;
                background:{status_bg}; border:1px solid {status_border}; color:{status_color};
            }}
            .chat-status-dot {{ width:6px; height:6px; border-radius:50%; background:{status_color}; display:inline-block; }}
            .chat-context {{
                background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px;
                padding:10px 14px; margin:8px 0 4px 0; font-size:11px; color:#64748B;
            }}
            .chat-context b {{ color:#334155; }}
            .msg-ai {{
                background:linear-gradient(135deg,#F8FAFF,#F0F4FF); border:1px solid #DBEAFE;
                border-radius:12px 12px 12px 2px; padding:12px 16px; margin:6px 0;
                font-size:13px; color:#1E293B; line-height:1.7;
            }}
            .msg-user {{
                background:linear-gradient(135deg,#2563EB,#1D4ED8); color:#FFFFFF;
                border-radius:12px 12px 2px 12px; padding:10px 16px; margin:6px 0 6px auto;
                font-size:13px; line-height:1.5; max-width:85%; text-align:right;
                width:fit-content; margin-left:auto;
            }}
            .msg-ai-label {{
                font-size:10px; font-weight:600; color:#64748B; margin-bottom:4px;
                display:flex; align-items:center; gap:4px;
            }}
            .msg-user-label {{
                font-size:10px; font-weight:600; color:#94A3B8; margin-bottom:4px; text-align:right;
            }}
        </style>
        <div class="chat-header">
            <div class="chat-avatar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
            </div>
            <div>
                <div class="chat-name">AI Underwriting Assistant</div>
                <div class="chat-tag">Ask me anything about this applicant</div>
            </div>
            <div class="chat-status">
                <span class="chat-status-dot"></span>
                {status_text}
            </div>
        </div>
        <div class="chat-context">
            Reviewing <b>{profile.get('FULL_NAME','N/A')}</b> &mdash;
            Score: <b>{score:.2f}</b> &middot;
            {profile.get('POLICY_TYPE','N/A')} / {profile.get('PLAN_TIER','N/A')} &middot;
            Premium: <b>${float(profile.get('FINAL_PREMIUM',0) or 0):,.0f}</b>
        </div>
        """, unsafe_allow_html=True)

        # Initialize chat history
        if "agent_chat_history" not in st.session_state:
            st.session_state["agent_chat_history"] = []

        # Auto-generate initial opinion if chat is empty
        if not st.session_state["agent_chat_history"]:
            with st.spinner("Analyzing applicant profile..."):
                try:
                    initial_prompt = (
                        f"Provide a concise professional underwriting opinion for this applicant. "
                        f"{applicant_context}. "
                        f"Format as: Risk Assessment (1-2 sentences), Recommendation (approve/review/decline with reason), "
                        f"Premium Note (1 sentence), Key Conditions (bullet points if any). Keep it concise."
                    )
                    initial_response = sf.ask_underwriting_agent(initial_prompt)
                except Exception as e:
                    initial_response = f"Unable to generate initial assessment: {e}"
            st.session_state["agent_chat_history"].append({"role": "ai", "content": initial_response})

        # Render chat messages
        for msg in st.session_state["agent_chat_history"]:
            safe_content = _html.escape(str(msg["content"])).replace("\n", "<br>")
            if msg["role"] == "ai":
                st.markdown(
                    '<div class="msg-ai-label">'
                    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>'
                    ' AI Assistant</div>'
                    f'<div class="msg-ai">{safe_content}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="msg-user-label">You</div>'
                    f'<div class="msg-user">{safe_content}</div>',
                    unsafe_allow_html=True
                )

        # Quick-action suggestion chips (only show when no pending question)
        if len(st.session_state["agent_chat_history"]) <= 2:
            chip_cols = st.columns(3)
            suggestions = [
                "What are the main risk factors?",
                "Is the premium fairly priced?",
                "Any exclusions needed?"
            ]
            for i, sug in enumerate(suggestions):
                with chip_cols[i]:
                    if st.button(sug, key=f"agent_chip_{i}", use_container_width=True):
                        st.session_state["agent_chat_history"].append({"role": "user", "content": sug})
                        with st.spinner("Thinking..."):
                            try:
                                follow_up_prompt = (
                                    f"Context: {applicant_context}. "
                                    f"Previous conversation: {st.session_state['agent_chat_history'][-2]['content'] if len(st.session_state['agent_chat_history']) >= 2 else 'Initial assessment'}. "
                                    f"User question: {sug}. "
                                    f"Provide a concise, focused answer."
                                )
                                follow_response = sf.ask_underwriting_agent(follow_up_prompt)
                            except Exception as e:
                                follow_response = f"Error: {e}"
                        st.session_state["agent_chat_history"].append({"role": "ai", "content": follow_response})
                        st.rerun()

        # Chat input
        user_question = st.chat_input("Ask about this applicant...", key="agent_chat_input")
        if user_question:
            st.session_state["agent_chat_history"].append({"role": "user", "content": user_question})
            recent_context = ""
            for m in st.session_state["agent_chat_history"][-4:]:
                role_label = "Assistant" if m["role"] == "ai" else "User"
                recent_context += f"{role_label}: {m['content'][:300]}\n"
            with st.spinner("Thinking..."):
                try:
                    follow_up_prompt = (
                        f"You are an AI underwriting expert. Applicant context: {applicant_context}. "
                        f"Recent conversation:\n{recent_context}\n"
                        f"User asks: {user_question}\n"
                        f"Provide a concise, professional answer focused on this applicant."
                    )
                    follow_response = sf.ask_underwriting_agent(follow_up_prompt)
                except Exception as e:
                    follow_response = f"Error: {e}"
            st.session_state["agent_chat_history"].append({"role": "ai", "content": follow_response})
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUB-PAGE 1: Smart Policy Quotation
    # ══════════════════════════════════════════════════════════════════════
    if st.session_state["uw_subpage"] == "smart_quote":

        # ── Live Data Fetch ──
        df_policies = pd.DataFrame()
        try:
            df_policies = sf.get_policies_data()
        except Exception as e:
            render_snowflake_error(e, "Snowflake Policy Book")

        # =====================================================================
        # SECTION 1: KPI CARDS ROW
        # =====================================================================
        if not df_policies.empty:
            total_policies = len(df_policies)
            active_count = len(df_policies[df_policies["STATUS"].astype(str).str.upper() == "ACTIVE"]) if "STATUS" in df_policies.columns else total_policies
            if "PREMIUM" in df_policies.columns:
                total_premium = pd.to_numeric(df_policies["PREMIUM"], errors="coerce").sum()
                avg_premium = pd.to_numeric(df_policies["PREMIUM"], errors="coerce").mean()
            else:
                total_premium = 0
                avg_premium = 0

            active_pct = (active_count / total_policies * 100) if total_policies > 0 else 0

            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.markdown(f"""
                <div class="uw-kpi-card">
                    <div class="uw-kpi-label">TOTAL POLICIES</div>
                    <div class="uw-kpi-value">{total_policies:,}</div>
                    <div class="uw-kpi-delta positive">&#9650; 4.2% from last cycle</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"""
                <div class="uw-kpi-card">
                    <div class="uw-kpi-label">ACTIVE BOOK</div>
                    <div class="uw-kpi-value">{active_count:,}</div>
                    <div class="uw-kpi-delta neutral">&#9679; {active_pct:.0f}% active coverage</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col3:
                st.markdown(f"""
                <div class="uw-kpi-card">
                    <div class="uw-kpi-label">TOTAL PREMIUM VOLUME</div>
                    <div class="uw-kpi-value">${total_premium:,.0f}</div>
                    <div class="uw-kpi-delta positive">&#9650; 8.1% YoY growth</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi_col4:
                st.markdown(f"""
                <div class="uw-kpi-card">
                    <div class="uw-kpi-label">AVERAGE PREMIUM</div>
                    <div class="uw-kpi-value">${avg_premium:,.2f}</div>
                    <div class="uw-kpi-delta neutral">&#9679; Benchmark within target</div>
                </div>
                """, unsafe_allow_html=True)

        # =====================================================================
        # SECTION 2: POLICY BOOK (left) + QUOTE A NEW POLICY (right)
        # =====================================================================
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        col_left, col_right = st.columns([1.15, 0.85])

        with col_left:
            with st.container(border=True):
                st.markdown("""
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid #F1F5F9;">
                    <div style="font-size:15px; font-weight:700; color:#0F172A; display:flex; align-items:center; gap:8px;"><span>📋</span> Policy Book</div>
                    <span style="font-size:11px; font-weight:600; font-family:monospace; background:#F1F5F9; color:#475569; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">Policy Records</span>
                </div>
                """, unsafe_allow_html=True)

                if not df_policies.empty:
                    filter_col1, filter_col2 = st.columns([1, 1])
                    with filter_col1:
                        search_term = st.text_input("Search", "", placeholder="e.g. POL-001 or Auto", label_visibility="collapsed", key="uw_search")
                    with filter_col2:
                        types = ["All Types"] + list(df_policies["TYPE"].dropna().unique()) if "TYPE" in df_policies.columns else ["All Types"]
                        selected_type = st.selectbox("Filter Type", types, label_visibility="collapsed", key="uw_type_filter")

                    filtered_df = df_policies.copy()
                    if search_term:
                        filtered_df = filtered_df[filtered_df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
                    if selected_type != "All Types" and "TYPE" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["TYPE"] == selected_type]

                    display_cols = [c for c in ["POLICY_ID", "TYPE", "TIER", "PREMIUM", "STATUS"] if c in filtered_df.columns]
                    st.dataframe(filtered_df[display_cols] if display_cols else filtered_df, use_container_width=True, height=340, hide_index=True)
                    st.caption(f"Showing {len(filtered_df)} of {len(df_policies)} rows")
                else:
                    st.info("No policy records returned from Snowflake.")

        with col_right:
            with st.container(border=True):
                st.markdown("""
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid #F1F5F9;">
                    <div style="font-size:15px; font-weight:700; color:#0F172A; display:flex; align-items:center; gap:8px;"><span>⚡</span> Quote a New Policy</div>
                    <span style="font-size:11px; font-weight:600; font-family:monospace; background:#F1F5F9; color:#475569; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">ML Model Input</span>
                </div>
                """, unsafe_allow_html=True)

                with st.form("quote_form"):
                    qf_c1, qf_c2 = st.columns(2)
                    with qf_c1:
                        age = st.slider("Applicant Age", 18, 85, 35)
                        credit = st.slider("Credit Score", 300, 850, 700)
                    with qf_c2:
                        income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, value=60000, step=5000)
                        coverage = st.number_input("Coverage Amount ($)", min_value=10000, max_value=2000000, value=250000, step=25000)
                    submitted = st.form_submit_button("⚡ Estimate Premium", use_container_width=True, type="primary")

                if submitted:
                    try:
                        est_price = sf.estimate_premium(age, income, credit, coverage)
                        risk_tier = "Low Risk" if credit >= 720 else ("Moderate Risk" if credit >= 620 else "Elevated Risk")
                        tier_color = "#10B981" if credit >= 720 else ("#F59E0B" if credit >= 620 else "#EF4444")
                        st.markdown(f"""
                        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:16px; text-align:center; margin-top:8px;">
                            <div style="font-size:12px; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Estimated Annual Premium</div>
                            <div style="font-size:28px; font-weight:800; color:#0F172A; margin:4px 0;">${est_price:,.2f}</div>
                            <span style="background:{tier_color}; color:#FFF; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:700;">{risk_tier}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        render_snowflake_error(e, "Live Prediction Model")

    # SUB-PAGE 2: AI Underwriting Copilot & Auto-Binder
    if st.session_state["uw_subpage"] == "ai_copilot":

        # === SVG Icon Definitions ===
        _svg_shield = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
        _svg_user_search = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="7" r="4"/><path d="M10.3 15H7a4 4 0 0 0-4 4v2"/><circle cx="17" cy="17" r="3"/><path d="m21 21-1.9-1.9"/></svg>'
        _svg_brain = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>'
        _svg_file_check = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><path d="m9 15 2 2 4-4"/></svg>'
        _svg_activity = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
        _svg_database = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
        _svg_scan = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M7 12h10"/></svg>'
        _svg_check_circle = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
        _svg_zap = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        _svg_clipboard = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>'
        _svg_download = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
        _svg_sparkles = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>'
        _svg_message = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
        _svg_bar_chart = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>'
        _svg_trending = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'

        # =====================================================================
        # SECTION 3A: HEADER CARD
        # =====================================================================
        st.markdown(f"""
        <div class="cp-header-card">
            <div class="cp-header-top">
                <div class="cp-header-left">
                    <div class="cp-logo">{_svg_shield}</div>
                    <div>
                        <div class="cp-header-title">AI Underwriting Copilot &amp; Auto-Binder</div>
                        <div class="cp-header-subtitle">AI-Powered Risk Assessment &amp; Automated Policy Decisioning</div>
                    </div>
                </div>
                <div class="cp-status-badge">
                    <div class="cp-status-dot"></div>
                    AI Engine Active
                </div>
            </div>
            <div class="cp-feature-grid">
                <div class="cp-feature-card">
                    <div class="cp-feature-icon blue">{_svg_user_search}</div>
                    <div class="cp-feature-title">Customer Risk Analysis</div>
                    <div class="cp-feature-desc">Aggregates data from 5 Snowflake tables including credit, demographics, and claims history for holistic risk profiling.</div>
                </div>
                <div class="cp-feature-card">
                    <div class="cp-feature-icon purple">{_svg_brain}</div>
                    <div class="cp-feature-title">ML Risk Prediction</div>
                    <div class="cp-feature-desc">Machine learning models score applicant risk using actuarial multipliers and predictive analytics in real time.</div>
                </div>
                <div class="cp-feature-card">
                    <div class="cp-feature-icon emerald">{_svg_file_check}</div>
                    <div class="cp-feature-title">Automated Binder Generation</div>
                    <div class="cp-feature-desc">Auto-routes decisions to Approve, Review, or Decline buckets and generates policy binder documents instantly.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =====================================================================
        # SECTION 3B: AI DECISION PROCESS VISUALIZATION
        # =====================================================================
        has_results = "uw_copilot_decision" in st.session_state and "uw_copilot_profile" in st.session_state
        step_active = ["active" if has_results else "", "active" if has_results else "", "active" if has_results else "", "active" if has_results else ""]

        st.markdown(f"""
        <div class="cp-workflow-bar">
            <div class="cp-flow-step">
                <div class="cp-flow-icon {step_active[0]}">{_svg_user_search.replace('stroke="#2563EB"', 'stroke="#2563EB"')}</div>
                <div class="cp-flow-label">Customer Selected</div>
            </div>
            <div class="cp-flow-connector"><div class="cp-flow-dot d1"></div><div class="cp-flow-dot d2"></div><div class="cp-flow-dot d3"></div></div>
            <div class="cp-flow-step">
                <div class="cp-flow-icon {step_active[1]}">{_svg_database}</div>
                <div class="cp-flow-label">Data Collection</div>
            </div>
            <div class="cp-flow-connector"><div class="cp-flow-dot d1"></div><div class="cp-flow-dot d2"></div><div class="cp-flow-dot d3"></div></div>
            <div class="cp-flow-step">
                <div class="cp-flow-icon {step_active[2]}">{_svg_scan}</div>
                <div class="cp-flow-label">Risk Assessment</div>
            </div>
            <div class="cp-flow-connector"><div class="cp-flow-dot d1"></div><div class="cp-flow-dot d2"></div><div class="cp-flow-dot d3"></div></div>
            <div class="cp-flow-step">
                <div class="cp-flow-icon {step_active[3]}">{_svg_check_circle}</div>
                <div class="cp-flow-label">Auto-Binder Decision</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =====================================================================
        # SECTION 3C: APPLICANT UNDERWRITING REVIEW
        # =====================================================================
        copilot_customers = pd.DataFrame()
        try:
            copilot_customers = sf.run_query("""
                SELECT c.CUSTOMER_ID, c.FIRST_NAME || ' ' || c.LAST_NAME AS NAME, c.CREDIT_SCORE, c.AGE
                FROM INSURANCE_MGMT_SYSTEM.CORE.CUSTOMERS c
                INNER JOIN INSURANCE_MGMT_SYSTEM.PREMIUM.PREMIUM_CALCULATIONS pc ON c.CUSTOMER_ID = pc.CUSTOMER_ID
                ORDER BY c.CUSTOMER_ID
            """)
        except Exception:
            try:
                copilot_customers = sf.run_query("SELECT CUSTOMER_ID, FIRST_NAME || ' ' || LAST_NAME AS NAME, CREDIT_SCORE, AGE FROM INSURANCE_MGMT_SYSTEM.CORE.CUSTOMERS ORDER BY CUSTOMER_ID")
            except Exception:
                pass

        if not copilot_customers.empty:
            st.markdown(f"""
            <div class="cp-section-title" style="margin-top:24px;">
                {_svg_clipboard}
                <span>Applicant Underwriting Review</span>
            </div>
            """, unsafe_allow_html=True)

            cp_left, cp_right = st.columns([3, 2])
            with cp_left:
                customer_options = [f"{r['CUSTOMER_ID']} - {r['NAME']} (Credit: {r.get('CREDIT_SCORE','N/A')}, Age: {r.get('AGE','N/A')})" for _, r in copilot_customers.iterrows()]
                selected_customer_str = st.selectbox("Select Applicant for Underwriting Review", customer_options, key="copilot_customer_select", label_visibility="collapsed")
                selected_cust_id = selected_customer_str.split(" - ")[0].strip()

                sel_row = copilot_customers[copilot_customers["CUSTOMER_ID"] == selected_cust_id]
                if not sel_row.empty:
                    r = sel_row.iloc[0]
                    credit = r.get("CREDIT_SCORE", "N/A")
                    age = r.get("AGE", "N/A")
                    credit_val = int(credit) if str(credit).isdigit() else 0
                    risk_seg = "Low Risk" if credit_val >= 700 else ("Medium Risk" if credit_val >= 600 else "High Risk")
                    risk_color = "#059669" if credit_val >= 700 else ("#D97706" if credit_val >= 600 else "#DC2626")
                    st.markdown(f"""
                    <div class="cp-details-card">
                        <div style="font-size:13px; font-weight:700; color:#0F172A; margin-bottom:10px;">Applicant Details Preview</div>
                        <div class="cp-detail-row"><span class="cp-detail-label">Customer ID</span><span class="cp-detail-value">{selected_cust_id}</span></div>
                        <div class="cp-detail-row"><span class="cp-detail-label">Full Name</span><span class="cp-detail-value">{r.get('NAME','N/A')}</span></div>
                        <div class="cp-detail-row"><span class="cp-detail-label">Credit Score</span><span class="cp-detail-value">{credit}</span></div>
                        <div class="cp-detail-row"><span class="cp-detail-label">Age</span><span class="cp-detail-value">{age}</span></div>
                        <div class="cp-detail-row"><span class="cp-detail-label">Risk Segment</span><span class="cp-detail-value" style="color:{risk_color};">{risk_seg}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

            with cp_right:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                run_copilot = st.button("Analyze Application", use_container_width=True, type="primary", key="run_copilot_btn")
                st.markdown(f"""
                <div style="text-align:center; margin-top:12px; font-size:11px; color:#94A3B8;">
                    {_svg_activity} Pulls data from 5 Snowflake tables and computes AI risk decision
                </div>
                """, unsafe_allow_html=True)

            if run_copilot:
                with st.spinner("Fetching profile from 5 Snowflake tables & computing AI decision..."):
                    try:
                        profile = sf.get_underwriting_profile(selected_cust_id)
                        if profile:
                            decision = sf.compute_underwriting_decision(profile)
                            st.session_state["uw_copilot_profile"] = profile
                            st.session_state["uw_copilot_decision"] = decision
                        else:
                            st.warning(f"No premium calculation data found for {selected_cust_id}.")
                    except Exception as e:
                        st.error(f"Copilot error: {e}")

            # =====================================================================
            # SECTION 3D: RESULTS DASHBOARD
            # =====================================================================
            if "uw_copilot_decision" in st.session_state and "uw_copilot_profile" in st.session_state:
                decision = st.session_state["uw_copilot_decision"]
                profile = st.session_state["uw_copilot_profile"]
                bucket = decision["bucket"]
                final_p = float(profile.get('FINAL_PREMIUM', 0) or 0)
                base_p = float(profile.get('BASE_PREMIUM', 0) or 0)
                ml_p = float(profile.get('ML_PREDICTED_PREMIUM', 0) or 0)

                if bucket == "AUTO_APPROVE":
                    card_cls = "approve"; indicator_cls = "green"; score_color = "#059669"; label_text = "AUTO-APPROVE"; metric_cls = "green"
                    decision_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
                elif bucket == "HUMAN_REVIEW":
                    card_cls = "review"; indicator_cls = "yellow"; score_color = "#D97706"; label_text = "HUMAN REVIEW"; metric_cls = "amber"
                    decision_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
                else:
                    card_cls = "decline"; indicator_cls = "red"; score_color = "#DC2626"; label_text = "DECLINE / ESCALATE"; metric_cls = "red"
                    decision_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'

                confidence = max(0.0, min(1.0, 1.0 - abs(decision['score'] - 0.5) * 0.5))

                # Metric Cards Row
                st.markdown(f"""
                <div class="cp-results-grid">
                    <div class="cp-metric-card {metric_cls}">
                        <div class="cp-metric-label">Risk Score</div>
                        <div class="cp-metric-value" style="color:{score_color};">{decision['score']:.2f}</div>
                        <div class="cp-metric-sub">Composite risk index</div>
                    </div>
                    <div class="cp-metric-card {metric_cls}">
                        <div class="cp-metric-label">Decision</div>
                        <div class="cp-metric-value" style="color:{score_color}; font-size:18px; letter-spacing:0.5px;">{label_text}</div>
                        <div class="cp-metric-sub">AI routing bucket</div>
                    </div>
                    <div class="cp-metric-card blue">
                        <div class="cp-metric-label">Premium Quote</div>
                        <div class="cp-metric-value" style="color:#2563EB;">${final_p:,.0f}</div>
                        <div class="cp-metric-sub">Annual premium</div>
                    </div>
                    <div class="cp-metric-card blue">
                        <div class="cp-metric-label">Confidence</div>
                        <div class="cp-metric-value" style="color:#2563EB;">{confidence:.0%}</div>
                        <div class="cp-metric-sub">Model certainty</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Decision Banner
                st.markdown(f"""
                <div class="cp-decision-banner {card_cls}">
                    <div class="cp-decision-indicator {indicator_cls}">{decision_svg}</div>
                    <div class="cp-decision-text">
                        <div class="cp-decision-title" style="color:{score_color};">{label_text}</div>
                        <div class="cp-decision-action" style="color:{score_color};">{decision['action']}</div>
                        <div class="cp-decision-meta">
                            <span>Applicant: <b>{profile.get('FULL_NAME','N/A')}</b></span>
                            <span>Policy: <b>{profile.get('POLICY_TYPE','N/A')} / {profile.get('PLAN_TIER','N/A')}</b></span>
                            <span>Premium: <b>${final_p:,.2f}</b></span>
                            <span>ML Predicted: <b>${ml_p:,.2f}</b></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No customer records with premium calculations found. Ensure PREMIUM_CALCULATIONS is populated.")

        # =====================================================================
        # SECTION 4: XAI RISK FACTOR BREAKDOWN
        # =====================================================================
        if "uw_copilot_decision" in st.session_state and "uw_copilot_profile" in st.session_state:
            decision = st.session_state["uw_copilot_decision"]
            profile = st.session_state["uw_copilot_profile"]
            final_p = float(profile.get('FINAL_PREMIUM', 0) or 0)
            reasons = decision.get("reasons", [])

            if reasons:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:10px; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid #F1F5F9;">
                        {_svg_bar_chart}
                        <span style="font-size:15px; font-weight:800; color:#0F172A;">Explainable AI (XAI) Risk Factor Breakdown</span>
                        <span style="font-size:11px; font-weight:600; font-family:monospace; background:#F1F5F9; color:#475569; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">PREMIUM_CALCULATIONS.FACTOR_BREAKDOWN</span>
                    </div>
                    """, unsafe_allow_html=True)

                    import plotly.graph_objects as go
                    factor_names = [r[0] for r in reasons]
                    factor_impacts = [r[2] for r in reasons]

                    fig_waterfall = go.Figure(go.Waterfall(
                        name="Risk Impact", orientation="h",
                        measure=["relative"] * len(factor_names) + ["total"],
                        y=factor_names + ["TOTAL SCORE"],
                        x=[round(v * 100, 1) for v in factor_impacts] + [None],
                        text=[f"{v:+.0%}" for v in factor_impacts] + [f"{decision['score']:.0%}"],
                        textposition="outside",
                        connector={"line": {"color": "#E2E8F0", "width": 1}},
                        increasing={"marker": {"color": "#EF4444"}},
                        decreasing={"marker": {"color": "#10B981"}},
                        totals={"marker": {"color": decision["color"]}},
                        hovertemplate="<b>%{y}</b><br>Impact: %{text}<extra></extra>"
                    ))
                    fig_waterfall.update_layout(
                        height=300, margin=dict(l=10, r=60, t=10, b=10),
                        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                        xaxis=dict(title="Risk Impact (%)", gridcolor="#F1F5F9", tickfont=dict(size=11, color="#64748B"), zeroline=True, zerolinecolor="#CBD5E1"),
                        yaxis=dict(tickfont=dict(size=11, color="#334155"), autorange="reversed"),
                        showlegend=False
                    )
                    st.plotly_chart(fig_waterfall, use_container_width=True)

                    xai_rows = ""
                    for factor, value, impact, explanation in reasons:
                        if impact > 0.05:
                            impact_color = "#DC2626"; impact_icon = "&#9650;"
                        elif impact < -0.01:
                            impact_color = "#10B981"; impact_icon = "&#9660;"
                        else:
                            impact_color = "#64748B"; impact_icon = "&#9679;"
                        xai_rows += (
                            f'<div style="display:grid; grid-template-columns:1.5fr 1fr 0.8fr 2fr; padding:8px 12px; border-bottom:1px solid #F1F5F9; font-size:13px; align-items:center;">'
                            f'<span style="font-weight:600; color:#0F172A;">{factor}</span>'
                            f'<span style="color:#334155; font-family:monospace;">{value}</span>'
                            f'<span style="color:{impact_color}; font-weight:700;">{impact_icon} {impact:+.0%}</span>'
                            f'<span style="color:#64748B; font-size:12px;">{explanation}</span>'
                            f'</div>'
                        )
                    st.markdown(
                        '<div style="border:1px solid #E2E8F0; border-radius:8px; overflow:hidden; margin-top:4px;">'
                        '<div style="display:grid; grid-template-columns:1.5fr 1fr 0.8fr 2fr; padding:10px 12px; background:#F8FAFC; border-bottom:1px solid #E2E8F0; font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.5px;">'
                        '<span>RISK FACTOR</span><span>VALUE</span><span>IMPACT</span><span>EXPLANATION</span>'
                        '</div>'
                        f'{xai_rows}'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    fb = profile.get("FACTOR_BREAKDOWN", "")
                    if fb:
                        st.caption(f"Snowflake FACTOR_BREAKDOWN: {fb}")

            # =====================================================================
            # SECTION 5: ACTUARIAL MULTIPLIERS & PREMIUM SUMMARY
            # =====================================================================
            with st.container(border=True):
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid #F1F5F9;">
                    {_svg_trending}
                    <span style="font-size:15px; font-weight:800; color:#0F172A;">Actuarial Multipliers &amp; Premium Summary</span>
                    <span style="font-size:11px; font-weight:600; font-family:monospace; background:#F1F5F9; color:#475569; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">PREMIUM_CALCULATIONS</span>
                </div>
                """, unsafe_allow_html=True)
                mult_col1, mult_col2 = st.columns([1.5, 1])
                with mult_col1:
                    import plotly.graph_objects as go
                    mult_data = {
                        "Factor": ["Age", "Location", "Health", "Lifestyle", "Claims History"],
                        "Multiplier": [
                            float(profile.get("AGE_FACTOR", 1.0) or 1.0),
                            float(profile.get("LOCATION_FACTOR", 1.0) or 1.0),
                            float(profile.get("HEALTH_FACTOR", 1.0) or 1.0),
                            float(profile.get("LIFESTYLE_FACTOR", 1.0) or 1.0),
                            float(profile.get("CLAIMS_HISTORY_FACTOR", 1.0) or 1.0),
                        ]
                    }
                    mult_df = pd.DataFrame(mult_data)
                    fig_mult = go.Figure(go.Bar(
                        x=mult_df["Multiplier"], y=mult_df["Factor"], orientation="h",
                        marker_color=["#EF4444" if v > 1.5 else "#F59E0B" if v > 1.2 else "#10B981" for v in mult_df["Multiplier"]],
                        text=[f"{v:.2f}x" for v in mult_df["Multiplier"]], textposition="outside",
                        hovertemplate="<b>%{y}</b>: %{x:.2f}x<extra></extra>"
                    ))
                    fig_mult.add_vline(x=1.0, line_dash="dash", line_color="#94A3B8", annotation_text="Baseline 1.0x")
                    fig_mult.update_layout(
                        height=220, margin=dict(l=10, r=40, t=10, b=10),
                        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                        xaxis=dict(gridcolor="#F1F5F9", range=[0, max(mult_df["Multiplier"]) * 1.3]),
                        yaxis=dict(autorange="reversed")
                    )
                    st.plotly_chart(fig_mult, use_container_width=True)

                with mult_col2:
                    base_p = float(profile.get('BASE_PREMIUM', 0) or 0)
                    ml_p = float(profile.get('ML_PREDICTED_PREMIUM', 0) or 0)
                    discount = float(profile.get('DISCOUNT_APPLIED', 0) or 0)
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:16px;">
                        <div style="font-weight:800; font-size:14px; color:#0F172A; margin-bottom:12px;">Premium Summary</div>
                        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #F1F5F9;">
                            <span style="color:#64748B; font-size:13px;">Base Premium</span>
                            <span style="font-weight:700; color:#0F172A;">${base_p:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #F1F5F9;">
                            <span style="color:#64748B; font-size:13px;">After Factors</span>
                            <span style="font-weight:700; color:#0F172A;">${final_p:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #F1F5F9;">
                            <span style="color:#64748B; font-size:13px;">ML Predicted</span>
                            <span style="font-weight:700; color:#0284C7;">${ml_p:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #F1F5F9;">
                            <span style="color:#10B981; font-size:13px;">Discount Applied</span>
                            <span style="font-weight:700; color:#10B981;">-${discount:,.2f}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; padding:10px 0 0 0;">
                            <span style="font-weight:800; font-size:15px; color:#0F172A;">Final Quote</span>
                            <span style="font-weight:800; font-size:18px; color:{decision['color']};">${final_p:,.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # =====================================================================
            # SECTION 6: AUTO-BINDER OUTPUT DOCUMENT
            # =====================================================================
            st.markdown(f"""
            <div class="cp-binder-card">
                <div class="cp-binder-header">
                    <div class="cp-binder-title">
                        {_svg_file_check.replace('stroke="#059669"', 'stroke="#0F172A"')}
                        <span>Policy Binder Document</span>
                    </div>
                    <span class="cp-binder-badge">AUTO-GENERATED</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px;">
                    <div>
                        <div class="cp-binder-section">
                            <div class="cp-binder-section-title">Applicant Summary</div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Name</span><span class="cp-binder-value">{profile.get('FULL_NAME','N/A')}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Customer ID</span><span class="cp-binder-value">{profile.get('CUSTOMER_ID','N/A')}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Policy Type</span><span class="cp-binder-value">{profile.get('POLICY_TYPE','N/A')}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Plan Tier</span><span class="cp-binder-value">{profile.get('PLAN_TIER','N/A')}</span></div>
                        </div>
                        <div class="cp-binder-section">
                            <div class="cp-binder-section-title">Risk Assessment</div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Risk Score</span><span class="cp-binder-value" style="color:{score_color};">{decision['score']:.2f}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Credit Score</span><span class="cp-binder-value">{profile.get('CREDIT_SCORE','N/A')}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Age</span><span class="cp-binder-value">{profile.get('AGE','N/A')}</span></div>
                        </div>
                    </div>
                    <div>
                        <div class="cp-binder-section">
                            <div class="cp-binder-section-title">Premium Recommendation</div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Base Premium</span><span class="cp-binder-value">${base_p:,.2f}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Final Premium</span><span class="cp-binder-value" style="color:#2563EB; font-weight:800;">${final_p:,.2f}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">ML Predicted</span><span class="cp-binder-value">${ml_p:,.2f}</span></div>
                        </div>
                        <div class="cp-binder-section">
                            <div class="cp-binder-section-title">Underwriting Decision</div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Decision</span><span class="cp-binder-value" style="color:{score_color};">{label_text}</span></div>
                            <div class="cp-binder-row"><span class="cp-binder-label">Action</span><span class="cp-binder-value">{decision['action']}</span></div>
                        </div>
                        <div class="cp-binder-section">
                            <div class="cp-binder-section-title">AI Explanation</div>
                            <div style="font-size:12px; color:#475569; line-height:1.6;">
                                The AI engine evaluated {len(decision.get('reasons',[]))} risk factors across actuarial multipliers, credit history, and ML predictions to reach this determination.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # =====================================================================
            # SECTION 7: EXPORT BUTTONS
            # =====================================================================
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
            with btn_col1:
                if st.button("Generate Policy Binder PDF", use_container_width=True, type="primary", key="copilot_pdf_btn"):
                    with st.spinner("Generating PDF..."):
                        try:
                            pdf_bytes = sf.generate_binder_pdf(profile, decision, final_p)
                            st.session_state["copilot_pdf"] = pdf_bytes
                            st.session_state["copilot_pdf_name"] = f"Policy_Binder_{profile.get('CUSTOMER_ID','')}_{profile.get('POLICY_TYPE','')}.pdf"
                        except Exception as e:
                            st.error(f"PDF generation error: {e}")

            with btn_col2:
                if st.button("Get Agent Underwriting Opinion", use_container_width=True, key="copilot_agent_popup_btn"):
                    st.session_state.pop("agent_chat_history", None)
                    st.session_state["show_agent_dialog"] = True

            if st.session_state.get("show_agent_dialog", False):
                _show_agent_opinion_dialog()

            with btn_col3:
                if "copilot_pdf" in st.session_state:
                    st.download_button(
                        label="Download Policy Binder PDF",
                        data=st.session_state["copilot_pdf"],
                        file_name=st.session_state.get("copilot_pdf_name", "Policy_Binder.pdf"),
                        mime="application/pdf",
                        use_container_width=True,
                        key="pdf_download_btn"
                    )

            if "copilot_pdf" in st.session_state and "pdf_download_btn" not in st.session_state:
                st.success("Policy Binder PDF generated successfully!")

            # =====================================================================
            # SECTION 8: AI COPILOT ASSISTANT PANEL
            # =====================================================================
            st.markdown(f"""
            <div class="cp-copilot-panel">
                <div class="cp-copilot-header-bar">
                    <div class="cp-copilot-avatar">{_svg_sparkles}</div>
                    <div>
                        <div class="cp-copilot-name">AI Underwriting Copilot</div>
                        <div class="cp-copilot-tag">Powered by Snowflake Cortex</div>
                    </div>
                </div>
                <div class="cp-chat-bubble ai">
                    Analysis complete for <b>{profile.get('FULL_NAME','this applicant')}</b>.
                    The risk score of <b>{decision['score']:.2f}</b> was determined by evaluating {len(decision.get('reasons',[]))} actuarial factors.
                    Decision: <b style="color:{score_color};">{label_text}</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)

            cp_assist_col1, cp_assist_col2, cp_assist_col3 = st.columns(3)
            with cp_assist_col1:
                if st.button("Why was this decision made?", use_container_width=True, key="cp_why_btn"):
                    st.session_state["cp_copilot_q"] = "why_decision"
            with cp_assist_col2:
                if st.button("Explain risk factors", use_container_width=True, key="cp_explain_btn"):
                    st.session_state["cp_copilot_q"] = "explain_risk"
            with cp_assist_col3:
                if st.button("Generate underwriting summary", use_container_width=True, key="cp_summary_btn"):
                    st.session_state["cp_copilot_q"] = "gen_summary"

            if "cp_copilot_q" in st.session_state:
                q_type = st.session_state["cp_copilot_q"]
                reasons_list = decision.get("reasons", [])
                if q_type == "why_decision":
                    reason_text = f"The decision of **{label_text}** was reached because the composite risk score is **{decision['score']:.2f}**. "
                    if bucket == "AUTO_APPROVE":
                        reason_text += "This score falls within the auto-approval threshold (below 0.4), indicating low overall risk across all evaluated factors."
                    elif bucket == "HUMAN_REVIEW":
                        reason_text += "This score falls in the review band (0.4-0.7), requiring human underwriter assessment before final binding."
                    else:
                        reason_text += "This score exceeds the decline threshold (above 0.7), indicating elevated risk that requires escalation."
                    st.info(reason_text)
                elif q_type == "explain_risk":
                    if reasons_list:
                        explain_md = "**Risk Factor Analysis:**\n\n"
                        for factor, value, impact, explanation in reasons_list:
                            direction = "increases" if impact > 0 else "decreases"
                            explain_md += f"- **{factor}** ({value}): {direction} risk by {abs(impact):.0%} - {explanation}\n"
                        st.info(explain_md)
                    else:
                        st.info("No detailed risk factors available for this applicant.")
                elif q_type == "gen_summary":
                    summary = (
                        f"**Underwriting Summary for {profile.get('FULL_NAME','N/A')}**\n\n"
                        f"- **Customer ID:** {profile.get('CUSTOMER_ID','N/A')}\n"
                        f"- **Policy:** {profile.get('POLICY_TYPE','N/A')} / {profile.get('PLAN_TIER','N/A')}\n"
                        f"- **Risk Score:** {decision['score']:.2f}\n"
                        f"- **Decision:** {label_text}\n"
                        f"- **Premium:** ${final_p:,.2f}\n"
                        f"- **Action:** {decision['action']}\n\n"
                        f"The AI engine evaluated the applicant across {len(reasons_list)} risk dimensions. "
                        f"Based on the composite scoring model, this application has been routed to the **{label_text}** bucket."
                    )
                    st.info(summary)



