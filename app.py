import html
import io
import json
import os
import re
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
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            --bg: {t["bg"]};
            --surface: {t["surface"]};
            --surface-alt: {t["surface_alt"]};
            --border: {t["border"]};
            --text: {t["text"]};
            --muted: {t["muted"]};
            --accent: {t["accent"]};
            --accent-soft: {t["accent_soft"]};
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
            --shadow-md: 0 4px 16px rgba(0,0,0,0.35), 0 2px 6px rgba(0,0,0,0.25);
            --shadow-lg: 0 10px 40px rgba(0,0,0,0.45), 0 4px 12px rgba(0,0,0,0.3);
        }}

        html, body, [class*="css"] {{
            font-family: 'Space Grotesk', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: var(--text);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: var(--bg) !important;
            background-image: radial-gradient(ellipse 80% 50% at 50% -10%, {t["accent_soft"]}, transparent) !important;
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
        section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
            background: linear-gradient(135deg, var(--bg) 0%, var(--surface) 100%) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.8rem 0.9rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: border-color 200ms ease, box-shadow 200ms ease !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:hover {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px {t["accent_soft"]}, var(--shadow-md) !important;
        }}
        .sidebar-head {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
            margin: 0.1rem 0 0.6rem 0;
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
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.32em;
            text-transform: lowercase;
            color: var(--muted);
            opacity: 0.35;
            transition: opacity 220ms ease;
            user-select: none;
        }}
        .sidebar-erde:hover {{
            opacity: 0.72;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            padding-left: 1.75rem;
            padding-right: 1.75rem;
            max-width: 1440px;
        }}

        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        .stTextInput input,
        .stDateInput input {{
            background-color: var(--surface-alt) !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
            border-radius: var(--radius-sm) !important;
        }}
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="input"] > div:focus-within,
        .stTextInput input:focus,
        .stDateInput input:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px {t["accent_soft"]} !important;
        }}
        .stButton > button,
        [data-testid="stPopover"] > button {{
            transition: transform 120ms ease, border-color 180ms ease, background-color 180ms ease, box-shadow 180ms ease;
            border-radius: var(--radius-sm) !important;
            font-family: 'Space Grotesk', 'Inter', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
        }}
        .stButton > button:active,
        [data-testid="stPopover"] > button:active {{
            transform: scale(0.982);
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {t["accent"]} 0%, {t["accent"]}cc 100%) !important;
            border-color: {t["accent"]} !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 8px {t["accent_soft"]}, 0 1px 2px rgba(0,0,0,0.2) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 4px 16px {t["accent_soft"]}, 0 2px 4px rgba(0,0,0,0.25) !important;
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
            background-color: var(--accent-soft) !important;
        }}

        @keyframes borderBeam {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(350%); }}
        }}
        @keyframes statusPulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.55; transform: scale(1.25); }}
        }}
        .topbar-wrap {{
            position: relative;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-top: 2px solid var(--accent);
            border-radius: var(--radius-lg);
            margin-bottom: 1.1rem;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }}
        .topbar-wrap::before {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 32%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #FFFFFF, var(--accent), transparent);
            opacity: 0.85;
            animation: borderBeam 4.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            pointer-events: none;
        }}
        .topbar {{
            padding: 1.1rem 1.4rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }}
        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }}
        .brand-mark {{
            width: 42px;
            height: 42px;
            border-radius: 10px;
            background: linear-gradient(135deg, {t["accent_soft"]} 0%, {t["surface"]} 100%);
            border: 1px solid {t["accent"]};
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 2px 8px {t["accent_soft"]};
        }}
        h1.topbar-title,
        .topbar-title {{
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
            color: var(--text) !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.25 !important;
            font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        }}
        .topbar-sub {{
            font-size: 0.82rem;
            color: var(--muted);
            margin: 0.1rem 0 0 0;
            letter-spacing: 0.01em;
        }}
        .badge-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            align-items: center;
        }}
        .pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.32rem 0.72rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text);
            box-shadow: var(--shadow-sm);
            letter-spacing: 0.01em;
        }}
        .dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
        }}
        .dot-green {{ background: #10B981; box-shadow: 0 0 8px #10B98188; animation: statusPulse 2.4s ease-in-out infinite; }}
        .dot-amber {{ background: #F59E0B; box-shadow: 0 0 6px #F59E0B55; }}
        .dot-accent {{ background: var(--accent); box-shadow: 0 0 8px {t["accent_soft"]}; animation: statusPulse 2.8s ease-in-out infinite; }}

        .topbar-team {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.6rem;
            padding: 0.65rem 1.4rem;
            background: rgba(0,0,0,0.12);
            border-top: 1px solid var(--border);
        }}
        .team-label {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.69rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--muted);
            margin-right: 0.2rem;
        }}
        .team-label svg {{ color: var(--accent); }}
        .member-chip {{
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text);
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 0.2rem 0.62rem 0.2rem 0.24rem;
            border-radius: 999px;
            box-shadow: var(--shadow-sm);
            transition: border-color 160ms ease;
        }}
        .member-chip:hover {{
            border-color: var(--accent);
        }}
        .member-avatar {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(135deg, {t["accent_soft"]} 0%, {t["surface"]} 100%);
            color: var(--accent);
            border: 1px solid var(--accent);
            font-size: 0.62rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        @keyframes fadeSlideUp {{
            from {{ opacity: 0; transform: perspective(1000px) translateY(12px) rotateX(4deg); }}
            to {{ opacity: 1; transform: perspective(1000px) translateY(0) rotateX(0deg); }}
        }}
        @keyframes shimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}
        @keyframes rankGrow {{
            from {{ transform: scaleX(0); }}
            to {{ transform: scaleX(1); }}
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
            margin-bottom: 1.2rem;
            perspective: 1200px;
        }}
        .kpi-card {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.1rem 1.2rem;
            animation: fadeSlideUp 380ms cubic-bezier(0.16, 1, 0.3, 1) both;
            transition: border-color 220ms ease, box-shadow 220ms ease, transform 160ms cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: var(--shadow-sm);
            transform-style: preserve-3d;
            will-change: transform;
            --rx: 0deg;
            --ry: 0deg;
            --mx: 50%;
            --my: 0%;
        }}
        .kpi-card:nth-child(1) {{ animation-delay: 0ms; }}
        .kpi-card:nth-child(2) {{ animation-delay: 60ms; }}
        .kpi-card:nth-child(3) {{ animation-delay: 120ms; }}
        .kpi-card:nth-child(4) {{ animation-delay: 180ms; }}
        .kpi-card::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0;
            transition: opacity 220ms ease;
        }}
        .kpi-card::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle 180px at var(--mx) var(--my), {t["accent_soft"]}, transparent 70%);
            opacity: 0;
            transition: opacity 220ms ease;
            pointer-events: none;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .kpi-card:hover {{
                border-color: var(--accent);
                box-shadow: 0 14px 32px rgba(0,0,0,0.42), 0 0 0 1px {t["accent_soft"]};
                transform: perspective(1000px) rotateX(var(--rx)) rotateY(var(--ry)) translateY(-3px) scale(1.012);
            }}
            .kpi-card:hover .kpi-head {{ transform: translateZ(14px); }}
            .kpi-card:hover .kpi-value {{ transform: translateZ(20px); }}
            .kpi-card:hover .kpi-meta {{ transform: translateZ(10px); }}
        }}
        .kpi-card:hover::before {{ opacity: 1; }}
        .kpi-card:hover::after {{ opacity: 1; }}
        .kpi-card:hover .kpi-icon {{ transform: scale(1.08) translateZ(8px); box-shadow: 0 4px 12px {t["accent_soft"]}; }}
        .kpi-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.6rem;
            transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .kpi-label {{
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .kpi-icon {{
            color: var(--accent);
            background: linear-gradient(135deg, {t["accent_soft"]} 0%, transparent 100%);
            border: 1px solid {t["accent_soft"]};
            width: 30px;
            height: 30px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 200ms ease;
            flex-shrink: 0;
        }}
        .kpi-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            line-height: 1.15;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.03em;
            word-break: break-word;
            transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .kpi-meta {{
            font-size: 0.77rem;
            color: var(--muted);
            margin-top: 0.32rem;
            letter-spacing: 0.01em;
            transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .panel-card {{
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.2rem 1.3rem;
            margin-bottom: 0.9rem;
            animation: fadeSlideUp 300ms cubic-bezier(0.16, 1, 0.3, 1) both;
            box-shadow: var(--shadow-sm);
            transition: border-color 200ms ease, box-shadow 200ms ease;
        }}
        .panel-card:hover {{
            border-color: var(--border);
            box-shadow: var(--shadow-md);
        }}
        .panel-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.85rem;
            padding-bottom: 0.65rem;
            border-bottom: 1px solid var(--border);
            letter-spacing: -0.01em;
        }}
        .panel-header svg {{ color: var(--accent); flex-shrink: 0; }}
        .panel-card p,
        .panel-card li,
        .ai-justified p,
        .ai-justified li,
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li {{
            text-align: justify !important;
            text-justify: inter-word !important;
        }}

        .rank-row {{
            margin-bottom: 0.78rem;
        }}
        .rank-row:last-child {{
            margin-bottom: 0;
        }}
        .rank-top {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: 0.82rem;
            margin-bottom: 0.3rem;
        }}
        .rank-name {{
            font-weight: 600;
            color: var(--text);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 60%;
            letter-spacing: -0.01em;
        }}
        .rank-val {{
            font-variant-numeric: tabular-nums;
            color: var(--muted);
            font-size: 0.77rem;
            font-weight: 500;
        }}
        .rank-track {{
            width: 100%;
            height: 5px;
            background: var(--surface-alt);
            border-radius: 999px;
            overflow: hidden;
        }}
        .rank-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent), {t["accent"]}aa);
            transform-origin: left center;
            animation: rankGrow 520ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }}

        .upload-intro {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.5rem 1.75rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1.1rem;
            box-shadow: var(--shadow-sm);
            transform-style: preserve-3d;
            transition: border-color 220ms ease, box-shadow 220ms ease, transform 180ms cubic-bezier(0.2, 0.8, 0.2, 1);
            --rx: 0deg;
            --ry: 0deg;
            --mx: 50%;
            --my: 50%;
        }}
        .upload-intro::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle 220px at var(--mx) var(--my), {t["accent_soft"]}, transparent 70%);
            opacity: 0;
            transition: opacity 220ms ease;
            pointer-events: none;
        }}
        @media (hover: hover) and (pointer: fine) {{
            .upload-intro:hover {{
                border-color: var(--accent);
                box-shadow: 0 14px 32px rgba(0,0,0,0.4), 0 0 0 1px {t["accent_soft"]};
                transform: perspective(1000px) rotateX(var(--rx)) rotateY(var(--ry)) translateY(-2px);
            }}
            .upload-intro:hover::after {{ opacity: 1; }}
            .upload-intro:hover .upload-icon-box {{ transform: translateZ(14px) scale(1.05); }}
        }}
        .stElementContainer:has(.tilt-script-anchor),
        .stElementContainer:has(.tilt-script-anchor) + .stElementContainer {{
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        .cmd-trigger {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.3rem 0.65rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: var(--surface-alt);
            color: var(--muted);
            cursor: pointer;
            transition: border-color 160ms ease, color 160ms ease;
        }}
        .cmd-trigger:hover {{
            border-color: var(--accent);
            color: var(--text);
        }}
        .cmd-kbd {{
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 0.66rem;
            padding: 0.08rem 0.35rem;
            border-radius: 5px;
            background: var(--bg);
            border: 1px solid var(--border);
            color: var(--text);
        }}
        .h2h-wrap {{
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.15rem 1.3rem;
            margin-top: 0.9rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
        }}
        .h2h-grid {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 1rem;
            align-items: center;
            margin-top: 0.4rem;
        }}
        .h2h-card {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.95rem 1.1rem;
        }}
        .h2h-card.winner {{
            border-color: var(--accent);
            box-shadow: 0 0 0 1px {t["accent_soft"]};
        }}
        .h2h-title {{
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.35rem;
        }}
        .h2h-val {{
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--accent);
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.02em;
        }}
        .h2h-sub {{
            font-size: 0.78rem;
            color: var(--muted);
            margin-top: 0.25rem;
        }}
        .h2h-vs {{
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: var(--muted);
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.45rem 0.7rem;
            text-align: center;
        }}
        .h2h-bar-track {{
            display: flex;
            width: 100%;
            height: 8px;
            border-radius: 999px;
            overflow: hidden;
            background: var(--bg);
            margin-top: 0.85rem;
            border: 1px solid var(--border);
        }}
        .h2h-bar-a {{
            background: var(--accent);
            height: 100%;
            transition: width 350ms ease;
        }}
        .h2h-bar-b {{
            background: {t["palette"][1] if len(t["palette"]) > 1 else "#3B82F6"};
            height: 100%;
            transition: width 350ms ease;
        }}
        .slide-banner {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
            border-radius: var(--radius-md);
            padding: 0.85rem 1.2rem;
            margin-bottom: 1rem;
        }}
        .slide-badge {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent);
        }}
        .slide-heading {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text);
            margin-top: 0.15rem;
        }}
        #cmdk-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(6, 9, 12, 0.72);
            backdrop-filter: blur(6px);
            z-index: 100000;
            display: none;
            align-items: flex-start;
            justify-content: center;
            padding-top: 14vh;
        }}
        #cmdk-overlay.open {{
            display: flex;
        }}
        #cmdk-box {{
            width: 92%;
            max-width: 520px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-top: 2px solid var(--accent);
            border-radius: 14px;
            box-shadow: 0 24px 64px rgba(0,0,0,0.6);
            overflow: hidden;
            font-family: 'Space Grotesk', 'Inter', sans-serif;
        }}
        #cmdk-input {{
            width: 100%;
            box-sizing: border-box;
            background: transparent;
            border: none;
            border-bottom: 1px solid var(--border);
            color: var(--text);
            font-size: 0.95rem;
            padding: 0.95rem 1.15rem;
            outline: none;
            font-family: inherit;
        }}
        #cmdk-list {{
            max-height: 300px;
            overflow-y: auto;
            padding: 0.45rem;
        }}
        .cmdk-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.65rem 0.85rem;
            border-radius: 8px;
            cursor: pointer;
            color: var(--text);
            font-size: 0.86rem;
            font-weight: 500;
            transition: background-color 120ms ease, color 120ms ease;
        }}
        .cmdk-item:hover {{
            background: {t["accent_soft"]};
            color: var(--accent);
        }}
        .cmdk-tag {{
            font-size: 0.7rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .stElementContainer:has(.spline-hero-anchor) {{
            display: none !important;
        }}
        .upload-icon-box {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, {t["accent_soft"]} 0%, transparent 100%);
            border: 1px solid {t["accent_soft"]};
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 2px 8px {t["accent_soft"]};
        }}
        .upload-intro h3 {{
            margin: 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            letter-spacing: -0.01em;
        }}
        .upload-intro p {{
            margin: 0.22rem 0 0 0;
            font-size: 0.85rem;
            color: var(--muted);
            line-height: 1.5;
        }}

        [data-testid="stFileUploader"] section {{
            background-color: var(--surface) !important;
            border: 1.5px dashed var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 1.25rem !important;
            color: var(--text) !important;
            transition: border-color 200ms ease !important;
        }}
        [data-testid="stFileUploader"] section:hover {{
            border-color: var(--accent) !important;
            background-color: var(--accent-soft) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.1rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.1rem;
            padding-bottom: 0;
            background: transparent !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-size: 0.86rem;
            font-weight: 600;
            color: var(--muted);
            padding: 0.6rem 1.1rem;
            border-radius: 0 !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            background: transparent !important;
            transition: color 180ms ease, border-color 180ms ease;
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            letter-spacing: 0.01em;
            margin-bottom: -1px;
            outline: none !important;
            box-shadow: none !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--text) !important;
            background: transparent !important;
            border-bottom-color: var(--border) !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
            background: transparent !important;
            border-bottom: 2px solid var(--accent) !important;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
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
            background: rgba(10, 12, 16, 0.78) !important;
            backdrop-filter: blur(8px);
        }}

        @media (max-width: 1024px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}
        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 3.1rem !important;
                padding-left: 0.65rem !important;
                padding-right: 0.65rem !important;
                padding-bottom: 1.5rem !important;
            }}
            .topbar {{
                padding: 0.75rem 0.9rem !important;
                gap: 0.55rem !important;
            }}
            .brand-mark {{
                width: 32px !important;
                height: 32px !important;
            }}
            h1.topbar-title,
            .topbar-title {{
                font-size: 1.05rem !important;
            }}
            .topbar-sub {{
                font-size: 0.74rem !important;
            }}
            .pill {{
                font-size: 0.7rem !important;
                padding: 0.25rem 0.55rem !important;
            }}
            .cmd-trigger {{
                display: none !important;
            }}
            .h2h-grid {{
                grid-template-columns: 1fr !important;
                gap: 0.55rem !important;
            }}
            .topbar-team {{
                display: grid !important;
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                padding: 0.5rem 0.85rem !important;
                gap: 0.4rem !important;
            }}
            .team-label {{
                grid-column: 1 / -1 !important;
                font-size: 0.64rem !important;
                margin: 0 0 0.05rem 0 !important;
            }}
            .member-chip {{
                font-size: 0.71rem !important;
                padding: 0.22rem 0.5rem 0.22rem 0.24rem !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }}
            .member-avatar {{
                width: 18px !important;
                height: 18px !important;
                font-size: 0.58rem !important;
                flex-shrink: 0 !important;
            }}
            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                gap: 0.65rem !important;
            }}
            section[data-testid="stSidebar"] hr {{
                margin: 0.5rem 0 !important;
            }}
            section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--bg) !important;
                border: 1px solid var(--border) !important;
                border-radius: var(--radius-md) !important;
                padding: 0.75rem 0.85rem !important;
            }}
            .sidebar-head {{
                margin: 0.1rem 0 0.25rem 0 !important;
            }}
            .sidebar-erde {{
                margin-top: 0.85rem !important;
                padding-top: 0.55rem !important;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 0.5rem !important;
            }}
            .kpi-card {{
                padding: 0.72rem 0.75rem !important;
            }}
            .kpi-icon {{
                width: 24px !important;
                height: 24px !important;
            }}
            .kpi-label {{
                font-size: 0.63rem !important;
            }}
            .kpi-value {{
                font-size: 1.05rem !important;
            }}
            .kpi-meta {{
                font-size: 0.68rem !important;
            }}
            .panel-card {{
                padding: 0.9rem 1rem !important;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                scrollbar-width: none;
            }}
            .stTabs [data-baseweb="tab"] {{
                font-size: 0.78rem !important;
                padding: 0.5rem 0.75rem !important;
                white-space: nowrap !important;
                border-bottom-width: 2px !important;
            }}
            [data-testid="stPlotlyChart"] {{
                max-width: 100% !important;
                overflow-x: hidden !important;
            }}
            .stElementContainer:has(.spline-hero-anchor) + .stElementContainer {{
                height: 225px !important;
                max-height: 225px !important;
                overflow: hidden !important;
                margin-bottom: -0.75rem !important;
            }}
            .stElementContainer:has(.spline-hero-anchor) + .stElementContainer iframe {{
                height: 240px !important;
                min-height: 240px !important;
                max-height: 240px !important;
            }}
            .upload-intro {{
                padding: 1rem !important;
                gap: 0.75rem !important;
            }}
            .upload-intro h3 {{
                font-size: 0.95rem !important;
            }}
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
                box-shadow: none !important;
            }}
            .topbar-team {{
                background: #F8FAFC !important;
                border-top: 1px solid #CBD5E1 !important;
            }}
            .member-chip {{
                background: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                color: #0F172A !important;
                box-shadow: none !important;
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
            <style>
              html, body {{
                margin: 0; padding: 0; width: 100%; height: 100%;
                background: transparent;
                font-family: 'Space Grotesk', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                display: flex; align-items: center; justify-content: center;
              }}
              .loader-card {{
                position: relative;
                width: 90%;
                max-width: 375px;
                background: radial-gradient(circle at 50% 0%, {t["accent_soft"]}, transparent 65%),
                            linear-gradient(145deg, {t["surface"]} 0%, {t["surface_alt"]} 100%);
                border: 1px solid {t["border"]};
                border-top: 2px solid {t["accent"]};
                border-radius: 18px;
                padding: 26px 28px 24px 28px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                box-sizing: border-box;
                box-shadow: 0 28px 64px rgba(0, 0, 0, 0.6), 0 0 0 1px {t["accent_soft"]};
              }}
              .bot-stage {{
                position: relative;
                width: 124px;
                height: 124px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 10px;
              }}
              .bot-aura {{
                position: absolute;
                inset: 14px;
                border-radius: 50%;
                background: radial-gradient(circle, {t["accent_soft"]} 0%, transparent 72%);
                animation: auraPulse 2.4s ease-in-out infinite;
              }}
              .bot-ring {{
                position: absolute;
                inset: 4px;
                border-radius: 50%;
                border: 1.5px solid transparent;
                border-top-color: {t["accent"]};
                border-right-color: {t["accent"]};
                opacity: 0.65;
                animation: spinRing 3.6s linear infinite;
              }}
              .bot-ring-inner {{
                position: absolute;
                inset: 12px;
                border-radius: 50%;
                border: 1px dashed {t["accent"]};
                opacity: 0.35;
                animation: spinRingRev 7s linear infinite;
              }}
              .bot-svg {{
                position: relative;
                width: 88px;
                height: 88px;
                animation: botFloat 2.4s ease-in-out infinite;
                filter: drop-shadow(0 10px 16px rgba(0,0,0,0.48));
              }}
              .bot-eye {{
                animation: eyeScan 2.4s ease-in-out infinite;
                transform-origin: center;
              }}
              .bot-eye-r {{
                animation-delay: 0.14s;
              }}
              .bot-pulse {{
                animation: corePulse 1.3s ease-in-out infinite;
              }}
              .calc-bar {{
                transform-origin: center bottom;
                animation: calcWave 0.85s ease-in-out infinite;
              }}
              .calc-bar-2 {{ animation-delay: 0.18s; }}
              .calc-bar-3 {{ animation-delay: 0.36s; }}
              @keyframes spinRing {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
              }}
              @keyframes spinRingRev {{
                from {{ transform: rotate(360deg); }}
                to {{ transform: rotate(0deg); }}
              }}
              @keyframes auraPulse {{
                0%, 100% {{ transform: scale(0.95); opacity: 0.6; }}
                50% {{ transform: scale(1.08); opacity: 1; }}
              }}
              @keyframes botFloat {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-7px); }}
              }}
              @keyframes eyeScan {{
                0%, 82%, 100% {{ transform: scaleY(1); opacity: 1; }}
                88% {{ transform: scaleY(0.16); opacity: 0.5; }}
              }}
              @keyframes calcWave {{
                0%, 100% {{ transform: scaleY(0.35); opacity: 0.55; }}
                50% {{ transform: scaleY(1); opacity: 1; }}
              }}
              @keyframes corePulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.4; }}
              }}
              .loader-label {{
                margin-top: 4px;
                font-size: 13.5px;
                font-weight: 600;
                color: {t["text"]};
                letter-spacing: -0.01em;
              }}
              .loader-track {{
                width: 78%;
                height: 4px;
                background: {t["bg"]};
                border-radius: 999px;
                overflow: hidden;
                margin-top: 12px;
              }}
              .loader-bar {{
                width: 45%;
                height: 100%;
                background: linear-gradient(90deg, {t["accent"]}, #FFFFFF, {t["accent"]});
                border-radius: 999px;
                animation: slide 1.1s ease-in-out infinite;
              }}
              @keyframes slide {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(230%); }}
              }}
            </style>
            </head>
            <body>
              <div class="loader-card">
                <div class="bot-stage">
                  <div class="bot-aura"></div>
                  <div class="bot-ring"></div>
                  <div class="bot-ring-inner"></div>
                  <svg class="bot-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                      <linearGradient id="shellGrad" x1="20" y1="20" x2="80" y2="90" gradientUnits="userSpaceOnUse">
                        <stop offset="0%" stop-color="{t["surface_alt"]}"/>
                        <stop offset="100%" stop-color="{t["bg"]}"/>
                      </linearGradient>
                    </defs>
                    <line x1="50" y1="11" x2="50" y2="21" stroke="{t["accent"]}" stroke-width="2.5" stroke-linecap="round"/>
                    <circle class="bot-pulse" cx="50" cy="8.5" r="4" fill="{t["accent"]}"/>
                    <rect x="20" y="21" width="60" height="44" rx="16" fill="url(#shellGrad)" stroke="{t["accent"]}" stroke-width="2.2"/>
                    <rect x="13" y="35" width="6.5" height="16" rx="3.2" fill="{t["accent"]}" opacity="0.8"/>
                    <rect x="80.5" y="35" width="6.5" height="16" rx="3.2" fill="{t["accent"]}" opacity="0.8"/>
                    <rect x="27" y="30" width="46" height="24" rx="10" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
                    <path d="M31 33 L41 33 L35 42 L29 42 Z" fill="#FFFFFF" opacity="0.06"/>
                    <rect class="bot-eye" x="35" y="38" width="9" height="8" rx="3.5" fill="{t["accent"]}"/>
                    <rect class="bot-eye bot-eye-r" x="56" y="38" width="9" height="8" rx="3.5" fill="{t["accent"]}"/>
                    <path d="M35 69 H65 L69 86 C69 89.5 66.2 92 62.5 92 H37.5 C33.8 92 31 89.5 31 86 Z" fill="url(#shellGrad)" stroke="{t["border"]}" stroke-width="2"/>
                    <rect x="42" y="75" width="3.5" height="10" rx="1.5" class="calc-bar" fill="{t["accent"]}"/>
                    <rect x="48.2" y="75" width="3.5" height="10" rx="1.5" class="calc-bar calc-bar-2" fill="{t["accent"]}"/>
                    <rect x="54.5" y="75" width="3.5" height="10" rx="1.5" class="calc-bar calc-bar-3" fill="{t["accent"]}"/>
                  </svg>
                </div>
                <div class="loader-label">{html.escape(label)}</div>
                <div class="loader-track"><div class="loader-bar"></div></div>
              </div>
            </body>
            </html>
            """,
            height=242,
        )

def inject_3d_tilt_script() -> None:
    st.markdown('<div class="tilt-script-anchor"></div>', unsafe_allow_html=True)
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"></head>
        <body>
        <script>
        (function() {
            try {
                const doc = window.parent.document;
                const win = window.parent;

                function runCountUp() {
                    const els = doc.querySelectorAll(".kpi-value");
                    els.forEach(function(el) {
                        const raw = (el.getAttribute("data-target-text") || el.textContent || "").trim();
                        if (el.getAttribute("data-counted") === raw) return;
                        el.setAttribute("data-target-text", raw);
                        el.setAttribute("data-counted", raw);
                        const match = raw.match(/^(-?[\\d,]+(?:\\.\\d+)?)(\\s*(?:Jt|M))?$/);
                        if (!match) return;
                        const numStr = match[1].replace(/,/g, "");
                        const target = parseFloat(numStr);
                        if (isNaN(target) || target === 0) return;
                        const suffix = match[2] || "";
                        const decimals = (match[1].split(".")[1] || "").length;
                        const duration = 680;
                        const start = win.performance.now();

                        function tick(now) {
                            const p = Math.min((now - start) / duration, 1);
                            const eased = 1 - Math.pow(1 - p, 3);
                            const cur = target * eased;
                            const formatted = cur.toLocaleString("en-US", {
                                minimumFractionDigits: decimals,
                                maximumFractionDigits: decimals
                            });
                            el.textContent = formatted + suffix;
                            if (p < 1) {
                                win.requestAnimationFrame(tick);
                            } else {
                                el.textContent = raw;
                            }
                        }
                        win.requestAnimationFrame(tick);
                    });
                }

                runCountUp();
                if (!win.__kpiObserver) {
                    win.__kpiObserver = new win.MutationObserver(function() {
                        runCountUp();
                    });
                    win.__kpiObserver.observe(doc.body, { childList: true, subtree: true });
                }

                if (!win.matchMedia || !win.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
                if (win.__tilt3dBound) return;
                win.__tilt3dBound = true;
                let rafId = null;
                let activeCard = null;
                let lastX = 0;
                let lastY = 0;

                function applyTilt() {
                    rafId = null;
                    if (!activeCard) return;
                    const rect = activeCard.getBoundingClientRect();
                    if (!rect.width || !rect.height) return;
                    const px = (lastX - rect.left) / rect.width;
                    const py = (lastY - rect.top) / rect.height;
                    const rx = ((0.5 - py) * 11).toFixed(2) + "deg";
                    const ry = ((px - 0.5) * 11).toFixed(2) + "deg";
                    activeCard.style.setProperty("--rx", rx);
                    activeCard.style.setProperty("--ry", ry);
                    activeCard.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
                    activeCard.style.setProperty("--my", (py * 100).toFixed(1) + "%");
                }

                doc.addEventListener("mousemove", function(e) {
                    const card = e.target.closest(".kpi-card, .upload-intro");
                    if (activeCard && activeCard !== card) {
                        activeCard.style.setProperty("--rx", "0deg");
                        activeCard.style.setProperty("--ry", "0deg");
                    }
                    activeCard = card;
                    if (!card) return;
                    lastX = e.clientX;
                    lastY = e.clientY;
                    if (!rafId) rafId = win.requestAnimationFrame(applyTilt);
                }, { passive: true });

                doc.addEventListener("mouseleave", function() {
                    if (activeCard) {
                        activeCard.style.setProperty("--rx", "0deg");
                        activeCard.style.setProperty("--ry", "0deg");
                        activeCard = null;
                    }
                }, { passive: true });

                if (!win.__cmdkBound) {
                    win.__cmdkBound = true;
                    const overlay = doc.createElement("div");
                    overlay.id = "cmdk-overlay";
                    overlay.innerHTML =
                        '<div id="cmdk-box">' +
                        '<input id="cmdk-input" type="text" placeholder="Ketik perintah (tab, cetak, sidebar)..." autocomplete="off"/>' +
                        '<div id="cmdk-list"></div>' +
                        '</div>';
                    doc.body.appendChild(overlay);

                    const commands = [
                        { label: "Buka Tab: Ringkasan & Grafik", tag: "Navigasi", act: () => clickTab(0) },
                        { label: "Buka Tab: Analisis Otomatis & AI", tag: "Navigasi", act: () => clickTab(1) },
                        { label: "Buka Tab: Chat AI Analis", tag: "Navigasi", act: () => clickTab(2) },
                        { label: "Buka Tab: Eksplorasi Data", tag: "Navigasi", act: () => clickTab(3) },
                        { label: "Fokus ke Input Chat AI", tag: "AI", act: () => { clickTab(2); setTimeout(() => { const el = doc.querySelector('[data-testid="stChatInput"] textarea'); if (el) el.focus(); }, 120); } },
                        { label: "Buka / Tutup Sidebar", tag: "Tampilan", act: () => { const b = doc.querySelector('[data-testid="stSidebarCollapseButton"] button, [data-testid="collapsedControl"] button'); if (b) b.click(); } },
                        { label: "Cetak Halaman (Print / PDF)", tag: "Ekspor", act: () => win.print() },
                        { label: "Gulir ke Atas Halaman", tag: "Navigasi", act: () => win.scrollTo({ top: 0, behavior: "smooth" }) }
                    ];

                    function clickTab(idx) {
                        const tabs = doc.querySelectorAll('.stTabs [role="tab"]');
                        if (tabs && tabs[idx]) tabs[idx].click();
                    }

                    const inp = overlay.querySelector("#cmdk-input");
                    const list = overlay.querySelector("#cmdk-list");

                    function renderCmdList(q) {
                        const kw = (q || "").toLowerCase().trim();
                        list.innerHTML = "";
                        commands.filter(c => !kw || c.label.toLowerCase().includes(kw) || c.tag.toLowerCase().includes(kw)).forEach(c => {
                            const item = doc.createElement("div");
                            item.className = "cmdk-item";
                            item.innerHTML = '<span>' + c.label + '</span><span class="cmdk-tag">' + c.tag + '</span>';
                            item.addEventListener("click", function() {
                                overlay.classList.remove("open");
                                c.act();
                            });
                            list.appendChild(item);
                        });
                    }

                    function openCmdk() {
                        renderCmdList("");
                        inp.value = "";
                        overlay.classList.add("open");
                        setTimeout(() => inp.focus(), 30);
                    }

                    inp.addEventListener("input", function() { renderCmdList(inp.value); });
                    overlay.addEventListener("click", function(e) { if (e.target === overlay) overlay.classList.remove("open"); });

                    doc.addEventListener("click", function(e) {
                        if (e.target.closest(".cmd-trigger")) openCmdk();
                    });
                    doc.addEventListener("keydown", function(e) {
                        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
                            e.preventDefault();
                            if (overlay.classList.contains("open")) overlay.classList.remove("open");
                            else openCmdk();
                        } else if (e.key === "Escape" && overlay.classList.contains("open")) {
                            overlay.classList.remove("open");
                        }
                    });
                }
            } catch (e) {}
        })();
        </script>
        </body>
        </html>
        """,
        height=0,
    )

def render_chat_auto_chart(query_df: pd.DataFrame, t: dict, chart_key: str) -> None:
    if query_df is None or len(query_df) < 2 or len(query_df.columns) < 2:
        return
    num_cols = query_df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        return
    other_cols = [c for c in query_df.columns if c not in num_cols]
    y_col = num_cols[0]
    fig = None
    if other_cols:
        x_col = other_cols[0]
        if pd.api.types.is_datetime64_any_dtype(query_df[x_col]):
            fig = px.area(
                query_df,
                x=x_col,
                y=y_col,
                markers=True,
                line_shape="spline",
                color_discrete_sequence=[t["accent"]],
            )
            fig.update_traces(fillcolor=t["accent_soft"], line=dict(width=2.2))
        else:
            plot_df = query_df.head(15)
            fig = px.bar(
                plot_df,
                x=x_col,
                y=y_col,
                color=x_col,
                text_auto=".2s",
                color_discrete_sequence=t["palette"],
            )
            fig.update_traces(marker_line_width=0)
            fig.update_layout(showlegend=False)
    elif len(num_cols) >= 2:
        fig = px.scatter(
            query_df,
            x=num_cols[0],
            y=num_cols[1],
            color_discrete_sequence=[t["accent"]],
        )
    if fig is not None:
        st.plotly_chart(
            style_plotly(fig, f"Visualisasi Otomatis ({y_col})", t, height=300),
            width="stretch",
            key=chart_key,
        )

def render_voice_input_widget(t: dict) -> None:
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style>
          html, body {{
            margin: 0; padding: 0; background: transparent;
            font-family: 'Space Grotesk', 'Inter', sans-serif;
          }}
          .voice-bar {{
            display: flex; align-items: center; gap: 10px;
          }}
          .mic-btn {{
            display: inline-flex; align-items: center; gap: 7px;
            background: {t["surface"]};
            color: {t["text"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
            padding: 7px 14px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            font-family: inherit;
            transition: border-color 180ms ease, background 180ms ease, color 180ms ease;
          }}
          .mic-btn:hover {{
            border-color: {t["accent"]};
            color: {t["accent"]};
          }}
          .mic-btn.listening {{
            border-color: #EF4444;
            color: #EF4444;
            background: rgba(239, 68, 68, 0.12);
          }}
          .voice-status {{
            font-size: 12px;
            color: {t["muted"]};
          }}
        </style>
        </head>
        <body>
          <div class="voice-bar">
            <button id="micBtn" class="mic-btn" type="button">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg>
              <span id="micLabel">Tanya Pakai Suara</span>
            </button>
            <span id="voiceStatus" class="voice-status"></span>
          </div>
          <script>
          (function() {{
            const btn = document.getElementById("micBtn");
            const lbl = document.getElementById("micLabel");
            const status = document.getElementById("voiceStatus");
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition || window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
            if (!SpeechRec) {{
              btn.disabled = true;
              btn.style.opacity = "0.5";
              status.textContent = "Browser ini belum mendukung input suara.";
              return;
            }}
            const rec = new SpeechRec();
            rec.lang = "id-ID";
            rec.interimResults = false;
            rec.maxAlternatives = 1;
            let active = false;

            btn.addEventListener("click", function() {{
              if (active) {{
                rec.stop();
                return;
              }}
              try {{
                active = true;
                btn.classList.add("listening");
                lbl.textContent = "Mendengarkan...";
                status.textContent = "Silakan bicara dalam bahasa Indonesia";
                rec.start();
              }} catch (err) {{
                active = false;
                btn.classList.remove("listening");
                lbl.textContent = "Tanya Pakai Suara";
              }}
            }});

            rec.onresult = function(event) {{
              const transcript = event.results[0][0].transcript;
              status.textContent = 'Terdengar: "' + transcript + '"';
              try {{
                const pdoc = window.parent.document;
                const ta = pdoc.querySelector('[data-testid="stChatInput"] textarea');
                if (ta) {{
                  const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value").set;
                  setter.call(ta, transcript);
                  ta.dispatchEvent(new Event("input", {{ bubbles: true }}));
                  ta.focus();
                  setTimeout(function() {{
                    const sendBtn = pdoc.querySelector('[data-testid="stChatInputSubmitButton"]');
                    if (sendBtn && !sendBtn.disabled) sendBtn.click();
                  }}, 120);
                }}
              }} catch (e) {{}}
            }};

            rec.onerror = function() {{
              status.textContent = "Suara tidak terbaca, coba lagi.";
            }};

            rec.onend = function() {{
              active = false;
              btn.classList.remove("listening");
              lbl.textContent = "Tanya Pakai Suara";
            }};
          }})();
          </script>
        </body>
        </html>
        """,
        height=44,
    )

def render_3d_ai_core(t: dict) -> None:
    st.markdown('<div class="spline-hero-anchor"></div>', unsafe_allow_html=True)
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <script type="module" src="https://cdn.spline.design/@splinetool/viewer@2.0.224/build/spline-viewer.js"></script>
        <style>
          html, body {{
            margin: 0; padding: 0; width: 100%; height: 100%;
            overflow: hidden;
            background: transparent;
          }}
          .stage {{
            position: relative;
            width: 100%;
            height: 460px;
            background: transparent;
            overflow: hidden;
            box-sizing: border-box;
            -webkit-mask-image: linear-gradient(to bottom, #000000 66%, transparent 100%);
            mask-image: linear-gradient(to bottom, #000000 66%, transparent 100%);
          }}
          @media (max-width: 640px) {{
            .stage {{
              height: 240px;
              -webkit-mask-image: linear-gradient(to bottom, #000000 66%, transparent 100%);
              mask-image: linear-gradient(to bottom, #000000 66%, transparent 100%);
            }}
            spline-viewer {{
              transform: scale(1.18);
              transform-origin: center 45%;
            }}
          }}
          spline-viewer {{
            width: 100%;
            height: 100%;
            display: block;
            background: transparent;
          }}
        </style>
        </head>
        <body>
          <div class="stage">
            <spline-viewer id="splineBot" url="https://prod.spline.design/YM-p4SVMlLBHCory/scene.splinecode" background="transparent"></spline-viewer>
          </div>
          <script>
          (function() {{
            const viewer = document.getElementById("splineBot");
            function hideLogo() {{
              if (!viewer || !viewer.shadowRoot) return false;
              const root = viewer.shadowRoot;
              const logo = root.querySelector('#logo, a[href*="spline.design"]');
              if (logo) {{
                logo.style.display = "none";
                logo.remove();
                return true;
              }}
              if (!root.querySelector("#hideSplineLogoStyle")) {{
                const st = document.createElement("style");
                st.id = "hideSplineLogoStyle";
                st.textContent = '#logo, a[href*="spline.design"] {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}';
                root.appendChild(st);
              }}
              return false;
            }}
            function hideTextObjects() {{
              try {{
                const sp = viewer && (viewer._spline || viewer.spline);
                if (!sp || !sp.findObjectByName) return;
                ["Text", "text", "nexbot", "Nexbot", "NEXBOT", "Title", "Logo"].forEach(function(n) {{
                  const obj = sp.findObjectByName(n);
                  if (obj) obj.visible = false;
                }});
              }} catch (e) {{}}
            }}
            if (viewer) {{
              viewer.addEventListener("load-complete", hideTextObjects);
              viewer.addEventListener("load", hideTextObjects);
            }}
            const timer = setInterval(function() {{
              const done = hideLogo();
              hideTextObjects();
              if (done) clearInterval(timer);
            }}, 150);
            setTimeout(function() {{ clearInterval(timer); }}, 10000);
          }})();
          </script>
        </body>
        </html>
        """,
        height=464,
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
        title=dict(
            text=title,
            font=dict(size=13, color=t["text"], family="Space Grotesk, Inter, sans-serif"),
            pad=dict(l=4),
        ),
        paper_bgcolor=t["surface"],
        plot_bgcolor=t["surface"],
        font=dict(family="Space Grotesk, Inter, sans-serif", color=t["muted"], size=11),
        margin=dict(l=12, r=12, t=44, b=12),
        height=height,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.24,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        hoverlabel=dict(
            bgcolor=t["surface_alt"],
            font_color=t["text"],
            bordercolor=t["accent"],
            font=dict(family="Space Grotesk, Inter, sans-serif", size=12),
        ),
        bargap=0.28,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=t["border"],
        zeroline=False,
        tickfont=dict(size=11),
    )
    fig.update_yaxes(
        gridcolor=t["grid"],
        zeroline=False,
        tickfont=dict(size=11),
    )
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
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b",
    ]
    if not api_key:
        return fallback
    try:
        from groq import Groq

        tmp_client = Groq(api_key=api_key)
        models = tmp_client.models.list().data
        excluded = ("whisper", "guard", "tts", "playai", "safeguard", "allam")
        priority = [
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-120b",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "qwen/qwen3-32b",
            "llama-3.1-8b-instant",
        ]

        def rank_key(mid: str) -> tuple[int, str]:
            return (priority.index(mid) if mid in priority else 99, mid)

        ids = sorted(
            (m.id for m in models if not any(ex in m.id.lower() for ex in excluded)),
            key=rank_key,
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
    client,
    preferred_model: str,
    available_models: list[str],
    messages: list[dict],
    temperature: float = 0.3,
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
                    temperature=temperature,
                    max_tokens=900,
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

def build_rich_data_context(
    filtered_df: pd.DataFrame,
    agg_df: pd.DataFrame,
    cat_col: str,
    num_col: str,
    date_col: str | None,
    source_name: str,
) -> str:
    col_lines = []
    for c in filtered_df.columns:
        dtype_str = str(filtered_df[c].dtype)
        null_cnt = int(filtered_df[c].isna().sum())
        if pd.api.types.is_numeric_dtype(filtered_df[c]):
            s = filtered_df[c].dropna()
            if not s.empty:
                col_lines.append(
                    f'- "{c}" ({dtype_str}): sum={s.sum():,.2f}, avg={s.mean():,.2f}, min={s.min():,.2f}, max={s.max():,.2f}, null={null_cnt}'
                )
            else:
                col_lines.append(f'- "{c}" ({dtype_str}): seluruhnya null')
        elif pd.api.types.is_datetime64_any_dtype(filtered_df[c]):
            s = filtered_df[c].dropna()
            if not s.empty:
                col_lines.append(
                    f'- "{c}" (tanggal): rentang {s.min().strftime("%Y-%m-%d")} s/d {s.max().strftime("%Y-%m-%d")}, null={null_cnt}'
                )
        else:
            nunique = int(filtered_df[c].nunique(dropna=True))
            samples = filtered_df[c].dropna().astype(str).unique().tolist()[:6]
            sample_str = ", ".join(samples)
            col_lines.append(
                f'- "{c}" (teks/kategori, {nunique} unik, contoh: [{sample_str}], null={null_cnt})'
            )

    agg_summary = summarize_agg_for_llm(
        agg_df[[cat_col, f"Total_{num_col}", "Kontribusi (%)"]], cat_col, num_col, max_rows=10
    )
    return (
        f"Dataset: {source_name}\n"
        f"Jumlah baris aktif (setelah filter): {len(filtered_df):,}\n"
        f"Dimensi aktif di grafik: Kategori='{cat_col}', Nilai='{num_col}', Kolom Tanggal='{date_col or 'Tidak ada'}'\n"
        f"Nama tabel DuckDB untuk query: data\n"
        f"Skema & Statistik Kolom:\n" + "\n".join(col_lines) + "\n\n"
        f"Ringkasan Agregasi Aktif ({num_col} per {cat_col}):\n{agg_summary}"
    )

def run_safe_duckdb_query(sql: str, filtered_df: pd.DataFrame) -> pd.DataFrame:
    cleaned = sql.strip().rstrip(";").strip()
    upper = cleaned.upper()
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        raise ValueError("Hanya query SELECT atau WITH yang diizinkan.")
    forbidden = (
        r"\b(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE|ATTACH|DETACH|COPY|EXPORT|IMPORT|PRAGMA|CALL|REPLACE|TRUNCATE)\b"
    )
    if re.search(forbidden, upper):
        raise ValueError("Query mengandung perintah yang tidak diizinkan.")
    con = duckdb.connect(database=":memory:")
    try:
        con.register("data", filtered_df)
        res = con.execute(cleaned).df()
        return res.head(25)
    finally:
        con.close()

def extract_sql_from_reply(text: str) -> str | None:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            obj = json.loads(stripped)
            if isinstance(obj, dict) and isinstance(obj.get("sql"), str):
                return obj["sql"].strip()
        except Exception:
            pass
    json_match = re.search(r"\{\s*\"sql\"\s*:\s*\"([^\"]+)\"\s*\}", text, re.DOTALL)
    if json_match:
        return json_match.group(1).replace("\\n", " ").strip()
    return None

def ask_ai_with_data_context(
    client,
    preferred_model: str,
    available_models: list[str],
    chat_history: list[dict],
    rich_context: str,
    filtered_df: pd.DataFrame,
) -> tuple[str, str | None, pd.DataFrame | None]:
    user_msgs = [m for m in chat_history if m.get("role") == "user"]
    last_q = user_msgs[-1]["content"].strip() if user_msgs else ""
    sql_query = None
    query_df = None

    router_prompt = (
        "Tugas Anda HANYA menentukan apakah pertanyaan pengguna membutuhkan query SQL DuckDB pada tabel `data`.\n"
        f"Skema data:\n{rich_context}\n\n"
        f"Pertanyaan pengguna: {last_q}\n\n"
        "ATURAN:\n"
        "- Jika pertanyaan meminta statistik, angka, total, rata-rata, filter, perbandingan, produk terlaris, atau rincian dari kolom dataset, balas HANYA 1 baris query DuckDB SELECT yang valid (pakai tanda kutip ganda untuk nama kolom, akhiri dengan LIMIT 25, tanpa markdown).\n"
        "- Jika pertanyaan hanya sapaan, tes, komentar, atau tidak butuh hitungan SQL baru, balas HANYA kata: NO_SQL"
    )
    try:
        route_out, used_model = chat_with_fallback(
            client,
            preferred_model,
            available_models,
            [{"role": "user", "content": router_prompt}],
            temperature=0.0,
        )
        route_clean = re.sub(r"```sql|```", "", route_out, flags=re.IGNORECASE).strip()
        if "NO_SQL" not in route_clean.upper() and re.match(
            r"^(SELECT|WITH)\b", route_clean, re.IGNORECASE
        ):
            candidate_sql = route_clean.split(";")[0].strip()
            query_df = run_safe_duckdb_query(candidate_sql, filtered_df)
            sql_query = candidate_sql
    except Exception:
        sql_query = None
        query_df = None
        used_model = preferred_model

    data_block = ""
    if query_df is not None:
        res_txt = (
            "Hasil perhitungan kosong (0 baris)."
            if query_df.empty
            else query_df.to_string(index=False)
        )
        data_block = f"\n\nHasil perhitungan langsung dari dataset:\n{res_txt}"

    clean_hist = [
        m
        for m in chat_history
        if m.get("role") in ("user", "assistant")
        and '"kategori' not in m.get("content", "")
        and "[P1082" not in m.get("content", "")
    ][-4:]

    answer_system = (
        "Anda adalah analis bisnis dan data profesional. Berikan jawaban dalam bahasa Indonesia yang natural, ramah, ringkas, dan jelas.\n"
        "ATURAN KETAT:\n"
        "- DILARANG menampilkan kode SQL, format JSON, tanda kurung kurawal {}, atau mengulang-ulang kalimat.\n"
        "- DILARANG menggunakan emoji.\n"
        "- Gunakan hanya angka nyata dari konteks atau hasil perhitungan berikut. Jika pengguna hanya menyapa atau mengetes, jawab singkat dan tawarkan bantuan analisis data.\n\n"
        f"Ringkasan konteks data aktif:\n{rich_context}{data_block}"
    )
    final_msgs = [{"role": "system", "content": answer_system}] + clean_hist
    final_reply, _ = chat_with_fallback(
        client, used_model, available_models, final_msgs, temperature=0.3
    )
    return final_reply, sql_query, query_df

def compute_smart_insights(
    filtered_df: pd.DataFrame,
    date_col: str | None,
    num_col: str,
    numeric_cols: list[str],
) -> dict:
    total_rows = len(filtered_df)
    dup_rows = int(filtered_df.duplicated().sum()) if total_rows <= 150000 else 0
    null_cols = {
        c: int(filtered_df[c].isna().sum())
        for c in filtered_df.columns
        if filtered_df[c].isna().any()
    }
    total_cells = max(total_rows * max(len(filtered_df.columns), 1), 1)
    completeness = 100.0 - (sum(null_cols.values()) / total_cells * 100.0)

    trend_growth = None
    anomaly_note = None
    if date_col:
        q_date = quote_ident(date_col)
        q_num = quote_ident(num_col)
        valid_dates = filtered_df[date_col].dropna()
        span_days = (valid_dates.max() - valid_dates.min()).days if not valid_dates.empty else 0
        date_expr = (
            f"DATE_TRUNC('month', CAST({q_date} AS DATE))"
            if span_days > 45
            else f"CAST({q_date} AS DATE)"
        )
        tdf = duckdb.sql(
            f"SELECT {date_expr} AS Periode, SUM({q_num}) AS Nilai FROM filtered_df WHERE {q_date} IS NOT NULL GROUP BY 1 ORDER BY 1"
        ).df()
        if len(tdf) >= 2:
            last_val = float(tdf.iloc[-1]["Nilai"])
            prev_val = float(tdf.iloc[-2]["Nilai"])
            if prev_val != 0:
                trend_growth = (last_val - prev_val) / abs(prev_val) * 100.0
        if len(tdf) >= 4:
            mean_v = float(tdf["Nilai"].mean())
            std_v = float(tdf["Nilai"].std())
            if std_v > 0:
                tdf["z"] = (tdf["Nilai"] - mean_v) / std_v
                peak_row = tdf.loc[tdf["z"].abs().idxmax()]
                if abs(float(peak_row["z"])) >= 1.5:
                    p_label = pd.to_datetime(peak_row["Periode"]).strftime("%Y-%m-%d")
                    arah = "lonjakan tertinggi" if float(peak_row["z"]) > 0 else "penurunan tajam"
                    anomaly_note = (
                        f"Terdeteksi {arah} pada periode {p_label} sebesar {float(peak_row['Nilai']):,.0f} "
                        f"(deviasi {abs(float(peak_row['z'])):.1f}x standar deviasi)."
                    )

    top_corr = None
    if len(numeric_cols) >= 2:
        sample_num = filtered_df[numeric_cols].dropna()
        if len(sample_num) >= 5:
            corr_mat = sample_num.corr(numeric_only=True)
            best_pair = None
            best_val = 0.0
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    c1, c2 = numeric_cols[i], numeric_cols[j]
                    val = corr_mat.loc[c1, c2]
                    if pd.notna(val) and abs(float(val)) > abs(best_val):
                        best_val = float(val)
                        best_pair = (c1, c2)
            if best_pair and abs(best_val) >= 0.35:
                top_corr = (best_pair[0], best_pair[1], best_val)

    return {
        "dup_rows": dup_rows,
        "null_cols": null_cols,
        "completeness": completeness,
        "trend_growth": trend_growth,
        "anomaly_note": anomaly_note,
        "top_corr": top_corr,
    }

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
    import datetime
    now_str = datetime.datetime.now().strftime("%d %B %Y, %H:%M")

    table_rows_html = ""
    for i, row in agg_df.iterrows():
        bg = "#F8FAFC" if i % 2 == 0 else "#FFFFFF"
        pct = float(row.get("Kontribusi (%)", 0))
        bar_w = min(pct, 100)
        val = float(row.iloc[1])
        table_rows_html += f"""
        <tr style="background:{bg};">
            <td style="padding:8px 12px;border-bottom:1px solid #E2E8F0;font-size:12.5px;">{html.escape(str(row.iloc[0]))}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #E2E8F0;font-size:12.5px;font-variant-numeric:tabular-nums;text-align:right;font-weight:600;">{val:,.0f}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #E2E8F0;font-size:12.5px;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="flex:1;height:6px;background:#E2E8F0;border-radius:999px;overflow:hidden;">
                        <div style="width:{bar_w:.1f}%;height:100%;background:#1D4ED8;border-radius:999px;"></div>
                    </div>
                    <span style="font-size:11px;color:#475569;min-width:36px;text-align:right;">{pct:.1f}%</span>
                </div>
            </td>
        </tr>"""

    top2_share = float(agg_df.head(2)["Kontribusi (%)"].sum()) if "Kontribusi (%)" in agg_df.columns else 0
    ai_paragraphs = ""
    for para in ai_text.split("\n"):
        para = para.strip()
        if not para:
            continue
        escaped = html.escape(para)
        if para.startswith(("1.", "2.", "3.", "#")):
            ai_paragraphs += f'<p style="margin:0 0 6px 0;font-weight:600;color:#1E293B;">{escaped}</p>'
        else:
            ai_paragraphs += f'<p style="margin:0 0 8px 0;color:#334155;">{escaped}</p>'

    doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Laporan Analisis — {html.escape(source_name)}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    padding: 32px 40px;
    max-width: 960px;
    margin: 0 auto;
    line-height: 1.6;
    font-size: 13.5px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .report-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 16px;
    border-bottom: 2px solid #0F172A;
    margin-bottom: 24px;
  }}
  .report-logo {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .report-logo-mark {{
    width: 40px; height: 40px;
    background: #1D4ED8;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
  }}
  .report-logo-mark svg {{ color: white; }}
  .report-title {{ font-size: 18px; font-weight: 700; color: #0F172A; letter-spacing: -0.02em; }}
  .report-subtitle {{ font-size: 11.5px; color: #64748B; margin-top: 2px; }}
  .report-meta {{ text-align: right; font-size: 11px; color: #64748B; line-height: 1.8; }}
  .report-meta strong {{ color: #334155; }}
  .print-btn {{
    display: inline-flex; align-items: center; gap: 6px;
    background: #1D4ED8; color: #fff; border: none;
    padding: 9px 18px; border-radius: 8px;
    font-weight: 600; font-size: 13px; cursor: pointer;
    margin-top: 10px;
    font-family: 'Inter', sans-serif;
  }}
  .print-btn:hover {{ background: #1E40AF; }}
  .section-title {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
  }}
  .section-title::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: #E2E8F0;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 28px;
  }}
  .kpi-card {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 16px;
    border-top: 3px solid #1D4ED8;
  }}
  .kpi-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94A3B8;
    margin-bottom: 6px;
  }}
  .kpi-value {{
    font-size: 20px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }}
  .kpi-sub {{
    font-size: 10.5px;
    color: #94A3B8;
    margin-top: 4px;
  }}
  .info-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 28px;
  }}
  .info-box {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 18px;
  }}
  .info-box h3 {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94A3B8;
    margin-bottom: 10px;
  }}
  .stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #F1F5F9;
  }}
  .stat-row:last-child {{ border-bottom: none; }}
  .stat-label {{ font-size: 12px; color: #475569; }}
  .stat-value {{ font-size: 12.5px; font-weight: 600; color: #0F172A; font-variant-numeric: tabular-nums; }}
  .ai-box {{
    background: #F0F7FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #1D4ED8;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 28px;
  }}
  .ai-box h3 {{
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #1D4ED8; margin-bottom: 12px;
  }}
  .ai-content {{ font-size: 12.5px; color: #1E3A5F; line-height: 1.65; }}
  .ai-content p {{ margin: 0 0 8px 0; }}
  .ai-content p:last-child {{ margin-bottom: 0; }}
  .table-wrap {{ margin-bottom: 28px; }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }}
  .data-table thead th {{
    background: #1D4ED8;
    color: #FFFFFF;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .data-table thead th:last-child {{ text-align: left; min-width: 160px; }}
  .data-table tbody tr:hover {{ background: #EFF6FF !important; }}
  .data-table td {{ vertical-align: middle; }}
  .footer {{
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #E2E8F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
    color: #94A3B8;
  }}
  @media print {{
    @page {{ size: A4 portrait; margin: 15mm 15mm 15mm 15mm; }}
    body {{ padding: 0; font-size: 11.5px; }}
    .print-btn {{ display: none !important; }}
    .kpi-card {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .ai-box {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .data-table thead th {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .kpi-value {{ font-size: 16px; }}
    .info-grid {{ grid-template-columns: 1fr 1fr; }}
  }}
</style>
</head>
<body>

  <div class="report-header">
    <div class="report-logo">
      <div class="report-logo-mark">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>
        </svg>
      </div>
      <div>
        <div class="report-title">AI-Powered Dashboard Pro</div>
        <div class="report-subtitle">Laporan Analisis Data Bisnis</div>
      </div>
    </div>
    <div class="report-meta">
      <div>Dataset: <strong>{html.escape(source_name)}</strong></div>
      <div>Dimensi: <strong>{html.escape(cat_col)}</strong> &times; <strong>{html.escape(num_col)}</strong></div>
      <div>Kelompok: <strong>Mahira Azzahra &amp; Adelia Amanta Wada</strong></div>
      <div>Dicetak: {now_str}</div>
      <button class="print-btn" onclick="window.print()">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Cetak / Simpan PDF
      </button>
    </div>
  </div>

  <div class="section-title">Ringkasan Eksekutif</div>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Total {html.escape(num_col)}</div>
      <div class="kpi-value">{total_sum:,.0f}</div>
      <div class="kpi-sub">Seluruh data terfilter</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Rata-rata / {html.escape(cat_col)}</div>
      <div class="kpi-value">{avg_val:,.0f}</div>
      <div class="kpi-sub">Per {html.escape(cat_col)}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Performa Tertinggi</div>
      <div class="kpi-value" style="font-size:14px;">{html.escape(top_cat)}</div>
      <div class="kpi-sub">{top_value:,.0f} &mdash; {top_share:.1f}% kontribusi</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Selisih Tertinggi&ndash;Terendah</div>
      <div class="kpi-value">{gap_value:,.0f}</div>
      <div class="kpi-sub">Terendah: {html.escape(bottom_cat)}</div>
    </div>
  </div>

  <div class="section-title">Detail Statistik</div>
  <div class="info-grid">
    <div class="info-box">
      <h3>Performa Kategori</h3>
      <div class="stat-row"><span class="stat-label">{html.escape(cat_col)} Tertinggi</span><span class="stat-value">{html.escape(top_cat)}</span></div>
      <div class="stat-row"><span class="stat-label">Nilai Tertinggi</span><span class="stat-value">{top_value:,.0f}</span></div>
      <div class="stat-row"><span class="stat-label">Kontribusi Tertinggi</span><span class="stat-value">{top_share:.1f}%</span></div>
      <div class="stat-row"><span class="stat-label">{html.escape(cat_col)} Terendah</span><span class="stat-value">{html.escape(bottom_cat)}</span></div>
      <div class="stat-row"><span class="stat-label">Nilai Terendah</span><span class="stat-value">{bottom_value:,.0f}</span></div>
      <div class="stat-row"><span class="stat-label">Selisih Gap</span><span class="stat-value">{gap_value:,.0f}</span></div>
    </div>
    <div class="info-box">
      <h3>Distribusi &amp; Konsentrasi</h3>
      <div class="stat-row"><span class="stat-label">Total {html.escape(num_col)}</span><span class="stat-value">{total_sum:,.0f}</span></div>
      <div class="stat-row"><span class="stat-label">Rata-rata per {html.escape(cat_col)}</span><span class="stat-value">{avg_val:,.0f}</span></div>
      <div class="stat-row"><span class="stat-label">Jumlah {html.escape(cat_col)}</span><span class="stat-value">{len(agg_df):,}</span></div>
      <div class="stat-row"><span class="stat-label">Konsentrasi Top 2</span><span class="stat-value">{top2_share:.1f}%</span></div>
    </div>
  </div>

  <div class="section-title">Analisis Strategis AI</div>
  <div class="ai-box">
    <h3>Groq AI — Analisis Bisnis Otomatis</h3>
    <div class="ai-content">{ai_paragraphs}</div>
  </div>

  <div class="section-title">Tabel Ringkasan Performa ({len(agg_df):,} {html.escape(cat_col)})</div>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>{html.escape(cat_col)}</th>
          <th style="text-align:right;">Total {html.escape(num_col)}</th>
          <th>Kontribusi (%)</th>
        </tr>
      </thead>
      <tbody>
        {table_rows_html}
      </tbody>
    </table>
  </div>

  <div class="footer">
    <div>AI-Powered Dashboard Pro &mdash; Kelompok: Mahira Azzahra &amp; Adelia Amanta Wada</div>
    <div>Dibuat otomatis pada {now_str}</div>
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
if "presentation_mode" not in st.session_state:
    st.session_state.presentation_mode = False
if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0

with st.sidebar:
    with st.container(border=True):
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
        global_loader, "Loading...", active_theme
    )
    time.sleep(2.2)
    global_loader.empty()
    st.session_state.app_booted = True

GROQ_API_KEY = resolve_groq_api_key(st.session_state.manual_api_key)
available_models = fetch_groq_models(GROQ_API_KEY)
if "selected_model" not in st.session_state or st.session_state.selected_model not in available_models:
    st.session_state.selected_model = available_models[0]

with st.sidebar:
    with st.container(border=True):
        sidebar_heading(ICON_KEY, "Pengaturan")
        manual_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            key="manual_api_key",
            help="Kosongkan jika sudah diatur di .env atau Streamlit Secrets.",
        )
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
    with st.container(border=True):
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
                    "_loaded_file_sig",
                ):
                    st.session_state.pop(k, None)
                st.session_state.presentation_mode = False
                st.session_state.upload_gen += 1
                st.rerun()
            pres_label = (
                "Keluar Mode Presentasi"
                if st.session_state.presentation_mode
                else "Mode Presentasi"
            )
            pres_icon = (
                ":material/close_fullscreen:"
                if st.session_state.presentation_mode
                else ":material/slideshow:"
            )
            if st.button(pres_label, icon=pres_icon, width="stretch"):
                st.session_state.presentation_mode = not st.session_state.presentation_mode
                st.session_state.slide_idx = 0
                st.rerun()

if sidebar_file is not None:
    st.session_state["uploaded_bytes"] = sidebar_file.getvalue()
    st.session_state["uploaded_name"] = sidebar_file.name

df = None
source_name = ""
if "uploaded_bytes" in st.session_state and "uploaded_name" in st.session_state:
    source_name = st.session_state["uploaded_name"]
    file_sig = f"{source_name}:{len(st.session_state['uploaded_bytes'])}"
    is_new_file = st.session_state.get("_loaded_file_sig") != file_sig
    if is_new_file:
        render_robot_loader(global_loader, f"Membaca dataset {source_name}...", active_theme)
        t_start = time.monotonic()
        df = load_dataset_cached(st.session_state["uploaded_bytes"], source_name)
        elapsed = time.monotonic() - t_start
        if elapsed < 0.85:
            time.sleep(0.85 - elapsed)
        global_loader.empty()
        st.session_state["_loaded_file_sig"] = file_sig
    else:
        df = load_dataset_cached(st.session_state["uploaded_bytes"], source_name)

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
                        <p class="topbar-sub">Prototype v2.0 - Rule-Based & AI Commentary + Chat Mode + Made By Maira & Wada</p>
                    </div>
                </div>
                <div class="badge-group">
                    {data_pill}
                    {ai_pill}
                    <span class="cmd-trigger">Perintah <span class="cmd-kbd">Ctrl+K</span></span>
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
inject_3d_tilt_script()

                                       
                             
                                       
if df is None:
    with st.sidebar:
        st.markdown('<div class="sidebar-erde">erde</div>', unsafe_allow_html=True)

    render_3d_ai_core(active_theme)

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
rich_context = build_rich_data_context(
    filtered_df, agg_df, cat_col, num_col, date_col, source_name
)
st.session_state.rich_context = rich_context
analysis_key = (
    f"{source_name}|{len(filtered_df)}|{total_sum:.2f}|{cat_col}|{num_col}|{selected_model}|{bool(client)}"
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
    st.session_state.chat_history = [
        {"role": "assistant", "content": ai_text},
    ]

if st.session_state.get("presentation_mode"):
    slide_titles = [
        ("Slide 1 / 3", "Ringkasan Eksekutif & Performa Utama"),
        ("Slide 2 / 3", f"Visualisasi {num_col} per {cat_col}"),
        ("Slide 3 / 3", "Audit Data, Anomali & Strategi AI"),
    ]
    cur_slide = int(st.session_state.get("slide_idx", 0)) % 3
    s_badge, s_title = slide_titles[cur_slide]
    st.markdown(
        f"""
        <div class="slide-banner">
            <div>
                <div class="slide-badge">{s_badge}</div>
                <div class="slide-heading">{html.escape(s_title)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav_c1, nav_c2, nav_c3 = st.columns([1, 1, 1], gap="small")
    if nav_c1.button("Sebelumnya", icon=":material/arrow_back:", width="stretch"):
        st.session_state.slide_idx = (cur_slide - 1) % 3
        st.rerun()
    if nav_c2.button("Berikutnya", icon=":material/arrow_forward:", width="stretch"):
        st.session_state.slide_idx = (cur_slide + 1) % 3
        st.rerun()
    if nav_c3.button("Keluar Presentasi", icon=":material/close:", width="stretch"):
        st.session_state.presentation_mode = False
        st.rerun()

    if cur_slide == 0:
        top5_slide = agg_df.head(5)
        rank_slide_html = ""
        for idx, row in top5_slide.iterrows():
            r_name = html.escape(str(row[cat_col]))
            r_val = format_compact(float(row[total_col]))
            r_pct = float(row["Kontribusi (%)"])
            bar_color = PALETTE[idx % len(PALETTE)]
            rank_slide_html += (
                f'<div class="rank-row">'
                f'<div class="rank-top"><span class="rank-name">{r_name}</span>'
                f'<span class="rank-val">{r_val} ({r_pct:.1f}%)</span></div>'
                f'<div class="rank-track"><div class="rank-fill" style="width:{min(r_pct, 100):.1f}%; background:{bar_color};"></div></div>'
                f'</div>'
            )
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="panel-header">{ICON_TROPHY}<span>5 Performa Teratas ({html.escape(cat_col)})</span></div>
                {rank_slide_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif cur_slide == 1:
        slide_df = agg_df.head(15)
        fig_slide = px.bar(
            slide_df,
            x=cat_col,
            y=total_col,
            color=cat_col,
            text_auto=".2s",
            color_discrete_sequence=PALETTE,
        )
        fig_slide.update_traces(marker_line_width=0)
        fig_slide.update_layout(showlegend=False)
        st.plotly_chart(
            style_plotly(fig_slide, f"{num_col} per {cat_col}", active_theme, height=460),
            width="stretch",
            key="pres_chart_main",
        )
    else:
        st.markdown(
            f'<div class="panel-card"><div class="panel-header">{ICON_CPU}<span>Analisis Strategis AI</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="ai-justified">', unsafe_allow_html=True)
        st.markdown(st.session_state.ai_text)
        st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

                                       
                                         
                                       
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
            fig_main.update_traces(marker_line_width=0)
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
            fig_main.update_traces(marker_line_width=0)
            fig_main.update_layout(showlegend=False)
        else:
            fig_main = px.pie(
                chart_df,
                names=cat_col,
                values=total_col,
                hole=0.48,
                color_discrete_sequence=PALETTE,
            )
        st.plotly_chart(
            style_plotly(
                fig_main, f"{num_col} per {cat_col}{chart_note}", active_theme, height=450
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

    if len(agg_df) >= 2:
        st.markdown("##### Perbandingan Head-to-Head")
        h_opts = agg_df[cat_col].astype(str).tolist()
        h2h_c1, h2h_c2 = st.columns(2, gap="small")
        with h2h_c1:
            item_a = st.selectbox("Item A", options=h_opts, index=0, key=f"h2h_a_{cat_col}")
        with h2h_c2:
            item_b = st.selectbox("Item B", options=h_opts, index=1, key=f"h2h_b_{cat_col}")
        row_a = agg_df[agg_df[cat_col].astype(str) == item_a].iloc[0]
        row_b = agg_df[agg_df[cat_col].astype(str) == item_b].iloc[0]
        val_a = float(row_a[total_col])
        val_b = float(row_b[total_col])
        trx_a = int(row_a["Transaksi"])
        trx_b = int(row_b["Transaksi"])
        pct_a = float(row_a["Kontribusi (%)"])
        pct_b = float(row_b["Kontribusi (%)"])
        pair_total = max(abs(val_a) + abs(val_b), 1e-9)
        w_a = max(min(abs(val_a) / pair_total * 100.0, 100.0), 0.0)
        w_b = 100.0 - w_a
        diff_ab = abs(val_a - val_b)
        win_a_cls = "winner" if val_a >= val_b else ""
        win_b_cls = "winner" if val_b > val_a else ""
        st.markdown(
            f"""
            <div class="h2h-wrap">
                <div class="h2h-grid">
                    <div class="h2h-card {win_a_cls}">
                        <div class="h2h-title">{html.escape(item_a)}</div>
                        <div class="h2h-val">{format_compact(val_a)}</div>
                        <div class="h2h-sub">{trx_a:,} transaksi &bull; {pct_a:.1f}% kontribusi</div>
                    </div>
                    <div class="h2h-vs">VS<br><span style="font-size:0.68rem;font-weight:500;">Selisih {format_compact(diff_ab)}</span></div>
                    <div class="h2h-card {win_b_cls}">
                        <div class="h2h-title">{html.escape(item_b)}</div>
                        <div class="h2h-val">{format_compact(val_b)}</div>
                        <div class="h2h-sub">{trx_b:,} transaksi &bull; {pct_b:.1f}% kontribusi</div>
                    </div>
                </div>
                <div class="h2h-bar-track">
                    <div class="h2h-bar-a" style="width:{w_a:.1f}%;"></div>
                    <div class="h2h-bar-b" style="width:{w_b:.1f}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_insights:
    col_rule, col_ai = st.columns(2, gap="medium")
    top2_share = float(agg_df.head(2)["Kontribusi (%)"].sum())
    smart_info = compute_smart_insights(filtered_df, date_col, num_col, numeric_cols)

    smart_items = [
        f"<li><strong>Kelengkapan Data:</strong> <b>{smart_info['completeness']:.1f}%</b> sel terisi ({smart_info['dup_rows']:,} baris duplikat terdeteksi).</li>"
    ]
    if smart_info["null_cols"]:
        null_desc = ", ".join(
            f"{html.escape(k)} ({v:,})" for k, v in list(smart_info["null_cols"].items())[:4]
        )
        smart_items.append(f"<li><strong>Nilai Kosong (Null):</strong> {null_desc}.</li>")
    if smart_info["trend_growth"] is not None:
        g = smart_info["trend_growth"]
        arah_g = "naik" if g >= 0 else "turun"
        smart_items.append(
            f"<li><strong>Pertumbuhan Periode Terakhir:</strong> {html.escape(num_col)} {arah_g} <b>{abs(g):.1f}%</b> dibanding periode sebelumnya.</li>"
        )
    if smart_info["anomaly_note"]:
        smart_items.append(
            f"<li><strong>Radar Anomali:</strong> {html.escape(smart_info['anomaly_note'])}</li>"
        )
    if smart_info["top_corr"]:
        c1, c2, r_val = smart_info["top_corr"]
        sifat = "searah (positif)" if r_val > 0 else "berlawanan (negatif)"
        smart_items.append(
            f"<li><strong>Korelasi Terkuat:</strong> <b>{html.escape(c1)}</b> &amp; <b>{html.escape(c2)}</b> berkorelasi {sifat} (<b>r = {r_val:.2f}</b>).</li>"
        )
    smart_list_html = "".join(smart_items)

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
            <div class="panel-card">
                <div class="panel-header">{ICON_ACTIVITY}<span>Audit Data &amp; Radar Anomali</span></div>
                <ul style="color:var(--text); line-height:1.75; padding-left:1.2rem; margin:0; font-size:0.92rem;">
                    {smart_list_html}
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
        st.markdown('<div class="ai-justified">', unsafe_allow_html=True)
        st.markdown(st.session_state.ai_text)
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab_chat:
    chat_top_l, chat_top_r = st.columns([4, 1])
    chat_top_l.caption(
        "Tanyakan detail, anomali, atau strategi bisnis berdasarkan data yang sedang aktif."
    )
    if chat_top_r.button("Reset Chat", icon=":material/refresh:", width="stretch"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": st.session_state.ai_text}
        ]
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

    chat_box = st.container()
    with chat_box:
        for idx_m, msg in enumerate(st.session_state.chat_history):
            if msg["role"] in ("user", "assistant"):
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg.get("query_rows") is not None:
                        render_chat_auto_chart(
                            msg["query_rows"], active_theme, f"chat_hist_chart_{idx_m}"
                        )
                    if msg.get("sql"):
                        with st.expander("Lihat Query & Data Perhitungan", expanded=False):
                            st.code(msg["sql"], language="sql")
                            if msg.get("query_rows") is not None:
                                st.dataframe(msg["query_rows"], width="stretch", hide_index=True)

    render_voice_input_widget(active_theme)
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
            with chat_box:
                st.chat_message("user").write(active_question)
            chat_loader = st.empty()
            render_robot_loader(
                chat_loader, "AI Analis sedang menyusun jawaban...", active_theme
            )
            try:
                answer, sql_used, query_df = ask_ai_with_data_context(
                    client,
                    selected_model,
                    available_models,
                    st.session_state.chat_history,
                    st.session_state.get("rich_context", ""),
                    filtered_df,
                )
                chat_loader.empty()
                msg_entry = {"role": "assistant", "content": answer}
                if sql_used:
                    msg_entry["sql"] = sql_used
                    msg_entry["query_rows"] = query_df
                st.session_state.chat_history.append(msg_entry)
                with chat_box:
                    with st.chat_message("assistant"):
                        st.write(answer)
                        if query_df is not None:
                            render_chat_auto_chart(
                                query_df,
                                active_theme,
                                f"chat_live_chart_{len(st.session_state.chat_history)}",
                            )
                        if sql_used:
                            with st.expander("Lihat Query & Data Perhitungan", expanded=False):
                                st.code(sql_used, language="sql")
                                if query_df is not None:
                                    st.dataframe(query_df, width="stretch", hide_index=True)
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
