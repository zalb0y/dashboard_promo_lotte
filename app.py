<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LOTTE MART ALAM SUTERA - Harga Promo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #E31837;
            --primary-dark: #B71430;
            --secondary: #FFD100;
            --accent: #00A651;
            --bg-main: #F5F5F7;
            --bg-card: #FFFFFF;
            --text-primary: #1D1D1F;
            --text-secondary: #6E6E73;
            --text-muted: #86868B;
            --border: #D2D2D7;
            --bblm-badge: #E31837;
            --normal-badge: #00A651;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
            --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-main);
            color: var(--text-primary);
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 20px 16px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-lg);
        }
        
        .header-content { max-width: 1200px; margin: 0 auto; }
        
        .store-name {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }
        
        .member-type {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.15);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        .member-type::before {
            content: '';
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 6px var(--accent);
        }
        
        .date-info {
            margin-top: 12px;
            font-size: 0.75rem;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .date-info svg { width: 14px; height: 14px; }
        
        /* Stats Bar */
        .stats-bar {
            display: flex;
            gap: 12px;
            margin-top: 16px;
            overflow-x: auto;
            padding-bottom: 4px;
            scrollbar-width: none;
        }
        
        .stats-bar::-webkit-scrollbar { display: none; }
        
        .stat-item {
            flex-shrink: 0;
            background: rgba(255,255,255,0.1);
            padding: 8px 14px;
            border-radius: var(--radius-md);
            backdrop-filter: blur(10px);
        }
        
        .stat-value {
            font-size: 1.1rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .stat-label {
            font-size: 0.65rem;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Filter Section */
        .filter-section {
            background: var(--bg-card);
            padding: 16px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 130px;
            z-index: 90;
        }
        
        .filter-container { max-width: 1200px; margin: 0 auto; }
        
        /* Search Box */
        .search-box {
            position: relative;
            margin-bottom: 12px;
        }
        
        .search-box input {
            width: 100%;
            padding: 14px 16px 14px 46px;
            border: 2px solid var(--border);
            border-radius: var(--radius-lg);
            font-size: 1rem;
            font-family: inherit;
            transition: all 0.2s;
            background: var(--bg-main);
        }
        
        .search-box input:focus {
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 4px rgba(227, 24, 55, 0.1);
        }
        
        .search-box svg {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            color: var(--text-muted);
        }
        
        /* Filter Pills */
        .filter-row {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            scrollbar-width: none;
            margin-bottom: 8px;
        }
        
        .filter-row::-webkit-scrollbar { display: none; }
        .filter-row:last-child { margin-bottom: 0; }
        
        .filter-label {
            flex-shrink: 0;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 8px 0;
            min-width: 60px;
        }
        
        .filter-pill {
            flex-shrink: 0;
            padding: 8px 16px;
            border: 1.5px solid var(--border);
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
            white-space: nowrap;
        }
        
        .filter-pill:hover { border-color: var(--primary); color: var(--primary); }
        
        .filter-pill.active {
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }
        
        .filter-pill.bblm { border-color: var(--bblm-badge); color: var(--bblm-badge); }
        .filter-pill.bblm.active { background: var(--bblm-badge); color: white; }
        .filter-pill.normal { border-color: var(--normal-badge); color: var(--normal-badge); }
        .filter-pill.normal.active { background: var(--normal-badge); color: white; }
        
        /* Category Select */
        .category-select {
            padding: 10px 14px;
            border: 1.5px solid var(--border);
            border-radius: var(--radius-md);
            font-size: 0.85rem;
            font-family: inherit;
            background: white;
            cursor: pointer;
            min-width: 120px;
            flex-shrink: 0;
        }
        
        .category-select:focus { outline: none; border-color: var(--primary); }
        
        /* Sort Buttons */
        .sort-btn {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 8px 12px;
            border: 1.5px solid var(--border);
            border-radius: var(--radius-md);
            font-size: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        .sort-btn:hover, .sort-btn.active { border-color: var(--primary); color: var(--primary); }
        .sort-btn svg { width: 12px; height: 12px; }
        
        /* Main Content */
        .main-content { max-width: 1200px; margin: 0 auto; padding: 16px; }
        
        .results-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 0 4px;
        }
        
        .results-count { font-size: 0.85rem; color: var(--text-secondary); }
        .results-count strong { color: var(--text-primary); font-weight: 600; }
        
        /* Product Cards */
        .product-list { display: flex; flex-direction: column; gap: 12px; }
        
        .product-card {
            background: var(--bg-card);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
            overflow: hidden;
            transition: all 0.2s;
        }
        
        .product-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
        
        .product-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 14px 14px 10px;
            gap: 10px;
        }
        
        .product-info { flex: 1; min-width: 0; }
        
        .product-code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        
        .product-name {
            font-size: 0.95rem;
            font-weight: 600;
            line-height: 1.3;
            color: var(--text-primary);
        }
        
        .product-badges { display: flex; gap: 6px; flex-shrink: 0; }
        
        .badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge-bblm { background: var(--bblm-badge); color: white; }
        .badge-normal { background: var(--normal-badge); color: white; }
        .badge-weight { background: var(--bg-main); color: var(--text-secondary); }
        
        /* Product Meta */
        .product-meta {
            display: flex;
            gap: 16px;
            padding: 0 14px 12px;
            font-size: 0.75rem;
        }
        
        .meta-item { display: flex; align-items: center; gap: 4px; color: var(--text-secondary); }
        .meta-item svg { width: 14px; height: 14px; }
        .meta-value { font-weight: 600; color: var(--text-primary); }
        .stock-low { color: #FF9500; }
        .stock-out { color: var(--primary); }
        
        /* Category Tags */
        .category-tags { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 14px 12px; }
        
        .category-tag {
            padding: 4px 10px;
            background: var(--bg-main);
            border-radius: 8px;
            font-size: 0.7rem;
            color: var(--text-secondary);
        }
        
        /* Price Table */
        .price-table-wrapper { overflow-x: auto; border-top: 1px solid var(--border); }
        
        .price-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.75rem;
            min-width: 400px;
        }
        
        .price-table th {
            background: var(--bg-main);
            padding: 10px 12px;
            text-align: center;
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--border);
        }
        
        .price-table th:first-child { text-align: left; padding-left: 14px; }
        
        .price-table td {
            padding: 10px 12px;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }
        
        .price-table td:first-child {
            text-align: left;
            padding-left: 14px;
            font-weight: 500;
            color: var(--text-secondary);
        }
        
        .price-table tr:last-child td { border-bottom: none; }
        
        .price-table .price-cell {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            color: var(--primary);
        }
        
        .price-table .qty-cell { color: var(--text-secondary); }
        
        /* Loading State */
        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px 20px;
            text-align: center;
        }
        
        .loading-spinner {
            width: 48px;
            height: 48px;
            border: 4px solid var(--border);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 16px;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .loading-text { color: var(--text-secondary); font-size: 0.9rem; }
        
        /* Empty State */
        .empty-state { text-align: center; padding: 60px 20px; }
        .empty-state svg { width: 80px; height: 80px; color: var(--text-muted); margin-bottom: 16px; }
        .empty-state h3 { font-size: 1.1rem; margin-bottom: 8px; color: var(--text-primary); }
        .empty-state p { color: var(--text-secondary); font-size: 0.9rem; }
        
        /* Error State */
        .error-state {
            background: #FFF5F5;
            border: 1px solid #FED7D7;
            border-radius: var(--radius-lg);
            padding: 20px;
            text-align: center;
            margin: 20px;
        }
        
        .error-state h3 { color: var(--primary); margin-bottom: 8px; }
        .error-state p { color: var(--text-secondary); font-size: 0.85rem; }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 24px 16px;
            color: var(--text-muted);
            font-size: 0.75rem;
        }
        
        /* Responsive */
        @media (min-width: 768px) {
            .header { padding: 24px; }
            .store-name { font-size: 1.5rem; }
            .filter-section { padding: 20px 24px; }
            .main-content { padding: 24px; }
            .product-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
                gap: 16px;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <h1 class="store-name">🛒 LOTTE MART ALAM SUTERA</h1>
            <div class="member-type" id="memberType">MEMBER HIJAU GOLD</div>
            <div class="date-info" id="dateInfo">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Memuat data...</span>
            </div>
            <div class="stats-bar" id="statsBar">
                <div class="stat-item">
                    <div class="stat-value" id="totalProducts">-</div>
                    <div class="stat-label">Total Produk</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="bblmCount">-</div>
                    <div class="stat-label">Promo BBLM</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="normalCount">-</div>
                    <div class="stat-label">Normal</div>
                </div>
            </div>
        </div>
    </header>
    
    <!-- Filter Section -->
    <section class="filter-section">
        <div class="filter-container">
            <!-- Search -->
            <div class="search-box">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input type="text" id="searchInput" placeholder="Cari nama produk..." oninput="filterProducts()">
            </div>
            
            <!-- Status Filter -->
            <div class="filter-row">
                <span class="filter-label">Status</span>
                <button class="filter-pill active" data-status="all" onclick="setStatusFilter('all', this)">Semua</button>
                <button class="filter-pill bblm" data-status="bblm" onclick="setStatusFilter('bblm', this)">🔥 BBLM</button>
                <button class="filter-pill normal" data-status="normal" onclick="setStatusFilter('normal', this)">✓ Normal</button>
            </div>
            
            <!-- Category Filter -->
            <div class="filter-row">
                <span class="filter-label">Category</span>
                <select class="category-select" id="categoryFirst" onchange="filterProducts()">
                    <option value="">All Category</option>
                </select>
                <select class="category-select" id="categorySecond" onchange="filterProducts()">
                    <option value="">All Second</option>
                </select>
            </div>
            
            <!-- Sort -->
            <div class="filter-row">
                <span class="filter-label">Sort</span>
                <button class="sort-btn active" data-sort="name" onclick="setSort('name', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                    </svg>
                    Nama A-Z
                </button>
                <button class="sort-btn" data-sort="name-desc" onclick="setSort('name-desc', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
                    </svg>
                    Nama Z-A
                </button>
                <button class="sort-btn" data-sort="category" onclick="setSort('category', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    Category
                </button>
                <button class="sort-btn" data-sort="stock" onclick="setSort('stock', this)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                    Stock
                </button>
            </div>
        </div>
    </section>
    
    <!-- Main Content -->
    <main class="main-content">
        <div class="results-info" id="resultsInfo" style="display: none;">
            <span class="results-count">Menampilkan <strong id="filteredCount">0</strong> dari <strong id="totalCount">0</strong> produk</span>
        </div>
        
        <div id="productContainer">
            <div class="loading">
                <div class="loading-spinner"></div>
                <p class="loading-text">Memuat data produk...</p>
            </div>
        </div>
    </main>
    
    <!-- Footer -->
    <footer class="footer">
        <p>© 2026 LOTTE MART ALAM SUTERA</p>
        <p>Data diperbarui setiap hari</p>
    </footer>
    
    <script>
        // ========================================
        // CONFIGURATION - GANTI URL INI!
        // ========================================
        const API_URL = 'https://script.google.com/macros/s/AKfycbyYJ2gas1y5EvLZYhOkKJF1S8_4h3kUXl0T0AUBuMS9WstulOhPxhvPjuxG4H0nRWXQOA/exec';
        
        // ========================================
        // STATE
        // ========================================
        let allProducts = [];
        let filteredProducts = [];
        let categories = { first: [], second: [], third: [], fourth: [] };
        let meta = {};
        let currentStatusFilter = 'all';
        let currentSort = 'name';
        let hasLevel4MinMax = false;
        let hasLevel5MinMax = false;
        
        // ========================================
        // INITIALIZATION
        // ========================================
        document.addEventListener('DOMContentLoaded', loadData);
        
        // ========================================
        // DATA LOADING
        // ========================================
        async function loadData() {
            showLoading();
            
            try {
                const response = await fetch(API_URL);
                const data = await response.json();
                
                if (data.success) {
                    processData(data);
                } else {
                    showError('Gagal memuat data: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error loading data:', error);
                showError('Tidak dapat terhubung ke server. Silakan refresh halaman.');
            }
        }
        
        // ========================================
        // DATA PROCESSING
        // ========================================
        function processData(data) {
            allProducts = data.products || [];
            categories = data.categories || { first: [], second: [], third: [], fourth: [] };
            meta = data.meta || {};
            hasLevel4MinMax = meta.hasLevel4MinMax || false;
            hasLevel5MinMax = meta.hasLevel5MinMax || false;
            
            // Update header
            if (meta.memberType) {
                document.getElementById('memberType').textContent = meta.memberType.replace(/^\d+-/, '').trim();
            }
            if (meta.reportDate) {
                document.getElementById('dateInfo').innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>Update: ${meta.reportDate}</span>
                `;
            }
            
            // Update stats
            const bblmCount = allProducts.filter(p => p.isBBLM).length;
            const normalCount = allProducts.filter(p => !p.isBBLM).length;
            document.getElementById('totalProducts').textContent = formatNumber(allProducts.length);
            document.getElementById('bblmCount').textContent = formatNumber(bblmCount);
            document.getElementById('normalCount').textContent = formatNumber(normalCount);
            
            populateCategoryFilters();
            filterProducts();
        }
        
        function populateCategoryFilters() {
            const firstSelect = document.getElementById('categoryFirst');
            const secondSelect = document.getElementById('categorySecond');
            
            firstSelect.innerHTML = '<option value="">All Category</option>';
            secondSelect.innerHTML = '<option value="">All Second</option>';
            
            categories.first.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                firstSelect.appendChild(option);
            });
            
            categories.second.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                secondSelect.appendChild(option);
            });
        }
        
        // ========================================
        // FILTERING & SORTING
        // ========================================
        function setStatusFilter(status, element) {
            currentStatusFilter = status;
            document.querySelectorAll('[data-status]').forEach(btn => btn.classList.remove('active'));
            element.classList.add('active');
            filterProducts();
        }
        
        function setSort(sort, element) {
            currentSort = sort;
            document.querySelectorAll('.sort-btn').forEach(btn => btn.classList.remove('active'));
            element.classList.add('active');
            filterProducts();
        }
        
        function filterProducts() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
            const categoryFirst = document.getElementById('categoryFirst').value;
            const categorySecond = document.getElementById('categorySecond').value;
            
            filteredProducts = allProducts.filter(product => {
                if (searchTerm && !product.name.toLowerCase().includes(searchTerm)) return false;
                if (currentStatusFilter === 'bblm' && !product.isBBLM) return false;
                if (currentStatusFilter === 'normal' && product.isBBLM) return false;
                if (categoryFirst && product.category.first !== categoryFirst) return false;
                if (categorySecond && product.category.second !== categorySecond) return false;
                return true;
            });
            
            filteredProducts.sort((a, b) => {
                switch (currentSort) {
                    case 'name': return a.name.localeCompare(b.name);
                    case 'name-desc': return b.name.localeCompare(a.name);
                    case 'category': return a.category.first.localeCompare(b.category.first) || a.category.second.localeCompare(b.category.second);
                    case 'stock': return b.stockQty - a.stockQty;
                    default: return 0;
                }
            });
            
            renderProducts();
        }
        
        // ========================================
        // RENDERING
        // ========================================
        function renderProducts() {
            const container = document.getElementById('productContainer');
            const resultsInfo = document.getElementById('resultsInfo');
            
            document.getElementById('filteredCount').textContent = formatNumber(filteredProducts.length);
            document.getElementById('totalCount').textContent = formatNumber(allProducts.length);
            resultsInfo.style.display = 'flex';
            
            if (filteredProducts.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3>Tidak ada produk ditemukan</h3>
                        <p>Coba ubah filter atau kata kunci pencarian</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = `
                <div class="product-list">
                    ${filteredProducts.map(product => renderProductCard(product)).join('')}
                </div>
            `;
        }
        
        function renderProductCard(product) {
            const stockClass = product.stockQty <= 0 ? 'stock-out' : product.stockQty < 10 ? 'stock-low' : '';
            const stockText = product.stockQty <= 0 ? 'Habis' : formatNumber(product.stockQty);
            
            const levels = [
                { name: 'Lv-1', data: product.levels.level1 },
                { name: 'Lv-2', data: product.levels.level2 },
                { name: 'Lv-3', data: product.levels.level3 }
            ];
            if (hasLevel4MinMax) levels.push({ name: 'Lv-4', data: product.levels.level4 });
            if (hasLevel5MinMax) levels.push({ name: 'Lv-5', data: product.levels.level5 });
            
            return `
                <div class="product-card">
                    <div class="product-header">
                        <div class="product-info">
                            <div class="product-code">#${product.code}</div>
                            <div class="product-name">${escapeHtml(product.name)}</div>
                        </div>
                        <div class="product-badges">
                            <span class="badge ${product.isBBLM ? 'badge-bblm' : 'badge-normal'}">
                                ${product.isBBLM ? '🔥 BBLM' : '✓ Normal'}
                            </span>
                            <span class="badge badge-weight">${product.weight}</span>
                        </div>
                    </div>
                    
                    <div class="product-meta">
                        <div class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                            </svg>
                            Stock: <span class="meta-value ${stockClass}">${stockText}</span>
                        </div>
                        <div class="meta-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Harga: <span class="meta-value">Rp ${formatNumber(product.salesPrice)}</span>
                        </div>
                    </div>
                    
                    <div class="category-tags">
                        ${product.category.first ? `<span class="category-tag">${escapeHtml(product.category.first)}</span>` : ''}
                        ${product.category.second ? `<span class="category-tag">${escapeHtml(product.category.second)}</span>` : ''}
                    </div>
                    
                    <div class="price-table-wrapper">
                        <table class="price-table">
                            <thead>
                                <tr>
                                    <th></th>
                                    ${levels.map(l => `<th>${l.name}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Min Qty</td>
                                    ${levels.map(l => `<td class="qty-cell">${l.data.min}</td>`).join('')}
                                </tr>
                                <tr>
                                    <td>Max Qty</td>
                                    ${levels.map(l => `<td class="qty-cell">${l.data.max}</td>`).join('')}
                                </tr>
                                <tr>
                                    <td>Harga</td>
                                    ${levels.map(l => `<td class="price-cell">Rp ${formatNumber(l.data.price)}</td>`).join('')}
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        }
        
        function showLoading() {
            document.getElementById('productContainer').innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    <p class="loading-text">Memuat data produk...</p>
                </div>
            `;
            document.getElementById('resultsInfo').style.display = 'none';
        }
        
        function showError(message) {
            document.getElementById('productContainer').innerHTML = `
                <div class="error-state">
                    <h3>⚠️ Terjadi Kesalahan</h3>
                    <p>${escapeHtml(message)}</p>
                    <p style="margin-top: 12px;"><button onclick="loadData()" style="padding: 10px 20px; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer;">Coba Lagi</button></p>
                </div>
            `;
        }
        
        // ========================================
        // UTILITIES
        // ========================================
        function formatNumber(num) { return new Intl.NumberFormat('id-ID').format(num); }
        function escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }
    </script>
</body>
</html>
