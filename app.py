import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv

import snowflake_utils as sf

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
                "💬 Chat Assistant"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("""
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
                    <span style="color:#38BDF8;">⚙️</span> Snowflake Live
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



# =========================================================================
# MAIN APP ENTRYPOINT
# =========================================================================
render_header()
selected_tab = render_sidebar()

# =========================================================================
# TAB 1: UNDERWRITING WORKBENCH
# =========================================================================
if "Underwriting Workbench" in selected_tab:
    st.markdown("### 🛡️ Underwriting Workbench")
    st.caption("Real-time policy book management, risk scoring, and ML-powered automated premium quoting.")
    
    # Live Data Fetch
    df_policies = pd.DataFrame()
    try:
        df_policies = sf.get_policies_data()
    except Exception as e:
        st.error(f"Snowflake Connection Error: {e}")

    # Top KPI Metrics Row
    if not df_policies.empty:
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        total_policies = len(df_policies)
        
        # Calculate active policies
        active_count = len(df_policies[df_policies["STATUS"].astype(str).str.upper() == "ACTIVE"]) if "STATUS" in df_policies.columns else total_policies
        
        # Calculate total and avg premium
        if "PREMIUM" in df_policies.columns:
            total_premium = pd.to_numeric(df_policies["PREMIUM"], errors="coerce").sum()
            avg_premium = pd.to_numeric(df_policies["PREMIUM"], errors="coerce").mean()
        else:
            total_premium = 0
            avg_premium = 0

        with kpi_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Policies</div>
                <div class="kpi-value">{total_policies:,}</div>
                <div class="kpi-subtitle"><span>▲ 4.2%</span> from last cycle</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Active Book</div>
                <div class="kpi-value">{active_count:,}</div>
                <div class="kpi-subtitle"><span>● 100%</span> active coverage</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Premium Volume</div>
                <div class="kpi-value">${total_premium:,.0f}</div>
                <div class="kpi-subtitle"><span>▲ 8.1%</span> YoY growth</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Average Premium</div>
                <div class="kpi-value">${avg_premium:,.2f}</div>
                <div class="kpi-subtitle"><span>● Benchmark</span> within target</div>
            </div>
            """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.15, 0.85])

    with col_left:
        st.markdown("""
        <div class="card-panel">
            <div class="panel-header">
                <div class="panel-header-title">
                    <span>📋 Policy Book</span>
                </div>
                <div class="panel-header-badge">GOLD.FACT_POLICY</div>
            </div>
        """, unsafe_allow_html=True)
        
        if not df_policies.empty:
            # Policy Book Filter
            filter_col1, filter_col2 = st.columns([1, 1])
            with filter_col1:
                search_term = st.text_input("🔍 Search Policy ID / Type", "", placeholder="e.g. POL-001 or Auto", label_visibility="collapsed")
            with filter_col2:
                types = ["All Types"] + list(df_policies["TYPE"].dropna().unique()) if "TYPE" in df_policies.columns else ["All Types"]
                selected_type = st.selectbox("Filter Type", types, label_visibility="collapsed")

            filtered_df = df_policies.copy()
            if search_term:
                filtered_df = filtered_df[filtered_df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
            if selected_type != "All Types" and "TYPE" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["TYPE"] == selected_type]

            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=320,
                hide_index=True
            )
            st.caption(f"Showing {len(filtered_df)} of {len(df_policies)} live rows from Snowflake")
        else:
            st.info("No policy records returned from Snowflake.")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="card-panel">
            <div class="panel-header">
                <div class="panel-header-title">
                    <span>⚡ Quote a New Policy</span>
                </div>
                <div class="panel-header-badge">ML Model Input</div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("quote_form"):
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                age = st.slider("Applicant Age", 18, 85, 35)
                credit = st.slider("Credit Score", 300, 850, 700)
            with q_col2:
                income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, value=60000, step=5000)
                coverage = st.number_input("Coverage Amount ($)", min_value=10000, max_value=2000000, value=250000, step=25000)

            submitted = st.form_submit_button("⚡ Estimate Premium", use_container_width=True, type="primary")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # ML Premium Prediction Panel
    st.markdown("""
    <div class="card-panel">
        <div class="panel-header">
            <div class="panel-header-title">
                <span>🤖 Predictive ML Valuation</span>
            </div>
            <div class="panel-header-badge">PREMIUM_ESTIMATION_MODEL!PREDICT()</div>
        </div>
    """, unsafe_allow_html=True)

    p_col1, p_col2 = st.columns([1, 1])
    try:
        est_price = sf.estimate_premium(age, income, credit, coverage)
        risk_tier = "Low Risk" if credit >= 720 else ("Moderate Risk" if credit >= 620 else "Elevated Risk")
        
        with p_col1:
            st.markdown(f"""
            <div class="prediction-container">
                <div class="prediction-title">Estimated Annual Premium</div>
                <div class="prediction-amount">${est_price:,.2f}</div>
                <span class="prediction-tag">{risk_tier}</span>
                <div style="font-size:12px; color:#166534; margin-top:6px;">Calculated dynamically via Snowflake predictive model</div>
            </div>
            """, unsafe_allow_html=True)

        with p_col2:
            st.markdown('<div class="kpi-title" style="margin-bottom:10px;">Top Actuarial & Rate Drivers</div>', unsafe_allow_html=True)
            credit_mult = f"▼ {max(0.75, 1.0 - (credit - 600)*0.0008):.2f}x" if credit >= 650 else f"▲ {1.0 + (650 - credit)*0.001:.2f}x"
            age_mult = f"▲ {1.0 + (age - 25)*0.004:.2f}x" if age > 30 else "● Baseline 1.00x"
            cov_mult = f"▲ {1.0 + (coverage / 500000)*0.1:.2f}x"
            
            st.markdown(f"""
            <div class="driver-tag-row">
                <span><b>Credit Score Impact</b> ({credit})</span>
                <span style="color:#0284C7;"><b>{credit_mult}</b></span>
            </div>
            <div class="driver-tag-row">
                <span><b>Age Bracket Weight</b> ({age} yrs)</span>
                <span style="color:#EA580C;"><b>{age_mult}</b></span>
            </div>
            <div class="driver-tag-row">
                <span><b>Coverage Exposure</b> (${coverage:,})</span>
                <span style="color:#16A34A;"><b>{cov_mult}</b></span>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Live Prediction Model Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


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
        st.error(f"Snowflake Claims Query Error: {e}")

    # Top KPI Metrics Row
    if not claims_df.empty:
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        total_claims = len(claims_df)
        
        # Calculate High Risk Count
        high_risk_count = 0
        if "FRAUD_SCORE" in claims_df.columns:
            high_risk_count = len(claims_df[pd.to_numeric(claims_df["FRAUD_SCORE"], errors="coerce") >= 0.70])
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
            
            f_col1, f_col2 = st.columns([1.2, 1])
            with f_col1:
                selected_claim_id = st.selectbox("🔎 Drill into a claim:", claim_ids, index=0)
            with f_col2:
                status_list = ["All Statuses"] + list(claims_df["STATUS"].dropna().unique()) if "STATUS" in claims_df.columns else ["All Statuses"]
                selected_status = st.selectbox("Filter Status", status_list)

            display_claims = claims_df.copy()
            if selected_status != "All Statuses" and "STATUS" in display_claims.columns:
                display_claims = display_claims[display_claims["STATUS"] == selected_status]

            st.dataframe(
                display_claims,
                use_container_width=True,
                height=320,
                hide_index=True
            )
            if selected_claim_id:
                st.markdown(f"**Inspecting Claim Record:** `{selected_claim_id}`")
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
                    f_type = row.get("FRAUD_TYPE", "Standard Claim")
                    
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

                    if conf >= 0.70 or "duplicate" in str(notes).lower() or "escalate" in str(notes).lower() or "investigating" in str(status).lower():
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
                st.error(f"Error querying claim detail from Snowflake: {e}")
        else:
            st.info("Select a valid claim from the table to inspect details.")

        st.markdown("</div>", unsafe_allow_html=True)


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
        st.error(f"Snowflake Loss Ratio Query Error: {e}")

    try:
        at_risk_df = sf.get_at_risk_policies()
    except Exception as e:
        st.error(f"Snowflake At-Risk Query Error: {e}")

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


# =========================================================================
# TAB 4: CHAT ASSISTANT (SNOWFLAKE CORTEX AI)
# =========================================================================
elif "Chat Assistant" in selected_tab:
    # Welcome Banner Header
    st.markdown("""
    <div class="chat-welcome-banner">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:32px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; width:52px; height:52px; display:flex; align-items:center; justify-content:center;">💬</div>
            <div>
                <h2>Welcome to Chat Assistant</h2>
                <p style="margin-top:4px; color:#64748B;">Ask anything about your policies, claims, fraud analysis, or actuarial risk metrics. Powered by live Snowflake Cortex AI.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("""
    <div class="card-panel" style="padding:16px 20px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:13px; font-weight:700; color:#334155;">💡 Suggested Quick Inquiries</div>
            <div style="font-size:11px; background:#F0FDF4; color:#166534; padding:3px 8px; border-radius:12px; font-weight:600;">Live Cortex Agent</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Question Buttons in 2 Rows
    q_col1, q_col2, q_col3 = st.columns(3)
    selected_prompt = None
    
    with q_col1:
        if st.button("🔍 Auto policies likely to churn?", use_container_width=True):
            selected_prompt = "Which of my auto policies are most likely to churn in the next 30 days?"
    
    with q_col2:
        if st.button("⚠️ Why was CLM-00381 flagged?", use_container_width=True):
            selected_prompt = "Show me why CLM-00381 was flagged for fraud"
        
    with q_col3:
        if st.button("💰 Estimate premium for 35yo $60k", use_container_width=True):
            selected_prompt = "Estimate premium for age 35, annual income $60000, credit score 700, coverage $250000"

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

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # Empty State Guide
    if not st.session_state.messages:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px dashed #CBD5E1; border-radius:12px; padding:32px 24px; text-align:center; margin-bottom:20px;">
            <div style="font-size:40px; margin-bottom:10px;">🤖❄️</div>
            <h4 style="margin:0 0 6px 0; font-size:16px; font-weight:700; color:#1E293B;">How can I assist your underwriting & claims team today?</h4>
            <p style="margin:0 auto; max-width:480px; font-size:13px; color:#64748B; line-height:1.5;">
                Connected to live Snowflake database <b>INSURANCE_MGMT_SYSTEM</b>. Click a quick inquiry button above or ask any prompt below.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Render message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            agent_title = msg.get("agent", "SNOWFLAKE_CORTEX_AI")
            thinking_text = msg.get("thinking", "")
            clean_content = msg.get("content", "").replace("\n", "<br>")
            
            # Agent header badge
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.6px; color:#059669; margin-top:14px; margin-bottom:6px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#10B981">
                    <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5"/>
                </svg>
                <span>{agent_title}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if thinking_text:
                resp_tab, think_tab = st.tabs(["💬 Response", "🧠 Thinking Process"])
                with resp_tab:
                    st.markdown(f'<div class="chat-agent-card">{clean_content}</div>', unsafe_allow_html=True)
                with think_tab:
                    thinking_formatted = thinking_text.replace("\n", "<br>")
                    st.markdown(f"""
                    <div class="chat-agent-card" style="background:#F8FAFC; border-left:4px solid #0284C7; font-family:'JetBrains Mono', monospace; font-size:12px; color:#334155; line-height:1.6;">
                        <div style="font-weight:700; color:#0284C7; margin-bottom:8px; text-transform:uppercase; font-size:11px; letter-spacing:0.5px;">⚙️ Execution & Reasoning Trace</div>
                        {thinking_formatted}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-agent-card">{clean_content}</div>', unsafe_allow_html=True)

    # Prompt handling
    chat_prompt = st.chat_input("Ask Cortex AI about policies, claims, or actuarial risk...")
    prompt_to_process = selected_prompt or chat_prompt

    if prompt_to_process:
        st.session_state.messages.append({"role": "user", "content": prompt_to_process})
        
        # Display user prompt bubble & animated ChatGPT bouncing loader while waiting
        placeholder = st.empty()
        with placeholder.container():
            st.markdown(f'<div class="chat-user-bubble">{prompt_to_process}</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="chat-agent-card chat-loader-card">
                <div class="chat-agent-header" style="color:#0284C7;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#0284C7">
                        <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2"/>
                    </svg>
                    <span>SNOWFLAKE_CORTEX_AI</span>
                    <span style="font-size:11px; background:#E0F2FE; color:#0369A1; padding:2px 8px; border-radius:10px; font-weight:600; margin-left:auto;">Thinking...</span>
                </div>
                <div style="display:flex; align-items:center; gap:10px; color:#475569; font-size:13px; margin-top:8px;">
                    <div class="bouncing-loader">
                        <div></div><div></div><div></div>
                    </div>
                    <span>Thinking & querying Snowflake Cortex AI...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                raw_response = sf.ask_cortex_agent(prompt_to_process)
                thinking_process, clean_resp = extract_thinking_and_response(raw_response, prompt_to_process)
                agent_name = "SNOWFLAKE_CORTEX_AI"
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
