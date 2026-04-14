"""
Mailer Dashboard
Dashboard untuk analisis Net Sales promo Leaflet Mailer (LMI & LSI).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.dashboard_core import (
    apply_custom_css, fmt_rp, metric_card, section_title, portal_badge,
    discover_files, get_division_config, get_bar_accent, parse_filename_dates,
    build_trend_chart, build_pie_chart, build_division_chart,
    load_mailer_lmi, load_mailer_lsi,
    STORE_REGION_MAP, PLOTLY_DARK_THEME, render_footer,
    DIVISION_MAP_LMI, DIVISION_MAP_LSI
)

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mailer Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 Mailer Dashboard")
    st.markdown("**Filter & Navigasi**")
    st.markdown("---")
    
    # Portal selection
    portal = st.radio("🏬 Portal", ["LMI", "LSI"])
    
    st.markdown("---")
    
    # Discover available files
    files = discover_files("Mailer", portal)
    
    if not files:
        st.warning(f"⚠️ Tidak ada file data untuk Mailer {portal}")
        st.info(f"Tambahkan file ke: `data/Mailer/{portal}/`")
        st.stop()
    
    # Period selection
    period_options = {f["period_label"]: f for f in files}
    selected_period = st.selectbox("📅 Pilih Periode", list(period_options.keys()))
    selected_file = period_options[selected_period]
    
    # Load data based on portal
    if portal == "LMI":
        store_df, store_total, cat_df, period_label = load_mailer_lmi(str(selected_file["path"]))
        DIVISION_MAP = DIVISION_MAP_LMI
    else:
        store_df, store_total, cat_df, period_label = load_mailer_lsi(str(selected_file["path"]))
        DIVISION_MAP = DIVISION_MAP_LSI
    
    # Get division config
    div_map, div_order, div_colors, div_card_colors, group_id_map = get_division_config(portal)
    bar_accent = get_bar_accent(portal)
    
    # Assign Division column
    cat_df = cat_df.copy()
    cat_df["Division"] = cat_df["Group"].map(div_map).fillna("Other")
    
    st.markdown("---")
    page = st.radio("📌 View", ["🏠 Overview", "🏪 By Store", "📦 By Category"])
    
    st.markdown("---")
    lm_thresh = st.slider("Min LM Contribution (%)", 0.0, 60.0, 0.0, 0.5)
    
    st.markdown("---")
    if st.button("🏠 Kembali ke Home"):
        st.switch_page("Home.py")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    
    # ── Trend Chart ──────────────────────────────────────────────────────────
    section_title("📈 Tren LM Net Sales & Contribution Seluruh Periode")
    
    # Build trend data from all files
    trend_data = []
    for i, f in enumerate(files):
        try:
            if portal == "LMI":
                _, st_tot, _, _ = load_mailer_lmi(str(f["path"]))
            else:
                _, st_tot, _, _ = load_mailer_lsi(str(f["path"]))
            trend_data.append({
                "Period Label": f["period_label"],
                "Total NS": st_tot["Total NS"],
                "Normal NS": st_tot["Normal NS"],
                "LM NS": st_tot["LM NS"],
                "LM Cont%": st_tot["LM Cont%"],
            })
        except Exception:
            continue
    
    if trend_data:
        trend_df = pd.DataFrame(trend_data[::-1])  # Reverse for chronological order
        current_idx = len(trend_df) - 1 - files.index(selected_file)
        
        fig_trend = build_trend_chart(trend_df, current_idx, bar_accent)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        with st.expander("📋 Lihat Detail Data Tren"):
            td = trend_df.copy()
            td["Total NS"] = td["Total NS"].apply(lambda x: f"{x:,.0f}")
            td["Normal NS"] = td["Normal NS"].apply(lambda x: f"{x:,.0f}")
            td["LM NS"] = td["LM NS"].apply(lambda x: f"{x:,.0f}")
            td["LM Cont%"] = td["LM Cont%"].apply(lambda x: f"{x:.2f}%")
            st.dataframe(td, use_container_width=True)
    
    st.markdown("---")
    
    # ── Badge & Title ─────────────────────────────────────────────────────────
    st.markdown(portal_badge(portal), unsafe_allow_html=True)
    st.markdown(f"## 📊 Net Sales Overview · {period_label}")
    
    # ── Division Filter ───────────────────────────────────────────────────────
    section_title("🏷️ Filter Division")
    available_divisions = [d for d in div_order if d in cat_df["Division"].unique()]
    selected_divisions = st.multiselect(
        "Pilih Division:", options=available_divisions, default=[],
        key="overview_division_filter", placeholder="Semua Division"
    )
    cat_div_filtered = cat_df[cat_df["Division"].isin(selected_divisions)] if selected_divisions else cat_df
    
    # ── Compute scorecard values ──────────────────────────────────────────────
    all_divs_selected = set(selected_divisions) == set(available_divisions)
    
    if all_divs_selected or not selected_divisions:
        total_ns = store_total["Total NS"]
        lm_ns = store_total["LM NS"]
        normal_ns = store_total["Normal NS"]
        lm_cont = store_total["LM Cont%"]
        sku_total_val = store_total["SKU Total"]
        sku_sale_val = store_total["SKU Sale"]
        sku_cont_val = store_total["SKU Cont%"]
        oos_val_total = store_total["OOS"]
        if portal == "LMI":
            trader_ns = store_df["Trader NS"].sum()
            regular_ns = store_df["Regular NS"].sum()
        else:
            lm_trader = store_df["LM Trader NS"].sum()
            lm_prof = store_df["LM Prof NS"].sum()
            lm_others = store_df["LM Others NS"].sum()
    else:
        total_ns = cat_div_filtered["Total NS"].sum()
        lm_ns = cat_div_filtered["LM NS"].sum()
        normal_ns = cat_div_filtered["Normal NS"].sum()
        lm_cont = (lm_ns / total_ns * 100) if total_ns else 0
        sku_total_val = cat_div_filtered["SKU Total"].sum()
        sku_sale_val = cat_div_filtered["SKU Sale"].sum()
        sku_cont_val = (sku_sale_val / sku_total_val * 100) if sku_total_val else 0
        oos_val_total = cat_div_filtered["OOS"].sum()
        if portal == "LMI":
            trader_ns = cat_div_filtered["Trader NS"].sum()
            regular_ns = cat_div_filtered["Regular NS"].sum()
        else:
            lm_trader = cat_div_filtered["LM Trader NS"].sum()
            lm_prof = cat_div_filtered["LM Prof NS"].sum()
            lm_others = cat_div_filtered["LM Others NS"].sum()
    
    # ── Scorecards ───────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Net Sales", fmt_rp(total_ns)), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("LM (Promo) Sales", fmt_rp(lm_ns), "green",
                                f"Kontribusi: {lm_cont:.2f}%"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Normal (Non-Promo)", fmt_rp(normal_ns), "orange",
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
        section_title("Komposisi LM vs Normal")
        fig1 = build_pie_chart(
            ["LM (Promo)", "Normal"], [lm_ns, normal_ns],
            [bar_accent, "#2d3a5a"], f"<b>{lm_cont:.1f}%</b><br>LM", bar_accent
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_b:
        section_title("SKU Promo: Terjual vs OOS vs Belum Terjual")
        oos_pie = int(oos_val_total)
        sold_pie = int(sku_sale_val)
        unsold_pie = max(0, int(sku_total_val) - sold_pie - oos_pie)
        fig_sku = build_pie_chart(
            ["Terjual", "OOS", "Belum Terjual"], [sold_pie, oos_pie, unsold_pie],
            ["#00f5d4", "#ff6b6b", "#2d3a5a"], f"<b>{sku_cont_val:.1f}%</b><br>Sell-Through", "#00f5d4"
        )
        st.plotly_chart(fig_sku, use_container_width=True)
    
    # ── LM Breakdown bar ─────────────────────────────────────────────────────
    if portal == "LSI":
        section_title("Breakdown Net Sales LM: Trader vs Prof vs Others")
        fig_lm = go.Figure(go.Bar(
            x=["Trader", "Professional", "Others"],
            y=[lm_trader, lm_prof, lm_others],
            marker_color=["#fee440", "#00d4ff", "#9b5de5"],
            text=[f"{v/lm_ns*100:.1f}%" if lm_ns else "0%" for v in [lm_trader, lm_prof, lm_others]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
    else:
        section_title("Breakdown Net Sales LM: Regular vs Trader")
        lm_total_breakdown = regular_ns + trader_ns
        fig_lm = go.Figure(go.Bar(
            x=["Regular (End User)", "Trader"],
            y=[regular_ns, trader_ns],
            marker_color=["#00f5d4", "#fee440"],
            text=[f"{v/lm_total_breakdown*100:.1f}%" if lm_total_breakdown else "0%" for v in [regular_ns, trader_ns]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
    fig_lm.update_layout(**{**PLOTLY_DARK_THEME, "height": 300,
        "margin": dict(t=30, b=10, l=10, r=10), "yaxis_title": "Net Sales LM"})
    st.plotly_chart(fig_lm, use_container_width=True)
    
    # ── LM Net Sales per Division ─────────────────────────────────────────────
    section_title("LM Net Sales per Division")
    div_data_src = cat_div_filtered if selected_divisions else cat_df
    div_bar = div_data_src.groupby("Division").agg(
        Total_NS=("Total NS", "sum"), Promo_NS=("LM NS", "sum"),
    ).reset_index()
    div_bar["Promo_Cont%"] = div_bar["Promo_NS"] / div_bar["Total_NS"] * 100
    div_bar = div_bar.sort_values("Promo_NS", ascending=False)
    
    fig_div = build_division_chart(div_bar, bar_accent, div_colors)
    st.plotly_chart(fig_div, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 – BY STORE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏪 By Store":
    st.markdown(portal_badge(portal), unsafe_allow_html=True)
    st.markdown(f"## 🏪 Analisis Net Sales per Store — {period_label}")
    
    filtered = store_df[store_df["LM Cont%"] >= lm_thresh].copy()
    
    # ── Region filter for LSI ─────────────────────────────────────────────────
    if portal == "LSI":
        filtered["Region"] = filtered["Store Name"].map(STORE_REGION_MAP)
        filtered = filtered[filtered["Region"].notna()].copy()
        
        st.markdown("### 📊 Peringkat Toko per Regional")
        available_regions = [r for r in ["Regional 1", "Regional 2", "Regional 3"]
                            if r in filtered["Region"].unique()]
        
        selected_region = st.selectbox(
            "🏢 Pilih Regional:",
            options=["Semua Regional"] + available_regions,
            key="region_filter"
        )
        
        if selected_region != "Semua Regional":
            filtered = filtered[filtered["Region"] == selected_region].copy()
    
    # ── Scorecards ───────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Store Aktif", str(len(filtered))), unsafe_allow_html=True)
    with c2:
        total_lm_ns = filtered["LM NS"].sum()
        avg_lm_cont = filtered["LM Cont%"].mean()
        st.markdown(metric_card("Net Sales LM", fmt_rp(total_lm_ns), "green",
                                f"Avg Cont: {avg_lm_cont:.2f}%"), unsafe_allow_html=True)
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
    
    # ── Net Sales & LM Contribution Charts ────────────────────────────────────
    col1, col2 = st.columns([3, 2])
    sorted_store = filtered.sort_values("LM Cont%", ascending=True)
    
    if portal == "LSI" and "Region" in sorted_store.columns:
        if selected_region == "Semua Regional":
            sorted_store["Display Name"] = sorted_store.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
        else:
            sorted_store["Display Name"] = sorted_store["Store Name"]
    else:
        sorted_store["Display Name"] = sorted_store["Store Name"]
    
    with col1:
        section_title("Total Net Sales per Store (LM vs Normal)")
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
        fig.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
            "height": max(420, len(filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=20), "xaxis_title": "Net Sales"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_title("LM Contribution % per Store")
        sorted_lm = sorted_store.copy()
        thresh_low = 5 if portal == "LSI" else 10
        thresh_mid = 10 if portal == "LSI" else 20
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
        fig2.update_layout(**{**PLOTLY_DARK_THEME, "height": max(420, len(filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=40), "xaxis_title": "LM Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # ── SKU Performance ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📦 SKU Performance per Store")
    section_title("SKU Terjual / OOS / Belum Terjual per Store")
    
    sku_store = filtered[filtered["SKU Total"] > 0].copy()
    sku_store["SKU Unsold"] = (sku_store["SKU Total"] - sku_store["SKU Sale"] - sku_store["OOS"]).clip(lower=0)
    sku_store["Sale_Pct"] = (sku_store["SKU Sale"] / sku_store["SKU Total"] * 100).round(1)
    sku_store["OOS_Pct"] = (sku_store["OOS"] / sku_store["SKU Total"] * 100).round(1)
    sku_store["Unsold_Pct"] = (sku_store["SKU Unsold"] / sku_store["SKU Total"] * 100).round(1)
    sku_store = sku_store.sort_values("LM Cont%", ascending=True)
    
    if portal == "LSI" and "Region" in sku_store.columns:
        if selected_region == "Semua Regional":
            sku_store["Display Name"] = sku_store.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
        else:
            sku_store["Display Name"] = sku_store["Store Name"]
    else:
        sku_store["Display Name"] = sku_store["Store Name"]
    
    fig_sku_s = go.Figure()
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["SKU Sale"], name="SKU Terjual",
        orientation="h", marker_color="#00f5d4",
        text=[f"{int(v)} ({p:.1f}%)" for v, p in zip(sku_store["SKU Sale"], sku_store["Sale_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["OOS"], name="OOS",
        orientation="h", marker_color="#ff6b6b",
        text=[f"{int(v)} ({p:.1f}%)" if v > 0 else "" for v, p in zip(sku_store["OOS"], sku_store["OOS_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_s.add_trace(go.Bar(
        y=sku_store["Display Name"], x=sku_store["SKU Unsold"], name="Belum Terjual",
        orientation="h", marker_color="#9b5de5",
        text=[f"{int(v)} ({p:.1f}%)" if v > 3 else "" for v, p in zip(sku_store["SKU Unsold"], sku_store["Unsold_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_s.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
        "height": max(500, len(sku_store)*26), "margin": dict(t=30, b=20, l=10, r=20),
        "xaxis_title": "Jumlah SKU",
        "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)})
    st.plotly_chart(fig_sku_s, use_container_width=True)
    
    # ── LM Breakdown per Store ────────────────────────────────────────────────
    st.markdown("---")
    sorted_br = filtered.sort_values("LM Cont%", ascending=True).copy()
    
    if portal == "LSI" and "Region" in sorted_br.columns:
        if selected_region == "Semua Regional":
            sorted_br["Display Name"] = sorted_br.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
        else:
            sorted_br["Display Name"] = sorted_br["Store Name"]
    else:
        sorted_br["Display Name"] = sorted_br["Store Name"]
    
    if portal == "LSI":
        section_title("Breakdown LM Sales: Trader / Prof / Others per Store")
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
        section_title("Breakdown LM Sales: Regular vs Trader per Store")
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
    
    fig_br.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
        "height": max(420, len(filtered)*22), "margin": dict(t=30, b=20, l=10, r=10),
        "xaxis_title": "Net Sales LM"})
    st.plotly_chart(fig_br, use_container_width=True)
    
    # ── Data Table ────────────────────────────────────────────────────────────
    st.markdown("---")
    section_title("📋 Detail Data per Store")
    table_df = filtered.sort_values("LM Cont%", ascending=False).copy()
    
    if portal == "LSI":
        disp = ["Region", "Store Name", "Total NS", "Normal NS", "LM NS", "LM Cont%",
                "LM Trader NS", "LM Prof NS", "LM Others NS",
                "SKU Total", "SKU Sale", "SKU Cont%", "OOS"] if "Region" in table_df.columns else \
               ["Store Name", "Total NS", "Normal NS", "LM NS", "LM Cont%",
                "LM Trader NS", "LM Prof NS", "LM Others NS",
                "SKU Total", "SKU Sale", "SKU Cont%", "OOS"]
        fmt = {"Total NS": "{:,.1f}", "Normal NS": "{:,.1f}", "LM NS": "{:,.1f}",
               "LM Cont%": "{:.2f}%", "LM Trader NS": "{:,.1f}", "LM Prof NS": "{:,.1f}",
               "LM Others NS": "{:,.1f}", "SKU Total": "{:,.0f}", "SKU Sale": "{:,.0f}",
               "SKU Cont%": "{:.2f}%", "OOS": "{:,.0f}"}
    else:
        disp = ["Store Name", "Total NS", "LM NS", "Normal NS", "LM Cont%",
                "Regular NS", "Regular Cont%", "Trader NS", "Trader Cont%",
                "SKU Total", "SKU Sale", "SKU Cont%", "OOS"]
        fmt = {"Total NS": "{:,.1f}", "LM NS": "{:,.1f}", "Normal NS": "{:,.1f}",
               "LM Cont%": "{:.2f}%", "Regular NS": "{:,.1f}", "Regular Cont%": "{:.2f}%",
               "Trader NS": "{:,.1f}", "Trader Cont%": "{:.2f}%",
               "SKU Total": "{:,.0f}", "SKU Sale": "{:,.0f}",
               "SKU Cont%": "{:.2f}%", "OOS": "{:,.0f}"}
    
    st.dataframe(table_df[[c for c in disp if c in table_df.columns]].style.format(
        {k: v for k, v in fmt.items() if k in table_df.columns}), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 – BY CATEGORY
# ════════════════════════════════════════════════════════════════════════════
elif page == "📦 By Category":
    st.markdown(portal_badge(portal), unsafe_allow_html=True)
    st.markdown(f"## 📦 Analisis Net Sales per Kategori — {period_label}")
    
    cat_filtered = cat_df[cat_df["LM Cont%"] >= lm_thresh].copy()
    
    # ── Division filter ───────────────────────────────────────────────────────
    st.markdown("### 📊 Peringkat Kategori per Division")
    available_divisions = [d for d in div_order if d in cat_filtered["Division"].unique()]
    
    selected_division = st.selectbox(
        "🏷️ Pilih Division:",
        options=["Semua Division"] + available_divisions,
        key="division_filter_cat"
    )
    
    if selected_division != "Semua Division":
        cat_filtered = cat_filtered[cat_filtered["Division"] == selected_division].copy()
    
    # ── Calculate metrics ─────────────────────────────────────────────────────
    total_cat_ns = cat_filtered["Total NS"].sum()
    total_lm_ns = cat_filtered["LM NS"].sum()
    lm_pct = total_lm_ns / total_cat_ns * 100 if total_cat_ns else 0
    total_sku_cat = cat_filtered["SKU Total"].sum()
    sale_sku_cat = cat_filtered["SKU Sale"].sum()
    pct_sku_cat = sale_sku_cat / total_sku_cat * 100 if total_sku_cat else 0
    
    # ── Scorecards ───────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(metric_card("Total Kategori Aktif", str(len(cat_filtered))), unsafe_allow_html=True)
    with c2:
        avg_lm_cont = cat_filtered["LM Cont%"].mean() if len(cat_filtered) else 0
        st.markdown(metric_card("Net Sales LM", fmt_rp(total_lm_ns), "green",
                                f"Avg Cont: {avg_lm_cont:.2f}%"), unsafe_allow_html=True)
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
    
    # ── Net Sales & LM Contribution Charts ────────────────────────────────────
    col1, col2 = st.columns([3, 2])
    sorted_cat = cat_filtered.sort_values("LM Cont%", ascending=True)
    
    div_abbrev = {"FRESH FOOD": "FF", "MEAL SOLUTION": "MS", "DRY FOOD": "DF",
                  "H&B HOME CARE": "HB", "ELECTRONIC": "EL", "NON FOOD": "NF", "Other": "OT"}
    
    if selected_division == "Semua Division":
        sorted_cat["Display Name"] = sorted_cat.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1)
    else:
        sorted_cat["Display Name"] = sorted_cat["Category"]
    
    with col1:
        section_title("Total Net Sales per Category (LM vs Normal)")
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
        fig.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
            "height": max(420, len(cat_filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=20), "xaxis_title": "Net Sales"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_title("LM Contribution % per Category")
        sorted_lm = sorted_cat.copy()
        thresh_low = 5 if portal == "LSI" else 10
        thresh_mid = 10 if portal == "LSI" else 20
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
        fig2.update_layout(**{**PLOTLY_DARK_THEME, "height": max(420, len(cat_filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=40), "xaxis_title": "LM Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # ── SKU Performance ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📦 SKU Performance per Category")
    section_title("SKU Terjual / OOS / Belum Terjual per Category")
    
    sku_cat = cat_filtered[cat_filtered["SKU Total"] > 0].copy()
    sku_cat["SKU Unsold"] = (sku_cat["SKU Total"] - sku_cat["SKU Sale"] - sku_cat["OOS"]).clip(lower=0)
    sku_cat["Sale_Pct"] = (sku_cat["SKU Sale"] / sku_cat["SKU Total"] * 100).round(1)
    sku_cat["OOS_Pct"] = (sku_cat["OOS"] / sku_cat["SKU Total"] * 100).round(1)
    sku_cat["Unsold_Pct"] = (sku_cat["SKU Unsold"] / sku_cat["SKU Total"] * 100).round(1)
    sku_cat = sku_cat.sort_values("LM Cont%", ascending=True)
    
    if selected_division == "Semua Division":
        sku_cat["Display Name"] = sku_cat.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1)
    else:
        sku_cat["Display Name"] = sku_cat["Category"]
    
    fig_sku_c = go.Figure()
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["SKU Sale"], name="SKU Terjual",
        orientation="h", marker_color="#00f5d4",
        text=[f"{int(v)} ({p:.1f}%)" for v, p in zip(sku_cat["SKU Sale"], sku_cat["Sale_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["OOS"], name="OOS",
        orientation="h", marker_color="#ff6b6b",
        text=[f"{int(v)} ({p:.1f}%)" if v > 0 else "" for v, p in zip(sku_cat["OOS"], sku_cat["OOS_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_c.add_trace(go.Bar(
        y=sku_cat["Display Name"], x=sku_cat["SKU Unsold"], name="Belum Terjual",
        orientation="h", marker_color="#9b5de5",
        text=[f"{int(v)} ({p:.1f}%)" if v > 3 else "" for v, p in zip(sku_cat["SKU Unsold"], sku_cat["Unsold_Pct"])],
        textposition="inside", textfont=dict(color="#1a1a2e", size=9, weight="bold"),
    ))
    fig_sku_c.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
        "height": max(500, len(sku_cat)*26), "margin": dict(t=30, b=20, l=10, r=20),
        "xaxis_title": "Jumlah SKU",
        "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)})
    st.plotly_chart(fig_sku_c, use_container_width=True)
    
    # ── LM Breakdown per Category ─────────────────────────────────────────────
    st.markdown("---")
    sorted_br = cat_filtered.sort_values("LM Cont%", ascending=True).copy()
    
    if selected_division == "Semua Division":
        sorted_br["Display Name"] = sorted_br.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1)
    else:
        sorted_br["Display Name"] = sorted_br["Category"]
    
    if portal == "LSI":
        section_title("Breakdown LM Sales: Trader / Prof / Others per Category")
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
        section_title("Breakdown LM Sales: Regular vs Trader per Category")
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
    
    fig_br.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
        "height": max(420, len(cat_filtered)*22), "margin": dict(t=30, b=20, l=10, r=10),
        "xaxis_title": "Net Sales LM"})
    st.plotly_chart(fig_br, use_container_width=True)
    
    # ── Data Table ────────────────────────────────────────────────────────────
    st.markdown("---")
    section_title("📋 Detail Data per Category")
    table_df = cat_filtered.sort_values("LM Cont%", ascending=False).copy()
    
    if portal == "LSI":
        disp = ["Division", "Category", "Total NS", "Normal NS", "LM NS", "LM Cont%",
                "LM Trader NS", "LM Prof NS", "LM Others NS",
                "SKU Total", "SKU Sale", "SKU Cont%", "OOS"]
        fmt = {"Total NS": "{:,.1f}", "Normal NS": "{:,.1f}", "LM NS": "{:,.1f}",
               "LM Cont%": "{:.2f}%", "LM Trader NS": "{:,.1f}", "LM Prof NS": "{:,.1f}",
               "LM Others NS": "{:,.1f}", "SKU Total": "{:,.0f}", "SKU Sale": "{:,.0f}",
               "SKU Cont%": "{:.2f}%", "OOS": "{:,.0f}"}
    else:
        disp = ["Division", "Category", "Total NS", "LM NS", "Normal NS", "LM Cont%",
                "Regular NS", "Regular Cont%", "Trader NS", "Trader Cont%",
                "SKU Total", "SKU Sale", "SKU Cont%", "OOS"]
        fmt = {"Total NS": "{:,.1f}", "LM NS": "{:,.1f}", "Normal NS": "{:,.1f}",
               "LM Cont%": "{:.2f}%", "Regular NS": "{:,.1f}", "Regular Cont%": "{:.2f}%",
               "Trader NS": "{:,.1f}", "Trader Cont%": "{:.2f}%",
               "SKU Total": "{:,.0f}", "SKU Sale": "{:,.0f}",
               "SKU Cont%": "{:.2f}%", "OOS": "{:,.0f}"}
    
    st.dataframe(table_df[[c for c in disp if c in table_df.columns]].style.format(
        {k: v for k, v in fmt.items() if k in table_df.columns}), use_container_width=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────
render_footer(portal, period_label)
