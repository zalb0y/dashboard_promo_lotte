"""
Home Page - Promo Dashboard Landing
Select between Mailer and Big Banner dashboards.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.dashboard_core import apply_custom_css

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Promo Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply custom CSS
apply_custom_css()

# ─── CUSTOM CSS FOR HOME PAGE ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide sidebar completely on home page */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    /* Center the main block content */
    .block-container {
        max-width: 1200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .home-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00d4ff 0%, #9b5de5 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .home-subtitle {
        font-size: 1.1rem;
        color: #a0aec0;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .promo-card {
        background: linear-gradient(145deg, #1e2a4a 0%, #2d3a5a 100%);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        transition: all 0.4s ease;
        cursor: pointer;
        text-align: center;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .promo-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,212,255,0.25);
        border-color: rgba(0,212,255,0.4);
    }
    
    .promo-card.mailer {
        border-top: 4px solid #00d4ff;
    }
    .promo-card.mailer:hover {
        box-shadow: 0 20px 60px rgba(0,212,255,0.3);
    }
    
    .promo-card.banner {
        border-top: 4px solid #9b5de5;
    }
    .promo-card.banner:hover {
        box-shadow: 0 20px 60px rgba(155,93,229,0.3);
    }
    
    .promo-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .promo-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.8rem;
    }
    
    .promo-desc {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .promo-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .promo-tag {
        background: rgba(0,212,255,0.1);
        color: #00d4ff;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .promo-tag.purple {
        background: rgba(155,93,229,0.1);
        color: #c084fc;
    }
    .promo-tag.green {
        background: rgba(0,245,212,0.1);
        color: #00f5d4;
    }
    .promo-tag.amber {
        background: rgba(254,228,64,0.1);
        color: #fee440;
    }
    
    .enter-btn {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: #ffffff;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .enter-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(0,212,255,0.4);
    }
    .enter-btn.purple {
        background: linear-gradient(135deg, #9b5de5 0%, #7b2cbf 100%);
    }
    .enter-btn.purple:hover {
        box-shadow: 0 8px 24px rgba(155,93,229,0.4);
    }
    
    .footer-info {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    .footer-info p {
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown('<h1 class="home-title">📊 Promo Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="home-subtitle">Analisis Net Sales & Performance Promosi</p>', unsafe_allow_html=True)

# ─── PROMO TYPE SELECTION ───────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="promo-card mailer">
        <div class="promo-icon">📄</div>
        <div class="promo-title">Mailer</div>
        <div class="promo-desc">
            Dashboard untuk promo Mailer dengan periode 2 mingguan.
        </div>
        <div class="promo-tags">
            <span class="promo-tag">LMI</span>
            <span class="promo-tag purple">LSI</span>
            <span class="promo-tag green">Bi-Weekly</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📄 Buka Dashboard Mailer", key="btn_mailer", use_container_width=True):
        st.switch_page("pages/Mailer.py")

with col2:
    st.markdown("""
    <div class="promo-card banner">
        <div class="promo-icon">🏷️</div>
        <div class="promo-title">Big Banner</div>
        <div class="promo-desc">
            Dashboard untuk promo Big Banner dengan periode mingguan.
        </div>
        <div class="promo-tags">
            <span class="promo-tag green">Hijau</span>
            <span class="promo-tag amber">Cokelat</span>
            <span class="promo-tag">End User</span>
            <span class="promo-tag purple">Weekly</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏷️ Buka Dashboard Big Banner", key="btn_banner", use_container_width=True):
        st.switch_page("pages/Big_Banner.py")

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-info">
    <p>💡 Pilih dashboard sesuai dengan tipe promo yang ingin dianalisis</p>
    <p>Data: Net Sales dalam IDR</p>
</div>
""", unsafe_allow_html=True)
