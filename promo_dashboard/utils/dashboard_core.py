"""
Dashboard Core Utilities
Shared styling, chart builders, data loaders, and helper functions
for Mailer and Big Banner dashboards.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Tuple, Optional, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# ── DIVISION CONFIGURATIONS ───────────────────────────────────────────────────

# LMI: 6 divisi + Other
DIVISION_MAP_LMI = {
    "FRESH FOOD": "FRESH FOOD",
    "MEAL SOLUTION": "MEAL SOLUTION",
    "DRY FOOD": "DRY FOOD",
    "H&B HOME CARE": "H&B HOME CARE",
    "ELECTRONIC": "ELECTRONIC",
    "NON FOOD": "NON FOOD",
    "OTHER": "Other",
}

DIVISION_ORDER_LMI = [
    "FRESH FOOD", "MEAL SOLUTION", "DRY FOOD",
    "H&B HOME CARE", "ELECTRONIC", "NON FOOD", "Other",
]

DIVISION_COLORS_LMI = {
    "FRESH FOOD": "#00f5d4",
    "MEAL SOLUTION": "#fee440",
    "DRY FOOD": "#00d4ff",
    "H&B HOME CARE": "#f97316",
    "ELECTRONIC": "#e879f9",
    "NON FOOD": "#9b5de5",
    "Other": "#718096",
}

DIVISION_CARD_COLOR_LMI = {
    "FRESH FOOD": "teal",
    "MEAL SOLUTION": "orange",
    "DRY FOOD": "blue",
    "H&B HOME CARE": "amber",
    "ELECTRONIC": "pink",
    "NON FOOD": "purple",
    "Other": "red",
}

# LSI: H&B HOME CARE → DRY FOOD, ELECTRONIC → NON FOOD (5 divisi)
DIVISION_MAP_LSI = {
    "FRESH FOOD": "FRESH FOOD",
    "MEAL SOLUTION": "MEAL SOLUTION",
    "DRY FOOD": "DRY FOOD",
    "H&B HOME CARE": "DRY FOOD",
    "ELECTRONIC": "NON FOOD",
    "NON FOOD": "NON FOOD",
    "OTHER": "Other",
}

DIVISION_ORDER_LSI = ["FRESH FOOD", "MEAL SOLUTION", "DRY FOOD", "NON FOOD", "Other"]

DIVISION_COLORS_LSI = {
    "FRESH FOOD": "#00f5d4",
    "MEAL SOLUTION": "#fee440",
    "DRY FOOD": "#00d4ff",
    "NON FOOD": "#9b5de5",
    "Other": "#718096",
}

DIVISION_CARD_COLOR_LSI = {
    "FRESH FOOD": "teal",
    "MEAL SOLUTION": "orange",
    "DRY FOOD": "blue",
    "NON FOOD": "purple",
    "Other": "red",
}

# ── CATEGORY → GROUP MAPPING ──────────────────────────────────────────────────

GROUP_ID_MAP_LMI = {
    "31": "FRESH FOOD", "32": "FRESH FOOD", "33": "FRESH FOOD",
    "34": "FRESH FOOD", "35": "FRESH FOOD",
    "80": "MEAL SOLUTION", "82": "MEAL SOLUTION",
    "11": "DRY FOOD", "17": "DRY FOOD", "21": "DRY FOOD",
    "23": "DRY FOOD", "24": "DRY FOOD",
    "14": "H&B HOME CARE", "19": "H&B HOME CARE",
    "86": "ELECTRONIC", "87": "ELECTRONIC", "88": "ELECTRONIC",
    "51": "NON FOOD", "57": "NON FOOD", "85": "NON FOOD",
    "13": "NON FOOD", "62": "NON FOOD", "71": "NON FOOD",
    "97": "OTHER", "98": "OTHER", "99": "OTHER",
}

GROUP_ID_MAP_LSI = {
    "31": "FRESH FOOD", "32": "FRESH FOOD", "33": "FRESH FOOD",
    "34": "FRESH FOOD", "35": "FRESH FOOD",
    "80": "MEAL SOLUTION", "82": "MEAL SOLUTION",
    "17": "DRY FOOD", "21": "DRY FOOD", "11": "DRY FOOD",
    "26": "DRY FOOD", "27": "DRY FOOD",
    "14": "H&B HOME CARE", "19": "H&B HOME CARE",
    "86": "ELECTRONIC", "87": "ELECTRONIC", "88": "ELECTRONIC",
    "51": "NON FOOD", "57": "NON FOOD", "85": "NON FOOD",
    "13": "NON FOOD", "62": "NON FOOD", "71": "NON FOOD",
    "97": "OTHER", "98": "OTHER", "99": "OTHER",
}

# Group labels for identifying group rows in data
GROUP_LABELS_LMI = [
    "FRESH FOOD", "MEAL SOLUTION", "DRY FOOD",
    "H&B HOME CARE", "ELECTRONIC", "NON FOOD", "TOTAL",
]

GROUP_LABELS_LSI = [
    "DFF", "DMS", "DF1", "DF2", "DF3", "DDF", 
    "ELC", "NF1", "NF2", "NFI", "OTH", "ALL",
]

# ── STORE REGION MAPPING (LSI) ────────────────────────────────────────────────

STORE_REGION_MAP = {
    # Regional 1 (13 stores)
    "Alam Sutera": "Regional 1", "Batam": "Regional 1", "Ciputat": "Regional 1",
    "Jambi": "Regional 1", "Jatake": "Regional 1", "Kelapa Gading": "Regional 1",
    "Lampung": "Regional 1", "Medan": "Regional 1", "Palembang": "Regional 1",
    "Pasar Rebo": "Regional 1", "Pekanbaru": "Regional 1", "Serang": "Regional 1",
    "Serpong": "Regional 1",
    # Regional 2 (13 stores)
    "Bandung": "Regional 2", "Bekasi": "Regional 2", "Bogor": "Regional 2",
    "Cibitung": "Regional 2", "Cikarang": "Regional 2", "Cilengsi": "Regional 2",
    "Cimahi": "Regional 2", "Cirebon": "Regional 2", "Karawang": "Regional 2",
    "Meruya": "Regional 2", "Pakansari": "Regional 2", "Tasikmalaya": "Regional 2",
    "Tegal": "Regional 2",
    # Regional 3 (13 stores)
    "Balikpapan": "Regional 3", "Banjarmasin": "Regional 3", "Denpasar": "Regional 3",
    "Makassar": "Regional 3", "Malang": "Regional 3", "Manado": "Regional 3",
    "Mastrip SBY": "Regional 3", "Mataram": "Regional 3", "Samarinda": "Regional 3",
    "Semarang": "Regional 3", "Sidoarjo": "Regional 3", "Solo": "Regional 3",
    "Yogyakarta": "Regional 3",
}

# ── PLOTLY DARK THEME DEFAULTS ────────────────────────────────────────────────

PLOTLY_DARK_THEME = dict(
    plot_bgcolor="#1a2035",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
    xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
    yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
    legend=dict(bgcolor="rgba(26,32,53,0.8)", bordercolor="#2d3748", borderwidth=1, font=dict(color="#e2e8f0")),
    hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
    margin=dict(t=30, b=20, l=10, r=10),
)


# ═══════════════════════════════════════════════════════════════════════════════
# STYLING & CSS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_custom_css():
    """Apply custom dark theme CSS to the Streamlit app."""
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        color: #e2e8f0 !important;
    }
    .main, section.main { background: transparent !important; }
    .block-container { padding-top: 1rem; max-width: 1400px; }

    header[data-testid="stHeader"] { display: none !important; height: 0 !important; visibility: hidden !important; }
    [data-testid="stDecoration"] { display: none !important; height: 0 !important; }
    .stApp > header, header.stAppHeader,
    [data-testid="stAppViewBlockContainer"] > header, .stApp header {
        display: none !important; height: 0 !important; background: transparent !important;
    }
    .stApp { margin-top: 0 !important; padding-top: 0 !important; }
    .stApp > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0 !important; margin-top: 0 !important; }
    [data-testid="stAppViewContainer"] > div:first-child { padding-top: 0 !important; }
    [data-testid="stAppViewBlockContainer"], .block-container { padding-top: 1rem !important; margin-top: 0 !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
    [data-testid="stSidebarHeader"] button,
    button[kind="headerNoPadding"] { display: none !important; visibility: hidden !important; }
    span[data-testid="stIconMaterial"] { font-size: 0 !important; visibility: hidden !important; display: none !important; }
    [data-testid="stSidebarHeader"] { display: none !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; font-family: 'Poppins', sans-serif !important; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1rem !important; }

    .metric-card {
        background: linear-gradient(145deg, #1e2a4a 0%, #2d3a5a 100%);
        border-radius: 20px; padding: 1.3rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        border-left: 4px solid #00d4ff;
        transition: all 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 12px 40px rgba(0,212,255,0.2); border-color: rgba(0,212,255,0.3); }
    .metric-card.green  { border-left-color: #00f5d4; box-shadow: 0 8px 32px rgba(0,245,212,0.15); }
    .metric-card.green:hover  { box-shadow: 0 12px 40px rgba(0,245,212,0.25); }
    .metric-card.orange { border-left-color: #fee440; box-shadow: 0 8px 32px rgba(254,228,64,0.15); }
    .metric-card.orange:hover { box-shadow: 0 12px 40px rgba(254,228,64,0.25); }
    .metric-card.purple { border-left-color: #9b5de5; box-shadow: 0 8px 32px rgba(155,93,229,0.15); }
    .metric-card.purple:hover { box-shadow: 0 12px 40px rgba(155,93,229,0.25); }
    .metric-card.red    { border-left-color: #ff6b6b; box-shadow: 0 8px 32px rgba(255,107,107,0.15); }
    .metric-card.red:hover    { box-shadow: 0 12px 40px rgba(255,107,107,0.25); }
    .metric-card.teal   { border-left-color: #00f5d4; box-shadow: 0 8px 32px rgba(0,245,212,0.15); }
    .metric-card.teal:hover   { box-shadow: 0 12px 40px rgba(0,245,212,0.25); }
    .metric-card.pink   { border-left-color: #e879f9; box-shadow: 0 8px 32px rgba(232,121,249,0.15); }
    .metric-card.pink:hover   { box-shadow: 0 12px 40px rgba(232,121,249,0.25); }
    .metric-card.amber  { border-left-color: #f97316; box-shadow: 0 8px 32px rgba(249,115,22,0.15); }
    .metric-card.amber:hover  { box-shadow: 0 12px 40px rgba(249,115,22,0.25); }

    .metric-value {
        font-size: 1.7rem; font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: -0.02em;
    }
    .metric-label { font-size: 0.72rem; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500; margin-top: 0.3rem; }
    .metric-delta { font-size: 0.82rem; margin-top: 0.25rem; color: #718096; }

    .section-title {
        font-size: 1.05rem; font-weight: 600; color: #ffffff;
        margin-bottom: 0.7rem; padding-left: 0.6rem;
        border-left: 4px solid #00d4ff; letter-spacing: 0.01em;
    }

    .insight-box {
        background: linear-gradient(135deg, rgba(0,212,255,0.08) 0%, rgba(123,44,191,0.08) 100%);
        border-left: 3px solid #00d4ff; border-radius: 0 12px 12px 0;
        padding: 0.75rem 1rem; margin-bottom: 0.6rem;
        font-size: 0.88rem; color: #93c5fd; backdrop-filter: blur(8px);
        border-top: 1px solid rgba(0,212,255,0.1);
    }
    .insight-box.warning {
        background: linear-gradient(135deg, rgba(254,228,64,0.08) 0%, rgba(255,107,107,0.08) 100%);
        border-left-color: #fee440; border-top-color: rgba(254,228,64,0.1); color: #fde68a;
    }
    .insight-box.success {
        background: linear-gradient(135deg, rgba(0,245,212,0.08) 0%, rgba(0,212,255,0.08) 100%);
        border-left-color: #00f5d4; border-top-color: rgba(0,245,212,0.1); color: #6ee7b7;
    }

    .portal-badge {
        display: inline-block; padding: 0.3rem 1.1rem; border-radius: 20px;
        font-weight: 700; font-size: 0.8rem; margin-bottom: 0.5rem;
        letter-spacing: 0.08em; font-family: 'Poppins', sans-serif;
    }
    .badge-lmi {
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.08));
        color: #00d4ff; border: 1px solid rgba(0,212,255,0.35); box-shadow: 0 0 12px rgba(0,212,255,0.15);
    }
    .badge-lsi {
        background: linear-gradient(135deg, rgba(155,93,229,0.15), rgba(123,44,191,0.08));
        color: #c084fc; border: 1px solid rgba(155,93,229,0.35); box-shadow: 0 0 12px rgba(155,93,229,0.15);
    }
    .badge-hijau {
        background: linear-gradient(135deg, rgba(0,245,212,0.15), rgba(0,245,212,0.08));
        color: #00f5d4; border: 1px solid rgba(0,245,212,0.35); box-shadow: 0 0 12px rgba(0,245,212,0.15);
    }
    .badge-cokelat {
        background: linear-gradient(135deg, rgba(180,120,60,0.15), rgba(180,120,60,0.08));
        color: #d4a574; border: 1px solid rgba(180,120,60,0.35); box-shadow: 0 0 12px rgba(180,120,60,0.15);
    }
    .badge-enduser {
        background: linear-gradient(135deg, rgba(254,228,64,0.15), rgba(254,228,64,0.08));
        color: #fee440; border: 1px solid rgba(254,228,64,0.35); box-shadow: 0 0 12px rgba(254,228,64,0.15);
    }

    h1, h2, h3 { color: #ffffff !important; font-family: 'Poppins', sans-serif !important; }
    p, li { color: #a0aec0; }
    [data-testid="stDataFrame"] { border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px; overflow: hidden; }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiselect"] > div > div {
        background-color: rgba(30,42,74,0.9) !important;
        border-color: rgba(255,255,255,0.12) !important; color: #e2e8f0 !important;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; }
    [data-testid="stCaption"] { color: #4a5568 !important; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; }
    ::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #00d4ff; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def fmt_rp(val: float) -> str:
    """Format value as Indonesian Rupiah."""
    if val >= 1_000_000_000:
        return f"Rp {val/1_000_000_000:.2f} B"
    elif val >= 1_000_000:
        return f"Rp {val/1_000_000:.2f} Jt"
    else:
        return f"Rp {val:,.0f}"


def fmt_number(val: float) -> str:
    """Format number with thousand separator."""
    return f"{val:,.0f}"


def metric_card(label: str, value: str, color: str = "blue", delta: str = None) -> str:
    """Generate HTML for a metric card."""
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    cls = {"blue": "", "green": "green", "orange": "orange", "purple": "purple",
           "red": "red", "teal": "teal", "pink": "pink", "amber": "amber"}.get(color, "")
    return f"""
    <div class="metric-card {cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>"""


def section_title(title: str) -> None:
    """Render a styled section title."""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def portal_badge(portal: str, promo_type: str = None) -> str:
    """Generate HTML for portal/promo type badge."""
    if promo_type:
        badge_map = {
            "Hijau": "badge-hijau",
            "Cokelat": "badge-cokelat", 
            "EndUser": "badge-enduser",
        }
        badge_cls = badge_map.get(promo_type, "badge-lmi" if portal == "LMI" else "badge-lsi")
        label = f"{portal} · {promo_type}"
    else:
        badge_cls = "badge-lmi" if portal == "LMI" else "badge-lsi"
        label = portal
    return f'<span class="portal-badge {badge_cls}">{label}</span>'


def parse_filename_dates(filename: str) -> Tuple[datetime, datetime, str]:
    """
    Parse dates from filename format: Prefix_YYYYMMDD_YYYYMMDD.ext
    Returns: (start_date, end_date, period_label)
    """
    pattern = r"_(\d{8})_(\d{8})\."
    match = re.search(pattern, filename)
    if match:
        start_str, end_str = match.groups()
        start_date = datetime.strptime(start_str, "%Y%m%d")
        end_date = datetime.strptime(end_str, "%Y%m%d")
        period_label = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}"
        return start_date, end_date, period_label
    return None, None, "Unknown Period"


def discover_files(promo_type: str, portal: str) -> List[Dict]:
    """
    Discover available data files for a given promo type and portal.
    Returns list of dicts with file info sorted by date.
    """
    if promo_type == "Mailer":
        folder = DATA_DIR / "Mailer" / portal
        prefix = f"Mailer{portal}"
    else:
        folder = DATA_DIR / "BigBanner" / portal
        prefix = f"Banner"
    
    if not folder.exists():
        return []
    
    files = []
    for f in folder.glob("*"):
        if f.suffix.lower() in [".xlsx", ".xlsb", ".xls"]:
            start_date, end_date, period_label = parse_filename_dates(f.name)
            if start_date:
                # Extract banner type for Big Banner
                banner_type = None
                if promo_type == "BigBanner":
                    if "Hijau" in f.name:
                        banner_type = "Hijau"
                    elif "Cokelat" in f.name:
                        banner_type = "Cokelat"
                    elif "EndUser" in f.name:
                        banner_type = "EndUser"
                
                files.append({
                    "path": f,
                    "filename": f.name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "period_label": period_label,
                    "banner_type": banner_type,
                })
    
    # Sort by start date descending (newest first)
    files.sort(key=lambda x: x["start_date"], reverse=True)
    return files


def get_division_config(portal: str) -> Tuple[Dict, List, Dict, Dict, Dict]:
    """Get division configuration based on portal."""
    if portal == "LMI":
        return (DIVISION_MAP_LMI, DIVISION_ORDER_LMI, DIVISION_COLORS_LMI, 
                DIVISION_CARD_COLOR_LMI, GROUP_ID_MAP_LMI)
    else:
        return (DIVISION_MAP_LSI, DIVISION_ORDER_LSI, DIVISION_COLORS_LSI,
                DIVISION_CARD_COLOR_LSI, GROUP_ID_MAP_LSI)


def get_group_labels(portal: str) -> List[str]:
    """Get group labels for identifying group rows."""
    return GROUP_LABELS_LMI if portal == "LMI" else GROUP_LABELS_LSI


def get_bar_accent(portal: str) -> str:
    """Get accent color for bar charts based on portal."""
    return "#00d4ff" if portal == "LMI" else "#9b5de5"


# ═══════════════════════════════════════════════════════════════════════════════
# CHART BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_trend_chart(trend_df: pd.DataFrame, current_idx: int, 
                      bar_accent: str, value_col: str = "LM NS",
                      cont_col: str = "LM Cont%") -> go.Figure:
    """Build trend chart with bar and line."""
    bar_colors = [
        bar_accent if i != current_idx else "#00f5d4"
        for i in range(len(trend_df))
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=trend_df["Period Label"], y=trend_df[value_col], name=f"{value_col}",
        marker_color=bar_colors, opacity=0.85,
        text=[f"{v:,.0f}" for v in trend_df[value_col]],
        textposition="outside", textfont=dict(color="#e2e8f0", size=11, weight="bold"),
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=trend_df["Period Label"], y=trend_df[cont_col], name=f"{cont_col}",
        mode="lines+markers+text",
        line=dict(color="#fee440", width=3),
        marker=dict(size=12, color="#fee440", line=dict(width=2, color="#1a1a2e")),
        text=[f"{v:.1f}%" for v in trend_df[cont_col]],
        textposition="bottom center", textfont=dict(color="#ffffff", size=12, family="Poppins"),
        yaxis="y2",
    ))
    
    fig.update_layout(
        plot_bgcolor=PLOTLY_DARK_THEME["plot_bgcolor"],
        paper_bgcolor=PLOTLY_DARK_THEME["paper_bgcolor"],
        font=PLOTLY_DARK_THEME["font"],
        hoverlabel=PLOTLY_DARK_THEME["hoverlabel"],
        height=350, 
        margin=dict(t=60, b=40, l=60, r=60),
        xaxis=dict(title="Periode", gridcolor="#2d3748", tickfont=dict(color="#94a3b8", size=12)),
        yaxis=dict(
            title=dict(text=value_col, font=dict(color=bar_accent)),
            tickfont=dict(color=bar_accent), gridcolor="#2d3748", side="left",
        ),
        yaxis2=dict(
            title=dict(text=cont_col, font=dict(color="#fee440")),
            tickfont=dict(color="#fee440"),
            overlaying="y", side="right", showgrid=False,
            range=[0, max(trend_df[cont_col]) * 1.5] if len(trend_df) else [0, 100],
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color="#e2e8f0"), bgcolor="rgba(26,32,53,0.8)"),
        barmode="overlay",
    )
    return fig


def build_pie_chart(labels: List[str], values: List[float], 
                    colors: List[str], center_text: str,
                    center_color: str = "#00d4ff") -> go.Figure:
    """Build a donut pie chart."""
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55, marker_colors=colors,
        textinfo="label+percent", textfont=dict(size=12, color="#ffffff"),
    ))
    fig.update_layout(
        plot_bgcolor=PLOTLY_DARK_THEME["plot_bgcolor"],
        paper_bgcolor=PLOTLY_DARK_THEME["paper_bgcolor"],
        font=PLOTLY_DARK_THEME["font"],
        hoverlabel=PLOTLY_DARK_THEME["hoverlabel"],
        showlegend=False, height=280,
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[dict(
            text=center_text, x=0.5, y=0.5,
            font=dict(size=16, color=center_color), showarrow=False
        )]
    )
    return fig


def build_horizontal_bar_chart(df: pd.DataFrame, y_col: str, x_col: str,
                                color_col: str = None, colors: List[str] = None,
                                text_col: str = None, show_avg_line: bool = False,
                                avg_value: float = None, height: int = None) -> go.Figure:
    """Build horizontal bar chart."""
    if colors is None:
        colors = ["#00d4ff"] * len(df)
    
    text_values = df[text_col].tolist() if text_col else [f"{v:,.0f}" for v in df[x_col]]
    
    fig = go.Figure(go.Bar(
        y=df[y_col], x=df[x_col],
        orientation="h", marker_color=colors,
        text=text_values,
        textposition="outside", textfont=dict(color="#e2e8f0"),
    ))
    
    if show_avg_line and avg_value is not None:
        fig.add_vline(
            x=avg_value, line_dash="dash", line_color="#718096",
            annotation_text="Avg", annotation_font=dict(color="#718096"),
            annotation_position="top"
        )
    
    calc_height = height or max(420, len(df) * 28)
    fig.update_layout(
        plot_bgcolor=PLOTLY_DARK_THEME["plot_bgcolor"],
        paper_bgcolor=PLOTLY_DARK_THEME["paper_bgcolor"],
        font=PLOTLY_DARK_THEME["font"],
        hoverlabel=PLOTLY_DARK_THEME["hoverlabel"],
        xaxis=PLOTLY_DARK_THEME["xaxis"],
        yaxis=PLOTLY_DARK_THEME["yaxis"],
        legend=PLOTLY_DARK_THEME["legend"],
        height=calc_height,
        margin=dict(t=20, b=20, l=10, r=40)
    )
    
    return fig


def build_stacked_bar_chart(df: pd.DataFrame, y_col: str, 
                            segments: List[Dict], height: int = None) -> go.Figure:
    """
    Build stacked horizontal bar chart.
    segments: List of dicts with keys: name, x_col, color, text_col (optional)
    """
    fig = go.Figure()
    
    for seg in segments:
        text_values = None
        if "text_col" in seg and seg["text_col"]:
            text_values = df[seg["text_col"]].tolist()
        elif "show_pct" in seg and seg["show_pct"]:
            text_values = [f"{v:.1f}%" if v > 0 else "" for v in df[seg["pct_col"]]]
        
        fig.add_trace(go.Bar(
            y=df[y_col], x=df[seg["x_col"]],
            name=seg["name"], orientation="h",
            marker_color=seg["color"],
            text=text_values,
            textposition="inside" if text_values else None,
            textfont=dict(color="#1a1a2e", size=10, weight="bold") if text_values else None,
        ))
    
    calc_height = height or max(420, len(df) * 22)
    fig.update_layout(
        plot_bgcolor=PLOTLY_DARK_THEME["plot_bgcolor"],
        paper_bgcolor=PLOTLY_DARK_THEME["paper_bgcolor"],
        font=PLOTLY_DARK_THEME["font"],
        hoverlabel=PLOTLY_DARK_THEME["hoverlabel"],
        xaxis=PLOTLY_DARK_THEME["xaxis"],
        yaxis=PLOTLY_DARK_THEME["yaxis"],
        barmode="stack", height=calc_height,
        margin=dict(t=30, b=20, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    
    return fig


def build_division_chart(div_bar: pd.DataFrame, bar_accent: str,
                         division_colors: Dict) -> go.Figure:
    """Build LM/Banner Net Sales per Division chart with dual axis."""
    div_colors = [division_colors.get(d, "#718096") for d in div_bar["Division"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=div_bar["Division"], y=div_bar["Promo_NS"], name="Promo Net Sales",
        marker_color=div_colors, opacity=0.85,
        text=[f"{v:,.0f}" for v in div_bar["Promo_NS"]],
        textposition="outside", textfont=dict(color="#e2e8f0", size=11, weight="bold"),
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=div_bar["Division"], y=div_bar["Promo_Cont%"], name="Promo Cont. %",
        mode="lines+markers+text",
        line=dict(color="#fee440", width=3),
        marker=dict(size=12, color="#fee440", line=dict(width=2, color="#1a1a2e")),
        text=[f"{v:.1f}%" for v in div_bar["Promo_Cont%"]],
        textposition="bottom center", textfont=dict(color="#ffffff", size=12, family="Poppins"),
        yaxis="y2",
    ))
    
    fig.update_layout(
        plot_bgcolor=PLOTLY_DARK_THEME["plot_bgcolor"],
        paper_bgcolor=PLOTLY_DARK_THEME["paper_bgcolor"],
        font=PLOTLY_DARK_THEME["font"],
        hoverlabel=PLOTLY_DARK_THEME["hoverlabel"],
        height=350, 
        margin=dict(t=60, b=40, l=60, r=60),
        xaxis=dict(title="Division", gridcolor="#2d3748", tickfont=dict(color="#94a3b8", size=12)),
        yaxis=dict(
            title=dict(text="Promo Net Sales", font=dict(color=bar_accent)),
            tickfont=dict(color=bar_accent), gridcolor="#2d3748", side="left",
        ),
        yaxis2=dict(
            title=dict(text="Promo Cont. %", font=dict(color="#fee440")),
            tickfont=dict(color="#fee440"),
            overlaying="y", side="right", showgrid=False,
            range=[0, max(div_bar["Promo_Cont%"]) * 1.5] if not div_bar.empty else [0, 100],
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color="#e2e8f0"), bgcolor="rgba(26,32,53,0.8)"),
        barmode="overlay",
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS - MAILER
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_mailer_lmi(filepath: str) -> Tuple[pd.DataFrame, Dict, pd.DataFrame, str]:
    """Load Mailer LMI data from Excel file."""
    path = Path(filepath)
    
    # ── By Store ──
    raw_store = pd.read_excel(path, sheet_name="By Store", header=None)
    period_label = str(raw_store.iloc[0, 0])
    
    data_rows = raw_store.iloc[3:].copy()
    total_mask = data_rows[0].astype(str).str.upper() == "LMI"
    total_row = data_rows[total_mask].iloc[0]
    store_rows = data_rows[~total_mask & data_rows[0].notna()].copy()
    store_rows.columns = range(store_rows.shape[1])
    
    store = pd.DataFrame({
        "Store ID": store_rows[0].values,
        "Store Name": store_rows[1].values,
        "Total NS": pd.to_numeric(store_rows[2], errors="coerce").values,
        "Normal NS": pd.to_numeric(store_rows[3], errors="coerce").values,
        "LM NS": pd.to_numeric(store_rows[4], errors="coerce").values,
        "LM Cont%": pd.to_numeric(store_rows[5], errors="coerce").values,
        "Regular NS": pd.to_numeric(store_rows[6], errors="coerce").values,
        "Regular Cont%": pd.to_numeric(store_rows[7], errors="coerce").values,
        "Trader NS": pd.to_numeric(store_rows[8], errors="coerce").values,
        "Trader Cont%": pd.to_numeric(store_rows[9], errors="coerce").values,
        "SKU Total": pd.to_numeric(store_rows[10], errors="coerce").values,
        "SKU Sale": pd.to_numeric(store_rows[11], errors="coerce").values,
        "SKU Cont%": pd.to_numeric(store_rows[12], errors="coerce").values,
        "OOS": pd.to_numeric(store_rows[13], errors="coerce").values,
    }).reset_index(drop=True)
    
    store_total = {
        "Total NS": pd.to_numeric(total_row[2], errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3], errors="coerce"),
        "LM NS": pd.to_numeric(total_row[4], errors="coerce"),
        "LM Cont%": pd.to_numeric(total_row[5], errors="coerce"),
        "SKU Total": pd.to_numeric(total_row[10], errors="coerce"),
        "SKU Sale": pd.to_numeric(total_row[11], errors="coerce"),
        "SKU Cont%": pd.to_numeric(total_row[12], errors="coerce"),
        "OOS": pd.to_numeric(total_row[13], errors="coerce"),
    }
    
    # ── By Cat ──
    raw_cat = pd.read_excel(path, sheet_name="By Cat", header=None)
    cat_rows = raw_cat.iloc[3:].copy()
    cat_rows.columns = range(cat_rows.shape[1])
    
    cat_data = []
    for _, r in cat_rows.iterrows():
        cat_id = r[0]
        if pd.isna(cat_id):
            continue
        cat_id_str = str(cat_id).strip()
        is_group = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LMI]
        cat_data.append({
            "Cat ID": cat_id_str,
            "Category": r[1],
            "Total NS": pd.to_numeric(r[2], errors="coerce"),
            "Normal NS": pd.to_numeric(r[3], errors="coerce"),
            "LM NS": pd.to_numeric(r[4], errors="coerce"),
            "LM Cont%": pd.to_numeric(r[5], errors="coerce"),
            "Regular NS": pd.to_numeric(r[6], errors="coerce"),
            "Regular Cont%": pd.to_numeric(r[7], errors="coerce"),
            "Trader NS": pd.to_numeric(r[8], errors="coerce"),
            "Trader Cont%": pd.to_numeric(r[9], errors="coerce"),
            "SKU Total": pd.to_numeric(r[10], errors="coerce"),
            "SKU Sale": pd.to_numeric(r[11], errors="coerce"),
            "SKU Cont%": pd.to_numeric(r[12], errors="coerce"),
            "OOS": pd.to_numeric(r[13], errors="coerce"),
            "Is Group": is_group,
        })
    
    cat_df = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: GROUP_ID_MAP_LMI.get(str(x).strip(), "OTHER")
    )
    
    return store, store_total, cat_detail, period_label


@st.cache_data
def load_mailer_lsi(filepath: str) -> Tuple[pd.DataFrame, Dict, pd.DataFrame, str]:
    """Load Mailer LSI data from xlsb file."""
    path = Path(filepath)
    raw = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Store", header=None)
    period_label = str(raw.iloc[0, 1])
    
    data_rows = raw.iloc[3:].copy()
    total_mask = data_rows[0].astype(str).str.upper() == "LSI"
    total_row = data_rows[total_mask].iloc[0]
    store_rows = data_rows[~total_mask & data_rows[0].notna()].copy()
    store_rows.columns = range(store_rows.shape[1])
    
    store = pd.DataFrame({
        "Store ID": store_rows[0].values,
        "Store Name": store_rows[1].values,
        "Total NS": pd.to_numeric(store_rows[2], errors="coerce").values,
        "Normal NS": pd.to_numeric(store_rows[3], errors="coerce").values,
        "LM NS": pd.to_numeric(store_rows[4], errors="coerce").values,
        "LM Cont%": pd.to_numeric(store_rows[5], errors="coerce").values,
        "LM Trader NS": pd.to_numeric(store_rows[6], errors="coerce").values,
        "LM Trader Cont%": pd.to_numeric(store_rows[7], errors="coerce").values,
        "LM Prof NS": pd.to_numeric(store_rows[8], errors="coerce").values,
        "LM Prof Cont%": pd.to_numeric(store_rows[9], errors="coerce").values,
        "LM Others NS": pd.to_numeric(store_rows[10], errors="coerce").values,
        "LM Others Cont%": pd.to_numeric(store_rows[11], errors="coerce").values,
        "SKU Total": pd.to_numeric(store_rows[12], errors="coerce").values,
        "SKU Sale": pd.to_numeric(store_rows[13], errors="coerce").values,
        "SKU Cont%": pd.to_numeric(store_rows[14], errors="coerce").values,
        "OOS": pd.to_numeric(store_rows[15], errors="coerce").values,
    }).reset_index(drop=True)
    
    store_total = {
        "Total NS": pd.to_numeric(total_row[2], errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3], errors="coerce"),
        "LM NS": pd.to_numeric(total_row[4], errors="coerce"),
        "LM Cont%": pd.to_numeric(total_row[5], errors="coerce"),
        "SKU Total": pd.to_numeric(total_row[12], errors="coerce"),
        "SKU Sale": pd.to_numeric(total_row[13], errors="coerce"),
        "SKU Cont%": pd.to_numeric(total_row[14], errors="coerce"),
        "OOS": pd.to_numeric(total_row[15], errors="coerce"),
    }
    
    raw_cat = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Cat", header=None)
    cat_rows = raw_cat.iloc[3:].copy()
    cat_rows.columns = range(cat_rows.shape[1])
    
    cat_data = []
    for _, r in cat_rows.iterrows():
        cat_id = r[0]
        if pd.isna(cat_id):
            continue
        cat_id_str = str(cat_id).strip()
        is_group = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LSI]
        cat_data.append({
            "Cat ID": cat_id_str,
            "Category": r[1],
            "Total NS": pd.to_numeric(r[2], errors="coerce"),
            "Normal NS": pd.to_numeric(r[3], errors="coerce"),
            "LM NS": pd.to_numeric(r[4], errors="coerce"),
            "LM Cont%": pd.to_numeric(r[5], errors="coerce"),
            "LM Trader NS": pd.to_numeric(r[6], errors="coerce"),
            "LM Trader Cont%": pd.to_numeric(r[7], errors="coerce"),
            "LM Prof NS": pd.to_numeric(r[8], errors="coerce"),
            "LM Prof Cont%": pd.to_numeric(r[9], errors="coerce"),
            "LM Others NS": pd.to_numeric(r[10], errors="coerce"),
            "LM Others Cont%": pd.to_numeric(r[11], errors="coerce"),
            "SKU Total": pd.to_numeric(r[12], errors="coerce"),
            "SKU Sale": pd.to_numeric(r[13], errors="coerce"),
            "SKU Cont%": pd.to_numeric(r[14], errors="coerce"),
            "OOS": pd.to_numeric(r[15], errors="coerce"),
            "Is Group": is_group,
        })
    
    cat_df = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: GROUP_ID_MAP_LSI.get(str(x).strip(), "OTHER")
    )
    
    return store, store_total, cat_detail, period_label


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS - BIG BANNER
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_banner_lsi_hijau_cokelat(filepath: str) -> Tuple[pd.DataFrame, Dict, pd.DataFrame, pd.DataFrame, str]:
    """
    Load Big Banner LSI (Hijau/Cokelat) data from xlsb file.
    Returns: store_df, store_total, cat_df, sku_df, period_label
    """
    path = Path(filepath)
    
    # ── Summary by Store ──
    raw_store = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Store", header=None)
    period_label = str(raw_store.iloc[0, 2])
    
    data_rows = raw_store.iloc[3:].copy()
    total_mask = data_rows[0].astype(str).str.upper() == "LSI"
    total_row = data_rows[total_mask].iloc[0]
    store_rows = data_rows[~total_mask & data_rows[0].notna()].copy()
    store_rows.columns = range(store_rows.shape[1])
    
    store = pd.DataFrame({
        "Store ID": store_rows[0].values,
        "Store Name": store_rows[1].values,
        "Total NS": pd.to_numeric(store_rows[2], errors="coerce").values,
        "Normal NS": pd.to_numeric(store_rows[3], errors="coerce").values,
        "Banner NS": pd.to_numeric(store_rows[4], errors="coerce").values,
        "Banner Cont%": pd.to_numeric(store_rows[5], errors="coerce").values,
        "Retailer NS": pd.to_numeric(store_rows[6], errors="coerce").values,
        "Retailer Cont%": pd.to_numeric(store_rows[7], errors="coerce").values,
        "Big NS": pd.to_numeric(store_rows[8], errors="coerce").values,
        "Big Cont%": pd.to_numeric(store_rows[9], errors="coerce").values,
        "Medium NS": pd.to_numeric(store_rows[10], errors="coerce").values,
        "Medium Cont%": pd.to_numeric(store_rows[11], errors="coerce").values,
        "SWK NS": pd.to_numeric(store_rows[12], errors="coerce").values,
        "SWK Cont%": pd.to_numeric(store_rows[13], errors="coerce").values,
        "Horeca NS": pd.to_numeric(store_rows[14], errors="coerce").values,
        "Horeca Cont%": pd.to_numeric(store_rows[15], errors="coerce").values,
        "Others NS": pd.to_numeric(store_rows[16], errors="coerce").values,
        "Others Cont%": pd.to_numeric(store_rows[17], errors="coerce").values,
        "NOC": pd.to_numeric(store_rows[18], errors="coerce").values,
    }).reset_index(drop=True)
    
    store_total = {
        "Total NS": pd.to_numeric(total_row[2], errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3], errors="coerce"),
        "Banner NS": pd.to_numeric(total_row[4], errors="coerce"),
        "Banner Cont%": pd.to_numeric(total_row[5], errors="coerce"),
        "Retailer NS": pd.to_numeric(total_row[6], errors="coerce"),
        "Retailer Cont%": pd.to_numeric(total_row[7], errors="coerce"),
        "Big NS": pd.to_numeric(total_row[8], errors="coerce"),
        "Medium NS": pd.to_numeric(total_row[10], errors="coerce"),
        "SWK NS": pd.to_numeric(total_row[12], errors="coerce"),
        "Horeca NS": pd.to_numeric(total_row[14], errors="coerce"),
        "Horeca Cont%": pd.to_numeric(total_row[15], errors="coerce"),
        "Others NS": pd.to_numeric(total_row[16], errors="coerce"),
        "Others Cont%": pd.to_numeric(total_row[17], errors="coerce"),
        "NOC": pd.to_numeric(total_row[18], errors="coerce"),
    }
    
    # ── Summary by Cat ──
    raw_cat = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Cat", header=None)
    cat_rows = raw_cat.iloc[3:].copy()
    cat_rows.columns = range(cat_rows.shape[1])
    
    cat_data = []
    for _, r in cat_rows.iterrows():
        cat_id = r[0]
        if pd.isna(cat_id):
            continue
        cat_id_str = str(cat_id).strip()
        is_group = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LSI]
        cat_data.append({
            "Cat ID": cat_id_str,
            "Category": r[1],
            "Total NS": pd.to_numeric(r[2], errors="coerce"),
            "Normal NS": pd.to_numeric(r[3], errors="coerce"),
            "Banner NS": pd.to_numeric(r[4], errors="coerce"),
            "Banner Cont%": pd.to_numeric(r[5], errors="coerce"),
            "Retailer NS": pd.to_numeric(r[6], errors="coerce"),
            "Retailer Cont%": pd.to_numeric(r[7], errors="coerce"),
            "Big NS": pd.to_numeric(r[8], errors="coerce"),
            "Big Cont%": pd.to_numeric(r[9], errors="coerce"),
            "Medium NS": pd.to_numeric(r[10], errors="coerce"),
            "Medium Cont%": pd.to_numeric(r[11], errors="coerce"),
            "SWK NS": pd.to_numeric(r[12], errors="coerce"),
            "SWK Cont%": pd.to_numeric(r[13], errors="coerce"),
            "Horeca NS": pd.to_numeric(r[14], errors="coerce"),
            "Horeca Cont%": pd.to_numeric(r[15], errors="coerce"),
            "Others NS": pd.to_numeric(r[16], errors="coerce"),
            "Others Cont%": pd.to_numeric(r[17], errors="coerce"),
            "Is Group": is_group,
        })
    
    cat_df = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: GROUP_ID_MAP_LSI.get(str(x).strip(), "OTHER")
    )
    
    # ── SKU Banner ──
    try:
        raw_sku = pd.read_excel(path, engine="pyxlsb", sheet_name="SKU_Banner", header=None)
        sku_rows = raw_sku.iloc[2:].copy()
        sku_rows.columns = range(sku_rows.shape[1])
        
        sku_df = pd.DataFrame({
            "Cat ID": sku_rows[1].values,
            "Category": sku_rows[2].values,
            "Product Code": sku_rows[3].values,
            "Product Name": sku_rows[4].values,
            "Remarks": sku_rows[5].values if 5 in sku_rows.columns else None,
        }).dropna(subset=["Product Code"])
    except Exception:
        sku_df = pd.DataFrame()
    
    return store, store_total, cat_detail, sku_df, period_label


@st.cache_data
def load_banner_lmi(filepath: str) -> Tuple[pd.DataFrame, Dict, pd.DataFrame, str]:
    """Load Big Banner LMI data (same structure as Mailer LMI)."""
    return load_mailer_lmi(filepath)


@st.cache_data  
def load_banner_lsi_enduser(filepath: str) -> Tuple[pd.DataFrame, Dict, pd.DataFrame, str]:
    """Load Big Banner LSI EndUser data (same structure as Mailer LSI)."""
    return load_mailer_lsi(filepath)


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def render_footer(portal: str, period_label: str):
    """Render dashboard footer."""
    st.markdown("---")
    st.caption(f"📊 Dashboard {portal} · {period_label} | Data: Net Sales dalam IDR")