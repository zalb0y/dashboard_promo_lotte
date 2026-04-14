"""
Big Banner Dashboard
Dashboard untuk analisis Net Sales promo Big Banner (Hijau, Cokelat, EndUser).
- Hijau & Cokelat (LSI): Breakdown Retailer/Horeca/Others + NOC
- EndUser: Sama struktur dengan Mailer
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.dashboard_core import (
    apply_custom_css, fmt_rp, fmt_number, metric_card, section_title, portal_badge,
    discover_files, get_division_config, get_bar_accent, parse_filename_dates,
    build_trend_chart, build_pie_chart, build_division_chart,
    load_banner_lsi_hijau_cokelat, load_banner_lmi, load_banner_lsi_enduser,
    STORE_REGION_MAP, PLOTLY_DARK_THEME, render_footer,
    DIVISION_MAP_LMI, DIVISION_MAP_LSI
)

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Big Banner Dashboard",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏷️ Big Banner Dashboard")
    st.markdown("**Filter & Navigasi**")
    st.markdown("---")
    
    # Portal (Company) selection
    portal = st.radio("🏬 Portal", ["LSI", "LMI"])
    
    st.markdown("---")
    
    # Banner Type selection (Hijau/Cokelat only available on LSI)
    if portal == "LSI":
        banner_type = st.radio("🎯 Banner Type", ["Hijau", "Cokelat", "EndUser"])
    else:
        banner_type = "EndUser"
        st.info("📍 LMI hanya tersedia untuk **EndUser**")
    
    st.markdown("---")
    
    # Discover available files
    all_files = discover_files("BigBanner", portal)
    
    # Filter by banner type
    files = [f for f in all_files if f["banner_type"] == banner_type]
    
    if not files:
        st.warning(f"⚠️ Tidak ada file data untuk Banner {banner_type} ({portal})")
        st.info(f"Tambahkan file ke: `data/BigBanner/{portal}/`")
        st.info(f"Format: `Banner{banner_type}{portal}_YYYYMMDD_YYYYMMDD.xlsx/xlsb`")
        st.stop()
    
    # Period selection
    period_options = {f["period_label"]: f for f in files}
    selected_period = st.selectbox("📅 Pilih Periode", list(period_options.keys()))
    selected_file = period_options[selected_period]
    
    # Load data based on banner type and portal
    if banner_type in ["Hijau", "Cokelat"]:
        # LSI only - special structure with NOC
        store_df, store_total, cat_df, sku_df, period_label = load_banner_lsi_hijau_cokelat(
            str(selected_file["path"])
        )
        has_noc = True
        has_sku_performance = False  # No SKU Sale/OOS columns
        promo_col = "Banner"  # Column prefix for promo metrics
    else:
        # EndUser - same structure as Mailer
        if portal == "LMI":
            store_df, store_total, cat_df, period_label = load_banner_lmi(str(selected_file["path"]))
        else:
            store_df, store_total, cat_df, period_label = load_banner_lsi_enduser(str(selected_file["path"]))
        has_noc = False
        has_sku_performance = True
        promo_col = "LM"  # Same as Mailer
        sku_df = pd.DataFrame()
    
    # Get division config
    div_map, div_order, div_colors, div_card_colors, group_id_map = get_division_config(portal)
    bar_accent = "#00f5d4" if banner_type == "Hijau" else "#d4a574" if banner_type == "Cokelat" else get_bar_accent(portal)
    
    # Assign Division column
    cat_df = cat_df.copy()
    cat_df["Division"] = cat_df["Group"].map(div_map).fillna("Other")
    
    st.markdown("---")
    
    # View selection
    page = st.radio("📌 View", ["🏠 Overview", "🏪 By Store", "📦 By Category"])
    
    st.markdown("---")
    
    # Threshold slider
    cont_label = f"{promo_col} Contribution (%)"
    banner_thresh = st.slider(f"Min {promo_col} Contribution (%)", 0.0, 60.0, 0.0, 0.5)
    
    st.markdown("---")
    if st.button("🏠 Kembali ke Home"):
        st.switch_page("Home.py")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: Get promo columns based on banner type
# ═══════════════════════════════════════════════════════════════════════════════

def get_promo_ns_col():
    return f"{promo_col} NS"

def get_promo_cont_col():
    return f"{promo_col} Cont%"


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    
    # ── Trend Chart ──────────────────────────────────────────────────────────
    section_title(f"📈 Tren {promo_col} Net Sales & Contribution Seluruh Periode")
    
    # Build trend data from all files of same banner type
    trend_data = []
    for i, f in enumerate(files):
        try:
            if banner_type in ["Hijau", "Cokelat"]:
                _, st_tot, _, _, _ = load_banner_lsi_hijau_cokelat(str(f["path"]))
                trend_data.append({
                    "Period Label": f["period_label"],
                    "Total NS": st_tot["Total NS"],
                    "Normal NS": st_tot["Normal NS"],
                    f"{promo_col} NS": st_tot["Banner NS"],
                    f"{promo_col} Cont%": st_tot["Banner Cont%"],
                    "NOC": st_tot.get("NOC", 0),
                })
            else:
                if portal == "LMI":
                    _, st_tot, _, _ = load_banner_lmi(str(f["path"]))
                else:
                    _, st_tot, _, _ = load_banner_lsi_enduser(str(f["path"]))
                trend_data.append({
                    "Period Label": f["period_label"],
                    "Total NS": st_tot["Total NS"],
                    "Normal NS": st_tot["Normal NS"],
                    f"{promo_col} NS": st_tot["LM NS"],
                    f"{promo_col} Cont%": st_tot["LM Cont%"],
                })
        except Exception:
            continue
    
    if trend_data:
        trend_df = pd.DataFrame(trend_data[::-1])  # Reverse for chronological order
        current_idx = len(trend_df) - 1 - files.index(selected_file)
        
        fig_trend = build_trend_chart(trend_df, current_idx, bar_accent, 
                                       f"{promo_col} NS", f"{promo_col} Cont%")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        with st.expander("📋 Lihat Detail Data Tren"):
            td = trend_df.copy()
            td["Total NS"] = td["Total NS"].apply(lambda x: f"{x:,.0f}")
            td["Normal NS"] = td["Normal NS"].apply(lambda x: f"{x:,.0f}")
            td[f"{promo_col} NS"] = td[f"{promo_col} NS"].apply(lambda x: f"{x:,.0f}")
            td[f"{promo_col} Cont%"] = td[f"{promo_col} Cont%"].apply(lambda x: f"{x:.2f}%")
            if "NOC" in td.columns:
                td["NOC"] = td["NOC"].apply(lambda x: f"{x:,.0f}")
            st.dataframe(td, use_container_width=True)
    
    st.markdown("---")
    
    # ── Badge & Title ─────────────────────────────────────────────────────────
    st.markdown(portal_badge(portal, banner_type), unsafe_allow_html=True)
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
        normal_ns = store_total["Normal NS"]
        
        if banner_type in ["Hijau", "Cokelat"]:
            promo_ns = store_total["Banner NS"]
            promo_cont = store_total["Banner Cont%"]
            retailer_ns = store_total["Retailer NS"]
            horeca_ns = store_total["Horeca NS"]
            others_ns = store_total["Others NS"]
            noc_total = store_total.get("NOC", 0)
        else:
            promo_ns = store_total["LM NS"]
            promo_cont = store_total["LM Cont%"]
            if has_sku_performance:
                sku_total_val = store_total["SKU Total"]
                sku_sale_val = store_total["SKU Sale"]
                sku_cont_val = store_total["SKU Cont%"]
                oos_val_total = store_total["OOS"]
    else:
        total_ns = cat_div_filtered["Total NS"].sum()
        normal_ns = cat_div_filtered["Normal NS"].sum()
        
        if banner_type in ["Hijau", "Cokelat"]:
            promo_ns = cat_div_filtered["Banner NS"].sum()
            promo_cont = (promo_ns / total_ns * 100) if total_ns else 0
            retailer_ns = cat_div_filtered["Retailer NS"].sum()
            horeca_ns = cat_div_filtered["Horeca NS"].sum()
            others_ns = cat_div_filtered["Others NS"].sum()
            noc_total = store_df["NOC"].sum()  # NOC is store-level
        else:
            promo_ns = cat_div_filtered["LM NS"].sum()
            promo_cont = (promo_ns / total_ns * 100) if total_ns else 0
            if has_sku_performance:
                sku_total_val = cat_div_filtered["SKU Total"].sum()
                sku_sale_val = cat_div_filtered["SKU Sale"].sum()
                sku_cont_val = (sku_sale_val / sku_total_val * 100) if sku_total_val else 0
                oos_val_total = cat_div_filtered["OOS"].sum()
    
    # ── Scorecards ───────────────────────────────────────────────────────────
    if banner_type in ["Hijau", "Cokelat"]:
        # Hijau/Cokelat: NOC + Retailer/Horeca/Others breakdown
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(metric_card("Total Net Sales", fmt_rp(total_ns)), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Banner (Promo) Sales", fmt_rp(promo_ns), "green",
                                    f"Kontribusi: {promo_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Normal (Non-Promo)", fmt_rp(normal_ns), "orange",
                                    f"Kontribusi: {100-promo_cont:.2f}%"), unsafe_allow_html=True)
        with c4:
            st.markdown(metric_card("Total NOC", fmt_number(noc_total), "purple",
                                    "Customer beli promo Banner"), unsafe_allow_html=True)
        with c5:
            avg_noc = noc_total / len(store_df) if len(store_df) else 0
            st.markdown(metric_card("Avg NOC per Store", f"{avg_noc:.1f}", "teal"), unsafe_allow_html=True)
        with c6:
            if len(store_df) > 0:
                top_noc_store = store_df.loc[store_df["NOC"].idxmax(), "Store Name"]
                top_noc_val = store_df["NOC"].max()
            else:
                top_noc_store = "–"
                top_noc_val = 0
            st.markdown(metric_card("Top NOC Store", str(top_noc_store), "pink",
                                    f"NOC: {fmt_number(top_noc_val)}"), unsafe_allow_html=True)
    else:
        # EndUser: Same as Mailer
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(metric_card("Total Net Sales", fmt_rp(total_ns)), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("LM (Promo) Sales", fmt_rp(promo_ns), "green",
                                    f"Kontribusi: {promo_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Normal (Non-Promo)", fmt_rp(normal_ns), "orange",
                                    f"Kontribusi: {100-promo_cont:.2f}%"), unsafe_allow_html=True)
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
        section_title(f"Komposisi {promo_col} vs Normal")
        fig1 = build_pie_chart(
            [f"{promo_col} (Promo)", "Normal"], [promo_ns, normal_ns],
            [bar_accent, "#2d3a5a"], f"<b>{promo_cont:.1f}%</b><br>{promo_col}", bar_accent
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_b:
        if banner_type in ["Hijau", "Cokelat"]:
            section_title("Breakdown: Retailer vs Horeca vs Others")
            fig_br = build_pie_chart(
                ["Retailer", "Horeca", "Others"], [retailer_ns, horeca_ns, others_ns],
                ["#00d4ff", "#fee440", "#9b5de5"], 
                f"<b>{promo_ns:,.0f}</b><br>Banner NS", "#00d4ff"
            )
            st.plotly_chart(fig_br, use_container_width=True)
        else:
            section_title("SKU Promo: Terjual vs OOS vs Belum Terjual")
            oos_pie = int(oos_val_total)
            sold_pie = int(sku_sale_val)
            unsold_pie = max(0, int(sku_total_val) - sold_pie - oos_pie)
            fig_sku = build_pie_chart(
                ["Terjual", "OOS", "Belum Terjual"], [sold_pie, oos_pie, unsold_pie],
                ["#00f5d4", "#ff6b6b", "#2d3a5a"], f"<b>{sku_cont_val:.1f}%</b><br>Sell-Through", "#00f5d4"
            )
            st.plotly_chart(fig_sku, use_container_width=True)
    
    # ── Breakdown bar ─────────────────────────────────────────────────────────
    if banner_type in ["Hijau", "Cokelat"]:
        section_title("Breakdown Banner Sales: Retailer (Big+Medium+SWK) vs Horeca vs Others")
        
        # Get Big/Medium/SWK from store_total
        big_ns = store_total.get("Big NS", 0)
        medium_ns = store_total.get("Medium NS", 0)
        swk_ns = store_total.get("SWK NS", 0)
        
        fig_br = go.Figure()
        
        # Retailer breakdown
        fig_br.add_trace(go.Bar(
            x=["Big", "Medium", "SWK", "Horeca", "Others"],
            y=[big_ns, medium_ns, swk_ns, horeca_ns, others_ns],
            marker_color=["#00d4ff", "#0099cc", "#006699", "#fee440", "#9b5de5"],
            text=[f"{v/promo_ns*100:.1f}%" if promo_ns else "0%" 
                  for v in [big_ns, medium_ns, swk_ns, horeca_ns, others_ns]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig_br.update_layout(**{**PLOTLY_DARK_THEME, "height": 300,
            "margin": dict(t=30, b=10, l=10, r=10), "yaxis_title": "Net Sales Banner"})
        st.plotly_chart(fig_br, use_container_width=True)
        
        # NOC Distribution
        st.markdown("---")
        section_title("📊 Distribusi NOC (Number of Customers) per Store")
        
        noc_sorted = store_df.sort_values("NOC", ascending=True).copy()
        noc_sorted["Region"] = noc_sorted["Store Name"].map(STORE_REGION_MAP)
        noc_sorted["Display Name"] = noc_sorted.apply(
            lambda r: f"[{r['Region'][-1] if pd.notna(r['Region']) else '?'}] {r['Store Name']}", axis=1
        )
        
        avg_noc = noc_sorted["NOC"].mean()
        colors = ["#ff6b6b" if v < avg_noc * 0.5 else "#fee440" if v < avg_noc else "#00f5d4"
                  for v in noc_sorted["NOC"]]
        
        fig_noc = go.Figure(go.Bar(
            y=noc_sorted["Display Name"], x=noc_sorted["NOC"],
            orientation="h", marker_color=colors,
            text=[f"{int(v):,}" for v in noc_sorted["NOC"]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig_noc.add_vline(x=avg_noc, line_dash="dash", line_color="#718096",
                          annotation_text=f"Avg: {avg_noc:.0f}", 
                          annotation_font=dict(color="#718096"),
                          annotation_position="top")
        fig_noc.update_layout(**{**PLOTLY_DARK_THEME, "height": max(500, len(noc_sorted)*26),
            "margin": dict(t=30, b=20, l=10, r=40), "xaxis_title": "NOC (Retail + Horeca)"})
        st.plotly_chart(fig_noc, use_container_width=True)
        
    else:
        # EndUser breakdown same as Mailer
        if portal == "LSI":
            section_title("Breakdown Net Sales LM: Trader vs Prof vs Others")
            lm_trader = store_df["LM Trader NS"].sum()
            lm_prof = store_df["LM Prof NS"].sum()
            lm_others = store_df["LM Others NS"].sum()
            
            fig_lm = go.Figure(go.Bar(
                x=["Trader", "Professional", "Others"],
                y=[lm_trader, lm_prof, lm_others],
                marker_color=["#fee440", "#00d4ff", "#9b5de5"],
                text=[f"{v/promo_ns*100:.1f}%" if promo_ns else "0%" for v in [lm_trader, lm_prof, lm_others]],
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
        else:
            section_title("Breakdown Net Sales LM: Regular vs Trader")
            regular_ns = store_df["Regular NS"].sum()
            trader_ns = store_df["Trader NS"].sum()
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
    
    # ── Promo Net Sales per Division ──────────────────────────────────────────
    section_title(f"{promo_col} Net Sales per Division")
    div_data_src = cat_div_filtered if selected_divisions else cat_df
    
    promo_ns_col = "Banner NS" if banner_type in ["Hijau", "Cokelat"] else "LM NS"
    
    div_bar = div_data_src.groupby("Division").agg(
        Total_NS=("Total NS", "sum"), Promo_NS=(promo_ns_col, "sum"),
    ).reset_index()
    div_bar["Promo_Cont%"] = div_bar["Promo_NS"] / div_bar["Total_NS"] * 100
    div_bar = div_bar.sort_values("Promo_NS", ascending=False)
    
    fig_div = build_division_chart(div_bar, bar_accent, div_colors)
    st.plotly_chart(fig_div, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 – BY STORE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏪 By Store":
    st.markdown(portal_badge(portal, banner_type), unsafe_allow_html=True)
    st.markdown(f"## 🏪 Analisis Net Sales per Store — {period_label}")
    
    # Filter by contribution threshold
    cont_col = "Banner Cont%" if banner_type in ["Hijau", "Cokelat"] else "LM Cont%"
    filtered = store_df[store_df[cont_col] >= banner_thresh].copy()
    
    # ── Region filter for LSI ─────────────────────────────────────────────────
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
    promo_ns_col = "Banner NS" if banner_type in ["Hijau", "Cokelat"] else "LM NS"
    
    if banner_type in ["Hijau", "Cokelat"]:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(metric_card("Total Store Aktif", str(len(filtered))), unsafe_allow_html=True)
        with c2:
            total_promo_ns = filtered[promo_ns_col].sum()
            avg_cont = filtered[cont_col].mean()
            st.markdown(metric_card("Net Sales Banner", fmt_rp(total_promo_ns), "green",
                                    f"Avg Cont: {avg_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            top = filtered.loc[filtered["Total NS"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest Revenue Store", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            total_noc = filtered["NOC"].sum()
            st.markdown(metric_card("Total NOC", fmt_number(total_noc), "purple",
                                    "Customer beli promo"), unsafe_allow_html=True)
        with c5:
            avg_noc = filtered["NOC"].mean() if len(filtered) else 0
            st.markdown(metric_card("Avg NOC per Store", f"{avg_noc:.1f}", "teal"), unsafe_allow_html=True)
        with c6:
            top_noc = filtered.loc[filtered["NOC"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Top NOC Store", str(top_noc), "pink"), unsafe_allow_html=True)
    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(metric_card("Total Store Aktif", str(len(filtered))), unsafe_allow_html=True)
        with c2:
            total_promo_ns = filtered[promo_ns_col].sum()
            avg_cont = filtered[cont_col].mean()
            st.markdown(metric_card("Net Sales LM", fmt_rp(total_promo_ns), "green",
                                    f"Avg Cont: {avg_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            top = filtered.loc[filtered["Total NS"].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest Revenue Store", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            top_lm = filtered.loc[filtered[cont_col].idxmax(), "Store Name"] if len(filtered) else "–"
            st.markdown(metric_card("Highest LM Cont% Store", str(top_lm), "purple"), unsafe_allow_html=True)
        with c5:
            st.markdown(metric_card("Avg SKU Sell-Through", f"{filtered['SKU Cont%'].mean():.1f}%", "teal"), unsafe_allow_html=True)
        with c6:
            st.markdown(metric_card("Total OOS SKU", f"{int(filtered['OOS'].sum()):,}", "red"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Net Sales & Contribution Charts ────────────────────────────────────────
    col1, col2 = st.columns([3, 2])
    sorted_store = filtered.sort_values(cont_col, ascending=True)
    
    if selected_region == "Semua Regional":
        sorted_store["Display Name"] = sorted_store.apply(
            lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
    else:
        sorted_store["Display Name"] = sorted_store["Store Name"]
    
    normal_col = "Normal NS"
    
    with col1:
        section_title(f"Total Net Sales per Store ({promo_col} vs Normal)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=sorted_store["Display Name"], x=sorted_store[normal_col],
            name="Normal", orientation="h", marker_color="#2d3a5a",
            text=[f"{v:,.0f}" for v in sorted_store[normal_col]],
            textposition="inside", textfont=dict(color="#94a3b8"),
        ))
        fig.add_trace(go.Bar(
            y=sorted_store["Display Name"], x=sorted_store[promo_ns_col],
            name=f"{promo_col} (Promo)", orientation="h", marker_color=bar_accent,
            text=[f"{v:,.0f}" for v in sorted_store[promo_ns_col]],
            textposition="inside", textfont=dict(color="#ffffff"),
        ))
        fig.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
            "height": max(420, len(filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=20), "xaxis_title": "Net Sales"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_title(f"{promo_col} Contribution % per Store")
        sorted_lm = sorted_store.copy()
        thresh_low = 5
        thresh_mid = 10
        colors = ["#ff6b6b" if v < thresh_low else "#fee440" if v < thresh_mid else "#00f5d4"
                  for v in sorted_lm[cont_col]]
        fig2 = go.Figure(go.Bar(
            y=sorted_lm["Display Name"], x=sorted_lm[cont_col],
            orientation="h", marker_color=colors,
            text=[f"{v:.1f}%" for v in sorted_lm[cont_col]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig2.add_vline(x=filtered[cont_col].mean(), line_dash="dash", line_color="#718096",
                       annotation_text="Avg", annotation_font=dict(color="#718096"),
                       annotation_position="top")
        fig2.update_layout(**{**PLOTLY_DARK_THEME, "height": max(420, len(filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=40), "xaxis_title": f"{promo_col} Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # ── NOC Chart for Hijau/Cokelat ───────────────────────────────────────────
    if banner_type in ["Hijau", "Cokelat"]:
        st.markdown("---")
        section_title("📊 NOC (Number of Customers) per Store")
        
        noc_sorted = filtered.sort_values("NOC", ascending=True).copy()
        if selected_region == "Semua Regional":
            noc_sorted["Display Name"] = noc_sorted.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
        else:
            noc_sorted["Display Name"] = noc_sorted["Store Name"]
        
        avg_noc = noc_sorted["NOC"].mean()
        colors = ["#ff6b6b" if v < avg_noc * 0.5 else "#fee440" if v < avg_noc else "#00f5d4"
                  for v in noc_sorted["NOC"]]
        
        fig_noc = go.Figure(go.Bar(
            y=noc_sorted["Display Name"], x=noc_sorted["NOC"],
            orientation="h", marker_color=colors,
            text=[f"{int(v):,}" for v in noc_sorted["NOC"]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig_noc.add_vline(x=avg_noc, line_dash="dash", line_color="#718096",
                          annotation_text=f"Avg: {avg_noc:.0f}", 
                          annotation_font=dict(color="#718096"),
                          annotation_position="top")
        fig_noc.update_layout(**{**PLOTLY_DARK_THEME, "height": max(420, len(noc_sorted)*28),
            "margin": dict(t=30, b=20, l=10, r=40), "xaxis_title": "NOC (Retail + Horeca)"})
        st.plotly_chart(fig_noc, use_container_width=True)
    
    # ── SKU Performance for EndUser ───────────────────────────────────────────
    if banner_type == "EndUser" and has_sku_performance:
        st.markdown("---")
        st.markdown("### 📦 SKU Performance per Store")
        section_title("SKU Terjual / OOS / Belum Terjual per Store")
        
        sku_store = filtered[filtered["SKU Total"] > 0].copy()
        sku_store["SKU Unsold"] = (sku_store["SKU Total"] - sku_store["SKU Sale"] - sku_store["OOS"]).clip(lower=0)
        sku_store["Sale_Pct"] = (sku_store["SKU Sale"] / sku_store["SKU Total"] * 100).round(1)
        sku_store["OOS_Pct"] = (sku_store["OOS"] / sku_store["SKU Total"] * 100).round(1)
        sku_store["Unsold_Pct"] = (sku_store["SKU Unsold"] / sku_store["SKU Total"] * 100).round(1)
        sku_store = sku_store.sort_values(cont_col, ascending=True)
        
        if selected_region == "Semua Regional":
            sku_store["Display Name"] = sku_store.apply(
                lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
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
    
    # ── Breakdown per Store ───────────────────────────────────────────────────
    st.markdown("---")
    sorted_br = filtered.sort_values(cont_col, ascending=True).copy()
    
    if selected_region == "Semua Regional":
        sorted_br["Display Name"] = sorted_br.apply(
            lambda r: f"[{r['Region'][-1]}] {r['Store Name']}", axis=1)
    else:
        sorted_br["Display Name"] = sorted_br["Store Name"]
    
    if banner_type in ["Hijau", "Cokelat"]:
        section_title("Breakdown Banner Sales: Retailer vs Horeca vs Others per Store")
        sorted_br["Retailer_Pct"] = (sorted_br["Retailer NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        sorted_br["Horeca_Pct"] = (sorted_br["Horeca NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        sorted_br["Others_Pct"] = (sorted_br["Others NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Retailer NS"],
            name="Retailer", orientation="h", marker_color="#00d4ff",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Retailer NS"], sorted_br["Retailer_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Horeca NS"],
            name="Horeca", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Horeca NS"], sorted_br["Horeca_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Others NS"],
            name="Others", orientation="h", marker_color="#9b5de5",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Others NS"], sorted_br["Others_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    elif portal == "LSI":
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
        "xaxis_title": f"Net Sales {promo_col}"})
    st.plotly_chart(fig_br, use_container_width=True)
    
    # ── Data Table ────────────────────────────────────────────────────────────
    st.markdown("---")
    section_title("📋 Detail Data per Store")
    table_df = filtered.sort_values(cont_col, ascending=False).copy()
    
    if banner_type in ["Hijau", "Cokelat"]:
        disp = ["Region", "Store Name", "Total NS", "Normal NS", "Banner NS", "Banner Cont%",
                "Retailer NS", "Big NS", "Medium NS", "SWK NS", "Horeca NS", "Others NS", "NOC"]
        fmt = {"Total NS": "{:,.1f}", "Normal NS": "{:,.1f}", "Banner NS": "{:,.1f}",
               "Banner Cont%": "{:.2f}%", "Retailer NS": "{:,.1f}", "Big NS": "{:,.1f}",
               "Medium NS": "{:,.1f}", "SWK NS": "{:,.1f}", "Horeca NS": "{:,.1f}",
               "Others NS": "{:,.1f}", "NOC": "{:,.0f}"}
    elif portal == "LSI":
        disp = ["Region", "Store Name", "Total NS", "Normal NS", "LM NS", "LM Cont%",
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
    st.markdown(portal_badge(portal, banner_type), unsafe_allow_html=True)
    st.markdown(f"## 📦 Analisis Net Sales per Kategori — {period_label}")
    
    cont_col = "Banner Cont%" if banner_type in ["Hijau", "Cokelat"] else "LM Cont%"
    promo_ns_col = "Banner NS" if banner_type in ["Hijau", "Cokelat"] else "LM NS"
    
    cat_filtered = cat_df[cat_df[cont_col] >= banner_thresh].copy()
    
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
    total_promo_ns = cat_filtered[promo_ns_col].sum()
    promo_pct = total_promo_ns / total_cat_ns * 100 if total_cat_ns else 0
    
    # ── Scorecards ───────────────────────────────────────────────────────────
    if banner_type in ["Hijau", "Cokelat"]:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(metric_card("Total Kategori Aktif", str(len(cat_filtered))), unsafe_allow_html=True)
        with c2:
            avg_cont = cat_filtered[cont_col].mean() if len(cat_filtered) else 0
            st.markdown(metric_card("Net Sales Banner", fmt_rp(total_promo_ns), "green",
                                    f"Avg Cont: {avg_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            top = cat_filtered.loc[cat_filtered["Total NS"].idxmax(), "Category"] if len(cat_filtered) else "–"
            st.markdown(metric_card("Highest Revenue Category", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            top_cont = cat_filtered.loc[cat_filtered[cont_col].idxmax(), "Category"] if len(cat_filtered) else "–"
            st.markdown(metric_card(f"Highest {promo_col} Cont%", str(top_cont), "purple"), unsafe_allow_html=True)
    else:
        total_sku_cat = cat_filtered["SKU Total"].sum()
        sale_sku_cat = cat_filtered["SKU Sale"].sum()
        pct_sku_cat = sale_sku_cat / total_sku_cat * 100 if total_sku_cat else 0
        
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.markdown(metric_card("Total Kategori Aktif", str(len(cat_filtered))), unsafe_allow_html=True)
        with c2:
            avg_cont = cat_filtered[cont_col].mean() if len(cat_filtered) else 0
            st.markdown(metric_card("Net Sales LM", fmt_rp(total_promo_ns), "green",
                                    f"Avg Cont: {avg_cont:.2f}%"), unsafe_allow_html=True)
        with c3:
            top = cat_filtered.loc[cat_filtered["Total NS"].idxmax(), "Category"] if len(cat_filtered) else "–"
            st.markdown(metric_card("Highest Revenue Category", str(top), "orange"), unsafe_allow_html=True)
        with c4:
            top_lm = cat_filtered.loc[cat_filtered[cont_col].idxmax(), "Category"] if len(cat_filtered) else "–"
            st.markdown(metric_card("Highest LM Cont% Category", str(top_lm), "purple"), unsafe_allow_html=True)
        with c5:
            st.markdown(metric_card("Avg SKU Sell-Through", f"{pct_sku_cat:.1f}%", "teal"), unsafe_allow_html=True)
        with c6:
            st.markdown(metric_card("Total OOS SKU", f"{int(cat_filtered['OOS'].sum()):,}", "red"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Net Sales & Contribution Charts ────────────────────────────────────────
    col1, col2 = st.columns([3, 2])
    sorted_cat = cat_filtered.sort_values(cont_col, ascending=True)
    
    div_abbrev = {"FRESH FOOD": "FF", "MEAL SOLUTION": "MS", "DRY FOOD": "DF",
                  "H&B HOME CARE": "HB", "ELECTRONIC": "EL", "NON FOOD": "NF", "Other": "OT"}
    
    if selected_division == "Semua Division":
        sorted_cat["Display Name"] = sorted_cat.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1)
    else:
        sorted_cat["Display Name"] = sorted_cat["Category"]
    
    with col1:
        section_title(f"Total Net Sales per Category ({promo_col} vs Normal)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=sorted_cat["Display Name"], x=sorted_cat["Normal NS"],
            name="Normal", orientation="h", marker_color="#2d3a5a",
            text=[f"{v:,.0f}" for v in sorted_cat["Normal NS"]],
            textposition="inside", textfont=dict(color="#94a3b8"),
        ))
        fig.add_trace(go.Bar(
            y=sorted_cat["Display Name"], x=sorted_cat[promo_ns_col],
            name=f"{promo_col} (Promo)", orientation="h", marker_color=bar_accent,
            text=[f"{v:,.0f}" for v in sorted_cat[promo_ns_col]],
            textposition="inside", textfont=dict(color="#ffffff"),
        ))
        fig.update_layout(**{**PLOTLY_DARK_THEME, "barmode": "stack",
            "height": max(420, len(cat_filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=20), "xaxis_title": "Net Sales"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        section_title(f"{promo_col} Contribution % per Category")
        sorted_lm = sorted_cat.copy()
        thresh_low = 5
        thresh_mid = 10
        colors = ["#ff6b6b" if v < thresh_low else "#fee440" if v < thresh_mid else "#00f5d4"
                  for v in sorted_lm[cont_col]]
        fig2 = go.Figure(go.Bar(
            y=sorted_lm["Display Name"], x=sorted_lm[cont_col],
            orientation="h", marker_color=colors,
            text=[f"{v:.1f}%" for v in sorted_lm[cont_col]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig2.add_vline(x=cat_filtered[cont_col].mean(), line_dash="dash", line_color="#718096",
                       annotation_text="Avg", annotation_font=dict(color="#718096"),
                       annotation_position="top")
        fig2.update_layout(**{**PLOTLY_DARK_THEME, "height": max(420, len(cat_filtered)*28),
            "margin": dict(t=20, b=20, l=10, r=40), "xaxis_title": f"{promo_col} Contribution (%)"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # ── Breakdown per Category ────────────────────────────────────────────────
    st.markdown("---")
    sorted_br = cat_filtered.sort_values(cont_col, ascending=True).copy()
    
    if selected_division == "Semua Division":
        sorted_br["Display Name"] = sorted_br.apply(
            lambda r: f"[{div_abbrev.get(r['Division'], 'OT')}] {r['Category']}", axis=1)
    else:
        sorted_br["Display Name"] = sorted_br["Category"]
    
    if banner_type in ["Hijau", "Cokelat"]:
        section_title("Breakdown Banner Sales: Retailer vs Horeca vs Others per Category")
        sorted_br["Retailer_Pct"] = (sorted_br["Retailer NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        sorted_br["Horeca_Pct"] = (sorted_br["Horeca NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        sorted_br["Others_Pct"] = (sorted_br["Others NS"] / sorted_br["Banner NS"] * 100).fillna(0).round(1)
        
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Retailer NS"],
            name="Retailer", orientation="h", marker_color="#00d4ff",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Retailer NS"], sorted_br["Retailer_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Horeca NS"],
            name="Horeca", orientation="h", marker_color="#fee440",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Horeca NS"], sorted_br["Horeca_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
        fig_br.add_trace(go.Bar(
            y=sorted_br["Display Name"], x=sorted_br["Others NS"],
            name="Others", orientation="h", marker_color="#9b5de5",
            text=[f"{p:.1f}%" if v > 0 else "" for v, p in zip(sorted_br["Others NS"], sorted_br["Others_Pct"])],
            textposition="inside", textfont=dict(color="#1a1a2e", size=10, weight="bold"),
        ))
    elif portal == "LSI":
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
        "xaxis_title": f"Net Sales {promo_col}"})
    st.plotly_chart(fig_br, use_container_width=True)
    
    # ── Data Table ────────────────────────────────────────────────────────────
    st.markdown("---")
    section_title("📋 Detail Data per Category")
    table_df = cat_filtered.sort_values(cont_col, ascending=False).copy()
    
    if banner_type in ["Hijau", "Cokelat"]:
        disp = ["Division", "Category", "Total NS", "Normal NS", "Banner NS", "Banner Cont%",
                "Retailer NS", "Big NS", "Medium NS", "SWK NS", "Horeca NS", "Others NS"]
        fmt = {"Total NS": "{:,.1f}", "Normal NS": "{:,.1f}", "Banner NS": "{:,.1f}",
               "Banner Cont%": "{:.2f}%", "Retailer NS": "{:,.1f}", "Big NS": "{:,.1f}",
               "Medium NS": "{:,.1f}", "SWK NS": "{:,.1f}", "Horeca NS": "{:,.1f}",
               "Others NS": "{:,.1f}"}
    elif portal == "LSI":
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


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 – SKU PROMO (Hijau/Cokelat only)
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 SKU Promo" and banner_type in ["Hijau", "Cokelat"]:
    st.markdown(portal_badge(portal, banner_type), unsafe_allow_html=True)
    st.markdown(f"## 📋 Daftar SKU Promo Banner {banner_type} — {period_label}")
    
    if sku_df.empty:
        st.warning("⚠️ Tidak ada data SKU Promo untuk periode ini.")
        st.info("Pastikan sheet 'SKU_Banner' tersedia di file data.")
    else:
        # ── Scorecards ────────────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(metric_card("Total SKU Promo", str(len(sku_df))), unsafe_allow_html=True)
        with c2:
            n_cat = sku_df["Category"].nunique()
            st.markdown(metric_card("Jumlah Kategori", str(n_cat), "green"), unsafe_allow_html=True)
        with c3:
            if "Remarks" in sku_df.columns:
                n_remarks = sku_df["Remarks"].notna().sum()
                st.markdown(metric_card("SKU dengan Remarks", str(n_remarks), "orange"), unsafe_allow_html=True)
            else:
                st.markdown(metric_card("SKU per Kategori (Avg)", 
                                        f"{len(sku_df)/n_cat:.1f}" if n_cat else "0", "orange"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ── Filter by Category ────────────────────────────────────────────────
        section_title("🔍 Filter SKU")
        categories = sorted(sku_df["Category"].dropna().unique().tolist())
        selected_cat = st.selectbox(
            "Pilih Kategori:", options=["Semua Kategori"] + categories,
            key="sku_cat_filter"
        )
        
        if selected_cat != "Semua Kategori":
            sku_filtered = sku_df[sku_df["Category"] == selected_cat].copy()
        else:
            sku_filtered = sku_df.copy()
        
        # ── Search ────────────────────────────────────────────────────────────
        search_term = st.text_input("🔎 Cari SKU (nama/kode):", placeholder="Ketik untuk mencari...")
        if search_term:
            mask = (sku_filtered["Product Name"].astype(str).str.contains(search_term, case=False, na=False) |
                    sku_filtered["Product Code"].astype(str).str.contains(search_term, case=False, na=False))
            sku_filtered = sku_filtered[mask]
        
        st.markdown(f"**Menampilkan {len(sku_filtered)} SKU**")
        
        # ── SKU Table ─────────────────────────────────────────────────────────
        section_title("📦 Daftar SKU Promo")
        
        disp_cols = ["Cat ID", "Category", "Product Code", "Product Name"]
        if "Remarks" in sku_filtered.columns:
            disp_cols.append("Remarks")
        
        st.dataframe(
            sku_filtered[disp_cols].reset_index(drop=True),
            use_container_width=True,
            height=min(600, 50 + len(sku_filtered) * 35)
        )
        
        # ── SKU per Category summary ──────────────────────────────────────────
        st.markdown("---")
        section_title("📊 Jumlah SKU per Kategori")
        
        sku_summary = sku_df.groupby("Category").size().reset_index(name="SKU Count")
        sku_summary = sku_summary.sort_values("SKU Count", ascending=True)
        
        fig_sku = go.Figure(go.Bar(
            y=sku_summary["Category"], x=sku_summary["SKU Count"],
            orientation="h", marker_color=bar_accent,
            text=[str(int(v)) for v in sku_summary["SKU Count"]],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig_sku.update_layout(**{**PLOTLY_DARK_THEME, "height": max(300, len(sku_summary)*30),
            "margin": dict(t=20, b=20, l=10, r=40), "xaxis_title": "Jumlah SKU"})
        st.plotly_chart(fig_sku, use_container_width=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────
render_footer(f"{portal} · {banner_type}", period_label)
