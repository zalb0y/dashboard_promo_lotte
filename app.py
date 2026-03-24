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

    /* ── Global ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        color: #e2e8f0 !important;
    }
    .main, section.main { background: transparent !important; }
    .block-container { padding-top: 1rem; max-width: 1400px; }

    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        visibility: hidden !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
    }
    .stApp > header,
    header.stAppHeader,
    [data-testid="stAppViewBlockContainer"] > header,
    .stApp header {
        display: none !important;
        height: 0 !important;
        background: transparent !important;
    }
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    .stApp > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    [data-testid="stAppViewContainer"] > div:first-child {
        padding-top: 0 !important;
    }
    [data-testid="stAppViewBlockContainer"],
    .block-container {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
    [data-testid="stSidebarHeader"] button,
    button[kind="headerNoPadding"] {
        display: none !important;
        visibility: hidden !important;
    }
    span[data-testid="stIconMaterial"] {
        font-size: 0 !important;
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] * { 
        color: #e2e8f0 !important; 
        font-family: 'Poppins', sans-serif !important; 
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(145deg, #1e2a4a 0%, #2d3a5a 100%);
        border-radius: 20px;
        padding: 1.3rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        border-left: 4px solid #00d4ff;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,212,255,0.2);
        border-color: rgba(0,212,255,0.3);
    }
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

    .metric-value {
        font-size: 1.7rem; font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    .metric-label {
        font-size: 0.72rem; color: #a0aec0;
        text-transform: uppercase; letter-spacing: 0.1em;
        font-weight: 500; margin-top: 0.3rem;
    }
    .metric-delta { font-size: 0.82rem; margin-top: 0.25rem; color: #718096; }

    /* ── Section Title ── */
    .section-title {
        font-size: 1.05rem; font-weight: 600; color: #ffffff;
        margin-bottom: 0.7rem; padding-left: 0.6rem;
        border-left: 4px solid #00d4ff;
        letter-spacing: 0.01em;
    }

    /* ── Insight Boxes ── */
    .insight-box {
        background: linear-gradient(135deg, rgba(0,212,255,0.08) 0%, rgba(123,44,191,0.08) 100%);
        border-left: 3px solid #00d4ff;
        border-radius: 0 12px 12px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        color: #93c5fd;
        backdrop-filter: blur(8px);
        border-top: 1px solid rgba(0,212,255,0.1);
    }
    .insight-box.warning {
        background: linear-gradient(135deg, rgba(254,228,64,0.08) 0%, rgba(255,107,107,0.08) 100%);
        border-left-color: #fee440;
        border-top-color: rgba(254,228,64,0.1);
        color: #fde68a;
    }
    .insight-box.success {
        background: linear-gradient(135deg, rgba(0,245,212,0.08) 0%, rgba(0,212,255,0.08) 100%);
        border-left-color: #00f5d4;
        border-top-color: rgba(0,245,212,0.1);
        color: #6ee7b7;
    }

    /* ── Portal Badge ── */
    .portal-badge {
        display: inline-block; padding: 0.3rem 1.1rem;
        border-radius: 20px; font-weight: 700; font-size: 0.8rem;
        margin-bottom: 0.5rem; letter-spacing: 0.08em;
        font-family: 'Poppins', sans-serif;
    }
    .badge-lmi {
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.08));
        color: #00d4ff;
        border: 1px solid rgba(0,212,255,0.35);
        box-shadow: 0 0 12px rgba(0,212,255,0.15);
    }
    .badge-lsi {
        background: linear-gradient(135deg, rgba(155,93,229,0.15), rgba(123,44,191,0.08));
        color: #c084fc;
        border: 1px solid rgba(155,93,229,0.35);
        box-shadow: 0 0 12px rgba(155,93,229,0.15);
    }

    /* ── Headings ── */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Poppins', sans-serif !important; }
    p, li { color: #a0aec0; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px; overflow: hidden;
    }

    /* ── Widgets ── */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiselect"] > div > div {
        background-color: rgba(30,42,74,0.9) !important;
        border-color: rgba(255,255,255,0.12) !important;
        color: #e2e8f0 !important;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; }
    [data-testid="stCaption"] { color: #4a5568 !important; }

    /* ── Scrollbar ── */
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
    cls = {"blue":"","green":"green","orange":"orange","purple":"purple","red":"red","teal":"teal"}.get(color,"")
    return f"""
    <div class="metric-card {cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>"""

def insight(text, kind="info"):
    cls = {"info":"","warning":"warning","success":"success"}.get(kind,"")
    return f'<div class="insight-box {cls}">💡 {text}</div>'

def calc_sku_cont(df):
    """
    Hitung ulang SKU Contribution %
    Formula: SKU Sale / SKU Total * 100
    (OOS sudah termasuk di dalam SKU Sale)
    """
    df = df.copy()
    df["SKU Cont% Calc"] = df.apply(
        lambda r: r["SKU Sale"] / r["SKU Total"] * 100
        if r["SKU Total"] > 0 else 0,
        axis=1
    )
    return df

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

# ─── DATA LOADERS ────────────────────────────────────────────────────────────
LMI_FILES = {
    1: {"path": "data/LM1_114_Jan_Nasional.xlsx",       "has_nan_col": True},
    2: {"path": "data/LM2_1528_Jan_Nasional.xlsx",       "has_nan_col": True},
    3: {"path": "data/LM3_29_Jan18_Feb_Nasional.xlsx",   "has_nan_col": True},
    4: {"path": "data/LM4_19_Feb4_Mar_Nasional.xlsx",    "has_nan_col": False},
}

LMI_PERIODS = {
    1: "1-14 Jan",
    2: "15-28 Jan",
    3: "29 Jan-18 Feb",
    4: "19 Feb-4 Mar",
}

LSI_PERIODS = {
    1: "30 Des-12 Jan",
    2: "13-26 Jan",
    3: "27 Jan-9 Feb",
    4: "10-23 Feb",
    5: "24 Feb-9 Mar",
    6: "10-23 Mar",
}

@st.cache_data
def load_lmi(lm_num=1):
    cfg  = LMI_FILES[lm_num]
    path = cfg["path"]
    nan  = cfg["has_nan_col"]

    raw_store = pd.read_excel(path, sheet_name="By Store", header=None)

    if nan:
        period_label = str(raw_store.iloc[1, 1])
        store_data = raw_store.iloc[4:16].copy()
        store_data.columns = range(store_data.shape[1])
        store_data = store_data[[1,2,3,4,5,6,7,8,9,10]]
        total_row  = raw_store.iloc[16]
        st_total   = {"Total NS": total_row[3], "Normal NS": total_row[4],
                      "LM NS": total_row[5], "LM Cont%": total_row[6]}
        cat_id_col, cat_name_col = 1, 2
        cat_start, num_cols = 4, [3,4,5,6,7,8,9,10]
    else:
        period_label = str(raw_store.iloc[0, 1])
        store_data = raw_store.iloc[3:15].copy()
        store_data.columns = range(store_data.shape[1])
        store_data = store_data[[0,1,2,3,4,5,6,7,8,9]]
        total_row  = raw_store.iloc[15]
        st_total   = {"Total NS": total_row[2], "Normal NS": total_row[3],
                      "LM NS": total_row[4], "LM Cont%": total_row[5]}
        cat_id_col, cat_name_col = 0, 1
        cat_start, num_cols = 3, [2,3,4,5,6,7,8,9]

    store_data.columns = ["Store ID","Store Name","Total NS","Normal NS","LM NS",
                          "LM Cont%","Regular NS","Regular Cont%","Trader NS","Trader Cont%"]
    store_data = store_data.dropna(subset=["Store ID"]).reset_index(drop=True)
    for col in store_data.columns[2:]:
        store_data[col] = pd.to_numeric(store_data[col], errors="coerce")

    raw_cat = pd.read_excel(path, sheet_name="By Cat", header=None)
    GROUP_LABELS = ["FRESH FOOD","MEAL SOLUTION","DRY FOOD","H&B HOME CARE","ELECTRONIC","NON FOOD","TOTAL"]
    all_rows = raw_cat.iloc[cat_start:].copy()
    all_rows.columns = range(all_rows.shape[1])

    rows = []
    for _, r in all_rows.iterrows():
        cat_id   = r[cat_id_col]
        cat_name = r[cat_name_col]
        if pd.isna(cat_id): continue
        c = num_cols
        rows.append({
            "Cat ID":       cat_id, "Category": cat_name,
            "Total NS":     pd.to_numeric(r[c[0]], errors="coerce"),
            "Normal NS":    pd.to_numeric(r[c[1]], errors="coerce"),
            "LM NS":        pd.to_numeric(r[c[2]], errors="coerce"),
            "LM Cont%":     pd.to_numeric(r[c[3]], errors="coerce"),
            "Regular NS":   pd.to_numeric(r[c[4]], errors="coerce"),
            "Regular Cont%":pd.to_numeric(r[c[5]], errors="coerce"),
            "Trader NS":    pd.to_numeric(r[c[6]], errors="coerce"),
            "Trader Cont%": pd.to_numeric(r[c[7]], errors="coerce"),
            "Is Group": str(cat_name).strip().upper() in [g.upper() for g in GROUP_LABELS],
        })
    cat_df = pd.DataFrame(rows)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()

    group_map = {
        "FRESH FOOD":    [31,32,33,34,35],
        "MEAL SOLUTION": [80,82],
        "DRY FOOD":      [11,17,21,23,24],
        "H&B HOME CARE": [14,19],
        "ELECTRONIC":    [86,87,88],
        "NON FOOD":      [51,57,85,13,62,71],
        "OTHER":         [97,98,99],
    }
    id_to_group = {i: grp for grp, ids in group_map.items() for i in ids}
    cat_detail["Group"] = cat_detail["Cat ID"].apply(
        lambda x: id_to_group.get(int(x), "OTHER") if str(x).isdigit() else "OTHER"
    )
    return store_data, st_total, cat_detail, period_label


@st.cache_data
def load_lsi(lm_num):
    path = f"data/LM{lm_num}_LSI_Summary.xlsb"
    raw = pd.read_excel(path, engine="pyxlsb", sheet_name="Summary by Store", header=None)
    period_label = str(raw.iloc[0, 1])

    data_rows = raw.iloc[3:].copy()
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
        if pd.isna(cat_id): continue
        cat_id_str = str(cat_id).strip()
        is_group = cat_id_str.upper() in [g.upper() for g in GROUP_LABELS_LSI]
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

    cat_df = pd.DataFrame(cat_data)
    cat_detail = cat_df[~cat_df["Is Group"]].copy()

    group_id_map = {
        "31":"FRESH FOOD","32":"FRESH FOOD","33":"FRESH FOOD","34":"FRESH FOOD","35":"FRESH FOOD",
        "80":"MEAL SOLUTION","82":"MEAL SOLUTION",
        "17":"DRY FOOD","21":"DRY FOOD","11":"DRY FOOD","26":"DRY FOOD","27":"DRY FOOD",
        "14":"H&B HOME CARE","19":"H&B HOME CARE",
        "86":"ELECTRONIC","87":"ELECTRONIC","88":"ELECTRONIC",
        "51":"NON FOOD","57":"NON FOOD","85":"NON FOOD","13":"NON FOOD","62":"NON FOOD","71":"NON FOOD",
        "97":"OTHER","98":"OTHER","99":"OTHER",
    }
    cat_detail = cat_detail.copy()
    cat_detail["Group"] = cat_detail["Cat ID"].apply(lambda x: group_id_map.get(str(x).strip(), "OTHER"))

    return store, store_total, cat_detail, period_label


@st.cache_data
def load_all_lsi_trend():
    trend_data = []
    for lm_num in range(1, 7):
        try:
            _, store_total, _, period_label = load_lsi(lm_num)
            trend_data.append({
                "Mailer": f"LM{lm_num}",
                "Period": LSI_PERIODS.get(lm_num, ""),
                "Total NS": store_total["Total NS"],
                "Normal NS": store_total["Normal NS"],
                "LM NS": store_total["LM NS"],
                "LM Cont%": store_total["LM Cont%"],
            })
        except Exception as e:
            pass
    return pd.DataFrame(trend_data)


@st.cache_data
def load_all_lmi_trend():
    trend_data = []
    for lm_num in range(1, 5):
        try:
            _, store_total, _, period_label = load_lmi(lm_num)
            trend_data.append({
                "Mailer": f"LM{lm_num}",
                "Period": LMI_PERIODS.get(lm_num, ""),
                "Total NS": store_total["Total NS"],
                "Normal NS": store_total["Normal NS"],
                "LM NS": store_total["LM NS"],
                "LM Cont%": store_total["LM Cont%"],
            })
        except Exception as e:
            pass
    return pd.DataFrame(trend_data)


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
        }
        selected_period = st.selectbox("📅 Pilih Periode", list(lsi_options.keys()))
        lm_num = lsi_options[selected_period]
        store_df, store_total, cat_df, period_label = load_lsi(lm_num)
        portal_label = "LSI"

        # ── Hitung ulang SKU Cont% untuk store dan cat ──
        # Formula: SKU Sale / SKU Total (OOS sudah termasuk dalam SKU Sale)
        store_df = calc_sku_cont(store_df)
        cat_df   = calc_sku_cont(cat_df)

        # Hitung ulang store_total SKU Cont% (agregat)
        sku_total_agg = store_total["SKU Total"]
        sku_sale_agg  = store_total["SKU Sale"]
        oos_agg       = store_total["OOS"]
        store_total["SKU Cont% Calc"] = (
            sku_sale_agg / sku_total_agg * 100
            if sku_total_agg else 0
        )
    else:
        lmi_options = {
            "LM1 · 1–14 Jan 2026":          1,
            "LM2 · 15–28 Jan 2026":         2,
            "LM3 · 29 Jan – 18 Feb 2026":   3,
            "LM4 · 19 Feb – 4 Mar 2026":    4,
        }
        selected_lmi = st.selectbox("📅 Pilih Periode", list(lmi_options.keys()))
        lm_num_lmi = lmi_options[selected_lmi]
        store_df, store_total, cat_df, period_label = load_lmi(lm_num_lmi)
        portal_label = "LMI"

    st.markdown("---")
    page = st.radio("📌 View", ["🏠 Overview", "🏪 By Store", "📦 By Category"])

    st.markdown("---")
    lm_thresh = st.slider("Min LM Contribution (%)", 0.0, 60.0, 0.0, 0.5)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown('<div class="section-title">📈 Tren LM Net Sales & Contribution Seluruh Periode</div>', unsafe_allow_html=True)

    if portal_label == "LSI":
        trend_df = load_all_lsi_trend()
        line_color = "#fee440"
        bar_color  = "#0ea5e9"
    else:
        trend_df = load_all_lmi_trend()
        line_color = "#fee440"
        bar_color  = "#00d4ff"

    if not trend_df.empty:
        current_lm = lm_num if portal_label == "LSI" else lm_num_lmi
        bar_colors = [bar_color if i+1 != current_lm else "#00f5d4" for i in range(len(trend_df))]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=trend_df["Mailer"], y=trend_df["LM NS"],
            name="LM Net Sales", marker_color=bar_colors, opacity=0.85,
            text=[f"{v:,.0f}" for v in trend_df["LM NS"]],
            textposition="outside", textfont=dict(color="#e2e8f0", size=11, weight="bold"),
            yaxis="y",
        ))
        fig_trend.add_trace(go.Scatter(
            x=trend_df["Mailer"], y=trend_df["LM Cont%"],
            name="LM Cont. %", mode="lines+markers+text",
            line=dict(color=line_color, width=3),
            marker=dict(size=12, color=line_color, line=dict(width=2, color="#1a1a2e")),
            text=[f"{v:.1f}%" for v in trend_df["LM Cont%"]],
            textposition="bottom center",
            textfont=dict(color="#ffffff", size=12, family="Poppins"),
            yaxis="y2",
        ))
        fig_trend.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            height=350, margin=dict(t=60, b=40, l=60, r=60),
            xaxis=dict(title="Periode", gridcolor="#2d3748", tickfont=dict(color="#94a3b8", size=12)),
            yaxis=dict(title=dict(text="LM Net Sales", font=dict(color=bar_color)),
                       tickfont=dict(color=bar_color), gridcolor="#2d3748", side="left"),
            yaxis2=dict(title=dict(text="LM Cont. %", font=dict(color=line_color)),
                        tickfont=dict(color=line_color), overlaying="y", side="right",
                        showgrid=False, range=[0, max(trend_df["LM Cont%"]) * 1.5]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        font=dict(color="#e2e8f0"), bgcolor="rgba(26,32,53,0.8)"),
            barmode="overlay",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        with st.expander("📋 Lihat Detail Data Tren"):
            trend_display = trend_df.copy()
            trend_display["Total NS"]  = trend_display["Total NS"].apply(lambda x: f"{x:,.0f}")
            trend_display["Normal NS"] = trend_display["Normal NS"].apply(lambda x: f"{x:,.0f}")
            trend_display["LM NS"]     = trend_display["LM NS"].apply(lambda x: f"{x:,.0f}")
            trend_display["LM Cont%"]  = trend_display["LM Cont%"].apply(lambda x: f"{x:.2f}%")
            st.dataframe(trend_display, use_container_width=True)

    st.markdown("---")

    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 📊 Net Sales Overview — {period_label}")

    total_ns  = store_total["Total NS"]
    lm_ns     = store_total["LM NS"]
    normal_ns = store_total["Normal NS"]
    lm_cont   = store_total["LM Cont%"]

    if portal_label == "LMI":
        trader_ns  = store_df["Trader NS"].sum()
        regular_ns = store_df["Regular NS"].sum()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(metric_card("Total Net Sales", fmt_rp(total_ns*1000)), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("LM (Promo) Sales", fmt_rp(lm_ns*1000), "green",
                                    f"Kontribusi: {lm_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Normal (Non-Promo)", fmt_rp(normal_ns*1000), "orange",
                                    f"Kontribusi: {100-lm_cont:.2f}%"), unsafe_allow_html=True)
        with c4:
            trader_cont = (trader_ns/total_ns*100) if total_ns else 0
            st.markdown(metric_card("Trader Sales", fmt_rp(trader_ns*1000), "purple",
                                    f"Kontribusi: {trader_cont:.3f}%"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-title">Komposisi LM vs Normal</div>', unsafe_allow_html=True)
            fig1 = go.Figure(go.Pie(
                labels=["LM (Promo)","Normal"], values=[lm_ns, normal_ns],
                hole=0.55, marker_colors=["#00d4ff","#2d3a5a"],
                textinfo="label+percent", textfont=dict(size=12, color="#ffffff"),
            ))
            fig1.update_layout(**{**PD, "showlegend":False, "height":280,
                "margin":dict(t=10,b=10,l=10,r=10),
                "annotations":[dict(text=f"<b>{lm_cont:.1f}%</b><br>LM",
                    x=0.5, y=0.5, font=dict(size=16, color="#00d4ff"), showarrow=False)]})
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">Komposisi Regular vs Trader</div>', unsafe_allow_html=True)
            regular_cont_pct = regular_ns / total_ns * 100 if total_ns else 0
            trader_cont_pct  = trader_ns  / total_ns * 100 if total_ns else 0
            fig2 = go.Figure(go.Pie(
                labels=["Regular (End User)","Trader"], values=[regular_ns, trader_ns],
                hole=0.55, marker_colors=["#00f5d4","#fee440"],
                textinfo="none",
                customdata=[regular_cont_pct, trader_cont_pct],
                hovertemplate="<b>%{label}</b><br>Net Sales: %{value:,.3f}<br>Kontribusi: %{customdata:.6f}%<extra></extra>",
            ))
            fig2.update_layout(**{**PD,
                "showlegend":True,
                "legend":dict(orientation="h", y=-0.12, x=0.5, xanchor="center", font=dict(color="#e2e8f0")),
                "margin":dict(t=10,b=50,l=10,r=10), "height":300,
                "annotations":[
                    dict(text=f"<b>{regular_cont_pct:.4f}%</b><br>Regular",
                         x=0.5, y=0.58, font=dict(size=14, color="#00f5d4"), showarrow=False),
                    dict(text=f"Trader: {trader_cont_pct:.6f}%",
                         x=0.5, y=0.32, font=dict(size=10, color="#718096"), showarrow=False),
                ]})
            st.plotly_chart(fig2, use_container_width=True)

    else:  # LSI
        sku_total    = store_total["SKU Total"]
        sku_sale     = store_total["SKU Sale"]
        oos          = store_total["OOS"]
        # ── Gunakan SKU Cont% Calc (formula baru) ──
        sku_cont_new = store_total["SKU Cont% Calc"]

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
            st.markdown(metric_card("Total SKU Promo", f"{int(sku_total):,}", "purple",
                                    f"Terjual: {int(sku_sale):,} SKU"), unsafe_allow_html=True)
        with c5:
            st.markdown(metric_card("SKU Sell-Through", f"{sku_cont_new:.1f}%", "teal",
                                    "% SKU terjual / total"), unsafe_allow_html=True)
        with c6:
            oos_rate = (oos / sku_total * 100) if sku_total else 0
            st.markdown(metric_card("OOS", f"{int(oos):,} SKU", "red",
                                    f"OOS Rate: {oos_rate:.1f}%"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-title">Komposisi LM vs Normal</div>', unsafe_allow_html=True)
            fig1 = go.Figure(go.Pie(
                labels=["LM (Promo)","Normal"], values=[lm_ns, normal_ns],
                hole=0.55, marker_colors=["#9b5de5","#2d3a5a"],
                textinfo="label+percent", textfont=dict(size=12, color="#ffffff"),
            ))
            fig1.update_layout(**{**PD, "showlegend":False, "height":280,
                "margin":dict(t=10,b=10,l=10,r=10),
                "annotations":[dict(text=f"<b>{lm_cont:.2f}%</b><br>LM",
                    x=0.5, y=0.5, font=dict(size=16, color="#9b5de5"), showarrow=False)]})
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">SKU Promo: Terjual vs OOS vs Belum Terjual</div>', unsafe_allow_html=True)
            oos_val    = int(oos)
            sold_val   = max(0, int(sku_sale) - oos_val)   # SKU Terjual murni (excl OOS)
            unsold_val = max(0, int(sku_total) - int(sku_sale))  # Belum Terjual
            fig_sku = go.Figure(go.Pie(
                labels=["Terjual","OOS","Belum Terjual"],
                values=[sold_val, oos_val, unsold_val],
                hole=0.55, marker_colors=["#00f5d4","#ff6b6b","#2d3a5a"],
                textinfo="label+percent", textfont=dict(size=11, color="#ffffff"),
            ))
            fig_sku.update_layout(**{**PD, "showlegend":False, "height":280,
                "margin":dict(t=10,b=10,l=10,r=10),
                "annotations":[dict(
                    # Tampilkan % baru (SKU Sale + OOS) / SKU Total
                    text=f"<b>{sku_cont_new:.1f}%</b><br>Sell-Through",
                    x=0.5, y=0.5, font=dict(size=14, color="#00f5d4"), showarrow=False)]})
            st.plotly_chart(fig_sku, use_container_width=True)

        st.markdown('<div class="section-title">Breakdown Net Sales LM: Trader vs Prof vs Others</div>', unsafe_allow_html=True)
        lm_trader = store_df["LM Trader NS"].sum()
        lm_prof   = store_df["LM Prof NS"].sum()
        lm_others = store_df["LM Others NS"].sum()
        fig_lm = go.Figure(go.Bar(
            x=["Trader","Professional","Others"],
            y=[lm_trader, lm_prof, lm_others],
            marker_color=["#fee440","#00d4ff","#9b5de5"],
            text=[f"{v/lm_ns*100:.1f}%" if lm_ns else "0%" for v in [lm_trader, lm_prof, lm_others]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig_lm.update_layout(**{**PD, "height":300,
            "margin":dict(t=30,b=10,l=10,r=10),
            "yaxis_title":"Net Sales LM"})
        st.plotly_chart(fig_lm, use_container_width=True)

    # ── Group contribution bar ──
    st.markdown('<div class="section-title">Kontribusi LM per Grup Kategori</div>', unsafe_allow_html=True)
    grp_data = cat_df.groupby("Group").agg(Total_NS=("Total NS","sum"), LM_NS=("LM NS","sum")).reset_index()
    grp_data["LM_Cont"] = grp_data["LM_NS"] / grp_data["Total_NS"] * 100
    grp_data = grp_data.sort_values("LM_Cont", ascending=False)
    bar_color_main = "#9b5de5" if portal_label == "LSI" else "#00d4ff"
    bar_color_dim  = "#5b3785" if portal_label == "LSI" else "#0a5f75"
    colors = [bar_color_main if v >= 20 else bar_color_dim for v in grp_data["LM_Cont"]]
    fig3 = go.Figure(go.Bar(
        x=grp_data["Group"], y=grp_data["LM_Cont"],
        marker_color=colors,
        text=[f"{v:.1f}%" for v in grp_data["LM_Cont"]],
        textposition="outside", textfont=dict(color="#e2e8f0"),
    ))
    fig3.add_hline(y=lm_cont, line_dash="dash", line_color="#fee440",
                   annotation_text=f"Avg: {lm_cont:.2f}%",
                   annotation_font=dict(color="#fee440"),
                   annotation_position="top right")
    fig3.update_layout(**{**PD, "height":320,
        "margin":dict(t=30,b=20,l=10,r=10),
        "yaxis_title":"LM Contribution (%)",
        "yaxis_range":[0, grp_data["LM_Cont"].max()*1.2]})
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 – BY STORE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏪 By Store":
    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 🏪 Analisis Net Sales per Store — {period_label}")

    filtered = store_df[store_df["LM Cont%"] >= lm_thresh].copy()

    if portal_label == "LSI":
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(metric_card("Total Store", str(len(filtered))), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Avg LM Cont%", f"{filtered['LM Cont%'].mean():.2f}%", "green"), unsafe_allow_html=True)
        with c3:
            top = filtered.loc[filtered["Total NS"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest Revenue Store", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            # ── Gunakan SKU Cont% Calc (formula baru) ──
            avg_sku_cont = filtered["SKU Cont% Calc"].mean()
            st.markdown(metric_card("Avg SKU Sell-Through", f"{avg_sku_cont:.1f}%", "teal",
                                    "(SKU Terjual+OOS)/SKU Total"), unsafe_allow_html=True)
        with c5:
            st.markdown(metric_card("Total OOS SKU", f"{int(filtered['OOS'].sum()):,}", "red"), unsafe_allow_html=True)
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(metric_card("Total Store Aktif", str(len(filtered))), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Avg LM Contribution", f"{filtered['LM Cont%'].mean():.2f}%", "green"), unsafe_allow_html=True)
        with c3:
            top = filtered.loc[filtered["Total NS"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest Revenue Store", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            top_lm = filtered.loc[filtered["LM Cont%"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest LM Cont% Store", str(top_lm), "purple"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    bar_color = "#9b5de5" if portal_label == "LSI" else "#00d4ff"
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-title">Total Net Sales per Store (LM vs Normal)</div>', unsafe_allow_html=True)
        sorted_store = filtered.sort_values("Total NS", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=sorted_store["Store Name"], x=sorted_store["Normal NS"],
            name="Normal", orientation="h", marker_color="#2d3a5a",
            text=[f"{v:,.0f}" for v in sorted_store["Normal NS"]],
            textposition="inside", textfont=dict(color="#94a3b8"),
        ))
        fig.add_trace(go.Bar(
            y=sorted_store["Store Name"], x=sorted_store["LM NS"],
            name="LM (Promo)", orientation="h", marker_color=bar_color,
            text=[f"{v:,.0f}" for v in sorted_store["LM NS"]],
            textposition="inside", textfont=dict(color="#ffffff"),
        ))
        fig.update_layout(**{**PD, "barmode":"stack",
            "height":max(420, len(filtered)*28),
            "margin":dict(t=20,b=20,l=10,r=20),
            "xaxis_title":"Net Sales"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">LM Contribution % per Store</div>', unsafe_allow_html=True)
        sorted_lm = filtered.sort_values("LM Cont%", ascending=True)
        thresh_low = 5 if portal_label == "LSI" else 10
        thresh_mid = 10 if portal_label == "LSI" else 20
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
            "margin":dict(t=20,b=20,l=10,r=40),
            "xaxis_title":"LM Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True)

    # ── SKU Section (LSI only) ──
    if portal_label == "LSI":
        st.markdown("---")
        st.markdown("### 📦 SKU Performance per Store")

        st.markdown('<div class="section-title">SKU Terjual / OOS / Belum Terjual per Store</div>', unsafe_allow_html=True)

        sku_store = filtered[filtered["SKU Total"] > 0].copy()
        # SKU Sale sudah include OOS, pisahkan:
        # SKU Terjual murni = SKU Sale - OOS
        # OOS = OOS
        # Belum Terjual = SKU Total - SKU Sale
        sku_store["SKU Sold"]   = (sku_store["SKU Sale"] - sku_store["OOS"]).clip(lower=0)
        sku_store["SKU Unsold"] = (sku_store["SKU Total"] - sku_store["SKU Sale"]).clip(lower=0)
        sku_store = sku_store.sort_values("SKU Total", ascending=True)

        fig_sku_combined = go.Figure()
        fig_sku_combined.add_trace(go.Bar(
            y=sku_store["Store Name"], x=sku_store["SKU Sold"],
            name="SKU Terjual", orientation="h", marker_color="#00f5d4",
            text=[f"{int(v)}" for v in sku_store["SKU Sold"]],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10),
            hovertemplate="<b>%{y}</b><br>SKU Terjual: %{x:,.0f}<extra></extra>",
        ))
        fig_sku_combined.add_trace(go.Bar(
            y=sku_store["Store Name"], x=sku_store["OOS"],
            name="OOS", orientation="h", marker_color="#ff6b6b",
            text=[f"{int(v)}" if v > 0 else "" for v in sku_store["OOS"]],
            textposition="inside", textfont=dict(color="#ffffff", size=10),
            hovertemplate="<b>%{y}</b><br>OOS: %{x:,.0f}<extra></extra>",
        ))
        fig_sku_combined.add_trace(go.Bar(
            y=sku_store["Store Name"], x=sku_store["SKU Unsold"],
            name="Belum Terjual", orientation="h", marker_color="#9b5de5",
            text=[f"{int(v)}" if v > 5 else "" for v in sku_store["SKU Unsold"]],
            textposition="inside", textfont=dict(color="#ffffff", size=10),
            hovertemplate="<b>%{y}</b><br>Belum Terjual: %{x:,.0f}<extra></extra>",
        ))

        # ── Annotation pakai SKU Cont% Calc ──
        for _, row in sku_store.iterrows():
            fig_sku_combined.add_annotation(
                x=row["SKU Total"] + (sku_store["SKU Total"].max() * 0.02),
                y=row["Store Name"],
                text=f"{row['SKU Cont% Calc']:.1f}%",
                showarrow=False,
                font=dict(color="#00f5d4", size=10),
                xanchor="left",
            )

        fig_sku_combined.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            barmode="stack",
            height=max(500, len(sku_store)*26),
            margin=dict(t=30, b=20, l=10, r=80),
            xaxis_title="Jumlah SKU",
            xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8"),
                       range=[0, sku_store["SKU Total"].max() * 1.15]),
            yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        font=dict(color="#e2e8f0")),
        )
        st.plotly_chart(fig_sku_combined, use_container_width=True)

        # ── Scatter: pakai SKU Cont% Calc ──
        st.markdown('<div class="section-title">Posisi Store: SKU Sell-Through vs OOS (ukuran = Total NS)</div>', unsafe_allow_html=True)
        fig_sc2 = px.scatter(filtered, x="OOS", y="SKU Cont% Calc",
            text="Store Name", size="Total NS", color="LM Cont%",
            color_continuous_scale="Purples",
            hover_data={"SKU Total":True,"SKU Sale":True,"LM NS":":,.0f"},
            labels={"SKU Cont% Calc": "SKU Sell-Through % (Terjual+OOS)/Total"})
        fig_sc2.update_traces(textposition="top center", textfont_size=9)
        fig_sc2.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            height=420, margin=dict(t=30, b=20, l=10, r=10),
            xaxis_title="Jumlah OOS",
            yaxis_title="SKU Sell-Through % (Terjual+OOS)/Total",
            xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_sc2, use_container_width=True)

        st.markdown('<div class="section-title">Breakdown LM Sales: Trader / Prof / Others per Store</div>', unsafe_allow_html=True)
        sorted_br = filtered.sort_values("LM NS", ascending=True)
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Trader NS"],
            name="Trader", orientation="h", marker_color="#fee440"))
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Prof NS"],
            name="Professional", orientation="h", marker_color="#00d4ff"))
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Others NS"],
            name="Others", orientation="h", marker_color="#9b5de5"))
        fig_br.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            barmode="stack",
            height=max(420, len(filtered)*22),
            margin=dict(t=30, b=20, l=10, r=10),
            xaxis_title="Net Sales LM",
            xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            legend=dict(bgcolor="rgba(26,32,53,0.8)", bordercolor="#2d3748", borderwidth=1,
                        font=dict(color="#e2e8f0")),
        )
        st.plotly_chart(fig_br, use_container_width=True)

    # ── Scatter NS vs LM% ──
    st.markdown('<div class="section-title">Posisi Store: Total NS vs LM Contribution%</div>', unsafe_allow_html=True)
    sc_color = "Purples" if portal_label == "LSI" else "Blues"
    fig3 = px.scatter(filtered, x="Total NS", y="LM Cont%",
        text="Store Name", size="Total NS", color="LM Cont%",
        color_continuous_scale=sc_color,
        hover_data={"LM NS":":,.0f","Normal NS":":,.0f","Total NS":":,.0f"})
    fig3.update_traces(textposition="top center", textfont_size=10)
    fig3.add_hline(y=filtered["LM Cont%"].mean(), line_dash="dot", line_color="#718096")
    fig3.add_vline(x=filtered["Total NS"].mean(), line_dash="dot", line_color="#718096")
    fig3.update_layout(**{**PD, "height":400,
        "xaxis_title":"Total Net Sales", "yaxis_title":"LM Contribution (%)",
        "coloraxis_showscale":False})
    st.plotly_chart(fig3, use_container_width=True)

    # ── Data Table ──
    st.markdown('<div class="section-title">📋 Detail Data per Store</div>', unsafe_allow_html=True)
    if portal_label == "LSI":
        disp = ["Store Name","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","OOS","SKU Cont% Calc"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "OOS":"{:,.0f}","SKU Cont% Calc":"{:.2f}%"}
    else:
        disp = ["Store Name","Total NS","LM NS","Normal NS","LM Cont%",
                "Regular NS","Regular Cont%","Trader NS","Trader Cont%"]
        fmt  = {"Total NS":"{:,.1f}","LM NS":"{:,.1f}","Normal NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","Regular NS":"{:,.1f}",
                "Regular Cont%":"{:.2f}%","Trader NS":"{:,.3f}","Trader Cont%":"{:.4f}%"}
    st.dataframe(filtered[disp].style.format(fmt), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 – BY CATEGORY
# ════════════════════════════════════════════════════════════════════════════
elif page == "📦 By Category":
    badge_cls = "badge-lsi" if portal_label == "LSI" else "badge-lmi"
    st.markdown(f'<span class="portal-badge {badge_cls}">{portal_label}</span>', unsafe_allow_html=True)
    st.markdown(f"## 📦 Analisis Net Sales per Kategori — {period_label}")

    cat_filtered = cat_df[cat_df["LM Cont%"] >= lm_thresh].copy()
    groups_available = sorted(cat_filtered["Group"].unique().tolist())
    selected_groups = st.multiselect("Filter Grup Kategori:", groups_available, default=groups_available)
    cat_filtered = cat_filtered[cat_filtered["Group"].isin(selected_groups)]

    total_cat_ns = cat_filtered["Total NS"].sum()
    total_lm_ns  = cat_filtered["LM NS"].sum()
    lm_pct = total_lm_ns / total_cat_ns * 100 if total_cat_ns else 0

    if portal_label == "LSI":
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(metric_card("Total Kategori", str(len(cat_filtered))), unsafe_allow_html=True)
        with c2: st.markdown(metric_card("Total Net Sales", fmt_rp(total_cat_ns*1000), "blue"), unsafe_allow_html=True)
        with c3: st.markdown(metric_card("LM Net Sales", fmt_rp(total_lm_ns*1000), "green", f"{lm_pct:.2f}%"), unsafe_allow_html=True)
        with c4:
            total_sku = cat_filtered["SKU Total"].sum()
            sale_sku  = cat_filtered["SKU Sale"].sum()
            oos_sku   = cat_filtered["OOS"].sum()
            # Formula: SKU Sale / SKU Total (OOS sudah termasuk dalam SKU Sale)
            pct_sku_new = sale_sku / total_sku * 100 if total_sku else 0
            st.markdown(metric_card("SKU Sell-Through", f"{pct_sku_new:.1f}%", "teal",
                                    f"{int(sale_sku):,} / {int(total_sku):,} SKU"), unsafe_allow_html=True)
        with c5:
            st.markdown(metric_card("Total OOS", f"{int(cat_filtered['OOS'].sum()):,} SKU", "red"), unsafe_allow_html=True)
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(metric_card("Total Kategori", str(len(cat_filtered))), unsafe_allow_html=True)
        with c2: st.markdown(metric_card("Total Net Sales", fmt_rp(total_cat_ns*1000), "blue"), unsafe_allow_html=True)
        with c3: st.markdown(metric_card("LM Net Sales", fmt_rp(total_lm_ns*1000), "green", f"{lm_pct:.2f}%"), unsafe_allow_html=True)
        with c4:
            top_cat = cat_filtered.loc[cat_filtered["LM Cont%"].idxmax(), "Category"] if len(cat_filtered) else "–"
            st.markdown(metric_card("Top LM Category", str(top_cat), "orange"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Treemap ──
    st.markdown('<div class="section-title">Treemap: Net Sales per Kategori</div>', unsafe_allow_html=True)
    treemap_df = cat_filtered[cat_filtered["Total NS"] > 0].copy()
    cs = "Purples" if portal_label == "LSI" else "Blues"
    fig_tree = px.treemap(treemap_df, path=["Group","Category"], values="Total NS",
        color="LM Cont%", color_continuous_scale=cs,
        hover_data={"LM NS":":,.0f","LM Cont%":":.2f"})
    fig_tree.update_layout(**{**PD, "height":420, "margin":dict(t=20,b=10,l=10,r=10)})
    fig_tree.update_coloraxes(colorbar_title="LM Cont%")
    st.plotly_chart(fig_tree, use_container_width=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="section-title">LM Contribution% vs Total NS per Kategori</div>', unsafe_allow_html=True)
        fig_bub = px.scatter(cat_filtered[cat_filtered["Total NS"]>1],
            x="Total NS", y="LM Cont%", size="Total NS", color="Group",
            text="Category", hover_data={"LM NS":":,.0f","Normal NS":":,.0f"})
        fig_bub.update_traces(textposition="top center", textfont_size=9)
        fig_bub.add_hline(y=lm_pct, line_dash="dot", line_color="#718096",
                          annotation_text=f"Avg {lm_pct:.1f}%",
                          annotation_font=dict(color="#718096"))
        fig_bub.update_layout(**{**PD, "height":420,
            "xaxis_title":"Total Net Sales", "yaxis_title":"LM Contribution (%)",
            "legend":dict(orientation="h", y=-0.2, font=dict(color="#e2e8f0"))})
        st.plotly_chart(fig_bub, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Top 10 Kategori by LM NS</div>', unsafe_allow_html=True)
        top10 = cat_filtered.nlargest(10,"LM NS").sort_values("LM NS")
        bar_color = "#9b5de5" if portal_label == "LSI" else "#00d4ff"
        fig_h = go.Figure(go.Bar(y=top10["Category"], x=top10["LM NS"],
            orientation="h", marker_color=bar_color,
            text=[f"{v:,.0f}" for v in top10["LM NS"]],
            textposition="outside", textfont=dict(color="#e2e8f0")))
        fig_h.update_layout(**{**PD, "height":420,
            "margin":dict(t=20,b=20,l=10,r=70),
            "xaxis_title":"LM Net Sales"})
        st.plotly_chart(fig_h, use_container_width=True)

    # ── SKU by Category (LSI only) ──
    if portal_label == "LSI":
        st.markdown("---")
        st.markdown("### 📦 SKU Performance per Kategori")

        st.markdown('<div class="section-title">SKU Terjual / OOS / Belum Terjual per Kategori</div>', unsafe_allow_html=True)

        sku_cat = cat_filtered[cat_filtered["SKU Total"] > 0].copy()
        # SKU Sale sudah include OOS, pisahkan:
        # SKU Terjual murni = SKU Sale - OOS
        # OOS = OOS
        # Belum Terjual = SKU Total - SKU Sale
        sku_cat["SKU Sold"]   = (sku_cat["SKU Sale"] - sku_cat["OOS"]).clip(lower=0)
        sku_cat["SKU Unsold"] = (sku_cat["SKU Total"] - sku_cat["SKU Sale"]).clip(lower=0)
        sku_cat = sku_cat.sort_values("SKU Total", ascending=True)

        fig_sku_combined = go.Figure()
        fig_sku_combined.add_trace(go.Bar(
            y=sku_cat["Category"], x=sku_cat["SKU Sold"],
            name="SKU Terjual", orientation="h", marker_color="#00f5d4",
            text=[f"{int(v)}" for v in sku_cat["SKU Sold"]],
            textposition="inside", textfont=dict(color="#1a1a2e", size=9),
            hovertemplate="<b>%{y}</b><br>SKU Terjual: %{x:,.0f}<extra></extra>",
        ))
        fig_sku_combined.add_trace(go.Bar(
            y=sku_cat["Category"], x=sku_cat["OOS"],
            name="OOS", orientation="h", marker_color="#ff6b6b",
            text=[f"{int(v)}" for v in sku_cat["OOS"]],
            textposition="inside", textfont=dict(color="#ffffff", size=9),
            hovertemplate="<b>%{y}</b><br>OOS: %{x:,.0f}<extra></extra>",
        ))
        fig_sku_combined.add_trace(go.Bar(
            y=sku_cat["Category"], x=sku_cat["SKU Unsold"],
            name="Belum Terjual", orientation="h", marker_color="#9b5de5",
            text=[f"{int(v)}" if v > 0 else "" for v in sku_cat["SKU Unsold"]],
            textposition="inside", textfont=dict(color="#ffffff", size=9),
            hovertemplate="<b>%{y}</b><br>Belum Terjual: %{x:,.0f}<extra></extra>",
        ))

        # ── Annotation pakai SKU Cont% Calc ──
        for _, row in sku_cat.iterrows():
            fig_sku_combined.add_annotation(
                x=row["SKU Total"] + (sku_cat["SKU Total"].max() * 0.02),
                y=row["Category"],
                text=f"{row['SKU Cont% Calc']:.1f}%",
                showarrow=False,
                font=dict(color="#00f5d4", size=10),
                xanchor="left",
            )

        fig_sku_combined.update_layout(
            plot_bgcolor="#1a2035", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Poppins, sans-serif"),
            hoverlabel=dict(bgcolor="#1e2a4a", bordercolor="#00d4ff", font=dict(color="#f1f5f9")),
            barmode="stack",
            height=max(500, len(sku_cat)*26),
            margin=dict(t=30, b=20, l=10, r=80),
            xaxis_title="Jumlah SKU",
            xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8"),
                       range=[0, sku_cat["SKU Total"].max() * 1.15]),
            yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", tickfont=dict(color="#94a3b8")),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        font=dict(color="#e2e8f0")),
        )
        st.plotly_chart(fig_sku_combined, use_container_width=True)

        # ── Scatter pakai SKU Cont% Calc ──
        st.markdown('<div class="section-title">SKU Total vs Terjual per Kategori (ukuran = OOS, warna = Sell-Through%)</div>', unsafe_allow_html=True)
        sku_sc_df = cat_filtered[cat_filtered["SKU Total"] > 0].copy()
        fig_sku_sc = px.scatter(sku_sc_df, x="SKU Total", y="SKU Sale",
            size="OOS", color="SKU Cont% Calc", text="Category",
            color_continuous_scale="RdYlGn",
            hover_data={"OOS":True,"LM Cont%":":.2f"},
            labels={"SKU Cont% Calc": "Sell-Through % (Terjual+OOS)/Total"})
        fig_sku_sc.update_traces(textposition="top center", textfont_size=9)
        max_val = sku_sc_df["SKU Total"].max()
        fig_sku_sc.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val],
            mode="lines", line=dict(dash="dot", color="#718096"),
            name="100% Sell-Through", showlegend=True))
        fig_sku_sc.update_layout(**{**PD, "height":420,
            "xaxis_title":"SKU Total", "yaxis_title":"SKU Terjual",
            "coloraxis_colorbar_title":"Sell-Through%"})
        st.plotly_chart(fig_sku_sc, use_container_width=True)

    # ── Group summary ──
    st.markdown('<div class="section-title">LM vs Normal per Grup Kategori</div>', unsafe_allow_html=True)
    grp_sum = cat_filtered.groupby("Group")[["LM NS","Normal NS","Total NS"]].sum().reset_index()
    grp_sum = grp_sum.sort_values("Total NS", ascending=False)
    fig_grp = go.Figure()
    fig_grp.add_trace(go.Bar(name="LM (Promo)", x=grp_sum["Group"], y=grp_sum["LM NS"],
        marker_color="#9b5de5" if portal_label=="LSI" else "#00d4ff",
        text=[f"{v/t*100:.1f}%" for v,t in zip(grp_sum["LM NS"],grp_sum["Total NS"])],
        textposition="outside", textfont=dict(color="#e2e8f0")))
    fig_grp.add_trace(go.Bar(name="Normal", x=grp_sum["Group"], y=grp_sum["Normal NS"],
        marker_color="#2d3a5a"))
    fig_grp.update_layout(**{**PD, "barmode":"group", "height":340,
        "yaxis_title":"Net Sales"})
    st.plotly_chart(fig_grp, use_container_width=True)

    # ── Data Table ──
    st.markdown('<div class="section-title">📋 Detail Data per Kategori</div>', unsafe_allow_html=True)
    if portal_label == "LSI":
        disp = ["Group","Category","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","OOS","SKU Cont% Calc"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "OOS":"{:,.0f}","SKU Cont% Calc":"{:.2f}%"}
    else:
        disp = ["Group","Category","Total NS","LM NS","Normal NS","LM Cont%",
                "Regular NS","Regular Cont%","Trader NS","Trader Cont%"]
        fmt  = {"Total NS":"{:,.1f}","LM NS":"{:,.1f}","Normal NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","Regular NS":"{:,.1f}",
                "Regular Cont%":"{:.2f}%","Trader NS":"{:,.3f}","Trader Cont%":"{:.4f}%"}
    st.dataframe(
        cat_filtered[disp].sort_values(["Group","LM Cont%"], ascending=[True,False])
        .style.format(fmt),
        use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(f"📊 Dashboard {portal_label} · {period_label} | Data: Net Sales")
