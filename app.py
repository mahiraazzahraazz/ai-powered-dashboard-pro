import html
import io
import os
import time
import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

                                       
                                   
                                       
st.set_page_config(
    page_title="AI-Powered Dashboard Pro",
    page_icon=":material/monitoring:",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

LOTTIE_LOADER_URL = (
    "https://lottie.host/871a30fc-e6b8-4b22-b6c7-5a0bd4d05c45/o86qS3h0tz.lottie"
)

                                       
                                               
                                       
THEMES = {
    "Midnight Emerald": {
        "bg": "#0D1312",
        "surface": "#131C1A",
        "surface_alt": "#1A2623",
        "border": "#253531",
        "text": "#F1F5F4",
        "muted": "#93A39F",
        "accent": "#10B981",
        "accent_soft": "rgba(16, 185, 129, 0.15)",
        "grid": "rgba(147, 163, 159, 0.12)",
        "plotly_tpl": "plotly_dark",
        "palette": ["#10B981", "#3B82F6", "#F59E0B", "#14B8A6", "#8B5CF6", "#EC4899"],
    },
    "Carbon Graphite": {
        "bg": "#111317",
        "surface": "#181B20",
        "surface_alt": "#1F242C",
        "border": "#2A303B",
        "text": "#F3F4F6",
        "muted": "#9CA3AF",
        "accent": "#3B82F6",
        "accent_soft": "rgba(59, 130, 246, 0.14)",
        "grid": "rgba(156, 163, 175, 0.12)",
        "plotly_tpl": "plotly_dark",
        "palette": ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#06B6D4"],
    },
    "Obsidian Indigo": {
        "bg": "#0F1016",
        "surface": "#161822",
        "surface_alt": "#1E2130",
        "border": "#2B2F42",
        "text": "#F4F4F6",
        "muted": "#9CA3B8",
        "accent": "#6366F1",
        "accent_soft": "rgba(99, 102, 241, 0.16)",
        "grid": "rgba(156, 163, 184, 0.12)",
        "plotly_tpl": "plotly_dark",
        "palette": ["#6366F1", "#38BDF8", "#10B981", "#F59E0B", "#F43F5E", "#A78BFA"],
    },
    "Steel Slate": {
        "bg": "#161B22",
        "surface": "#1D242D",
        "surface_alt": "#252E3A",
        "border": "#303B4A",
        "text": "#F0F6FC",
        "muted": "#8B949E",
        "accent": "#0EA5E9",
        "accent_soft": "rgba(14, 165, 233, 0.15)",
        "grid": "rgba(139, 148, 158, 0.13)",
        "plotly_tpl": "plotly_dark",
        "palette": ["#0EA5E9", "#2DD4BF", "#A78BFA", "#FBBF24", "#FB7185", "#60A5FA"],
    },
}

                                     
ICON_BAR_CHART = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/>'
    '<line x1="6" y1="20" x2="6" y2="16"/></svg>'
)
ICON_LAYERS = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/>'
    '<polyline points="2 12 12 17 22 12"/></svg>'
)
ICON_TREND = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>'
)
ICON_AWARD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>'
)
ICON_ACTIVITY = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
)
ICON_FILE_TEXT = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
    '<polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/>'
    '<line x1="16" y1="17" x2="8" y2="17"/></svg>'
)
ICON_CPU = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/>'
    '<line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/>'
    '<line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/>'
    '<line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/>'
    '<line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>'
)
ICON_UPLOAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
    '<polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
)
ICON_USERS = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
    '<circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'
    '<path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
)
ICON_TROPHY = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>'
    '<path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>'
    '<path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>'
    '<path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>'
)
ICON_PALETTE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/>'
    '<circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/>'
    '<path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>'
)
ICON_KEY = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/></svg>'
)
ICON_DATABASE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/>'
    '<path d="M3 12a9 3 0 0 0 18 0"/></svg>'
)

def inject_theme_css(t: dict) -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            --bg: {t["bg"]};
            --surface: {t["surface"]};
            --surface-alt: {t["surface_alt"]};
            --border: {t["border"]};
            --text: {t["text"]};
            --muted: {t["muted"]};
            --accent: {t["accent"]};
            --accent-soft: {t["accent_soft"]};
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: var(--text);
        }}

        
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }}
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        [data-testid="stDeployButton"],
        #MainMenu,
        footer {{
            display: none !important;
        }}

        
        section[data-testid="stSidebar"] {{
            background-color: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
        }}
        .sidebar-head {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--muted);
            margin: 0.15rem 0 0.65rem 0;
        }}
        .sidebar-head svg {{
            color: var(--accent);
            flex-shrink: 0;
        }}
        .sidebar-erde {{
            margin-top: 1.75rem;
            padding-top: 0.85rem;
            border-top: 1px solid var(--border);
            text-align: center;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.28em;
            text-transform: lowercase;
            color: var(--muted);
            opacity: 0.38;
            transition: opacity 200ms ease;
            user-select: none;
        }}
        .sidebar-erde:hover {{
            opacity: 0.78;
        }}

        .block-container {{
            padding-top: 2.2rem;
            padding-bottom: 2.2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1440px;
        }}

        
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        .stTextInput input,
        .stDateInput input {{
            background-color: var(--surface-alt) !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
        }}
        .stButton > button,
        [data-testid="stPopover"] > button {{
            transition: transform 120ms ease, border-color 180ms ease, background-color 180ms ease;
            border-radius: 10px !important;
        }}
        .stButton > button:active,
        [data-testid="stPopover"] > button:active {{
            transform: scale(0.985);
        }}
        .stButton > button[kind="primary"] {{
            background-color: var(--accent) !important;
            border-color: var(--accent) !important;
            color: #FFFFFF !important;
            font-weight: 600;
        }}
        .stButton > button[kind="secondary"],
        [data-testid="stPopover"] > button {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
        }}
        .stButton > button[kind="secondary"]:hover,
        [data-testid="stPopover"] > button:hover {{
            border-color: var(--accent) !important;
            color: var(--accent) !important;
        }}

        
        .topbar-wrap {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 1rem;
            overflow: hidden;
        }}
        .topbar {{
            padding: 1.05rem 1.35rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }}
        .brand-mark {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: var(--accent-soft);
            border: 1px solid var(--accent);
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .topbar-title {{
            font-size: 1.3rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
            margin: 0;
            line-height: 1.25;
        }}
        .topbar-sub {{
            font-size: 0.83rem;
            color: var(--muted);
            margin: 0.12rem 0 0 0;
        }}
        .badge-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }}
        .pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.77rem;
            font-weight: 600;
            padding: 0.34rem 0.75rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: var(--surface-alt);
            color: var(--text);
        }}
        .dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }}
        .dot-green {{ background: #10B981; }}
        .dot-amber {{ background: #F59E0B; }}
        .dot-accent {{ background: var(--accent); }}

        
        .topbar-team {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.65rem;
            padding: 0.6rem 1.35rem;
            background: var(--surface-alt);
            border-top: 1px solid var(--border);
        }}
        .team-label {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.71rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
            margin-right: 0.25rem;
        }}
        .team-label svg {{ color: var(--accent); }}
        .member-chip {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.79rem;
            font-weight: 600;
            color: var(--text);
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 0.22rem 0.65rem 0.22rem 0.26rem;
            border-radius: 999px;
        }}
        .member-avatar {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--accent-soft);
            color: var(--accent);
            border: 1px solid var(--accent);
            font-size: 0.64rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}

        
        @keyframes fadeSlideUp {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
            margin-bottom: 1.15rem;
        }}
        .kpi-card {{
            position: relative;
            overflow: hidden;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            animation: fadeSlideUp 240ms cubic-bezier(0.2, 0, 0, 1) both;
            transition: border-color 180ms cubic-bezier(0.2, 0, 0, 1), background-color 180ms ease;
        }}
        .kpi-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: var(--accent);
            opacity: 0;
            transition: opacity 180ms ease;
        }}
        .kpi-card:hover {{
            border-color: var(--accent);
            background: var(--surface-alt);
        }}
        .kpi-card:hover::before {{ opacity: 1; }}
        .kpi-card:hover .kpi-icon {{ transform: scale(1.06); }}
        .kpi-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .kpi-label {{
            font-size: 0.74rem;
            font-weight: 600;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .kpi-icon {{
            color: var(--accent);
            background: var(--accent-soft);
            width: 28px;
            height: 28px;
            border-radius: 7px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 180ms cubic-bezier(0.2, 0, 0, 1);
        }}
        .kpi-value {{
            font-size: 1.45rem;
            font-weight: 700;
            color: var(--text);
            line-height: 1.2;
            font-variant-numeric: tabular-nums;
            word-break: break-word;
        }}
        .kpi-meta {{
            font-size: 0.79rem;
            color: var(--muted);
            margin-top: 0.3rem;
        }}

        
        .panel-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.15rem 1.25rem;
            margin-bottom: 0.9rem;
            animation: fadeSlideUp 260ms cubic-bezier(0.2, 0, 0, 1) both;
        }}
        .panel-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.92rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 0.8rem;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid var(--border);
        }}
        .panel-header svg {{ color: var(--accent); }}

        
        .rank-row {{
            margin-bottom: 0.72rem;
        }}
        .rank-row:last-child {{
            margin-bottom: 0;
        }}
        .rank-top {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: 0.82rem;
            margin-bottom: 0.28rem;
        }}
        .rank-name {{
            font-weight: 600;
            color: var(--text);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 62%;
        }}
        .rank-val {{
            font-variant-numeric: tabular-nums;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 500;
        }}
        .rank-track {{
            width: 100%;
            height: 6px;
            background: var(--surface-alt);
            border-radius: 999px;
            overflow: hidden;
        }}
        .rank-fill {{
            height: 100%;
            border-radius: 999px;
            background: var(--accent);
        }}

        
        .upload-intro {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 0.9rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .upload-icon-box {{
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background: var(--accent-soft);
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .upload-intro h3 {{
            margin: 0;
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text);
        }}
        .upload-intro p {{
            margin: 0.2rem 0 0 0;
            font-size: 0.86rem;
            color: var(--muted);
        }}

        
        [data-testid="stFileUploader"] section {{
            background-color: var(--surface) !important;
            border: 1.5px dashed var(--border) !important;
            border-radius: 12px;
            padding: 1rem;
            color: var(--text) !important;
        }}
        [data-testid="stFileUploader"] section:hover {{
            border-color: var(--accent) !important;
        }}

        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.25rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 0.85rem;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--muted);
            padding: 0.55rem 1rem;
        }}
        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
        }}

        
        .stElementContainer:has(.center-loader-anchor) {{
            display: none !important;
        }}
        .stElementContainer:has(.center-loader-anchor) + .stElementContainer iframe {{
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 99999 !important;
            background: rgba(10, 12, 16, 0.72) !important;
            backdrop-filter: blur(6px);
        }}

        
        @media (max-width: 1024px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}
        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 1.5rem;
                padding-left: 0.85rem;
                padding-right: 0.85rem;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.6rem;
            }}
            .kpi-card {{ padding: 0.8rem 0.85rem; }}
            .kpi-label {{ font-size: 0.68rem; }}
            .kpi-value {{ font-size: 1.12rem; }}
            .kpi-meta {{ font-size: 0.72rem; }}
            .topbar {{ padding: 0.9rem 1rem; }}
            .topbar-team {{ padding: 0.55rem 1rem; }}
            .topbar-title {{ font-size: 1.12rem; }}
        }}

        
        @media print {{
            @page {{ size: A4 portrait; margin: 10mm; }}
            section[data-testid="stSidebar"],
            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stFileUploader"],
            [data-testid="stChatInput"],
            [data-testid="stPopover"],
            [role="tablist"],
            .stTabs [data-baseweb="tab-list"],
            .stButton,
            .stDownloadButton,
            .badge-group {{
                display: none !important;
            }}
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            body {{
                background: #FFFFFF !important;
                color: #0F172A !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            .block-container {{
                padding: 0 !important;
                max-width: 100% !important;
                width: 100% !important;
            }}
            .topbar-wrap, .kpi-card, .panel-card {{
                background: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                color: #0F172A !important;
                break-inside: avoid;
            }}
            .topbar-team {{
                background: #F8FAFC !important;
                border-top: 1px solid #CBD5E1 !important;
            }}
            .member-chip {{
                background: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                color: #0F172A !important;
            }}
            .member-avatar {{
                background: #EFF6FF !important;
                color: #2563EB !important;
                border-color: #2563EB !important;
            }}
            .topbar-title, .kpi-value, .panel-header, .rank-name {{
                color: #0F172A !important;
            }}
            .topbar-sub, .kpi-label, .kpi-meta, .team-label, .rank-val {{
                color: #475569 !important;
            }}
            [data-testid="stHorizontalBlock"] {{ display: block !important; }}
            [data-testid="column"],
            [data-testid="stColumn"] {{
                width: 100% !important;
                max-width: 100% !important;
                flex: 1 1 100% !important;
            }}
            .js-plotly-plot, .plot-container, .svg-container {{
                width: 100% !important;
                max-width: 100% !important;
            }}
            [data-testid="stPlotlyChart"] {{
                border: 1px solid #CBD5E1 !important;
                border-radius: 10px;
                padding: 4px;
                margin-bottom: 12px;
                break-inside: avoid;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_robot_loader(slot, label: str, t: dict) -> None:
    with slot.container():
        st.markdown('<div class="center-loader-anchor"></div>', unsafe_allow_html=True)
        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
            <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
            <style>
              html, body {{
                margin: 0; padding: 0; width: 100%; height: 100%;
                background: transparent;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                display: flex; align-items: center; justify-content: center;
              }}
              .loader-card {{
                width: 90%;
                max-width: 380px;
                background: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 16px;
                padding: 24px 28px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-sizing: border-box;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
              }}
              .loader-label {{
                margin-top: 6px;
                font-size: 14px;
                font-weight: 600;
                color: {t["text"]};
              }}
              .loader-track {{
                width: 72%;
                height: 4px;
                background: {t["surface_alt"]};
                border-radius: 999px;
                overflow: hidden;
                margin-top: 10px;
              }}
              .loader-bar {{
                width: 45%;
                height: 100%;
                background: {t["accent"]};
                border-radius: 999px;
                animation: slide 1.2s ease-in-out infinite;
              }}
              @keyframes slide {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(230%); }}
              }}
            </style>
            </head>
            <body>
              <div class="loader-card">
                <dotlottie-player
                  src="{LOTTIE_LOADER_URL}"
                  background="transparent"
                  speed="1"
                  style="width: 145px; height: 145px;"
                  loop
                  autoplay>
                </dotlottie-player>
                <div class="loader-label">{html.escape(label)}</div>
                <div class="loader-track"><div class="loader-bar"></div></div>
              </div>
            </body>
            </html>
            """,
            height=235,
        )

def resolve_groq_api_key(manual_key: str) -> str:
    if manual_key:
        return manual_key.strip()
    env_key = os.getenv("GROQ_API_KEY", "").strip()
    if env_key:
        return env_key
    try:
        return str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except Exception:
        return ""

def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'

def format_compact(value: float) -> str:
    abs_val = abs(value)
    if abs_val >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f} M"
    if abs_val >= 1_000_000:
        return f"{value / 1_000_000:,.2f} Jt"
    return f"{value:,.0f}"

def detect_date_column(df: pd.DataFrame) -> str | None:
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col
        if any(k in col.lower() for k in ("date", "tanggal", "tgl", "bulan", "month")):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.7:
                df[col] = parsed
                return col
    return None

def style_plotly(fig, title: str, t: dict, height: int = 360):
    fig.update_layout(
        template=t["plotly_tpl"],
        title=dict(text=title, font=dict(size=14, color=t["text"])),
        paper_bgcolor=t["surface"],
        plot_bgcolor=t["surface"],
        font=dict(family="Inter, sans-serif", color=t["muted"], size=12),
        margin=dict(l=16, r=16, t=46, b=16),
        height=height,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5
        ),
        hoverlabel=dict(
            bgcolor=t["surface_alt"], font_color=t["text"], bordercolor=t["accent"]
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=t["border"], zeroline=False)
    fig.update_yaxes(gridcolor=t["grid"], zeroline=False)
    return fig

def load_dataset_smart(file_source, filename: str) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(file_source)
    else:
        df = pd.read_excel(file_source)
        unnamed_ratio = sum(str(c).startswith("Unnamed:") for c in df.columns) / max(
            len(df.columns), 1
        )
        if unnamed_ratio >= 0.4 and not df.empty:
            if hasattr(file_source, "seek"):
                file_source.seek(0)
            preview = pd.read_excel(file_source, header=None, nrows=12)
            best_row = int(preview.notna().sum(axis=1).idxmax())
            if hasattr(file_source, "seek"):
                file_source.seek(0)
            df = pd.read_excel(file_source, header=best_row)

    df = df.dropna(how="all").dropna(axis=1, how="all")
    df.columns = [str(c).strip() for c in df.columns]

    for col in df.columns:
        if df[col].dtype == object:
            s = df[col].dropna().astype(str).str.strip()
            if s.empty:
                continue
            cleaned = (
                s.str.replace(r"(?i)rp\.?\s*", "", regex=True)
                .str.replace(r"\s+", "", regex=True)
            )
            is_id_num = (
                cleaned.str.match(r"^-?\d{1,3}(\.\d{3})+(,\d+)?$").mean() > 0.7
            )
            if is_id_num:
                cleaned = cleaned.str.replace(".", "", regex=False).str.replace(
                    ",", ".", regex=False
                )
            else:
                cleaned = cleaned.str.replace(",", "", regex=False)
            parsed = pd.to_numeric(cleaned, errors="coerce")
            if parsed.notna().mean() > 0.75:
                full_series = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .str.replace(r"(?i)rp\.?\s*", "", regex=True)
                    .str.replace(r"\s+", "", regex=True)
                )
                if is_id_num:
                    full_series = full_series.str.replace(
                        ".", "", regex=False
                    ).str.replace(",", ".", regex=False)
                else:
                    full_series = full_series.str.replace(",", "", regex=False)
                df[col] = pd.to_numeric(full_series, errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_dataset_cached(file_bytes: bytes, filename: str) -> pd.DataFrame:
    return load_dataset_smart(io.BytesIO(file_bytes), filename)

def pick_default_category(df: pd.DataFrame, categorical_cols: list[str]) -> int:
    if "Region" in categorical_cols:
        return categorical_cols.index("Region")
    for idx, col in enumerate(categorical_cols):
        low = col.lower()
        if low == "id" or low.endswith("_id") or "transaction" in low:
            continue
        nunique = df[col].nunique(dropna=True)
        if 2 <= nunique <= 50:
            return idx
    for idx, col in enumerate(categorical_cols):
        if 2 <= df[col].nunique(dropna=True) <= 50:
            return idx
    return 0

@st.cache_data(ttl=300, show_spinner=False)
def fetch_groq_models(api_key: str) -> list[str]:
    fallback = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]
    if not api_key:
        return fallback
    try:
        from groq import Groq

        tmp_client = Groq(api_key=api_key)
        models = tmp_client.models.list().data
        excluded = ("whisper", "guard", "tts", "playai", "safeguard")
        ids = sorted(
            m.id for m in models if not any(ex in m.id.lower() for ex in excluded)
        )
        return ids if ids else fallback
    except Exception:
        return fallback

def summarize_agg_for_llm(
    grouped_df: pd.DataFrame, cat_col: str, num_col: str, max_rows: int = 15
) -> str:
    total_rows = len(grouped_df)
    if total_rows <= max_rows:
        return grouped_df.to_string(index=False)
    head_part = grouped_df.head(max_rows).to_string(index=False)
    tail_part = grouped_df.tail(3).to_string(index=False)
    return (
        f"Total {total_rows} {cat_col}. Menampilkan Top {max_rows}:\n"
        f"{head_part}\n\n3 {cat_col} Terendah:\n{tail_part}"
    )

def trim_messages(messages: list[dict], max_history: int = 6) -> list[dict]:
    system_msgs = [m for m in messages if m.get("role") == "system"]
    other_msgs = [m for m in messages if m.get("role") != "system"]
    return system_msgs[:1] + other_msgs[-max_history:]

def chat_with_fallback(
    client, preferred_model: str, available_models: list[str], messages: list[dict]
) -> tuple[str, str]:
    candidates = [preferred_model] + [m for m in available_models if m != preferred_model]
    trimmed = trim_messages(messages, max_history=6)
    last_err = None
    for model_id in candidates:
        for attempt_msgs in (trimmed, trim_messages(messages, max_history=2)):
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=attempt_msgs,
                    temperature=0.7,
                    max_tokens=1024,
                )
                return response.choices[0].message.content, model_id
            except Exception as e:
                last_err = e
                err_str = str(e).lower()
                if "context_length_exceeded" in err_str or "reduce the length" in err_str:
                    continue
                if "404" in err_str or "model_not_found" in err_str or "does not exist" in err_str:
                    break
                raise
    raise RuntimeError(last_err)

def generate_ai_commentary(
    grouped_df: pd.DataFrame,
    cat_col: str,
    num_col: str,
    model_name: str,
    available_models: list[str],
    client,
) -> str:
    if not client:
        return "Analisis AI belum aktif karena `GROQ_API_KEY` belum diatur."

    text_summary = summarize_agg_for_llm(grouped_df, cat_col, num_col)
    prompt = f"""
Berikut adalah ringkasan data {num_col} per {cat_col}:
{text_summary}

Buat analisis bisnis singkat dalam bahasa Indonesia yang profesional tanpa emoji:
1. {cat_col} Dominan: sebutkan kontribusinya.
2. {cat_col} Perlu Perhatian: sebutkan yang tertinggal & kemungkinan faktornya.
3. Rekomendasi Aksi: 2-3 langkah konkret yang bisa langsung dieksekusi.
"""
    try:
        text, used_model = chat_with_fallback(
            client, model_name, available_models, [{"role": "user", "content": prompt}]
        )
        if used_model != model_name:
            return f"{text}\n\n*Catatan: otomatis dialihkan ke model `{used_model}`.*"
        return text
    except Exception as e:
        return f"Terjadi kendala saat memanggil Groq AI: {e}"

def build_printable_report_html(
    source_name: str,
    cat_col: str,
    num_col: str,
    total_sum: float,
    avg_val: float,
    top_cat: str,
    top_value: float,
    top_share: float,
    bottom_cat: str,
    bottom_value: float,
    gap_value: float,
    agg_df: pd.DataFrame,
    ai_text: str,
) -> bytes:
    table_html = agg_df.to_html(index=False, border=0, classes="report-table")
    ai_html = html.escape(ai_text).replace("\n", "<br>")
    doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Laporan Analisis — {html.escape(source_name)}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; margin: 28px auto; max-width: 900px; line-height: 1.55; }}
  .head {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0F172A; padding-bottom: 12px; margin-bottom: 18px; }}
  .head h1 {{ margin: 0; font-size: 20px; }}
  .meta {{ font-size: 12px; color: #475569; margin-top: 4px; }}
  .print-btn {{ background: #2563EB; color: #fff; border: none; padding: 8px 14px; border-radius: 6px; font-weight: 600; cursor: pointer; }}
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }}
  .kpi {{ border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px 12px; }}
  .kpi-l {{ font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 600; }}
  .kpi-v {{ font-size: 18px; font-weight: 700; margin-top: 4px; }}
  .box {{ border: 1px solid #CBD5E1; border-radius: 8px; padding: 14px 16px; margin-bottom: 16px; }}
  .box h2 {{ margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase; color: #334155; }}
  .report-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .report-table th, .report-table td {{ border-bottom: 1px solid #E2E8F0; padding: 8px 10px; text-align: left; }}
  .report-table th {{ background: #F8FAFC; font-weight: 600; }}
  @media print {{ .print-btn {{ display: none; }} body {{ margin: 10px; }} }}
</style>
</head>
<body>
  <div class="head">
    <div>
      <h1>Laporan Analisis — AI-Powered Dashboard Pro</h1>
      <div class="meta">Dataset: <strong>{html.escape(source_name)}</strong> | Dimensi: {html.escape(cat_col)} &times; {html.escape(num_col)} | Kelompok: <strong>Mahira Azzahra &amp; Adelia Amanta Wada</strong></div>
    </div>
    <button class="print-btn" onclick="window.print()">Cetak / Simpan PDF</button>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="kpi-l">Total {html.escape(num_col)}</div><div class="kpi-v">{total_sum:,.0f}</div></div>
    <div class="kpi"><div class="kpi-l">Rata-rata / {html.escape(cat_col)}</div><div class="kpi-v">{avg_val:,.0f}</div></div>
    <div class="kpi"><div class="kpi-l">Performa Tertinggi</div><div class="kpi-v">{html.escape(top_cat)} ({top_share:.1f}%)</div></div>
    <div class="kpi"><div class="kpi-l">Selisih Tertinggi - Terendah</div><div class="kpi-v">{gap_value:,.0f}</div></div>
  </div>
  <div class="box">
    <h2>Ringkasan Statistik (Otomatis)</h2>
    <ul>
      <li><strong>Tertinggi:</strong> {html.escape(top_cat)} ({top_value:,.0f})</li>
      <li><strong>Terendah:</strong> {html.escape(bottom_cat)} ({bottom_value:,.0f})</li>
      <li><strong>Selisih:</strong> {gap_value:,.0f}</li>
    </ul>
  </div>
  <div class="box">
    <h2>Analisis Strategis AI</h2>
    <div>{ai_html}</div>
  </div>
  <div class="box">
    <h2>Tabel Ringkasan Performa</h2>
    {table_html}
  </div>
</body>
</html>"""
    return doc.encode("utf-8")

def sidebar_heading(icon_svg: str, title: str) -> None:
    st.markdown(
        f'<div class="sidebar-head">{icon_svg}<span>{html.escape(title)}</span></div>',
        unsafe_allow_html=True,
    )

                                       
                      
                                       
if "selected_theme_name" not in st.session_state:
    st.session_state.selected_theme_name = "Midnight Emerald"
if "manual_api_key" not in st.session_state:
    st.session_state.manual_api_key = ""
if "upload_gen" not in st.session_state:
    st.session_state.upload_gen = 0

with st.sidebar:
    sidebar_heading(ICON_PALETTE, "Tampilan & Tema")
    selected_theme_name = st.selectbox(
        "Pilih Tema Dashboard",
        options=list(THEMES.keys()),
        key="selected_theme_name",
    )

active_theme = THEMES[selected_theme_name]
PALETTE = active_theme["palette"]
inject_theme_css(active_theme)

global_loader = st.empty()
if "app_booted" not in st.session_state:
    render_robot_loader(
        global_loader, "Menyiapkan AI-Powered Dashboard Pro...", active_theme
    )
    time.sleep(4.6)
    global_loader.empty()
    st.session_state.app_booted = True

with st.sidebar:
    st.divider()
    sidebar_heading(ICON_KEY, "Pengaturan AI")
    manual_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        key="manual_api_key",
        help="Kosongkan jika sudah diatur di .env atau Streamlit Secrets.",
    )

GROQ_API_KEY = resolve_groq_api_key(manual_api_key)
available_models = fetch_groq_models(GROQ_API_KEY)
if "selected_model" not in st.session_state or st.session_state.selected_model not in available_models:
    st.session_state.selected_model = available_models[0]

with st.sidebar:
    selected_model = st.selectbox(
        "Model AI",
        options=available_models,
        key="selected_model",
        help="Daftar model otomatis diambil dari akun Groq Anda.",
    )

if GROQ_API_KEY:
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

with st.sidebar:
    st.divider()
    sidebar_heading(ICON_DATABASE, "Sumber Data")
    sidebar_file = st.file_uploader(
        "Upload / Ganti file Excel atau CSV",
        type=["xlsx", "xls", "csv"],
        key=f"sidebar_uploader_{st.session_state.upload_gen}",
    )
    if "uploaded_bytes" in st.session_state:
        if st.button(
            "Kembali ke Halaman Awal",
            icon=":material/arrow_back:",
            width="stretch",
        ):
            for k in (
                "uploaded_bytes",
                "uploaded_name",
                "analysis_key",
                "ai_text",
                "chat_history",
            ):
                st.session_state.pop(k, None)
            st.session_state.upload_gen += 1
            st.rerun()

if sidebar_file is not None:
    st.session_state["uploaded_bytes"] = sidebar_file.getvalue()
    st.session_state["uploaded_name"] = sidebar_file.name

df = None
source_name = ""
if "uploaded_bytes" in st.session_state and "uploaded_name" in st.session_state:
    source_name = st.session_state["uploaded_name"]
    render_robot_loader(global_loader, f"Membaca dataset {source_name}...", active_theme)
    df = load_dataset_cached(st.session_state["uploaded_bytes"], source_name)
    global_loader.empty()

topbar_slot = st.empty()

def render_topbar(slot, source_name: str, df_obj, client_obj) -> None:
    ai_pill = (
        '<span class="pill"><span class="dot dot-green"></span>Groq AI Aktif</span>'
        if client_obj
        else '<span class="pill"><span class="dot dot-amber"></span>Mode Rule-Based</span>'
    )
    data_pill = (
        f'<span class="pill"><span class="dot dot-accent"></span>{html.escape(source_name)} ({len(df_obj):,} baris)</span>'
        if df_obj is not None
        else '<span class="pill">Belum ada dataset</span>'
    )
    slot.markdown(
        f"""
        <div class="topbar-wrap">
            <div class="topbar">
                <div class="topbar-left">
                    <div class="brand-mark">{ICON_BAR_CHART}</div>
                    <div>
                        <h1 class="topbar-title">AI-Powered Dashboard Pro</h1>
                        <p class="topbar-sub">Ruang Kerja Analitik — DuckDB, Grafik Interaktif &amp; Analisis AI</p>
                    </div>
                </div>
                <div class="badge-group">
                    {data_pill}
                    {ai_pill}
                </div>
            </div>
            <div class="topbar-team">
                <span class="team-label">{ICON_USERS}<span>Kelompok</span></span>
                <span class="member-chip"><span class="member-avatar">MA</span>Mahira Azzahra</span>
                <span class="member-chip"><span class="member-avatar">AA</span>Adelia Amanta Wada</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_topbar(topbar_slot, source_name, df, client)

                                       
                             
                                       
if df is None:
    with st.sidebar:
        st.markdown('<div class="sidebar-erde">erde</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="upload-intro">
            <div class="upload-icon-box">{ICON_UPLOAD}</div>
            <div>
                <h3>Unggah Dataset untuk Memulai Analisis</h3>
                <p>Mendukung format Excel (.xlsx, .xls) dan CSV hingga 200MB. Sistem otomatis mendeteksi kolom kategori, angka, dan tanggal.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    main_upload = st.file_uploader(
        "Pilih atau seret file Excel / CSV ke sini",
        type=["xlsx", "xls", "csv"],
        key="main_uploader",
    )

    if main_upload is not None:
        st.session_state["uploaded_bytes"] = main_upload.getvalue()
        st.session_state["uploaded_name"] = main_upload.name
        st.rerun()
    else:
        st.stop()

                                       
                                               
                                       
date_col = detect_date_column(df)
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = [
    c for c in df.columns if c not in numeric_cols and c != date_col
]

if not categorical_cols or not numeric_cols:
    with st.sidebar:
        st.markdown('<div class="sidebar-erde">erde</div>', unsafe_allow_html=True)
    st.warning(
        "Data harus memiliki minimal 1 kolom kategori/teks dan 1 kolom angka untuk dianalisis.",
        icon=":material/warning:",
    )
    st.stop()

default_cat = pick_default_category(df, categorical_cols)
default_num = numeric_cols.index("Sales") if "Sales" in numeric_cols else 0

tb_c1, tb_c2, tb_c3, tb_c4 = st.columns([1.15, 1.15, 1.0, 1.5], gap="small")

with tb_c1:
    cat_col = st.selectbox("Kolom Kategori", options=categorical_cols, index=default_cat)
with tb_c2:
    num_col = st.selectbox("Kolom Nilai", options=numeric_cols, index=default_num)
with tb_c3:
    chart_type = st.selectbox(
        "Jenis Grafik",
        options=["Bar Chart", "Horizontal Bar", "Donut Chart"],
        index=0,
    )

nunique_cat = df[cat_col].nunique(dropna=True)
with tb_c4:
    if nunique_cat <= 50:
        unique_cats = sorted(df[cat_col].dropna().astype(str).unique().tolist())
        selected_cats = st.multiselect(
            f"Filter {cat_col}",
            options=unique_cats,
            default=unique_cats,
        )
        filtered_df = df[df[cat_col].astype(str).isin(selected_cats)].copy()
    else:
        search_q = st.text_input(
            f"Cari {cat_col} ({nunique_cat:,} unik)",
            placeholder="Ketik kata kunci...",
        ).strip()
        if search_q:
            filtered_df = df[
                df[cat_col].astype(str).str.contains(search_q, case=False, na=False)
            ].copy()
        else:
            filtered_df = df.copy()

if date_col and not filtered_df.empty:
    min_d = filtered_df[date_col].min().date()
    max_d = filtered_df[date_col].max().date()
    with st.sidebar:
        st.divider()
        date_range = st.date_input(
            f"Rentang {date_col}",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df[date_col] >= start_d) & (filtered_df[date_col] <= end_d)
        ]

with st.sidebar:
    st.markdown('<div class="sidebar-erde">erde</div>', unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter saat ini.", icon=":material/info:")
    st.stop()

                                       
                    
                                       
q_cat = quote_ident(cat_col)
q_num = quote_ident(num_col)
query = f"""
SELECT {q_cat} AS Category, SUM({q_num}) AS Total_Value, COUNT(*) AS Transaksi
FROM filtered_df
WHERE {q_cat} IS NOT NULL
GROUP BY {q_cat}
ORDER BY Total_Value DESC
"""
agg_df = duckdb.sql(query).df()
total_col = f"Total_{num_col}"
agg_df = agg_df.rename(columns={"Category": cat_col, "Total_Value": total_col})

total_sum = float(agg_df[total_col].sum())
avg_val = float(agg_df[total_col].mean())
agg_df["Kontribusi (%)"] = (
    (agg_df[total_col] / total_sum * 100).round(1) if total_sum else 0.0
)

top_cat = str(agg_df.iloc[0][cat_col])
top_value = float(agg_df.iloc[0][total_col])
top_share = float(agg_df.iloc[0]["Kontribusi (%)"])
bottom_cat = str(agg_df.iloc[-1][cat_col])
bottom_value = float(agg_df.iloc[-1][total_col])
gap_value = top_value - bottom_value

                                       
                      
                                       
st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-head">
                <span class="kpi-label">Total {html.escape(num_col)}</span>
                <span class="kpi-icon">{ICON_LAYERS}</span>
            </div>
            <div class="kpi-value">{format_compact(total_sum)}</div>
            <div class="kpi-meta">{len(filtered_df):,} baris terfilter</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-head">
                <span class="kpi-label">Rata-rata / {html.escape(cat_col)}</span>
                <span class="kpi-icon">{ICON_TREND}</span>
            </div>
            <div class="kpi-value">{format_compact(avg_val)}</div>
            <div class="kpi-meta">Dari {len(agg_df):,} {html.escape(cat_col)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-head">
                <span class="kpi-label">Performa Tertinggi</span>
                <span class="kpi-icon">{ICON_AWARD}</span>
            </div>
            <div class="kpi-value">{html.escape(top_cat)}</div>
            <div class="kpi-meta">{format_compact(top_value)} ({top_share:.1f}% kontribusi)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-head">
                <span class="kpi-label">Selisih Tertinggi - Terendah</span>
                <span class="kpi-icon">{ICON_ACTIVITY}</span>
            </div>
            <div class="kpi-value">{format_compact(gap_value)}</div>
            <div class="kpi-meta">Terendah: {html.escape(bottom_cat)}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

                                       
                     
                                       
selected_model = st.session_state.selected_model
analysis_key = (
    f"{source_name}|{len(filtered_df)}|{cat_col}|{num_col}|{selected_model}|{bool(client)}"
)
if st.session_state.get("analysis_key") != analysis_key:
    loader_slot = st.empty()
    render_robot_loader(
        loader_slot, "AI Analis sedang memproses ringkasan data...", active_theme
    )
    ai_text = generate_ai_commentary(
        agg_df[[cat_col, total_col, "Kontribusi (%)"]],
        cat_col,
        num_col,
        selected_model,
        available_models,
        client,
    )
    loader_slot.empty()
    st.session_state.analysis_key = analysis_key
    st.session_state.ai_text = ai_text
    compact_summary = summarize_agg_for_llm(
        agg_df[[cat_col, total_col, "Kontribusi (%)"]], cat_col, num_col
    )
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "Anda adalah analis bisnis senior yang membantu memahami data. "
                f"Berikut ringkasan {num_col} per {cat_col}:\n{compact_summary}"
            ),
        },
        {"role": "assistant", "content": ai_text},
    ]

                                       
                                         
                                       
tab_overview, tab_insights, tab_chat, tab_data = st.tabs(
    ["Ringkasan & Grafik", "Analisis Otomatis & AI", "Chat AI Analis", "Eksplorasi Data"]
)

with tab_overview:
    bento_left, bento_right = st.columns([1.45, 1], gap="medium")
    chart_df = agg_df.head(20)
    chart_note = f" (Top 20 dari {len(agg_df):,})" if len(agg_df) > 20 else ""

    with bento_left:
        if chart_type == "Bar Chart":
            fig_main = px.bar(
                chart_df,
                x=cat_col,
                y=total_col,
                color=cat_col,
                text_auto=".2s",
                color_discrete_sequence=PALETTE,
            )
            fig_main.update_layout(showlegend=False)
        elif chart_type == "Horizontal Bar":
            fig_main = px.bar(
                chart_df.sort_values(total_col, ascending=True),
                x=total_col,
                y=cat_col,
                orientation="h",
                color=cat_col,
                text_auto=".2s",
                color_discrete_sequence=PALETTE,
            )
            fig_main.update_layout(showlegend=False)
        else:
            fig_main = px.pie(
                chart_df,
                names=cat_col,
                values=total_col,
                hole=0.45,
                color_discrete_sequence=PALETTE,
            )
        st.plotly_chart(
            style_plotly(
                fig_main, f"{num_col} per {cat_col}{chart_note}", active_theme, height=430
            ),
            width="stretch",
        )

    with bento_right:
        if date_col:
            q_date = quote_ident(date_col)
            valid_dates = filtered_df[date_col].dropna()
            span_days = (
                (valid_dates.max() - valid_dates.min()).days
                if not valid_dates.empty
                else 0
            )
            if span_days > 45:
                date_expr = f"DATE_TRUNC('month', CAST({q_date} AS DATE))"
                trend_title = f"Tren Bulanan {num_col}"
            else:
                date_expr = f"CAST({q_date} AS DATE)"
                trend_title = f"Tren Harian {num_col}"
            trend_query = f"""
            SELECT {date_expr} AS Tanggal, SUM({q_num}) AS Nilai
            FROM filtered_df
            WHERE {q_date} IS NOT NULL
            GROUP BY 1
            ORDER BY 1
            """
            trend_df = duckdb.sql(trend_query).df()
            fig_side = px.area(
                trend_df,
                x="Tanggal",
                y="Nilai",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=[active_theme["accent"]],
            )
            fig_side.update_traces(
                fillcolor=active_theme["accent_soft"], line=dict(width=2.5)
            )
            st.plotly_chart(
                style_plotly(fig_side, trend_title, active_theme, height=220),
                width="stretch",
            )
        else:
            fig_side = px.pie(
                chart_df,
                names=cat_col,
                values=total_col,
                hole=0.5,
                color_discrete_sequence=PALETTE,
            )
            st.plotly_chart(
                style_plotly(fig_side, f"Proporsi {num_col}", active_theme, height=220),
                width="stretch",
            )

                                           
        top5 = agg_df.head(5)
        rank_rows_html = ""
        for idx, row in top5.iterrows():
            r_name = html.escape(str(row[cat_col]))
            r_val = format_compact(float(row[total_col]))
            r_pct = float(row["Kontribusi (%)"])
            bar_color = PALETTE[idx % len(PALETTE)]
            rank_rows_html += (
                f'<div class="rank-row">'
                f'<div class="rank-top">'
                f'<span class="rank-name">{r_name}</span>'
                f'<span class="rank-val">{r_val} ({r_pct:.1f}%)</span>'
                f'</div>'
                f'<div class="rank-track"><div class="rank-fill" style="width:{min(r_pct, 100):.1f}%; background:{bar_color};"></div></div>'
                f'</div>'
            )
        st.markdown(
            f"""
            <div class="panel-card" style="margin-top:0.35rem;">
                <div class="panel-header">{ICON_TROPHY}<span>Peringkat Performa Teratas</span></div>
                {rank_rows_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("##### Ringkasan Performa Lengkap")
    st.dataframe(
        agg_df,
        width="stretch",
        hide_index=True,
        column_config={
            total_col: st.column_config.NumberColumn(format="%,.0f"),
            "Kontribusi (%)": st.column_config.ProgressColumn(
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
        },
    )

with tab_insights:
    col_rule, col_ai = st.columns(2, gap="medium")
    top2_share = float(agg_df.head(2)["Kontribusi (%)"].sum())

    with col_rule:
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="panel-header">{ICON_FILE_TEXT}<span>Ringkasan Otomatis (Berbasis Aturan)</span></div>
                <ul style="color:var(--text); line-height:1.75; padding-left:1.2rem; margin:0; font-size:0.92rem;">
                    <li><strong>{html.escape(cat_col)} Tertinggi:</strong> <b>{html.escape(top_cat)}</b> sebesar <b>{top_value:,.0f}</b> ({top_share:.1f}% dari total).</li>
                    <li><strong>{html.escape(cat_col)} Terendah:</strong> <b>{html.escape(bottom_cat)}</b> sebesar <b>{bottom_value:,.0f}</b>.</li>
                    <li><strong>Selisih:</strong> <b>{gap_value:,.0f}</b> antara performa terbaik dan terendah.</li>
                    <li><strong>Konsentrasi Top 2:</strong> 2 {html.escape(cat_col)} teratas menyumbang <b>{top2_share:.1f}%</b> dari keseluruhan {html.escape(num_col)}.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_ai:
        st.markdown(
            f'<div class="panel-card"><div class="panel-header">{ICON_CPU}<span>Analisis Strategis AI</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.ai_text)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_chat:
    chat_top_l, chat_top_r = st.columns([4, 1])
    chat_top_l.caption(
        "Tanyakan detail, anomali, atau strategi bisnis berdasarkan data yang sedang aktif."
    )
    if chat_top_r.button("Reset Chat", icon=":material/refresh:", width="stretch"):
        st.session_state.chat_history = [
            m for m in st.session_state.chat_history if m.get("role") == "system"
        ] + [{"role": "assistant", "content": st.session_state.ai_text}]
        st.rerun()

    q_col1, q_col2, q_col3 = st.columns(3)
    quick_prompt = None
    if q_col1.button(f"Strategi naikkan {bottom_cat}?", width="stretch"):
        quick_prompt = (
            f"Berikan 3 strategi konkret untuk meningkatkan {num_col} di {bottom_cat}."
        )
    if q_col2.button("Analisis ketimpangan data", width="stretch"):
        quick_prompt = f"Jelaskan kenapa terjadi selisih sebesar {gap_value:,.0f} dan risikonya bagi bisnis."
    if q_col3.button("Ringkasan eksekutif 3 poin", width="stretch"):
        quick_prompt = (
            "Buatkan ringkasan eksekutif dalam 3 poin singkat untuk presentasi manajemen."
        )

    for msg in st.session_state.chat_history:
        if msg["role"] in ("user", "assistant"):
            st.chat_message(msg["role"]).write(msg["content"])

    typed_prompt = st.chat_input("Tanyakan sesuatu tentang data ini...")
    active_question = quick_prompt or typed_prompt

    if active_question:
        if not client:
            st.warning(
                "Fitur chat membutuhkan GROQ_API_KEY. Isi API Key di menu Pengaturan atau file `.env`.",
                icon=":material/lock:",
            )
        else:
            st.session_state.chat_history.append(
                {"role": "user", "content": active_question}
            )
            st.chat_message("user").write(active_question)
            chat_loader = st.empty()
            render_robot_loader(
                chat_loader, "AI Analis sedang menyusun jawaban...", active_theme
            )
            try:
                answer, _used = chat_with_fallback(
                    client,
                    selected_model,
                    available_models,
                    st.session_state.chat_history,
                )
                chat_loader.empty()
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )
                st.chat_message("assistant").write(answer)
            except Exception as e:
                chat_loader.empty()
                st.error(f"Terjadi kendala pada chat: {e}", icon=":material/error:")

with tab_data:
    st.markdown("##### Pratinjau Dataset Terfilter")
    if len(filtered_df) > 1000:
        st.caption(
            f"Menampilkan 1.000 baris pertama dari {len(filtered_df):,} baris agar browser tetap ringan."
        )
        st.dataframe(filtered_df.head(1000), width="stretch", hide_index=True)
    else:
        st.dataframe(filtered_df, width="stretch", hide_index=True)

    dl_col1, dl_col2 = st.columns(2)
    csv_bytes = agg_df.to_csv(index=False).encode("utf-8")
    dl_col1.download_button(
        label="Unduh Ringkasan Agregasi (CSV)",
        icon=":material/download:",
        data=csv_bytes,
        file_name=f"ringkasan_{cat_col}_{num_col}.csv",
        mime="text/csv",
        width="stretch",
    )
    report_bytes = build_printable_report_html(
        source_name,
        cat_col,
        num_col,
        total_sum,
        avg_val,
        top_cat,
        top_value,
        top_share,
        bottom_cat,
        bottom_value,
        gap_value,
        agg_df,
        st.session_state.ai_text,
    )
    dl_col2.download_button(
        label="Unduh Laporan Siap Cetak (HTML/PDF)",
        icon=":material/print:",
        data=report_bytes,
        file_name=f"laporan_{cat_col}_{num_col}.html",
        mime="text/html",
        width="stretch",
    )
    st.caption(
        "Tip: Anda juga bisa menekan Ctrl+P langsung di halaman ini untuk mencetak tampilan bersih tanpa tombol."
    )
