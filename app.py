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

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12), 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #3b82f6;
    }
    .metric-card.green  { border-left-color: #22c55e; }
    .metric-card.orange { border-left-color: #f97316; }
    .metric-card.purple { border-left-color: #8b5cf6; }
    .metric-card.red    { border-left-color: #ef4444; }
    .metric-card.teal   { border-left-color: #14b8a6; }
    .metric-value { font-size: 1.7rem; font-weight: 700; color: #1e293b; }
    .metric-label { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-delta { font-size: 0.85rem; margin-top: 0.2rem; color: #64748b; }
    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #1e293b;
        margin-bottom: 0.5rem; padding-bottom: 0.3rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .insight-box {
        background: #eff6ff; border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0; padding: 0.8rem 1rem;
        margin-bottom: 0.6rem; font-size: 0.9rem; color: #1e40af;
    }
    .insight-box.warning { background: #fff7ed; border-left-color: #f97316; color: #9a3412; }
    .insight-box.success { background: #f0fdf4; border-left-color: #22c55e; color: #166534; }
    .portal-badge {
        display: inline-block; padding: 0.3rem 1rem;
        border-radius: 20px; font-weight: 700; font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .badge-lmi { background: #dbeafe; color: #1d4ed8; }
    .badge-lsi { background: #f3e8ff; color: #7c3aed; }
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

# ─── DATA LOADERS ────────────────────────────────────────────────────────────

@st.cache_data
def load_lmi():
    path = "LM1_114_Jan_Nasional.xlsx"
    raw_store = pd.read_excel(path, sheet_name="By Store", header=None)
    period_label = str(raw_store.iloc[1, 1])

    store = raw_store.iloc[4:16].copy()
    store.columns = range(store.shape[1])
    store = store[[1,2,3,4,5,6,7,8,9,10]]
    store.columns = ["Store ID","Store Name","Total NS","Normal NS","LM NS",
                     "LM Cont%","Regular NS","Regular Cont%","Trader NS","Trader Cont%"]
    store = store.dropna(subset=["Store ID"]).reset_index(drop=True)
    for col in store.columns[2:]:
        store[col] = pd.to_numeric(store[col], errors="coerce")

    total_row = raw_store.iloc[16]
    store_total = {"Total NS": total_row[3], "Normal NS": total_row[4],
                   "LM NS": total_row[5], "LM Cont%": total_row[6]}

    raw_cat = pd.read_excel(path, sheet_name="By Cat", header=None)
    GROUP_LABELS = ["FRESH FOOD","MEAL SOLUTION","DRY FOOD","H&B HOME CARE","ELECTRONIC","NON FOOD","TOTAL"]
    all_rows = raw_cat.iloc[4:].copy()
    all_rows.columns = range(all_rows.shape[1])

    rows = []
    for _, r in all_rows.iterrows():
        cat_id, cat_name = r[1], r[2]
        if pd.isna(cat_id): continue
        rows.append({
            "Cat ID": cat_id, "Category": cat_name,
            "Total NS": pd.to_numeric(r[3], errors="coerce"),
            "Normal NS": pd.to_numeric(r[4], errors="coerce"),
            "LM NS": pd.to_numeric(r[5], errors="coerce"),
            "LM Cont%": pd.to_numeric(r[6], errors="coerce"),
            "Regular NS": pd.to_numeric(r[7], errors="coerce"),
            "Regular Cont%": pd.to_numeric(r[8], errors="coerce"),
            "Trader NS": pd.to_numeric(r[9], errors="coerce"),
            "Trader Cont%": pd.to_numeric(r[10], errors="coerce"),
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
    return store, store_total, cat_detail, period_label


@st.cache_data
def load_lsi(lm_num):
    path = f"LM{lm_num}_LSI_Summary.xlsb"

    # ── By Store ──
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
        "Total NS":        pd.to_numeric(store_rows[2], errors="coerce").values,
        "Normal NS":       pd.to_numeric(store_rows[3], errors="coerce").values,
        "LM NS":           pd.to_numeric(store_rows[4], errors="coerce").values,
        "LM Cont%":        pd.to_numeric(store_rows[5], errors="coerce").values,
        "LM Trader NS":    pd.to_numeric(store_rows[6], errors="coerce").values,
        "LM Trader Cont%": pd.to_numeric(store_rows[7], errors="coerce").values,
        "LM Prof NS":      pd.to_numeric(store_rows[8], errors="coerce").values,
        "LM Prof Cont%":   pd.to_numeric(store_rows[9], errors="coerce").values,
        "LM Others NS":    pd.to_numeric(store_rows[10], errors="coerce").values,
        "LM Others Cont%": pd.to_numeric(store_rows[11], errors="coerce").values,
        "SKU Total":       pd.to_numeric(store_rows[12], errors="coerce").values,
        "SKU Sale":        pd.to_numeric(store_rows[13], errors="coerce").values,
        "SKU Cont%":       pd.to_numeric(store_rows[14], errors="coerce").values,
        "OOS":             pd.to_numeric(store_rows[15], errors="coerce").values,
    }).reset_index(drop=True)

    store_total = {
        "Total NS":  pd.to_numeric(total_row[2], errors="coerce"),
        "Normal NS": pd.to_numeric(total_row[3], errors="coerce"),
        "LM NS":     pd.to_numeric(total_row[4], errors="coerce"),
        "LM Cont%":  pd.to_numeric(total_row[5], errors="coerce"),
        "SKU Total": pd.to_numeric(total_row[12], errors="coerce"),
        "SKU Sale":  pd.to_numeric(total_row[13], errors="coerce"),
        "SKU Cont%": pd.to_numeric(total_row[14], errors="coerce"),
        "OOS":       pd.to_numeric(total_row[15], errors="coerce"),
    }

    # ── By Cat ──
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


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bar-chart.png", width=55)
    st.title("Dashboard Filter")

    st.markdown("---")
    portal = st.radio("🏬 Portal", ["LMI (114 Store)", "LSI (600 Store)"])

    st.markdown("---")
    if portal == "LSI (600 Store)":
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
    else:
        store_df, store_total, cat_df, period_label = load_lmi()
        portal_label = "LMI"

    st.markdown("---")
    page = st.radio("📌 View", ["🏠 Overview", "🏪 By Store", "📦 By Category"])

    st.markdown("---")
    lm_thresh = st.slider("Min LM Contribution (%)", 0.0, 60.0, 0.0, 0.5)
    st.markdown("---")
    st.caption("Data: Net Sales (dalam ribuan Rupiah)")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
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
                hole=0.55, marker_colors=["#3b82f6","#e2e8f0"],
                textinfo="label+percent", textfont_size=13,
            ))
            fig1.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=260,
                annotations=[dict(text=f"<b>{lm_cont:.1f}%</b><br>LM", x=0.5, y=0.5,
                                  font_size=16, showarrow=False)])
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">Komposisi Regular vs Trader</div>', unsafe_allow_html=True)
            regular_cont_pct = regular_ns / total_ns * 100 if total_ns else 0
            trader_cont_pct  = trader_ns  / total_ns * 100 if total_ns else 0
            fig2 = go.Figure(go.Pie(
                labels=["Regular (End User)","Trader"], values=[regular_ns, trader_ns],
                hole=0.55, marker_colors=["#22c55e","#f97316"],
                textinfo="none",
                customdata=[regular_cont_pct, trader_cont_pct],
                hovertemplate="<b>%{label}</b><br>Net Sales: %{value:,.3f}<br>Kontribusi: %{customdata:.6f}%<extra></extra>",
            ))
            fig2.update_layout(
                showlegend=True, legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
                margin=dict(t=10,b=50,l=10,r=10), height=290,
                annotations=[
                    dict(text=f"<b>{regular_cont_pct:.4f}%</b><br>Regular",
                         x=0.5, y=0.58, font_size=14, showarrow=False),
                    dict(text=f"Trader: {trader_cont_pct:.6f}%",
                         x=0.5, y=0.32, font_size=10, showarrow=False, font_color="#94a3b8"),
                ])
            st.plotly_chart(fig2, use_container_width=True)

    else:  # LSI
        sku_total = store_total["SKU Total"]
        sku_sale  = store_total["SKU Sale"]
        sku_cont  = store_total["SKU Cont%"]
        oos       = store_total["OOS"]

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
            st.markdown(metric_card("SKU Sell-Through", f"{sku_cont:.1f}%", "teal",
                                    "% SKU promo terjual"), unsafe_allow_html=True)
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
                hole=0.55, marker_colors=["#8b5cf6","#e2e8f0"],
                textinfo="label+percent", textfont_size=13,
            ))
            fig1.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=260,
                annotations=[dict(text=f"<b>{lm_cont:.2f}%</b><br>LM", x=0.5, y=0.5,
                                  font_size=16, showarrow=False)])
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">SKU Promo: Terjual vs OOS vs Belum Terjual</div>', unsafe_allow_html=True)
            oos_val    = int(oos)
            sold_val   = int(sku_sale)
            unsold_val = max(0, int(sku_total) - sold_val - oos_val)
            fig_sku = go.Figure(go.Pie(
                labels=["Terjual","OOS","Belum Terjual"],
                values=[sold_val, oos_val, unsold_val],
                hole=0.55, marker_colors=["#22c55e","#ef4444","#e2e8f0"],
                textinfo="label+percent", textfont_size=12,
            ))
            fig_sku.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=260,
                annotations=[dict(text=f"<b>{sku_cont:.1f}%</b><br>Sell-Through",
                                  x=0.5, y=0.5, font_size=14, showarrow=False)])
            st.plotly_chart(fig_sku, use_container_width=True)

        st.markdown('<div class="section-title">Breakdown Net Sales LM: Trader vs Prof vs Others</div>', unsafe_allow_html=True)
        lm_trader = store_df["LM Trader NS"].sum()
        lm_prof   = store_df["LM Prof NS"].sum()
        lm_others = store_df["LM Others NS"].sum()
        fig_lm = go.Figure(go.Bar(
            x=["Trader","Professional","Others"],
            y=[lm_trader, lm_prof, lm_others],
            marker_color=["#f97316","#3b82f6","#94a3b8"],
            text=[f"{v/lm_ns*100:.1f}%" if lm_ns else "0%" for v in [lm_trader, lm_prof, lm_others]],
            textposition="outside",
        ))
        fig_lm.update_layout(height=300, margin=dict(t=30,b=10,l=10,r=10),
            plot_bgcolor="white", yaxis=dict(gridcolor="#f1f5f9"),
            yaxis_title="Net Sales LM (Rp 000)")
        st.plotly_chart(fig_lm, use_container_width=True)

    # ── Group contribution bar (both portals) ──
    st.markdown('<div class="section-title">Kontribusi LM per Grup Kategori</div>', unsafe_allow_html=True)
    grp_data = cat_df.groupby("Group").agg(Total_NS=("Total NS","sum"), LM_NS=("LM NS","sum")).reset_index()
    grp_data["LM_Cont"] = grp_data["LM_NS"] / grp_data["Total_NS"] * 100
    grp_data = grp_data.sort_values("LM_Cont", ascending=False)
    bar_color_main = "#8b5cf6" if portal_label == "LSI" else "#3b82f6"
    bar_color_dim  = "#c4b5fd" if portal_label == "LSI" else "#93c5fd"
    colors = [bar_color_main if v >= 20 else bar_color_dim for v in grp_data["LM_Cont"]]
    fig3 = go.Figure(go.Bar(
        x=grp_data["Group"], y=grp_data["LM_Cont"],
        marker_color=colors,
        text=[f"{v:.1f}%" for v in grp_data["LM_Cont"]], textposition="outside",
    ))
    fig3.add_hline(y=lm_cont, line_dash="dash", line_color="#f97316",
                   annotation_text=f"Avg: {lm_cont:.2f}%", annotation_position="top right")
    fig3.update_layout(height=320, margin=dict(t=30,b=20,l=10,r=10),
        yaxis_title="LM Contribution (%)",
        yaxis_range=[0, grp_data["LM_Cont"].max()*1.2],
        plot_bgcolor="white", yaxis=dict(gridcolor="#f1f5f9"))
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
            st.markdown(metric_card("Avg SKU Sell-Through", f"{filtered['SKU Cont%'].mean():.1f}%", "teal"), unsafe_allow_html=True)
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

    bar_color = "#8b5cf6" if portal_label == "LSI" else "#3b82f6"
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-title">Total Net Sales per Store (LM vs Normal)</div>', unsafe_allow_html=True)
        sorted_store = filtered.sort_values("Total NS", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=sorted_store["Store Name"], x=sorted_store["Normal NS"],
            name="Normal", orientation="h", marker_color="#e2e8f0",
            text=[f"{v:,.0f}" for v in sorted_store["Normal NS"]],
            textposition="inside", textfont_color="gray",
        ))
        fig.add_trace(go.Bar(
            y=sorted_store["Store Name"], x=sorted_store["LM NS"],
            name="LM (Promo)", orientation="h", marker_color=bar_color,
            text=[f"{v:,.0f}" for v in sorted_store["LM NS"]],
            textposition="inside", textfont_color="white",
        ))
        fig.update_layout(barmode="stack", height=max(420, len(filtered)*28),
            margin=dict(t=20,b=20,l=10,r=20), legend=dict(orientation="h", y=1.05),
            xaxis_title="Net Sales (Rp 000)", plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">LM Contribution % per Store</div>', unsafe_allow_html=True)
        sorted_lm = filtered.sort_values("LM Cont%", ascending=True)
        thresh_low = 5 if portal_label == "LSI" else 10
        thresh_mid = 10 if portal_label == "LSI" else 20
        colors = ["#ef4444" if v < thresh_low else "#f97316" if v < thresh_mid else "#22c55e"
                  for v in sorted_lm["LM Cont%"]]
        fig2 = go.Figure(go.Bar(
            y=sorted_lm["Store Name"], x=sorted_lm["LM Cont%"],
            orientation="h", marker_color=colors,
            text=[f"{v:.1f}%" for v in sorted_lm["LM Cont%"]], textposition="outside",
        ))
        fig2.add_vline(x=filtered["LM Cont%"].mean(), line_dash="dash", line_color="#94a3b8",
                       annotation_text="Avg", annotation_position="top")
        fig2.update_layout(height=max(420, len(filtered)*28),
            margin=dict(t=20,b=20,l=10,r=40),
            xaxis_title="LM Contribution (%)", plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
        st.plotly_chart(fig2, use_container_width=True)

    # ── SKU Section (LSI only) ──
    if portal_label == "LSI":
        st.markdown("---")
        st.markdown("### 📦 SKU Performance per Store")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-title">SKU Sell-Through % per Store</div>', unsafe_allow_html=True)
            sorted_sku = filtered.sort_values("SKU Cont%", ascending=True)
            sku_colors = ["#ef4444" if v < 60 else "#f97316" if v < 75 else "#22c55e" for v in sorted_sku["SKU Cont%"]]
            fig_sku = go.Figure(go.Bar(
                y=sorted_sku["Store Name"], x=sorted_sku["SKU Cont%"],
                orientation="h", marker_color=sku_colors,
                text=[f"{v:.1f}%" for v in sorted_sku["SKU Cont%"]], textposition="outside",
            ))
            fig_sku.add_vline(x=filtered["SKU Cont%"].mean(), line_dash="dash", line_color="#94a3b8",
                              annotation_text="Avg")
            fig_sku.update_layout(height=max(420, len(filtered)*22),
                margin=dict(t=20,b=20,l=10,r=50),
                xaxis_title="SKU Sell-Through (%)", plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
            st.plotly_chart(fig_sku, use_container_width=True)

        with col4:
            st.markdown('<div class="section-title">OOS per Store</div>', unsafe_allow_html=True)
            sorted_oos = filtered.sort_values("OOS", ascending=True)
            oos_colors = ["#22c55e" if v <= 15 else "#f97316" if v <= 40 else "#ef4444" for v in sorted_oos["OOS"]]
            fig_oos = go.Figure(go.Bar(
                y=sorted_oos["Store Name"], x=sorted_oos["OOS"],
                orientation="h", marker_color=oos_colors,
                text=[f"{int(v)}" for v in sorted_oos["OOS"]], textposition="outside",
            ))
            fig_oos.update_layout(height=max(420, len(filtered)*22),
                margin=dict(t=20,b=20,l=10,r=50),
                xaxis_title="Jumlah SKU OOS", plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
            st.plotly_chart(fig_oos, use_container_width=True)

        st.markdown('<div class="section-title">Posisi Store: SKU Sell-Through vs OOS (ukuran = Total NS)</div>', unsafe_allow_html=True)
        fig_sc2 = px.scatter(filtered, x="OOS", y="SKU Cont%",
            text="Store Name", size="Total NS", color="LM Cont%",
            color_continuous_scale="Purples",
            hover_data={"SKU Total":True,"SKU Sale":True,"LM NS":":,.0f"})
        fig_sc2.update_traces(textposition="top center", textfont_size=9)
        fig_sc2.update_layout(height=420, margin=dict(t=20,b=20,l=10,r=10),
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#f1f5f9"), yaxis=dict(gridcolor="#f1f5f9"),
            xaxis_title="Jumlah OOS", yaxis_title="SKU Sell-Through (%)",
            coloraxis_showscale=False)
        st.plotly_chart(fig_sc2, use_container_width=True)

        st.markdown('<div class="section-title">Breakdown LM Sales: Trader / Prof / Others per Store</div>', unsafe_allow_html=True)
        sorted_br = filtered.sort_values("LM NS", ascending=True)
        fig_br = go.Figure()
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Trader NS"],
            name="Trader", orientation="h", marker_color="#f97316"))
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Prof NS"],
            name="Professional", orientation="h", marker_color="#3b82f6"))
        fig_br.add_trace(go.Bar(y=sorted_br["Store Name"], x=sorted_br["LM Others NS"],
            name="Others", orientation="h", marker_color="#94a3b8"))
        fig_br.update_layout(barmode="stack", height=max(420, len(filtered)*22),
            margin=dict(t=20,b=20,l=10,r=20), legend=dict(orientation="h", y=1.05),
            xaxis_title="Net Sales LM (Rp 000)", plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
        st.plotly_chart(fig_br, use_container_width=True)

    # ── Scatter NS vs LM% ──
    st.markdown('<div class="section-title">Posisi Store: Total NS vs LM Contribution%</div>', unsafe_allow_html=True)
    sc_color = "Purples" if portal_label == "LSI" else "Blues"
    fig3 = px.scatter(filtered, x="Total NS", y="LM Cont%",
        text="Store Name", size="Total NS", color="LM Cont%",
        color_continuous_scale=sc_color,
        hover_data={"LM NS":":,.0f","Normal NS":":,.0f","Total NS":":,.0f"})
    fig3.update_traces(textposition="top center", textfont_size=10)
    fig3.add_hline(y=filtered["LM Cont%"].mean(), line_dash="dot", line_color="#94a3b8")
    fig3.add_vline(x=filtered["Total NS"].mean(), line_dash="dot", line_color="#94a3b8")
    fig3.update_layout(height=400, margin=dict(t=20,b=20,l=10,r=10),
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#f1f5f9"), yaxis=dict(gridcolor="#f1f5f9"),
        xaxis_title="Total Net Sales (Rp 000)", yaxis_title="LM Contribution (%)",
        coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

    # ── Data Table ──
    st.markdown('<div class="section-title">📋 Detail Data per Store</div>', unsafe_allow_html=True)
    if portal_label == "LSI":
        disp = ["Store Name","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
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
            pct_sku = sale_sku/total_sku*100 if total_sku else 0
            st.markdown(metric_card("SKU Sell-Through", f"{pct_sku:.1f}%", "teal",
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
    fig_tree.update_layout(height=420, margin=dict(t=20,b=10,l=10,r=10))
    fig_tree.update_coloraxes(colorbar_title="LM Cont%")
    st.plotly_chart(fig_tree, use_container_width=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="section-title">LM Contribution% vs Total NS per Kategori</div>', unsafe_allow_html=True)
        fig_bub = px.scatter(cat_filtered[cat_filtered["Total NS"]>1],
            x="Total NS", y="LM Cont%", size="Total NS", color="Group",
            text="Category", hover_data={"LM NS":":,.0f","Normal NS":":,.0f"})
        fig_bub.update_traces(textposition="top center", textfont_size=9)
        fig_bub.add_hline(y=lm_pct, line_dash="dot", line_color="#94a3b8",
                          annotation_text=f"Avg {lm_pct:.1f}%")
        fig_bub.update_layout(height=420, margin=dict(t=20,b=20,l=10,r=10),
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#f1f5f9"), yaxis=dict(gridcolor="#f1f5f9"),
            xaxis_title="Total Net Sales (Rp 000)", yaxis_title="LM Contribution (%)",
            legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_bub, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Top 10 Kategori by LM NS</div>', unsafe_allow_html=True)
        top10 = cat_filtered.nlargest(10,"LM NS").sort_values("LM NS")
        bar_color = "#8b5cf6" if portal_label == "LSI" else "#3b82f6"
        fig_h = go.Figure(go.Bar(y=top10["Category"], x=top10["LM NS"],
            orientation="h", marker_color=bar_color,
            text=[f"{v:,.0f}" for v in top10["LM NS"]], textposition="outside"))
        fig_h.update_layout(height=420, margin=dict(t=20,b=20,l=10,r=70),
            plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"),
            xaxis_title="LM Net Sales (Rp 000)")
        st.plotly_chart(fig_h, use_container_width=True)

    # ── SKU by Category (LSI only) ──
    if portal_label == "LSI":
        st.markdown("---")
        st.markdown("### 📦 SKU Performance per Kategori")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-title">SKU Sell-Through % per Kategori</div>', unsafe_allow_html=True)
            sku_cat = cat_filtered[cat_filtered["SKU Total"] > 0].sort_values("SKU Cont%", ascending=True)
            sku_colors = ["#ef4444" if v < 60 else "#f97316" if v < 75 else "#22c55e" for v in sku_cat["SKU Cont%"]]
            fig_sc = go.Figure(go.Bar(
                y=sku_cat["Category"], x=sku_cat["SKU Cont%"],
                orientation="h", marker_color=sku_colors,
                text=[f"{v:.1f}%" for v in sku_cat["SKU Cont%"]], textposition="outside"))
            fig_sc.add_vline(x=sku_cat["SKU Cont%"].mean(), line_dash="dash", line_color="#94a3b8",
                             annotation_text="Avg")
            fig_sc.update_layout(height=500, margin=dict(t=20,b=20,l=10,r=50),
                plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"),
                xaxis_title="SKU Sell-Through (%)")
            st.plotly_chart(fig_sc, use_container_width=True)

        with col4:
            st.markdown('<div class="section-title">OOS per Kategori</div>', unsafe_allow_html=True)
            oos_cat = cat_filtered[cat_filtered["OOS"] > 0].sort_values("OOS", ascending=True)
            oos_colors = ["#22c55e" if v <= 10 else "#f97316" if v <= 50 else "#ef4444" for v in oos_cat["OOS"]]
            fig_oc = go.Figure(go.Bar(
                y=oos_cat["Category"], x=oos_cat["OOS"],
                orientation="h", marker_color=oos_colors,
                text=[f"{int(v)}" for v in oos_cat["OOS"]], textposition="outside"))
            fig_oc.update_layout(height=500, margin=dict(t=20,b=20,l=10,r=50),
                plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"),
                xaxis_title="Jumlah SKU OOS")
            st.plotly_chart(fig_oc, use_container_width=True)

        st.markdown('<div class="section-title">SKU Total vs Terjual per Kategori (ukuran = OOS, warna = Sell-Through%)</div>', unsafe_allow_html=True)
        sku_sc_df = cat_filtered[cat_filtered["SKU Total"] > 0].copy()
        fig_sku_sc = px.scatter(sku_sc_df, x="SKU Total", y="SKU Sale",
            size="OOS", color="SKU Cont%", text="Category",
            color_continuous_scale="RdYlGn",
            hover_data={"OOS":True,"LM Cont%":":.2f"})
        fig_sku_sc.update_traces(textposition="top center", textfont_size=9)
        max_val = sku_sc_df["SKU Total"].max()
        fig_sku_sc.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val],
            mode="lines", line=dict(dash="dot", color="#94a3b8"), name="100% Sell-Through",
            showlegend=True))
        fig_sku_sc.update_layout(height=420, margin=dict(t=20,b=20,l=10,r=10),
            plot_bgcolor="white",
            xaxis=dict(gridcolor="#f1f5f9"), yaxis=dict(gridcolor="#f1f5f9"),
            xaxis_title="SKU Total", yaxis_title="SKU Terjual",
            coloraxis_colorbar_title="Sell-Through%")
        st.plotly_chart(fig_sku_sc, use_container_width=True)

    # ── Group summary ──
    st.markdown('<div class="section-title">LM vs Normal per Grup Kategori</div>', unsafe_allow_html=True)
    grp_sum = cat_filtered.groupby("Group")[["LM NS","Normal NS","Total NS"]].sum().reset_index()
    grp_sum = grp_sum.sort_values("Total NS", ascending=False)
    fig_grp = go.Figure()
    fig_grp.add_trace(go.Bar(name="LM (Promo)", x=grp_sum["Group"], y=grp_sum["LM NS"],
        marker_color="#8b5cf6" if portal_label=="LSI" else "#3b82f6",
        text=[f"{v/t*100:.1f}%" for v,t in zip(grp_sum["LM NS"],grp_sum["Total NS"])],
        textposition="outside"))
    fig_grp.add_trace(go.Bar(name="Normal", x=grp_sum["Group"], y=grp_sum["Normal NS"],
        marker_color="#e2e8f0"))
    fig_grp.update_layout(barmode="group", height=340,
        margin=dict(t=30,b=20,l=10,r=10), legend=dict(orientation="h", y=1.08),
        yaxis_title="Net Sales (Rp 000)", plot_bgcolor="white", yaxis=dict(gridcolor="#f1f5f9"))
    st.plotly_chart(fig_grp, use_container_width=True)

    # ── Data Table ──
    st.markdown('<div class="section-title">📋 Detail Data per Kategori</div>', unsafe_allow_html=True)
    if portal_label == "LSI":
        disp = ["Group","Category","Total NS","Normal NS","LM NS","LM Cont%",
                "LM Trader NS","LM Prof NS","LM Others NS",
                "SKU Total","SKU Sale","SKU Cont%","OOS"]
        fmt  = {"Total NS":"{:,.1f}","Normal NS":"{:,.1f}","LM NS":"{:,.1f}",
                "LM Cont%":"{:.2f}%","LM Trader NS":"{:,.1f}","LM Prof NS":"{:,.1f}",
                "LM Others NS":"{:,.1f}","SKU Total":"{:,.0f}","SKU Sale":"{:,.0f}",
                "SKU Cont%":"{:.2f}%","OOS":"{:,.0f}"}
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