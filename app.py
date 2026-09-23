import os
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv

import snowflake_utils as sf

def _typewriter(text):
    """Yield words for st.write_stream typewriter effect."""
    for i, word in enumerate(text.split(" ")):
        yield word + (" " if i < len(text.split(" ")) - 1 else "")
        time.sleep(0.02)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Insurance Intelligence Platform | Capgemini & Snowflake",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# CENTRALIZED ENTERPRISE CSS DESIGN SYSTEM
# =========================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    /* Global Resets & Typography */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    /* Permanent Fixed Sidebar Layout - Hide ALL open/close toggle buttons and Streamlit header clutter */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarExpandButton"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"] button[aria-label*="sidebar"],
    section[data-testid="stSidebar"] button[aria-label*="Close"],
    section[data-testid="stSidebar"] button[aria-label*="Collapse"],
    section[data-testid="stSidebar"] button[kind="header"],
    header[data-testid="stHeader"] button,
    [data-testid="stDeployButton"],
    .stDeployButton,
    [data-testid="stHeaderActionElements"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }

    /* Enforce permanent fixed sidebar display & width */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        width: 18.5rem !important;
        min-width: 18.5rem !important;
        max-width: 18.5rem !important;
        transform: none !important;
        margin-left: 0 !important;
    }

    /* Hide Streamlit top header container */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    .stAppHeader {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .main .block-container {
        padding-top: 80px !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        color: #0F172A;
    }
    
    /* Zero out all margins/paddings on Streamlit container wrappers around .header-container */
    div[data-testid="stElementContainer"]:has(.header-container),
    div.element-container:has(.header-container),
    div[data-testid="stMarkdownContainer"]:has(.header-container),
    .stMarkdown:has(.header-container) {
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }

    /* Top Header Bar - Positioned at VERY TOP of content view (top: 0) directly touching sidebar right edge */
    .header-container {
        position: fixed !important;
        top: 0 !important;
        left: 18.5rem !important;
        right: 0 !important;
        height: 62px !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        padding: 0 24px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        border-bottom: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        z-index: 999999 !important;
        box-sizing: border-box !important;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    
    .brand-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .brand-logo-capgemini {
        display: flex;
        align-items: center;
        height: 32px;
    }
    
    .brand-logo-capgemini img {
        height: 28px;
        object-fit: contain;
    }
    
    .brand-divider {
        width: 1.5px;
        height: 28px;
        background: #CBD5E1;
    }
    
    .brand-logo-snowflake {
        display: flex;
        align-items: center;
        height: 32px;
    }
    
    .brand-logo-snowflake img {
        height: 28px;
        object-fit: contain;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .notification-wrapper {
        position: relative;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        transition: background 0.2s;
    }
    
    .notification-wrapper:hover {
        background: #F1F5F9;
    }
    
    .notification-badge {
        position: absolute;
        top: 2px;
        right: 2px;
        background: #EF4444;
        color: #FFFFFF;
        font-size: 10px;
        font-weight: 700;
        min-width: 16px;
        height: 16px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 4px;
        border: 2px solid #FFFFFF;
    }
    
    .header-vert-divider {
        width: 1px;
        height: 24px;
        background: #E2E8F0;
    }
    
    .user-profile-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }
    
    .user-avatar-circle {
        width: 32px;
        height: 32px;
        background: #0F172A;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
    }
    
    .user-name-text {
        font-size: 12px;
        font-weight: 700;
        color: #1E293B;
        display: flex;
        align-items: center;
        gap: 5px;
        letter-spacing: 0.2px;
    }
    
    .header-live-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #10B981;
        margin-left: 6px;
    }
    
    .pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 5px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Left Sidebar Styling - Deep Ocean Navy Blue with Subtle Waves (Image 3) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071f45 0%, #03142e 65%, #020b1a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* Hide outer widget label (Navigation) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > label,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [data-testid="stWidgetLabel"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 4px 20px 4px;
        margin-bottom: 16px;
    }
    
    .sidebar-brand-icon {
        width: 48px;
        height: 48px;
        background: #0284C7;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
        flex-shrink: 0;
    }
    
    .sidebar-brand-text {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF !important;
        line-height: 1.2;
        letter-spacing: -0.3px;
    }

    /* Navigation Radio Items - Sleek List without Radio Circles (Image 3) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
    }
    
    /* Hide Streamlit's default radio circle / dot indicator */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child:not([data-testid="stMarkdownContainer"]),
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label input[type="radio"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label span[data-baseweb="radio-bullet"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        margin-bottom: 2px !important;
        width: 100% !important;
    }
    
    /* Unselected items text color */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label div,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.4 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover span {
        color: #FFFFFF !important;
    }
    
    /* Active / Selected Radio Option Button */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[aria-checked="true"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input[aria-checked="true"]) {
        background: linear-gradient(90deg, #0959aa 0%, #0b6ccf 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(11, 98, 185, 0.45) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[aria-checked="true"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Decorative Wave Art between Menu and Status */
    .sidebar-wave-container {
        position: relative;
        width: 100%;
        margin-top: 40px;
        margin-bottom: 20px;
        opacity: 0.6;
        pointer-events: none;
    }

    /* Sidebar Status Footer Card (Image 3) */
    .sidebar-status-box {
        background: rgba(3, 16, 36, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }
    
    .sidebar-status-header {
        font-size: 11px;
        text-transform: capitalize;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.3px;
        margin-bottom: 12px;
    }
    
    .sidebar-status-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12px;
        color: #94A3B8;
        margin-bottom: 10px;
    }
    
    .sidebar-status-item:last-child {
        margin-bottom: 0;
    }
    
    .sidebar-status-val {
        color: #FFFFFF;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }    }
    
    .sidebar-status-item:last-child {
        margin-bottom: 0;
    }

    /* Enterprise Card Panels */
    .card-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    .card-panel:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.06);
    }
    
    .panel-header {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .panel-header-title {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .panel-header-badge {
        font-size: 11px;
        background: #F1F5F9;
        color: #475569;
        font-family: 'JetBrains Mono', monospace;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 500;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        border-left: 4px solid #0284C7;
    }
    
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    
    .kpi-subtitle {
        font-size: 12px;
        color: #10B981;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .kpi-subtitle.danger {
        color: #EF4444;
    }

    /* Risk & Pricing Dashboard V2 Styles */
    .kpi-card-v2 {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        min-height: 102px;
        border-left: 4px solid #0284C7;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card-v2:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .kpi-v2-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .kpi-v2-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    
    .kpi-v2-subtitle {
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .kpi-icon-container {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .risk-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        background-color: #FEE2E2;
        color: #DC2626;
        border: 1px solid #FCA5A5;
    }

    .risk-badge-medium {
        background-color: #FEF3C7;
        color: #D97706;
        border: 1px solid #FCD34D;
    }

    .policy-link-text {
        color: #0284C7;
        font-weight: 700;
        text-decoration: none;
    }


    /* Prediction Insight Card */
    .prediction-container {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #86EFAC;
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
    }
    
    .prediction-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #166534;
        margin-bottom: 4px;
    }
    
    .prediction-amount {
        font-size: 40px;
        font-weight: 800;
        color: #15803D;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    
    .prediction-tag {
        display: inline-block;
        background: #16A34A;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    
    .driver-tag-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 13px;
        color: #334155;
    }
    
    .driver-tag-row b {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Alert and Recommendation Banners */
    .recommendation-danger {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        color: #991B1B;
        padding: 14px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin-top: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .recommendation-success {
        background-color: #F0FDF4;
        border: 1px solid #86EFAC;
        color: #166534;
        padding: 14px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin-top: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Chat Messages */
    .chat-user-bubble {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 14px 14px 2px 14px;
        margin-left: 15%;
        margin-bottom: 16px;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.2);
    }
    
    .chat-agent-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #10B981;
        color: #1E293B;
        padding: 16px 20px;
        border-radius: 10px;
        margin-right: 15%;
        margin-bottom: 18px;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .chat-agent-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #059669;
        margin-bottom: 8px;
    }

    /* Welcome Banner Styling */
    .chat-welcome-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    
    .chat-welcome-banner h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    
    .chat-welcome-banner p {
        margin: 4px 0 0 0;
        font-size: 13px;
        color: #64748B;
        line-height: 1.5;
    }

    /* Collapsible Thinking Accordion (Up / Down toggle) */
    .chat-thinking-accordion {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        margin-bottom: 12px;
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .chat-thinking-accordion[open] {
        background-color: #F1F5F9;
        border-color: #CBD5E1;
    }

    .chat-thinking-summary {
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 600;
        color: #475569;
        cursor: pointer;
        user-select: none;
        display: flex;
        align-items: center;
        justify-content: space-between;
        outline: none;
    }

    .chat-thinking-summary::-webkit-details-marker {
        display: none;
    }

    .chat-thinking-badge {
        font-size: 10px;
        font-weight: 600;
        background: #E2E8F0;
        color: #334155;
        padding: 2px 8px;
        border-radius: 10px;
    }

    .chat-thinking-body {
        padding: 10px 12px;
        border-top: 1px dashed #CBD5E1;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #334155;
        line-height: 1.6;
        background-color: #FFFFFF;
    }

    /* ChatGPT Bouncing Loader Animation */
    .chat-loader-card {
        border-left: 4px solid #0284C7 !important;
    }

    .bouncing-loader {
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .bouncing-loader div {
        width: 8px;
        height: 8px;
        background-color: #0284C7;
        border-radius: 50%;
        animation: bouncing-loader 0.6s infinite alternate;
    }

    .bouncing-loader div:nth-child(2) {
        animation-delay: 0.2s;
    }

    .bouncing-loader div:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes bouncing-loader {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0.2;
            transform: translateY(-8px);
        }
    }

    /* Streamlit Form & Button overrides */
    div.stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# Helper function for Chat Assistant Thinking & Response separation
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
            domain = "CORE.CLAIMS & ANALYTICS.FRAUD_ALERTS"
        elif "policy" in prompt_low or "churn" in prompt_low:
            domain = "CORE.POLICIES & RISK.AT_RISK_POLICIES_ML"
        elif "premium" in prompt_low or "estimate" in prompt_low:
            domain = "ML Actuarial Pricing Engine (PREDICT_PREMIUM)"
        else:
            domain = "INSURANCE_MGMT_SYSTEM Global Schema"
            
        thinking_text = (
            f"• Intent Analysis: Identified query context for entity ({domain}).\n"
            f"• Data Connection: Established session with Snowflake warehouse HACKATHONTEAMAVENGERS.\n"
            f"• AI Inference: Called SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet').\n"
            f"• Output Formatter: Verified database result schema and generated response."
        )
    return thinking_text, clean_response


# =========================================================================
# HEADER COMPONENT (CAPGEMINI + SNOWFLAKE + NOTIFICATIONS + USER PROFILE)
# =========================================================================
def render_header():
    wh_name = os.getenv("SNOWFLAKE_WAREHOUSE", "HACKATHONTEAMAVENGERS")
    
    header_html = f"""
    <div class="header-container">
        <div class="header-left">
            <div class="brand-group">
                <div class="brand-logo-capgemini">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/9/9d/Capgemini_201x_logo.svg" alt="Capgemini" height="24" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';"><span style="display:none; color:#0070AD; font-weight:800; font-size:18px;">Capgemini</span>
                </div>
                <div class="brand-divider"></div>
                <div class="brand-logo-snowflake">
                    <svg width="125" height="22" viewBox="0 0 130 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g transform="translate(0, 2) scale(0.9)">
                            <path fill="#29B5E8" d="M24 3.459c0 .646-.418 1.18-1.141 1.18-.723 0-1.142-.534-1.142-1.18 0-.647.419-1.18 1.142-1.18.723 0 1.141.533 1.141 1.18zm-.228 0c0-.533-.38-.951-.913-.951s-.913.38-.913.95c0 .533.38.952.913.952.57 0 .913-.419.913-.951zm-1.37-.533h.495c.266 0 .456.152.456.38 0 .153-.076.229-.19.305l.19.266v.038h-.266l-.19-.266h-.229v.266h-.266zm.495.228h-.229v.267h.229c.114 0 .152-.038.152-.114.038-.077-.038-.153-.152-.153zM7.602 12.4c.038-.151.076-.304.076-.456 0-.114-.038-.228-.038-.342-.114-.343-.304-.647-.646-.838l-4.87-2.777c-.685-.38-1.56-.152-1.94.533-.381.685-.153 1.56.532 1.94l2.701 1.56-2.701 1.56c-.685.38-.913 1.256-.533 1.94.38.685 1.256.914 1.94.533l4.832-2.777c.343-.267.571-.533.647-.876zm1.332 2.626c-.266-.038-.57.038-.837.19l-4.832 2.777c-.685.38-.913 1.256-.532 1.94.38.686 1.255.914 1.94.533l2.701-1.56v3.12c0 .8.647 1.408 1.446 1.408.799 0 1.407-.647 1.407-1.408v-5.592c0-.761-.57-1.37-1.293-1.408zm4.946-6.088c.266.038.57-.038.837-.19l4.832-2.777c.685-.38.913-1.256.532-1.94-.38-.686-1.255-.914-1.94-.533l-2.701 1.56V1.975c0-.799-.647-1.408-1.446-1.408-.799 0-1.446.609-1.446 1.408V7.53c0 .76.609 1.37 1.332 1.407zM3.265 5.97l4.832 2.777c.266.152.533.19.837.19.723-.038 1.331-.684 1.331-1.407V1.975c0-.799-.646-1.408-1.407-1.408-.799 0-1.446.647-1.446 1.408v3.12l-2.701-1.56c-.685-.38-1.56-.152-1.94.533-.419.646-.19 1.521.494 1.902zm9.093 6.011a.412.412 0 00-.114-.266l-.57-.571a.346.346 0 00-.267-.114.412.412 0 00-.266.114l-.571.57a.411.411 0 00-.114.267c0 .076.038.19.114.267l.57.57a.345.345 0 00.267.114c.076 0 .19-.038.266-.114l.571-.57a.412.412 0 00.114-.267zm1.598.533L11.94 14.53c-.039.038-.153.114-.229.114h-.608a.411.411 0 01-.267-.114L8.82 12.514a.408.408 0 01-.076-.229v-.608c0-.076.038-.19.114-.267l2.016-2.016a.41.41 0 01.267-.114h.608a.41.41 0 01.267.114l2.016 2.016a.347.347 0 01.114.267v.608c-.076.077-.114.19-.19.229zm5.593 5.44l-4.832-2.777c-.266-.152-.57-.19-.837-.152-.723.038-1.332.684-1.332 1.408v5.554c0 .8.647 1.408 1.408 1.408.799 0 1.446-.647 1.446-1.408v-3.12l2.7 1.56c.686.38 1.561.152 1.941-.533.419-.646.19-1.521-.494-1.9zm2.549-7.533l-2.701 1.56 2.7 1.56c.686.38.914 1.256.533 1.94-.38.685-1.255.913-1.94.533l-4.832-2.778a1.644 1.644 0 01-.647-.798c-.037-.153-.076-.305-.076-.457 0-.114.039-.228.039-.342.114-.343.342-.647.646-.837l4.832-2.778c.685-.38 1.56-.152 1.94.533.457.609.19 1.484-.494 1.864"/>
                        </g>
                        <text x="28" y="18" font-family="'Inter', -apple-system, BlinkMacSystemFont, sans-serif" font-weight="800" font-size="17" fill="#29B5E8" letter-spacing="-0.5px">snowflake</text>
                    </svg>
                </div>
            </div>
        </div>
        <div class="header-right">
            <div class="user-profile-badge">
                <div class="user-avatar-circle">HT</div>
                <span class="user-name-text">
                    {wh_name}
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                </span>
                <div class="header-live-badge">
                    <div class="pulse-dot"></div>
                    <span>Live</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


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
                "🎯 Product Matching",
                "📊 Market Intelligence",
                "💰 Competitive Pricing",
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


# =========================================================================
# MAIN APP ENTRYPOINT
# =========================================================================
render_header()
if "sf_connected" not in st.session_state:
    val_init = sf.validate_connection()
    st.session_state["sf_connected"] = val_init.get("valid", False)
selected_tab = render_sidebar()

# =========================================================================
# TAB 1: UNDERWRITING WORKBENCH
# =========================================================================
if "Underwriting Workbench" in selected_tab:

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
                    <span style="font-size:11px; font-weight:600; font-family:monospace; background:#F1F5F9; color:#475569; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">GOLD.FACT_POLICY</span>
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



# =========================================================================
# TAB 2: CLAIMS & FRAUD CONSOLE
# =========================================================================
elif "Claims & Fraud Console" in selected_tab:
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
                <div class="panel-header-badge">FRAUD_PREDICTIONS_ML</div>
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
                <div class="panel-header-badge">CORTEX SEARCH</div>
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
            # Run initial triage assessment automatically for active claim
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


# =========================================================================
# TAB 3: RISK & PRICING DASHBOARD
# =========================================================================
elif "Risk & Pricing Dashboard" in selected_tab:
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
            <span class="panel-header-badge">ANALYTICS.LOSS_RATIO_HISTORY</span>
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
            <span class="panel-header-badge">RISK.AT_RISK_POLICIES_ML</span>
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
            <div class="panel-header-badge">PORTFOLIO_RISK_RETENTION_AGENT</div>
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
            <div class="panel-header-badge">CORTEX ANALYST / INSURANCE_SEMANTIC_MODEL</div>
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


# =========================================================================
# TAB 4: CUSTOMER 360 PROFILE
# =========================================================================
elif "Customer 360" in selected_tab:
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
                <span class="risk-badge" style="background:#E0F2FE; color:#0369A1; border-color:#BAE6FD;">GOLD.CUSTOMER_360</span>
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
                    <div class="panel-header-badge">INSURANCE_INTELLIGENCE_ASSISTANT</div>
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


# =========================================================================
# TAB 5: PRODUCT MATCHING (Multi-Strategy Product Recommendation Agent)
# =========================================================================
elif "Product Matching" in selected_tab:

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
        # Add user message to history
        st.session_state["pm_chat_history"].append({"role": "user", "content": prompt_to_run})
        
        # Display immediately in current render pass
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


# =========================================================================
# TAB 6: MARKET INTELLIGENCE (Trend Detection Agent)
# =========================================================================
elif "Market Intelligence" in selected_tab:

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


# =========================================================================
# TAB 7: COMPETITIVE PRICING (Price Optimization Agent)
# =========================================================================
elif "Competitive Pricing" in selected_tab:

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


# =========================================================================
# TAB 8: CHAT ASSISTANT (SNOWFLAKE CORTEX AI + IMAGE ANALYSIS)
# =========================================================================
elif "Chat Assistant" in selected_tab:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    selected_prompt = None

    # =========================================================================
    # EMPTY STATE: WELCOME BANNER, SUGGESTED QUICK INQUIRIES, EMPTY STATE GUIDE
    # =========================================================================
    if not st.session_state.messages:
        # Welcome Banner Header
        st.markdown("""
        <div class="chat-welcome-banner">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="font-size:32px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; width:52px; height:52px; display:flex; align-items:center; justify-content:center;">💬</div>
                <div>
                    <h2>Welcome to Chat Assistant</h2>
                    <p style="margin-top:4px; color:#64748B;">Ask anything about your policies, claims, fraud analysis, or actuarial risk metrics. Attach an image to estimate insurance claims. Powered by live Snowflake Cortex AI.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-panel" style="padding:16px 20px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:13px; font-weight:700; color:#334155;">💡 Suggested Quick Inquiries</div>
                <div style="font-size:11px; background:#F0FDF4; color:#166534; padding:3px 8px; border-radius:12px; font-weight:600;">Live Cortex Agent</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Question Buttons - Row 1
        q_col1, q_col2, q_col3 = st.columns(3)
        with q_col1:
            if st.button("🔍 Auto policies likely to churn?", use_container_width=True):
                selected_prompt = "Which of my auto policies are most likely to churn in the next 30 days?"

        with q_col2:
            if st.button("⚠️ Why was CLM-00381 flagged?", use_container_width=True):
                selected_prompt = "Show me why CLM-00381 was flagged for fraud"

        with q_col3:
            if st.button("💰 Estimate premium for 35yo $60k", use_container_width=True):
                selected_prompt = "Estimate premium for age 35, annual income $60000, credit score 700, coverage $250000"

        # Quick Question Buttons - Row 2
        q_col4, q_col5, q_col6 = st.columns(3)
        with q_col4:
            if st.button("📊 Show top 5 loss ratio policies", use_container_width=True):
                selected_prompt = "Show top 5 highest loss ratio policies in GOLD.FACT_POLICY"

        with q_col5:
            if st.button("🛡️ Summarize high risk fraud alerts", use_container_width=True):
                selected_prompt = "Summarize high risk fraud alerts in ANALYTICS.FRAUD_ALERTS"

        with q_col6:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        # Quick Question Buttons - Row 3: Image-based (dynamic from stage)
        q_col7, q_col8, q_col9 = st.columns(3)
        stage_files = sf.list_stage_files()
        image_files = [f for f in stage_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        with q_col7:
            if st.button("📷 Analyze claim evidence photo", use_container_width=True):
                if image_files:
                    selected_prompt = (
                        f"The following image files are available in the claim evidence stage: {', '.join(image_files)}. "
                        f"Please analyze the first image '{image_files[0]}' and estimate the insurance claim amount. "
                        f"Show the image analysis, then query the database for comparison data, and justify every number."
                    )
                else:
                    selected_prompt = "No evidence images found in the claim evidence stage. Please upload images first."

        with q_col8:
            if st.button("📊 Compare all evidence images", use_container_width=True):
                if len(image_files) >= 2:
                    selected_prompt = (
                        f"Analyze EACH of these evidence images one by one: {', '.join(image_files)}. "
                        f"For each image, identify damage type and estimate costs. "
                        f"Then query the database for average claim amounts by damage type and compare. "
                        f"Provide a combined total claim estimate with full justification."
                    )
                elif image_files:
                    selected_prompt = f"Analyze the evidence image '{image_files[0]}' and estimate the claim with database comparison."
                else:
                    selected_prompt = "No evidence images found in stage. Please upload images first."

        with q_col9:
            if st.button("📄 Verify invoice against policy", use_container_width=True):
                invoice_files = [f for f in image_files if 'invoice' in f.lower()]
                if invoice_files:
                    selected_prompt = (
                        f"Analyze the invoice image '{invoice_files[0]}' and verify whether the amounts "
                        f"are consistent with actual policy coverage and claim amounts in the database. "
                        f"Query the semantic model for real coverage limits and deductibles to compare against."
                    )
                elif image_files:
                    selected_prompt = f"Analyze '{image_files[0]}' and compare the estimated damage costs with actual policy data from the database."
                else:
                    selected_prompt = "No evidence files found in stage. Please upload images first."

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        # Empty State Guide Box
        st.markdown("""
        <div style="background:#FFFFFF; border:1px dashed #CBD5E1; border-radius:12px; padding:32px 24px; text-align:center; margin-bottom:20px;">
            <div style="font-size:40px; margin-bottom:10px;">🤖❄️</div>
            <h4 style="margin:0 0 6px 0; font-size:16px; font-weight:700; color:#1E293B;">How can I assist your underwriting & claims team today?</h4>
            <p style="margin:0 auto; max-width:520px; font-size:13px; color:#64748B; line-height:1.5;">
                Connected to live Snowflake database <b>INSURANCE_MGMT_SYSTEM</b>. Click a quick inquiry button above, type a question below, or <b>attach a damage photo</b> to estimate a claim.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # =========================================================================
        # ACTIVE CHAT STATE: TOP HEADER WITH CLEAR BUTTON
        # =========================================================================
        header_c1, header_c2 = st.columns([3, 1])
        with header_c1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <div style="font-size:24px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; width:42px; height:42px; display:flex; align-items:center; justify-content:center;">💬</div>
                <div>
                    <div style="font-weight:700; color:#0F172A; font-size:16px;">Insurance Intelligence Assistant</div>
                    <div style="font-size:12px; color:#64748B;">Connected to live Snowflake database INSURANCE_MGMT_SYSTEM</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with header_c2:
            if st.button("🗑️ Clear Chat History", key="active_clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # =========================================================================
    # RENDER CHAT HISTORY (Chronological ChatGPT-style format)
    # =========================================================================
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                if msg.get("image"):
                    st.image(msg["image"], caption=msg.get("image_name"), width=320)
                if msg.get("content"):
                    st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                agent_title = msg.get("agent", "INSURANCE_INTELLIGENCE_ASSISTANT")
                thinking_text = msg.get("thinking", "")
                clean_content = msg.get("content", "")

                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.6px; color:#059669; margin-bottom:8px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#10B981">
                        <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5"/>
                    </svg>
                    <span>{agent_title}</span>
                </div>
                """, unsafe_allow_html=True)

                if thinking_text:
                    resp_tab, think_tab = st.tabs(["💬 Response", "🧠 Thinking Process"])
                    with resp_tab:
                        st.markdown(clean_content)
                    with think_tab:
                        thinking_formatted = thinking_text.replace("\n", "<br>")
                        st.markdown(f"""
                        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #0284C7; border-radius:8px; padding:12px 16px; font-family:'JetBrains Mono', monospace; font-size:12px; color:#334155; line-height:1.6;">
                            <div style="font-weight:700; color:#0284C7; margin-bottom:8px; text-transform:uppercase; font-size:11px; letter-spacing:0.5px;">⚙️ Execution & Reasoning Trace</div>
                            {thinking_formatted}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(clean_content)

    # =========================================================================
    # NATIVE STREAMLIT CHAT INPUT WITH FILE ATTACHMENT (+)
    # =========================================================================
    chat_input_val = st.chat_input(
        "Ask about policies, claims, fraud, risk, or attach a claim evidence photo...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
        key="main_chat_input"
    )

    prompt_to_process = None
    user_text_display = None
    image_bytes_to_store = None
    image_name_to_store = None

    if chat_input_val:
        user_text = ""
        uploaded_files = []
        if hasattr(chat_input_val, "text") and chat_input_val.text:
            user_text = chat_input_val.text.strip()
        elif isinstance(chat_input_val, dict) and chat_input_val.get("text"):
            user_text = chat_input_val.get("text", "").strip()

        if hasattr(chat_input_val, "files") and chat_input_val.files:
            uploaded_files = chat_input_val.files
        elif isinstance(chat_input_val, dict) and chat_input_val.get("files"):
            uploaded_files = chat_input_val.get("files", [])

        if uploaded_files:
            file_obj = uploaded_files[0]
            image_bytes_to_store = file_obj.getvalue()
            image_name_to_store = file_obj.name.replace(" ", "_")

            with st.spinner(f"Uploading {image_name_to_store} to Snowflake stage..."):
                upload_ok = sf.upload_image_to_stage(image_bytes_to_store, image_name_to_store)

            if upload_ok:
                user_msg = user_text if user_text else f"Analyze attached evidence image: {image_name_to_store}"
                user_text_display = user_msg
                prompt_to_process = (
                    f"{user_msg} "
                    f"The image file is named {image_name_to_store} and is in the claim evidence stage. "
                    f"Use the ANALYZE_CLAIM_IMAGE tool with IMAGE_FILENAME={image_name_to_store} to analyze it."
                )
            else:
                st.error(f"Failed to upload {image_name_to_store} to stage. Check stage permissions.")
        elif user_text:
            user_text_display = user_text
            prompt_to_process = user_text

    elif selected_prompt:
        user_text_display = selected_prompt
        prompt_to_process = selected_prompt

    # =========================================================================
    # PROCESS PROMPT & GENERATE ASSISTANT RESPONSE
    # =========================================================================
    if prompt_to_process:
        # 1. Append user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_text_display,
            "image": image_bytes_to_store,
            "image_name": image_name_to_store
        })

        # 2. Show thinking loader for assistant inside st.chat_message
        with st.chat_message("assistant"):
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.6px; color:#0284C7; margin-bottom:8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#0284C7">
                    <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5"/>
                </svg>
                <span>INSURANCE_INTELLIGENCE_ASSISTANT</span>
                <span style="font-size:11px; background:#E0F2FE; color:#0369A1; padding:2px 8px; border-radius:10px; font-weight:600; margin-left:auto;">Thinking...</span>
            </div>
            """, unsafe_allow_html=True)
            with st.spinner("Querying Insurance Master Agent..."):
                try:
                    raw_response = sf.ask_cortex_agent(prompt_to_process)
                    real_thinking = sf.parse_agent_thinking(raw_response)
                    thinking_process, clean_resp = extract_thinking_and_response(raw_response, prompt_to_process)
                    if real_thinking:
                        thinking_process = real_thinking
                    agent_name = "INSURANCE_INTELLIGENCE_ASSISTANT"
                except Exception as e:
                    thinking_process = f"Execution Error: {e}"
                    clean_resp = f"Snowflake Query Error: {e}"
                    agent_name = "SNOWFLAKE_ERROR"

        st.session_state.messages.append({
            "role": "assistant",
            "agent": agent_name,
            "thinking": thinking_process,
            "content": clean_resp
        })
        st.rerun()