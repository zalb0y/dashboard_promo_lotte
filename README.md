# 📊 Net Sales Dashboard – LM1 Jan 2026

Dashboard Streamlit interaktif untuk analisis Net Sales periode **1–14 Januari 2026** secara Nasional.

## 📁 Struktur Project

```
antigravity_project/
├── app.py                        # Main Streamlit app
├── requirements.txt              # Python dependencies
├── LM1_114_Jan_Nasional.xlsx     # Data source (2 sheet: By Store & By Cat)
└── README.md
```

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan dashboard
```bash
streamlit run app.py
```

### 3. Buka di browser
Dashboard akan terbuka otomatis di `http://localhost:8501`

---

## 📊 Fitur Dashboard

### 🏠 Overview
- KPI cards: Total NS, LM Sales, Normal Sales, Trader Sales
- Donut chart komposisi LM vs Normal
- Donut chart Regular vs Trader
- Bar chart kontribusi LM per grup kategori
- Key Insights otomatis

### 🏪 By Store
- KPI per store (jumlah store, avg LM Cont%, top revenue store)
- Stacked bar: LM vs Normal per store
- Bar horizontal: LM Contribution% per store (color-coded)
- Scatter plot: Total NS vs LM Contribution%
- Komposisi Regular vs Trader per store
- Data table dengan highlight
- Key Insights

### 📦 By Category
- Filter grup kategori (multiselect)
- KPI cards
- Treemap: Net Sales by Group > Category (diwarnai LM Cont%)
- Bubble chart: LM Cont% vs Total NS
- Top 10 kategori by LM NS
- Group summary bar chart
- Heatmap kontribusi LM per kategori
- Data table
- Key Insights

---

## 📌 Keterangan Data

| Kolom | Keterangan |
|-------|-----------|
| LM NS | Net Sales dari produk promo (flyer) |
| Normal NS | Net Sales dari produk non-promo |
| LM Cont% | Kontribusi LM terhadap total Net Sales |
| Regular NS | Net Sales dari Customer End User |
| Trader NS | Net Sales dari Customer Trader |
| Regular Cont% / Trader Cont% | Kontribusi masing-masing segmen customer |

> Semua angka dalam **ribuan Rupiah (Rp 000)**
