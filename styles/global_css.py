import streamlit as st


def inject_global_css():
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


