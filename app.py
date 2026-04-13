import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Net Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS (DARK THEME) ────────────────────────────────────────────────
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

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────
def fmt_rp(val):
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.2f} M"
    elif val >= 1_000:
        return f"Rp {val/1_000:.1f} K"
    return f"Rp {val:.0f}"

def metric_card(label, value, color="blue", delta=None):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    cls = {"blue":"","green":"green","orange":"orange","purple":"purple",
           "red":"red","teal":"teal","pink":"pink","amber":"amber"}.get(color,"")
    return f"""
    <div class="metric-card {cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>"""

# ── Plotly dark layout defaults ──
PD = dict(
    plot_bgcolor="#1a2035",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
    xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
    yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
    legend=dict(bgcolor="rgba(26,32,53,0.8)", bordercolor="#2d3748", borderwidth=1, font=dict(color="#e2e8f0")),
    hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
    margin=dict(t=30, b=20, l=10, r=10),
)

# ─── DIVISION CONFIG ──────────────────────────────────────────────────────────
# LMI: 6 divisi berdiri sendiri + Other
DIVISION_MAP_LMI = {
    "FRESH FOOD":    "FRESH FOOD",
    "MEAL SOLUTION": "MEAL SOLUTION",
    "DRY FOOD":      "DRY FOOD",
    "H&B HOME CARE": "H&B HOME CARE",
    "ELECTRONIC":    "ELECTRONIC",
    "NON FOOD":      "NON FOOD",
    "OTHER":         "Other",
}
DIVISION_ORDER_LMI = [
    "FRESH FOOD", "MEAL SOLUTION", "DRY FOOD",
    "H&B HOME CARE", "ELECTRONIC", "NON FOOD", "Other",
]
DIVISION_COLORS_LMI = {
    "FRESH FOOD":    "#00f5d4",
    "MEAL SOLUTION": "#fee440",
    "DRY FOOD":      "#00d4ff",
    "H&B HOME CARE": "#f97316",
    "ELECTRONIC":    "#e879f9",
    "NON FOOD":      "#9b5de5",
    "Other":         "#718096",
}
DIVISION_CARD_COLOR_LMI = {
    "FRESH FOOD":    "teal",
    "MEAL SOLUTION": "orange",
    "DRY FOOD":      "blue",
    "H&B HOME CARE": "amber",
    "ELECTRONIC":    "pink",
    "NON FOOD":      "purple",
    "Other":         "red",
}

# LSI: H&B HOME CARE → DRY FOOD, ELECTRONIC → NON FOOD (5 divisi)
DIVISION_MAP_LSI = {
    "FRESH FOOD":    "FRESH FOOD",
    "MEAL SOLUTION": "MEAL SOLUTION",
    "DRY FOOD":      "DRY FOOD",
    "H&B HOME CARE": "DRY FOOD",
    "ELECTRONIC":    "NON FOOD",
    "NON FOOD":      "NON FOOD",
    "OTHER":         "Other",
}
DIVISION_ORDER_LSI = ["FRESH FOOD", "MEAL SOLUTION", "DRY FOOD", "NON FOOD", "Other"]
DIVISION_COLORS_LSI = {
    "FRESH FOOD":    "#00f5d4",
    "MEAL SOLUTION": "#fee440",
    "DRY FOOD":      "#00d4ff",
    "NON FOOD":      "#9b5de5",
    "Other":         "#718096",
}
DIVISION_CARD_COLOR_LSI = {
    "FRESH FOOD":    "teal",
    "MEAL SOLUTION": "orange",
    "DRY FOOD":      "blue",
    "NON FOOD":      "purple",
    "Other":         "red",
}

# ─── CATEGORY → GROUP MAPPING ─────────────────────────────────────────────────
# LMI (dikonfirmasi dari data aktual Excel):
#   31=Fish, 32=Meat, 33=Fruits, 34=Vegetable, 35=Dairy&Frozen  → FRESH FOOD
#   80=Bakery, 82=Delica                                         → MEAL SOLUTION
#   11=Biscuit/Snacks, 17=Bulk Product, 21=Sauces&Spices,
#   23=Drinks, 24=Milk                                           → DRY FOOD
#   14=Home Care, 19=H&B                                         → H&B HOME CARE
#   86=IT/Gadget, 87=Small Appliance, 88=Big Appliance           → ELECTRONIC
#   51=Kitchen, 57=Bathroom, 85=DIY, 13=Interior&Bedding,
#   62=Textile, 71=Stationary/Toys                               → NON FOOD
#   97=Business Supplies, 98=Donation, 99=Miscellaneous          → OTHER
GROUP_ID_MAP_LMI = {
    "31": "FRESH FOOD",    "32": "FRESH FOOD",    "33": "FRESH FOOD",
    "34": "FRESH FOOD",    "35": "FRESH FOOD",
    "80": "MEAL SOLUTION", "82": "MEAL SOLUTION",
    "11": "DRY FOOD",      "17": "DRY FOOD",      "21": "DRY FOOD",
    "23": "DRY FOOD",      "24": "DRY FOOD",
    "14": "H&B HOME CARE", "19": "H&B HOME CARE",
    "86": "ELECTRONIC",    "87": "ELECTRONIC",    "88": "ELECTRONIC",
    "51": "NON FOOD",      "57": "NON FOOD",      "85": "NON FOOD",
    "13": "NON FOOD",      "62": "NON FOOD",      "71": "NON FOOD",
    "97": "OTHER",         "98": "OTHER",         "99": "OTHER",
}

GROUP_ID_MAP_LSI = {
    "31": "FRESH FOOD",    "32": "FRESH FOOD",    "33": "FRESH FOOD",
    "34": "FRESH FOOD",    "35": "FRESH FOOD",
    "80": "MEAL SOLUTION", "82": "MEAL SOLUTION",
    "17": "DRY FOOD",      "21": "DRY FOOD",      "11": "DRY FOOD",
    "26": "DRY FOOD",      "27": "DRY FOOD",
    "14": "H&B HOME CARE", "19": "H&B HOME CARE",
    "86": "ELECTRONIC",    "87": "ELECTRONIC",    "88": "ELECTRONIC",
    "51": "NON FOOD",      "57": "NON FOOD",      "85": "NON FOOD",
    "13": "NON FOOD",      "62": "NON FOOD",      "71": "NON FOOD",
    "97": "OTHER",         "98": "OTHER",         "99": "OTHER",
}

# ─── PERIODS ─────────────────────────────────────────────────────────────────
LMI_PERIODS = {
    1: "1-14 Jan",      2: "15-28 Jan",
    3: "29 Jan-18 Feb", 4: "19 Feb-4 Mar",
    5: "5-25 Mar",      6: "26 Mar-8 Apr",
}
LSI_PERIODS = {
    1: "30 Des-12 Jan", 2: "13-26 Jan",
    3: "27 Jan-9 Feb",  4: "10-23 Feb",
    5: "24 Feb-9 Mar",  6: "10-23 Mar", 
    7: "24 Mar-6 Apr",
}

# ─── DATA LOADERS ────────────────────────────────────────────────────────────
@st.cache_data
def load_lmi(lm_num):
    # Nama file pakai spasi sesuai penamaan aktual di folder data
    path = f"data/LM{lm_num}_LMI_Summary.xlsx"

    # ── By Store ──
    raw_store    = pd.read_excel(path, sheet_name="By Store", header=None)
    period_label = str(raw_store.iloc[0, 0])

    data_rows  = raw_store.iloc[3:].copy()
    total_mask = data_rows[0].astype(str).str.upper() == "LMI"
    total_row  = data_rows[total_mask].iloc[0]
    store_rows = data_rows[~total_mask & data_rows[0].notna()].copy()
    store_rows.columns = range(store_rows.shape[1])

    store = pd.DataFrame({
        "Store ID":      store_rows[0].values,
        "Store Name":    store_rows[1].values,
        "Total NS":      pd.to_numeric(store_rows[2],  errors="coerce").values,
        "Normal NS":     pd.to_numeric(store_rows[3],  errors="coerce").values,
        "LM NS":         pd.to_numeric(store_rows[4],  errors="coerce").values,
        "LM Cont%":      pd.to_numeric(store_rows[5],  errors="coerce").values,
        "Regular NS":    pd.to_numeric(store_rows[6],  errors="coerce").values,
        "Regular Cont%": pd.to_numeric(store_rows[7],  errors="coerce").values,
        "Trader NS":     pd.to_numeric(store_rows[8],  errors="coerce").values,
        "Trader Cont%":  pd.to_numeric(store_rows[9],  errors="coerce").values,
        "SKU Total":     pd.to_numeric(store_rows[10], errors="coerce").values,
        "SKU Sale":      pd.to_numeric(store_rows[11], errors="coerce").values,
        "SKU Cont%":     pd.to_numeric(store_rows[12], errors="coerce").values,
        "OOS":           pd.to_numeric(store_rows[13], errors="coerce").values,
    }).reset_index(drop=True)

    store_total = {
        "Total NS":  pd.to_numeric(total_row[2],  errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3],  errors="coerce"),
        "LM NS":     pd.to_numeric(total_row[4],  errors="coerce"),
        "LM Cont%":  pd.to_numeric(total_row[5],  errors="coerce"),
        "SKU Total": pd.to_numeric(total_row[10], errors="coerce"),
        "SKU Sale":  pd.to_numeric(total_row[11], errors="coerce"),
        "SKU Cont%": pd.to_numeric(total_row[12], errors="coerce"),
        "OOS":       pd.to_numeric(total_row[13], errors="coerce"),
    }

    # ── By Cat ──
    raw_cat = pd.read_excel(path, sheet_name="By Cat", header=None)
    GROUP_LABELS_LMI = [
        "FRESH FOOD", "MEAL SOLUTION", "DRY FOOD",
        "H&B HOME CARE", "ELECTRONIC", "NON FOOD", "TOTAL",
    ]
    cat_rows = raw_cat.iloc[3:].copy()
    cat_rows.columns = range(cat_rows.shape[1])

    cat_data = []
    for _, r in cat_rows.iterrows():
        cat_id = r[0]
        if pd.isna(cat_id):
            continue
        cat_id_str = str(cat_id).strip()
        is_group   = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LMI]
        cat_data.append({
            "Cat ID":        cat_id_str,
            "Category":      r[1],
            "Total NS":      pd.to_numeric(r[2],  errors="coerce"),
            "Normal NS":     pd.to_numeric(r[3],  errors="coerce"),
            "LM NS":         pd.to_numeric(r[4],  errors="coerce"),
            "LM Cont%":      pd.to_numeric(r[5],  errors="coerce"),
            "Regular NS":    pd.to_numeric(r[6],  errors="coerce"),
            "Regular Cont%": pd.to_numeric(r[7],  errors="coerce"),
            "Trader NS":     pd.to_numeric(r[8],  errors="coerce"),
            "Trader Cont%":  pd.to_numeric(r[9],  errors="coerce"),
            "SKU Total":     pd.to_numeric(r[10], errors="coerce"),
            "SKU Sale":      pd.to_numeric(r[11], errors="coerce"),
            "SKU Cont%":     pd.to_numeric(r[12], errors="coerce"),
            "OOS":           pd.to_numeric(r[13], errors="coerce"),
            "Is Group":      is_group,
        })

    cat_df     = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: GROUP_ID_MAP_LMI.get(str(x).strip(), "OTHER")
    )
    return store, store_total, cat_detail, period_label


@st.cache_data
def load_lsi(lm_num):
    path = f"data/LM{lm_num}_LSI_Summary.xlsb"
    raw  = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Store", header=None)
    period_label = str(raw.iloc[0, 1])

    data_rows  = raw.iloc[3:].copy()
    total_mask = data_rows[0].astype(str).str.upper() == "LSI"
    total_row  = data_rows[total_mask].iloc[0]
    store_rows = data_rows[~total_mask & data_rows[0].notna()].copy()
    store_rows.columns = range(store_rows.shape[1])

    store = pd.DataFrame({
        "Store ID":        store_rows[0].values,
        "Store Name":      store_rows[1].values,
        "Total NS":        pd.to_numeric(store_rows[2],  errors="coerce").values,
        "Normal NS":       pd.to_numeric(store_rows[3],  errors="coerce").values,
        "LM NS":           pd.to_numeric(store_rows[4],  errors="coerce").values,
        "LM Cont%":        pd.to_numeric(store_rows[5],  errors="coerce").values,
        "LM Trader NS":    pd.to_numeric(store_rows[6],  errors="coerce").values,
        "LM Trader Cont%": pd.to_numeric(store_rows[7],  errors="coerce").values,
        "LM Prof NS":      pd.to_numeric(store_rows[8],  errors="coerce").values,
        "LM Prof Cont%":   pd.to_numeric(store_rows[9],  errors="coerce").values,
        "LM Others NS":    pd.to_numeric(store_rows[10], errors="coerce").values,
        "LM Others Cont%": pd.to_numeric(store_rows[11], errors="coerce").values,
        "SKU Total":       pd.to_numeric(store_rows[12], errors="coerce").values,
        "SKU Sale":        pd.to_numeric(store_rows[13], errors="coerce").values,
        "SKU Cont%":       pd.to_numeric(store_rows[14], errors="coerce").values,
        "OOS":             pd.to_numeric(store_rows[15], errors="coerce").values,
    }).reset_index(drop=True)

    store_total = {
        "Total NS":  pd.to_numeric(total_row[2],  errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3],  errors="coerce"),
        "LM NS":     pd.to_numeric(total_row[4],  errors="coerce"),
        "LM Cont%":  pd.to_numeric(total_row[5],  errors="coerce"),
        "SKU Total": pd.to_numeric(total_row[12], errors="coerce"),
        "SKU Sale":  pd.to_numeric(total_row[13], errors="coerce"),
        "SKU Cont%": pd.to_numeric(total_row[14], errors="coerce"),
        "OOS":       pd.to_numeric(total_row[15], errors="coerce"),
    }

    raw_cat = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Cat", header=None)
    GROUP_LABELS_LSI = ["DFF","DMS","DF1","DF2","DF3","DDF","ELC","NF1","NF2","NFI","OTH","ALL"]
    cat_rows = raw_cat.iloc[3:].copy()
    cat_rows.columns = range(cat_rows.shape[1])

    cat_data = []
    for _, r in cat_rows.iterrows():
        cat_id = r[0]
        if pd.isna(cat_id):
            continue
        cat_id_str = str(cat_id).strip()
        is_group   = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LSI]
        cat_data.append({
            "Cat ID":          cat_id_str,
            "Category":        r[1],
            "Total NS":        pd.to_numeric(r[2],  errors="coerce"),
            "Normal NS":       pd.to_numeric(r[3],  errors="coerce"),
            "LM NS":           pd.to_numeric(r[4],  errors="coerce"),
            "LM Cont%":        pd.to_numeric(r[5],  errors="coerce"),
            "LM Trader NS":    pd.to_numeric(r[6],  errors="coerce"),
            "LM Trader Cont%": pd.to_numeric(r[7],  errors="coerce"),
            "LM Prof NS":      pd.to_numeric(r[8],  errors="coerce"),
            "LM Prof Cont%":   pd.to_numeric(r[9],  errors="coerce"),
            "LM Others NS":    pd.to_numeric(r[10], errors="coerce"),
            "LM Others Cont%": pd.to_numeric(r[11], errors="coerce"),
            "SKU Total":       pd.to_numeric(r[12], errors="coerce"),
            "SKU Sale":        pd.to_numeric(r[13], errors="coerce"),
            "SKU Cont%":       pd.to_numeric(r[14], errors="coerce"),
            "OOS":             pd.to_numeric(r[15], errors="coerce"),
            "Is Group":        is_group,
        })

    cat_df     = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: GROUP_ID_MAP_LSI.get(str(x).strip(), "OTHER")
    )
    return store, store_total, cat_detail, period_label


# ─── STORE REGION MAPPING (LSI) ───────────────────────────────────────────────
# 36 active stores mapped to their regions
STORE_REGION_MAP = {
    # Regional 1 (13 stores)
    "Alam Sutera": "Regional 1",
    "Batam": "Regional 1",
    "Ciputat": "Regional 1",
    "Jambi": "Regional 1",
    "Jatake": "Regional 1",
    "Kelapa Gading": "Regional 1",
    "Lampung": "Regional 1",
    "Medan": "Regional 1",
    "Palembang": "Regional 1",
    "Pasar Rebo": "Regional 1",
    "Pekanbaru": "Regional 1",
    "Serang": "Regional 1",
    "Serpong": "Regional 1",
    # Regional 2 (13 stores)
    "Bandung": "Regional 2",
    "Bekasi": "Regional 2",
    "Bogor": "Regional 2",
    "Cibitung": "Regional 2",
    "Cikarang": "Regional 2",
    "Cilengsi": "Regional 2",
    "Cimahi": "Regional 2",
    "Cirebon": "Regional 2",
    "Karawang": "Regional 2",
    "Meruya": "Regional 2",
    "Pakansari": "Regional 2",
    "Tasikmalaya": "Regional 2",
    "Tegal": "Regional 2",
    # Regional 3 (13 stores)
    "Balikpapan": "Regional 3",
    "Banjarmasin": "Regional 3",
    "Denpasar": "Regional 3",
    "Makassar": "Regional 3",
    "Malang": "Regional 3",
    "Manado": "Regional 3",
    "Mastrip SBY": "Regional 3",
    "Mataram": "Regional 3",
    "Samarinda": "Regional 3",
    "Semarang": "Regional 3",
    "Sidoarjo": "Regional 3",
    "Solo": "Regional 3",
    "Yogyakarta": "Regional 3",
}

@st.cache_data
def load_all_lmi_trend():
    rows = []
    n = 1
    while True:
        try:
            _, st_tot, _, _ = load_lmi(n)
            rows.append({"Mailer": f"LM{n}", "Period": LMI_PERIODS.get(n, ""),
                         "Total NS": st_tot["Total NS"], "Normal NS": st_tot["Normal NS"],
                         "LM NS": st_tot["LM NS"],       "LM Cont%": st_tot["LM Cont%"]})
            n += 1
        except Exception:
            break
    return pd.DataFrame(rows)

@st.cache_data
def load_all_lsi_trend():
    rows = []
    n = 1
    while True:
        try:
            _, st_tot, _, _ = load_lsi(n)
            rows.append({"Mailer": f"LM{n}", "Period": LSI_PERIODS.get(n, ""),
                         "Total NS": st_tot["Total NS"], "Normal NS": st_tot["Normal NS"],
                         "LM NS": st_tot["LM NS"],       "LM Cont%": st_tot["LM Cont%"]})
            n += 1
        except Exception:
            break  # ← stop otomatis saat file LM berikutnya tidak ada
    return pd.DataFrame(rows)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Dashboard")
    st.markdown("**Filter & Navigasi**")
    st.markdown("---")
    portal = st.radio("🏬 Portal", ["LMI", "LSI"])

    st.markdown("---")
    if portal == "LSI":
        lsi_options = {
            "LM1 · 30 Des 2025 – 12 Jan 2026": 1,
            "LM2 · 13 Jan – 26 Jan 2026":       2,
            "LM3 · 27 Jan – 9 Feb 2026":        3,
            "LM4 · 10 Feb – 23 Feb 2026":       4,
            "LM5 · 24 Feb – 9 Mar 2026":        5,
            "LM6 · 10 Mar – 23 Mar 2026":       6,
            "LM7 . 24 Mar - 6 Apr 2026":        7,
        }
        sel          = st.selectbox("📅 Pilih Periode", list(lsi_options.keys()))
        lm_num       = lsi_options[sel]
        store_df, store_total, cat_df, period_label = load_lsi(lm_num)
        DIVISION_MAP        = DIVISION_MAP_LSI
        DIVISION_ORDER      = DIVISION_ORDER_LSI
        DIVISION_COLORS     = DIVISION_COLORS_LSI
        DIVISION_CARD_COLOR = DIVISION_CARD_COLOR_LSI
        portal_label        = "LSI"
        bar_accent          = "#9b5de5"
    else:
        lmi_options = {
            "LM1 · 1 – 14 Jan 2026":          1,
            "LM2 · 15 – 28 Jan 2026":         2,
            "LM3 · 29 Jan – 18 Feb 2026":     3,
            "LM4 · 19 Feb – 4 Mar 2026":      4,
            "LM5 · 5 – 25 Mar 2026":          5,
            "LM6 · 26 Mar – 8 Apr 2026":      6,
        }
        sel          = st.selectbox("📅 Pilih Periode", list(lmi_options.keys()))
        lm_num       = lmi_options[sel]
        store_df, store_total, cat_df, period_label = load_lmi(lm_num)
        DIVISION_MAP        = DIVISION_MAP_LMI
        DIVISION_ORDER      = DIVISION_ORDER_LMI
        DIVISION_COLORS     = DIVISION_COLORS_LMI
        DIVISION_CARD_COLOR = DIVISION_CARD_COLOR_LMI
        portal_label        = "LMI"
        bar_accent          = "#00d4ff"

    # Assign Division column ke cat_df
    cat_df = cat_df.copy()
    cat_df["Division"] = cat_df["Group"].map(DIVISION_MAP).fillna("Other")

    st.markdown("---")
    page      = st.radio("📌 View", ["🏠 Overview", "🏪 By Store", "📦 By Category"])
    st.markdown("---")
    lm_thresh = st.slider("Min LM Contribution (%)", 0.0, 60.0, 0.0, 0.5)
    st.markdown("---")
    st.caption("Data: Net Sales (dalam ribuan Rupiah)")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    # ── Trend Chart ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📈 Tren LM Net Sales & Contribution Seluruh Periode</div>', unsafe_allow_html=True)
    trend_df = load_all_lsi_trend() if portal_label == "LSI" else load_all_lmi_trend()

    if not trend_df.empty:
        bar_colors_trend = [
            bar_accent if i + 1 != lm_num else "#00f5d4"
            for i in range(len(trend_df))
        ]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=trend_df["Mailer"], y=trend_df["LM NS"], name="LM Net Sales",
            marker_color=bar_colors_trend, opacity=0.85,
            text=[f"{v:,.0f}" for v in trend_df["LM NS"]],
            textposition="outside", textfont=dict(color="#e2e8f0", size=11, weight="bold"),
            yaxis="y",
        ))
        fig_trend.add_trace(go.Scatter(
            x=trend_df["Mailer"], y=trend_df["LM Cont%"], name="LM Cont. %",
            mode="lines+markers+text",
            line=dict(color="#fee440", width=3),
            marker=dict(size=12, color="#fee440", line=dict(width=2, color="#1a1a2e")),
            text=[f"{v:.1f}%" for v in trend_df["LM Cont%"]],
            textposition="bottom center", textfont=dict(color="#ffffff", size=12, family="Poppins"),
            yaxis="y2",
        ))
        fig_trend.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            height=350, margin=dict(t=60, b=40, l=60, r=60),
            xaxis=dict(title="Periode", gridcolor="#2d3748", tickfont=dict(color="#94a3b8", size=12)),
            yaxis=dict(
                title=dict(text="LM Net Sales", font=dict(color=bar_accent)),
                tickfont=dict(color=bar_accent), gridcolor="#2d3748", side="left",
            ),
            yaxis2=dict(
                title=dict(text="LM Cont. %", font=dict(color="#fee440")),
                tickfont=dict(color="#fee440"),
                overlaying="y", side="right", showgrid=False,
                range=[0, max(trend_df["LM Cont%"]) * 1.5],
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        font=dict(color="#e2e8f0"), bgcolor="rgba(26,32,53,0.8)"),
            barmode="overlay",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        with st.expander("📋 Lihat Detail Data Tren"):
            td = trend_df.copy()
            td["Total NS"]  = td["Total NS"].apply(lambda x: f"{x:,.0f}")
            td["Normal NS"] = td["Normal NS"].apply(lambda x: f"{x:,.0f}")
            td["LM NS"]     = td["LM NS"].apply(lambda x: f"{x:,.0f}")
            td["LM Cont%"]  = td["LM Cont%"].apply(lambda x: f"{x:.2f}%")
            st.dataframe(td, use_container_width=True)

    st.markdown("---")

    # ── Badge & Title ─────────────────────────────────────────────────────────
    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 📊 Net Sales Overview, {period_label}")

    # ── Division Filter ───────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🏷️ Filter Division</div>', unsafe_allow_html=True)
    available_divisions = [d for d in DIVISION_ORDER if d in cat_df["Division"].unique()]
    selected_divisions  = st.multiselect(
        "Pilih Division :", options=available_divisions, default=[],
        key="overview_division_filter",
        help="Filter berdasarkan division",
        placeholder="Choose Option",
    )
    cat_div_filtered = cat_df[cat_df["Division"].isin(selected_divisions)] if selected_divisions else cat_df

    # ── Compute scorecard values ──────────────────────────────────────────────
    all_divs_selected = set(selected_divisions) == set(available_divisions)

    if all_divs_selected or not selected_divisions:
        total_ns      = store_total["Total NS"]
        lm_ns         = store_total["LM NS"]
        normal_ns     = store_total["Normal NS"]
        lm_cont       = store_total["LM Cont%"]
        sku_total_val = store_total["SKU Total"]
        sku_sale_val  = store_total["SKU Sale"]
        sku_cont_val  = store_total["SKU Cont%"]
        oos_val_total = store_total["OOS"]
        if portal_label == "LMI":
            trader_ns  = store_df["Trader NS"].sum()
            regular_ns = store_df["Regular NS"].sum()
        else:
            lm_trader = store_df["LM Trader NS"].sum()
            lm_prof   = store_df["LM Prof NS"].sum()
            lm_others = store_df["LM Others NS"].sum()
    else:
        total_ns      = cat_div_filtered["Total NS"].sum()
        lm_ns         = cat_div_filtered["LM NS"].sum()
        normal_ns     = cat_div_filtered["Normal NS"].sum()
        lm_cont       = (lm_ns / total_ns * 100) if total_ns else 0
        sku_total_val = cat_div_filtered["SKU Total"].sum()
        sku_sale_val  = cat_div_filtered["SKU Sale"].sum()
        sku_cont_val  = (sku_sale_val / sku_total_val * 100) if sku_total_val else 0
        oos_val_total = cat_div_filtered["OOS"].sum()
        if portal_label == "LMI":
            trader_ns  = cat_div_filtered["Trader NS"].sum()
            regular_ns = cat_div_filtered["Regular NS"].sum()
        else:
            lm_trader = cat_div_filtered["LM Trader NS"].sum()
            lm_prof   = cat_div_filtered["LM Prof NS"].sum()
            lm_others = cat_div_filtered["LM Others NS"].sum()

    # ── Scorecards 6 kolom ───────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Net Sales", fmt_rp(total_ns*1000)), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("LM (Promo) Sales", fmt_rp(lm_ns*1000), "green",
                                f"Kontribusi: {lm_cont:.2f}%"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Normal (Non-Promo)", fmt_rp(normal_ns*1000), "orange",
                                f"Kontribusi: {100-lm_cont:.2f}%"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("Total SKU Promo", f"{int(sku_total_val):,}", "purple",
                                f"Terjual: {int(sku_sale_val):,} SKU"), unsafe_allow_html=True)
    with c5:
        st.markdown(metric_card("SKU Sell-Through", f"{sku_cont_val:.1f}%", "teal",
                                "% SKU promo terjual"), unsafe_allow_html=True)
    with c6:
        oos_rate = (oos_val_total / sku_total_val * 100) if sku_total_val else 0
        st.markdown(metric_card("OOS", f"{int(oos_val_total):,} SKU", "red",
                                f"OOS Rate: {oos_rate:.1f}%"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pie charts ────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Komposisi LM vs Normal</div>', unsafe_allow_html=True)
        fig1 = go.Figure(go.Pie(
            labels=["LM (Promo)","Normal"], values=[lm_ns, normal_ns],
            hole=0.55, marker_colors=[bar_accent,"#2d3a5a"],
            textinfo="label+percent", textfont=dict(size=12, color="#ffffff"),
        ))
        fig1.update_layout(**{**PD, "showlegend":False, "height":280,
            "margin":dict(t=10,b=10,l=10,r=10),
            "annotations":[dict(text=f"<b>{lm_cont:.1f}%</b><br>LM",
                x=0.5, y=0.5, font=dict(size=16, color=bar_accent), showarrow=False)]})
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">SKU Promo: Terjual vs OOS vs Belum Terjual</div>', unsafe_allow_html=True)
        oos_pie    = int(oos_val_total)
        sold_pie   = int(sku_sale_val)
        unsold_pie = max(0, int(sku_total_val) - sold_pie - oos_pie)
        fig_sku = go.Figure(go.Pie(
            labels=["Terjual","OOS","Belum Terjual"],
            values=[sold_pie, oos_pie, unsold_pie],
            hole=0.55, marker_colors=["#00f5d4","#ff6b6b","#2d3a5a"],
            textinfo="label+percent", textfont=dict(size=11, color="#ffffff"),
        ))
        fig_sku.update_layout(**{**PD, "showlegend":False, "height":280,
            "margin":dict(t=10,b=10,l=10,r=10),
            "annotations":[dict(text=f"<b>{sku_cont_val:.1f}%</b><br>Sell-Through",
                x=0.5, y=0.5, font=dict(size=14, color="#00f5d4"), showarrow=False)]})
        st.plotly_chart(fig_sku, use_container_width=True)

    # ── LM Breakdown bar ─────────────────────────────────────────────────────
    if portal_label == "LSI":
        st.markdown('<div class="section-title">Breakdown Net Sales LM: Trader vs Prof vs Others</div>', unsafe_allow_html=True)
        fig_lm = go.Figure(go.Bar(
            x=["Trader","Professional","Others"],
            y=[lm_trader, lm_prof, lm_others],
            marker_color=["#fee440","#00d4ff","#9b5de5"],
            text=[f"{v/lm_ns*100:.1f}%" if lm_ns else "0%" for v in [lm_trader, lm_prof, lm_others]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
    else:
        st.markdown('<div class="section-title">Breakdown Net Sales LM: Regular vs Trader</div>', unsafe_allow_html=True)
        lm_total_breakdown = regular_ns + trader_ns
        fig_lm = go.Figure(go.Bar(
            x=["Regular (End User)","Trader"],
            y=[regular_ns, trader_ns],
            marker_color=["#00f5d4","#fee440"],
            text=[f"{v/lm_total_breakdown*100:.1f}%" if lm_total_breakdown else "0%" for v in [regular_ns, trader_ns]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
    fig_lm.update_layout(**{**PD, "height":300,
        "margin":dict(t=30,b=10,l=10,r=10), "yaxis_title":"Net Sales LM"})
    st.plotly_chart(fig_lm, use_container_width=True)

    # ── LM Net Sales per Division ─────────────────────────────────────────────
    st.markdown('<div class="section-title">LM Net Sales per Division</div>', unsafe_allow_html=True)
    # Use filtered data if divisions are selected, otherwise use all data
    div_data_src = cat_div_filtered if selected_divisions else cat_df
    div_bar = div_data_src.groupby("Division").agg(
        Total_NS=("Total NS","sum"), LM_NS=("LM NS","sum"),
    ).reset_index()
    div_bar["LM_Cont%"] = div_bar["LM_NS"] / div_bar["Total_NS"] * 100
    # Sort by LM_NS descending (largest to smallest)
    div_bar = div_bar.sort_values("LM_NS", ascending=False)
    div_colors = [DIVISION_COLORS.get(d,"#718096") for d in div_bar["Division"]]

    fig_div = go.Figure()
    fig_div.add_trace(go.Bar(
        x=div_bar["Division"], y=div_bar["LM_NS"], name="LM Net Sales",
        marker_color=div_colors, opacity=0.85,
        text=[f"{v:,.0f}" for v in div_bar["LM_NS"]],
        textposition="outside", textfont=dict(color="#e2e8f0", size=11, weight="bold"), yaxis="y",
    ))
    fig_div.add_trace(go.Scatter(
        x=div_bar["Division"], y=div_bar["LM_Cont%"], name="LM Cont. %",
        mode="lines+markers+text",
        line=dict(color="#fee440", width=3),
        marker=dict(size=12, color="#fee440", line=dict(width=2, color="#1a1a2e")),
        text=[f"{v:.1f}%" for v in div_bar["LM_Cont%"]],
        textposition="bottom center", textfont=dict(color="#ffffff", size=12, family="Poppins"), yaxis="y2",
    ))
    fig_div.update_layout(
        plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
        hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
        height=350, margin=dict(t=60, b=40, l=60, r=60),
        xaxis=dict(title="Division", gridcolor="#2d3748", tickfont=dict(color="#94a3b8", size=12)),
        yaxis=dict(
            title=dict(text="LM Net Sales", font=dict(color=bar_accent)),
            tickfont=dict(color=bar_accent), gridcolor="#2d3748", side="left",
        ),
        yaxis2=dict(
            title=dict(text="LM Cont. %", font=dict(color="#fee440")),
            tickfont=dict(color="#fee440"),
            overlaying="y", side="right", showgrid=False,
            range=[0, max(div_bar["LM_Cont%"]) * 1.5] if not div_bar.empty else [0, 100],
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color="#e2e8f0"), bgcolor="rgba(26,32,53,0.8)"),
        barmode="overlay",
    )
    st.plotly_chart(fig_div, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 – BY STORE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏪 By Store":
    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 🏪 Analisis Net Sales per Store — {period_label}")

    filtered = store_df[store_df["LM Cont%"] >= lm_thresh].copy()

    # ── Load region data for LSI ──────────────────────────────────────────────
    if portal_label == "LSI":
        # Apply region mapping directly from STORE_REGION_MAP
        filtered["Region"] = filtered["Store Name"].map(STORE_REGION_MAP)
        # Filter out stores without region (DCHD, LSI Export, Total All, etc.)
        filtered = filtered[filtered["Region"].notna()].copy()
        
        # ── Region filter (affects ALL visualizations) ────────────────────────
        st.markdown("### 📊 Peringkat Toko per Regional")
        available_regions = [r for r in ["Regional 1", "Regional 2", "Regional 3"] 
                            if r in filtered["Region"].unique()]
        
        selected_region = st.selectbox(
            "🏢 Pilih Regional:",
            options=["Semua Regional"] + available_regions,
            key="region_filter"
        )
        
        # Apply region filter to ALL data
        if selected_region != "Semua Regional":
            filtered = filtered[filtered["Region"] == selected_region].copy()

    # ── Scorecards 6 kolom ───────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Store Aktif", str(len(filtered))), unsafe_allow_html=True)
    with c2:
        total_lm_ns = filtered["LM NS"].sum()
        avg_lm_cont = filtered["LM Cont%"].mean()
        st.markdown(metric_card("Net Sales LM", fmt_rp(total_lm_ns*1000), "green", f"Avg Cont: {avg_lm_cont:.2f}%"), unsafe_allow_html=True)
    with c3:
        top = filtered.loc[filtered["Total NS"].idxmax(), "Store Name"] if len(filtered) else "–"
        st.markdown(metric_card("Highest Revenue Store", str(top), "orange"), unsafe_allow_html=True)
    with c4:
        top_lm = filtered.loc[filtered["LM Cont%"].idxmax(), "Store Name"] if len(filtered) else "–"
        st.markdown(metric_card("Highest LM Cont% Store", str(top_lm), "purple"), unsafe_allow_html=True)
    with c5:
        st.markdown(metric_card("Avg SKU Sell-Through", f"{filtered['SKU Cont%'].mean():.1f}%", "teal"), unsafe_allow_html=True)
    with c6:
        st.markdown(metric_card("Total OOS SKU", f"{int(filtered['OOS'].sum()):,}", "red"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: Net Sales & LM Contribution per Store (Synchronized View)
    # Sorting: by LM Cont% (highest first)
    # ══════════════════════════════════════════════════════════════════════════
    
    if portal_label == "LSI":
        # Create synchronized side-by-side charts
        col1, col2 = st.columns(2)
        
        # Sort by LM Cont% descending (highest contribution first)
        # For horizontal bar chart, we reverse so highest appears at top
        sorted_store = filtered.sort_values("LM Cont%", ascending=True)
        
        # Create display name with region prefix
        if selected_region == "Semua Regional":
            sorted_store["Display Name"] = sorted_store.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1
            )
        else:
            sorted_store["Display Name"] = sorted_store["Store Name"]
        
        with col1:
            st.markdown('<div class="section-title">Total Net Sales per Store (LM vs Normal)</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=sorted_store["Display Name"], x=sorted_store["Normal NS"],
                name="Normal", orientation="h", marker_color="#2d3a5a",
                text=[f"{v:,.0f}" for v in sorted_store["Normal NS"]],
                textposition="inside", textfont=dict(color="#94a3b8"),
            ))
            fig.add_trace(go.Bar(
                y=sorted_store["Display Name"], x=sorted_store["LM NS"],
                name="LM (Promo)", orientation="h", marker_color=bar_accent,
                text=[f"{v:,.0f}" for v in sorted_store["LM NS"]],
                textposition="inside", textfont=dict(color="#ffffff"),
            ))
            fig.update_layout(**{**PD, "barmode":"stack",
                "height":max(420, len(filtered)*28),
                "margin":dict(t=20,b=20,l=10,r=20), "xaxis_title":"Net Sales"})
            st.plotly_chart(fig, use_container_width=True, key="ns_chart_lsi")

        with col2:
            st.markdown('<div class="section-title">LM Contribution % per Store</div>', unsafe_allow_html=True)
            
            # Use same sort order as left chart for synchronization
            sorted_lm = sorted_store.copy()
            thresh_low = 5
            thresh_mid = 10
            colors = ["#ff6b6b" if v < thresh_low else "#fee440" if v < thresh_mid else "#00f5d4"
                      for v in sorted_lm["LM Cont%"]]
            fig2 = go.Figure(go.Bar(
                y=sorted_lm["Display Name"], x=sorted_lm["LM Cont%"],
                orientation="h", marker_color=colors,
                text=[f"{v:.1f}%" for v in sorted_lm["LM Cont%"]],
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
            fig2.add_vline(x=filtered["LM Cont%"].mean(), line_dash="dash", line_color="#718096",
                           annotation_text="Avg", annotation_font=dict(color="#718096"),
                           annotation_position="top")
            fig2.update_layout(**{**PD, "height":max(420, len(filtered)*28),
                "margin":dict(t=20,b=20,l=10,r=40), "xaxis_title":"LM Contribution (%)"})
            st.plotly_chart(fig2, use_container_width=True, key="lm_chart_lsi")
    
    else:
        # ── LMI: Standard visualization (no region) ───────────────────────────
        # Sort by LM Cont% descending (highest contribution first)
        sorted_store = filtered.sort_values("LM Cont%", ascending=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-title">Total Net Sales per Store (LM vs Normal)</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=sorted_store["Store Name"], x=sorted_store["Normal NS"],
                name="Normal", orientation="h", marker_color="#2d3a5a",
                text=[f"{v:,.0f}" for v in sorted_store["Normal NS"]],
                textposition="inside", textfont=dict(color="#94a3b8"),
            ))
            fig.add_trace(go.Bar(
                y=sorted_store["Store Name"], x=sorted_store["LM NS"],
                name="LM (Promo)", orientation="h", marker_color=bar_accent,
                text=[f"{v:,.0f}" for v in sorted_store["LM NS"]],
                textposition="inside", textfont=dict(color="#ffffff"),
            ))
            fig.update_layout(**{**PD, "barmode":"stack",
                "height":max(420, len(filtered)*28),
                "margin":dict(t=20,b=20,l=10,r=20), "xaxis_title":"Net Sales"})
            st.plotly_chart(fig, use_container_width=True, key="ns_chart_lmi")

        with col2:
            st.markdown('<div class="section-title">LM Contribution % per Store</div>', unsafe_allow_html=True)
            # Use same order as left chart
            sorted_lm = sorted_store.copy()
            thresh_low = 10
            thresh_mid = 20
            colors = ["#ff6b6b" if v < thresh_low else "#fee440" if v < thresh_mid else "#00f5d4"
                      for v in sorted_lm["LM Cont%"]]
            fig2 = go.Figure(go.Bar(
                y=sorted_lm["Store Name"], x=sorted_lm["LM Cont%"],
                orientation="h", marker_color=colors,
                text=[f"{v:.1f}%" for v in sorted_lm["LM Cont%"]],
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
            fig2.add_vline(x=filtered["LM Cont%"].mean(), line_dash="dash", line_color="#718096",
                           annotation_text="Avg", annotation_font=dict(color="#718096"),
                           annotation_position="top")
            fig2.update_layout(**{**PD, "height":max(420, len(filtered)*28),
                "margin":dict(t=20,b=20,l=10,r=40), "xaxis_title":"LM Contribution (%)"})
            st.plotly_chart(fig2, use_container_width=True, key="lm_chart_lmi")

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: SKU Performance per Store (Enhanced Labels)
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📦 SKU Performance per Store")
    st.markdown('<div class="section-title">SKU Terjual / OOS / Belum Terjual per Store</div>', unsafe_allow_html=True)

    sku_store = filtered[filtered["SKU Total"] > 0].copy()
    sku_store["SKU Unsold"] = (sku_store["SKU Total"] - sku_store["SKU Sale"] - sku_store["OOS"]).clip(lower=0)
    
    # Calculate percentages for labels
    sku_store["Sale_Pct"] = (sku_store["SKU Sale"] / sku_store["SKU Total"] * 100).round(1)
    sku_store["OOS_Pct"] = (sku_store["OOS"] / sku_store["SKU Total"] * 100).round(1)
    sku_store["Unsold_Pct"] = (sku_store["SKU Unsold"] / sku_store["SKU Total"] * 100).round(1)
    
    # Sort by LM Cont% (ascending for bottom-up display, highest at top)
    sku_store = sku_store.sort_values("LM Cont%", ascending=True)
    
    if portal_label == "LSI":
        if selected_region == "Semua Regional":
            sku_store["Display Name"] = sku_store.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1
            )
        else:
            sku_store["Display Name"] = sku_store["Store Name"]
    else:
        sku_store["Display Name"] = sku_store["Store Name"]

    fig_sku_s = go.Figure()
    
    # SKU Terjual with Qty + Percentage
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["SKU Sale"], name="SKU Terjual",
        orientation="h", marker_color="#00f5d4",
        text=[f"{int(v)} ({p:.1f}%)" for v, p in zip(sku_store["SKU Sale"], sku_store["Sale_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>SKU Terjual: %{x:,.0f}<extra></extra>",
    ))
    
    # OOS with Qty + Percentage
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["OOS"], name="OOS",
        orientation="h", marker_color="#ff6b6b",
        text=[f"{int(v)} ({p:.1f}%)" if v > 0 else "" for v, p in zip(sku_store["OOS"], sku_store["OOS_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>OOS: %{x:,.0f}<extra></extra>",
    ))
    
    # Belum Terjual with Qty + Percentage
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["SKU Unsold"], name="Belum Terjual",
        orientation="h", marker_color="#9b5de5",
        text=[f"{int(v)} ({p:.1f}%)" if v > 3 else "" for v, p in zip(sku_store["SKU Unsold"], sku_store["Unsold_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>Belum Terjual: %{x:,.0f}<extra></extra>",
    ))
    
    fig_sku_s.update_layout(
        plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
        hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
        barmode="stack", height=max(500, len(sku_store)*26),
        margin=dict(t=30, b=20, l=10, r=20), xaxis_title="Jumlah SKU",
        xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8"),
                   range=[0, sku_store["SKU Total"].max() * 1.05]),
        yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color="#e2e8f0")),
    )
    st.plotly_chart(fig_sku_s, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: LM Breakdown per Store (With Inside Percentage Labels)
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    
    # Sort by LM Cont% (ascending for bottom-up display, highest at top)
    sorted_br = filtered.sort_values("LM Cont%", ascending=True).copy()
    
    if portal_label == "LSI":
        if selected_region == "Semua Regional":
            sorted_br["Display Name"] = sorted_br.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1
            )
        else:
            sorted_br["Display Name"] = sorted_br["Store Name"]
    else:
        sorted_br["Display Name"] = sorted_br["Store Name"]
    
    if portal_label == "LSI":
        st.markdown('<div class="section-title">Breakdown LM Sales: Trader / Prof / Others per Store</div>', unsafe_allow_html=True)
        
        # Calculate percentages for each segment
        sorted_br["Trader_Pct"] = (sorted_br["LM Trader NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        sorted_br["Prof_Pct"] = (sorted_br["LM Prof NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        sorted_br["Others_Pct"] = (sorted_br["LM Others NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Trader NS"],
            name="Trader", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Trader NS"], sorted_br["Trader_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Prof NS"],
            name="Professional", orientation="h", marker_color="#00d4ff",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Prof NS"], sorted_br["Prof_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Others NS"],
            name="Others", orientation="h", marker_color="#9b5de5",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Others NS"], sorted_br["Others_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    else:
        st.markdown('<div class="section-title">Breakdown LM Sales: Regular vs Trader per Store</div>', unsafe_allow_html=True)
        
        # Calculate percentages for each segment
        lm_total = sorted_br["Regular NS"] + sorted_br["Trader NS"]
        sorted_br["Regular_Pct"] = (sorted_br["Regular NS"] / lm_total * 100).fillna(0).round(1)
        sorted_br["Trader_Pct"] = (sorted_br["Trader NS"] / lm_total * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Regular NS"],
            name="Regular (End User)", orientation="h", marker_color="#00f5d4",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Regular NS"], sorted_br["Regular_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Trader NS"],
            name="Trader", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Trader NS"], sorted_br["Trader_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    
    fig_br.update_layout(
        plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
        hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
        barmode="stack", height=max(420, len(filtered)*22),
        margin=dict(t=30, b=20, l=10, r=10), xaxis_title="Net Sales LM",
        xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        legend=dict(bgcolor="rgba(26,32,53,0.8)", bordercolor="#2d3748", borderwidth=1,
                    font=dict(color="#e2e8f0")),
    )
    st.plotly_chart(fig_br, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: Data Table
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('<div class="section-title">📋 Detail Data per Store</div>', unsafe_allow_html=True)
    
    # Sort by LM Cont% descending (highest first)
    table_df = filtered.sort_values("LM Cont%", ascending=False).copy()
    
    if portal_label == "LSI":
        disp = ["Region", "Store Name","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
    else:
        disp = ["Store Name","Total NS","LM NS","Normal NS","LM Cont%",
                "Regular NS","Regular Cont%","Trader NS","Trader Cont%",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","LM NS":"{:,.1f}","Normal NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","Regular NS":"{:,.1f}","Regular Cont%":"{:.2f}%",
                "Trader NS":"{:,.1f}","Trader Cont%":"{:.2f}%",
                "SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
    
    st.dataframe(table_df[disp].style.format(fmt), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 – BY CATEGORY
# ════════════════════════════════════════════════════════════════════════════
elif page == "📦 By Category":
    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 📦 Analisis Net Sales per Kategori — {period_label}")

    cat_filtered = cat_df[cat_df["LM Cont%"] >= lm_thresh].copy()

    # ── Division filter (affects ALL visualizations) ─────────────────────────
    st.markdown("### 📊 Peringkat Kategori per Division")
    
    # Get available divisions based on portal
    if portal_label == "LSI":
        division_order_list = ["FRESH FOOD", "MEAL SOLUTION", "DRY FOOD", "NON FOOD", "Other"]
    else:
        division_order_list = ["FRESH FOOD", "MEAL SOLUTION", "DRY FOOD", "H&B HOME CARE", "ELECTRONIC", "NON FOOD", "Other"]
    
    available_divisions = [d for d in division_order_list if d in cat_filtered["Division"].unique()]
    
    selected_division = st.selectbox(
        "🏷️ Pilih Division:",
        options=["Semua Division"] + available_divisions,
        key="division_filter_cat"
    )
    
    # Apply division filter to ALL data
    if selected_division != "Semua Division":
        cat_filtered = cat_filtered[cat_filtered["Division"] == selected_division].copy()

    # ── Calculate metrics ────────────────────────────────────────────────────
    total_cat_ns  = cat_filtered["Total NS"].sum()
    total_lm_ns   = cat_filtered["LM NS"].sum()
    lm_pct        = total_lm_ns / total_cat_ns * 100 if total_cat_ns else 0
    total_sku_cat = cat_filtered["SKU Total"].sum()
    sale_sku_cat  = cat_filtered["SKU Sale"].sum()
    pct_sku_cat   = sale_sku_cat / total_sku_cat * 100 if total_sku_cat else 0

    # ── Scorecards 6 kolom ───────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Kategori Aktif", str(len(cat_filtered))), unsafe_allow_html=True)
    with c2:
        avg_lm_cont = cat_filtered["LM Cont%"].mean() if len(cat_filtered) else 0
        st.markdown(metric_card("Net Sales LM", fmt_rp(total_lm_ns*1000), "green", f"Avg Cont: {avg_lm_cont:.2f}%"), unsafe_allow_html=True)
    with c3:
        top = cat_filtered.loc[cat_filtered["Total NS"].idxmax(), "Category"] if len(cat_filtered) else "–"
        st.markdown(metric_card("Highest Revenue Category", str(top), "orange"), unsafe_allow_html=True)
    with c4:
        top_lm = cat_filtered.loc[cat_filtered["LM Cont%"].idxmax(), "Category"] if len(cat_filtered) else "–"
        st.markdown(metric_card("Highest LM Cont% Category", str(top_lm), "purple"), unsafe_allow_html=True)
    with c5:
        st.markdown(metric_card("Avg SKU Sell-Through", f"{pct_sku_cat:.1f}%", "teal"), unsafe_allow_html=True)
    with c6:
        st.markdown(metric_card("Total OOS SKU", f"{int(cat_filtered['OOS'].sum()):,}", "red"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: Net Sales & LM Contribution per Category (Synchronized View)
    # Sorting: by LM Cont% (highest first)
    # ══════════════════════════════════════════════════════════════════════════
    
    # Create synchronized side-by-side charts
    col1, col2 = st.columns(2)
    
    # Sort by LM Cont% descending (highest contribution first)
    # For horizontal bar chart, we reverse so highest appears at top
    sorted_cat = cat_filtered.sort_values("LM Cont%", ascending=True)
    
    # Create display name with division prefix
    if selected_division == "Semua Division":
        # Create abbreviation for division
        div_abbrev = {
            "FRESH FOOD": "FF",
            "MEAL SOLUTION": "MS",
            "DRY FOOD": "DF",
            "H&B HOME CARE": "HB",
            "ELECTRONIC": "EL",
            "NON FOOD": "NF",
            "Other": "OT",
        }
        sorted_cat["Display Name"] = sorted_cat.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1
        )
    else:
        sorted_cat["Display Name"] = sorted_cat["Category"]
    
    with col1:
        st.markdown('<div class="section-title">Total Net Sales per Category (LM vs Normal)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=sorted_cat["Display Name"], x=sorted_cat["Normal NS"],
            name="Normal", orientation="h", marker_color="#2d3a5a",
            text=[f"{v:,.0f}" for v in sorted_cat["Normal NS"]],
            textposition="inside", textfont=dict(color="#94a3b8"),
        ))
        fig.add_trace(go.Bar(
            y=sorted_cat["Display Name"], x=sorted_cat["LM NS"],
            name="LM (Promo)", orientation="h", marker_color=bar_accent,
            text=[f"{v:,.0f}" for v in sorted_cat["LM NS"]],
            textposition="inside", textfont=dict(color="#ffffff"),
        ))
        fig.update_layout(**{**PD, "barmode":"stack",
            "height":max(420, len(cat_filtered)*28),
            "margin":dict(t=20,b=20,l=10,r=20), "xaxis_title":"Net Sales"})
        st.plotly_chart(fig, use_container_width=True, key="ns_chart_cat")

    with col2:
        st.markdown('<div class="section-title">LM Contribution % per Category</div>', unsafe_allow_html=True)
        
        # Use same sort order as left chart for synchronization
        sorted_lm = sorted_cat.copy()
        if portal_label == "LSI":
            thresh_low = 5
            thresh_mid = 10
        else:
            thresh_low = 10
            thresh_mid = 20
        colors = ["#ff6b6b" if v < thresh_low else "#fee440" if v < thresh_mid else "#00f5d4"
                  for v in sorted_lm["LM Cont%"]]
        fig2 = go.Figure(go.Bar(
            y=sorted_lm["Display Name"], x=sorted_lm["LM Cont%"],
            orientation="h", marker_color=colors,
            text=[f"{v:.1f}%" for v in sorted_lm["LM Cont%"]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig2.add_vline(x=cat_filtered["LM Cont%"].mean(), line_dash="dash", line_color="#718096",
                       annotation_text="Avg", annotation_font=dict(color="#718096"),
                       annotation_position="top")
        fig2.update_layout(**{**PD, "height":max(420, len(cat_filtered)*28),
            "margin":dict(t=20,b=20,l=10,r=40), "xaxis_title":"LM Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True, key="lm_chart_cat")

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: SKU Performance per Category (Enhanced Labels)
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📦 SKU Performance per Category")
    st.markdown('<div class="section-title">SKU Terjual / OOS / Belum Terjual per Category</div>', unsafe_allow_html=True)

    sku_cat = cat_filtered[cat_filtered["SKU Total"] > 0].copy()
    sku_cat["SKU Unsold"] = (sku_cat["SKU Total"] - sku_cat["SKU Sale"] - sku_cat["OOS"]).clip(lower=0)
    
    # Calculate percentages for labels
    sku_cat["Sale_Pct"] = (sku_cat["SKU Sale"] / sku_cat["SKU Total"] * 100).round(1)
    sku_cat["OOS_Pct"] = (sku_cat["OOS"] / sku_cat["SKU Total"] * 100).round(1)
    sku_cat["Unsold_Pct"] = (sku_cat["SKU Unsold"] / sku_cat["SKU Total"] * 100).round(1)
    
    # Sort by LM Cont% (ascending for bottom-up display, highest at top)
    sku_cat = sku_cat.sort_values("LM Cont%", ascending=True)
    
    # Create display name with division prefix
    if selected_division == "Semua Division":
        div_abbrev = {
            "FRESH FOOD": "FF", "MEAL SOLUTION": "MS", "DRY FOOD": "DF",
            "H&B HOME CARE": "HB", "ELECTRONIC": "EL", "NON FOOD": "NF", "Other": "OT",
        }
        sku_cat["Display Name"] = sku_cat.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1
        )
    else:
        sku_cat["Display Name"] = sku_cat["Category"]

    fig_sku_c = go.Figure()
    
    # SKU Terjual with Qty + Percentage
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["SKU Sale"], name="SKU Terjual",
        orientation="h", marker_color="#00f5d4",
        text=[f"{int(v)} ({p:.1f}%)" for v, p in zip(sku_cat["SKU Sale"], sku_cat["Sale_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>SKU Terjual: %{x:,.0f}<extra></extra>",
    ))
    
    # OOS with Qty + Percentage
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["OOS"], name="OOS",
        orientation="h", marker_color="#ff6b6b",
        text=[f"{int(v)} ({p:.1f}%)" if v > 0 else "" for v, p in zip(sku_cat["OOS"], sku_cat["OOS_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>OOS: %{x:,.0f}<extra></extra>",
    ))
    
    # Belum Terjual with Qty + Percentage
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["SKU Unsold"], name="Belum Terjual",
        orientation="h", marker_color="#9b5de5",
        text=[f"{int(v)} ({p:.1f}%)" if v > 3 else "" for v, p in zip(sku_cat["SKU Unsold"], sku_cat["Unsold_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
        hovertemplate="<b>%{y}</b><br>Belum Terjual: %{x:,.0f}<extra></extra>",
    ))
    
    fig_sku_c.update_layout(
        plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
        hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
        barmode="stack", height=max(500, len(sku_cat)*26),
        margin=dict(t=30, b=20, l=10, r=20), xaxis_title="Jumlah SKU",
        xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8"),
                   range=[0, sku_cat["SKU Total"].max() * 1.05] if len(sku_cat) else [0, 100]),
        yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color="#e2e8f0")),
    )
    st.plotly_chart(fig_sku_c, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: LM Breakdown per Category (With Inside Percentage Labels)
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    
    # Sort by LM Cont% (ascending for bottom-up display, highest at top)
    sorted_br = cat_filtered.sort_values("LM Cont%", ascending=True).copy()
    
    # Create display name with division prefix
    if selected_division == "Semua Division":
        div_abbrev = {
            "FRESH FOOD": "FF", "MEAL SOLUTION": "MS", "DRY FOOD": "DF",
            "H&B HOME CARE": "HB", "ELECTRONIC": "EL", "NON FOOD": "NF", "Other": "OT",
        }
        sorted_br["Display Name"] = sorted_br.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1
        )
    else:
        sorted_br["Display Name"] = sorted_br["Category"]
    
    if portal_label == "LSI":
        st.markdown('<div class="section-title">Breakdown LM Sales: Trader / Prof / Others per Category</div>', unsafe_allow_html=True)
        
        # Calculate percentages for each segment
        sorted_br["Trader_Pct"] = (sorted_br["LM Trader NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        sorted_br["Prof_Pct"] = (sorted_br["LM Prof NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        sorted_br["Others_Pct"] = (sorted_br["LM Others NS"] / sorted_br["LM NS"] * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Trader NS"],
            name="Trader", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Trader NS"], sorted_br["Trader_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Prof NS"],
            name="Professional", orientation="h", marker_color="#00d4ff",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Prof NS"], sorted_br["Prof_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["LM Others NS"],
            name="Others", orientation="h", marker_color="#9b5de5",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["LM Others NS"], sorted_br["Others_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    else:
        st.markdown('<div class="section-title">Breakdown LM Sales: Regular vs Trader per Category</div>', unsafe_allow_html=True)
        
        # Calculate percentages for each segment
        lm_total = sorted_br["Regular NS"] + sorted_br["Trader NS"]
        sorted_br["Regular_Pct"] = (sorted_br["Regular NS"] / lm_total * 100).fillna(0).round(1)
        sorted_br["Trader_Pct"] = (sorted_br["Trader NS"] / lm_total * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Regular NS"],
            name="Regular (End User)", orientation="h", marker_color="#00f5d4",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Regular NS"], sorted_br["Regular_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Trader NS"],
            name="Trader", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Trader NS"], sorted_br["Trader_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    
    fig_br.update_layout(
        plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
        hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
        barmode="stack", height=max(420, len(cat_filtered)*22),
        margin=dict(t=30, b=20, l=10, r=10), xaxis_title="Net Sales LM",
        xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
        legend=dict(bgcolor="rgba(26,32,53,0.8)", bordercolor="#2d3748", borderwidth=1,
                    font=dict(color="#e2e8f0")),
    )
    st.plotly_chart(fig_br, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION: Data Table
    # Sorting: by LM Cont% (highest first) - same as other charts
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('<div class="section-title">📋 Detail Data per Category</div>', unsafe_allow_html=True)
    
    # Sort by LM Cont% descending (highest first)
    table_df = cat_filtered.sort_values("LM Cont%", ascending=False).copy()
    
    if portal_label == "LSI":
        disp = ["Division", "Category","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
    else:
        disp = ["Division", "Category","Total NS","LM NS","Normal NS","LM Cont%",
                "Regular NS","Regular Cont%","Trader NS","Trader Cont%",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","LM NS":"{:,.1f}","Normal NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","Regular NS":"{:,.1f}","Regular Cont%":"{:.2f}%",
                "Trader NS":"{:,.1f}","Trader Cont%":"{:.2f}%",
                "SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
    
    st.dataframe(table_df[disp].style.format(fmt), use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(f"📊 Dashboard {portal_label} · {period_label} | Data: Net Sales (dalam ribuan Rupiah)")
