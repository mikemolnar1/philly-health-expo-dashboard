#!/usr/bin/env python3

import json

# Load the expanded data
with open('expanded_data.json', 'r') as f:
    organizations = json.load(f)

# Enhanced HTML template with new features
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Philadelphia Health Expo - Community Nonprofit Partners Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            line-height: 1.6;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #ffffff;
        }

        .header p {
            font-size: 1.1rem;
            color: #cbd5e1;
            opacity: 0.9;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #9ca3af;
            font-size: 0.9rem;
        }

        .controls {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .control-group label {
            font-size: 0.9rem;
            color: #cbd5e1;
            font-weight: 500;
        }

        .control-group input, .control-group select {
            padding: 10px 12px;
            background: #262626;
            border: 1px solid #404040;
            border-radius: 6px;
            color: #e0e0e0;
            font-size: 0.9rem;
        }

        .control-group input:focus, .control-group select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }

        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 10px 16px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: background 0.2s ease;
        }

        .btn:hover {
            background: #2563eb;
        }

        .btn-secondary {
            background: #6b7280;
        }

        .btn-secondary:hover {
            background: #4b5563;
        }

        .view-toggle {
            display: flex;
            background: #262626;
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid #404040;
        }

        .view-toggle button {
            padding: 10px 16px;
            background: transparent;
            border: none;
            color: #9ca3af;
            cursor: pointer;
            flex: 1;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .view-toggle button.active {
            background: #3b82f6;
            color: white;
        }

        .tier-filter, .zone-filter {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .tier-btn, .zone-btn {
            padding: 8px 12px;
            background: #262626;
            border: 1px solid #404040;
            color: #e0e0e0;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .tier-btn.active, .zone-btn.active {
            background: #059669;
            border-color: #059669;
            color: white;
        }

        .tier-btn.tier-1.active { background: #059669; }
        .tier-btn.tier-2.active { background: #d97706; }
        .tier-btn.tier-3.active { background: #dc2626; }

        .zone-btn.wellness.active { background: #10b981; }
        .zone-btn.career.active { background: #f59e0b; }
        .zone-btn.family.active { background: #ec4899; }
        .zone-btn.community.active { background: #8b5cf6; }

        .table-container {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: #262626;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            color: #cbd5e1;
            border-bottom: 1px solid #404040;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        th:hover {
            background: #374151;
        }

        th.sortable::after {
            content: ' ↕️';
            opacity: 0.5;
            font-size: 0.8rem;
        }

        th.sorted-asc::after {
            content: ' ↑';
            opacity: 1;
            color: #3b82f6;
        }

        th.sorted-desc::after {
            content: ' ↓';
            opacity: 1;
            color: #3b82f6;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid #2a2a2a;
            color: #e0e0e0;
        }

        tr:hover {
            background: #252525;
        }

        .tier-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
            color: white;
            min-width: 60px;
            justify-content: center;
        }

        .tier-1 { background: #059669; }
        .tier-2 { background: #d97706; }
        .tier-3 { background: #dc2626; }

        .zone-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
            color: white;
            min-width: 100px;
            justify-content: center;
        }

        .zone-wellness { background: #10b981; }
        .zone-career { background: #f59e0b; }
        .zone-family { background: #ec4899; }
        .zone-community { background: #8b5cf6; }

        .cards-view {
            display: none;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }

        .org-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .org-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }

        .org-card h3 {
            color: #3b82f6;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .org-card .details {
            display: grid;
            gap: 8px;
            font-size: 0.9rem;
        }

        .org-card .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .org-card .detail-label {
            color: #9ca3af;
            font-weight: 500;
            min-width: 80px;
        }

        .no-results {
            text-align: center;
            padding: 40px;
            color: #6b7280;
            font-size: 1.1rem;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #6b7280;
            font-size: 0.9rem;
        }

        .link-button {
            color: #3b82f6;
            text-decoration: none;
            padding: 4px 8px;
            border-radius: 4px;
            transition: background 0.2s ease;
        }

        .link-button:hover {
            background: rgba(59, 130, 246, 0.1);
        }

        @media (max-width: 768px) {
            .controls-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .table-wrapper {
                font-size: 0.8rem;
            }
            
            th, td {
                padding: 8px 12px;
            }

            .cards-view {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🏥 Philadelphia Health Expo</h1>
            <p>Community Nonprofit Partners - Comprehensive Resource Directory</p>
            <p style="font-size: 0.9rem; margin-top: 10px;">1101 Arch St, Philadelphia, PA 19107 • Lat: 39.9536, Lon: -75.1592</p>
        </header>

        <section class="stats" id="stats">
            <!-- Stats will be populated by JavaScript -->
        </section>

        <section class="controls">
            <div class="controls-grid">
                <div class="control-group">
                    <label for="search">🔍 Search by Name or City</label>
                    <input type="text" id="search" placeholder="Search organizations..." />
                </div>
                
                <div class="control-group">
                    <label for="category">🏷️ Filter by Category</label>
                    <select id="category">
                        <option value="">All Categories</option>
                        <!-- Options populated by JavaScript -->
                    </select>
                </div>

                <div class="control-group">
                    <label for="expo-zone">🎪 Filter by Expo Zone</label>
                    <select id="expo-zone">
                        <option value="">All Expo Zones</option>
                        <option value="Wellness Zone">🏥 Wellness Zone</option>
                        <option value="Career Zone">💼 Career Zone</option>
                        <option value="Family Resource Hub">👨‍👩‍👧‍👦 Family Resource Hub</option>
                        <option value="Community Partners Pavilion">🤝 Community Partners Pavilion</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label for="revenue">💰 Filter by Revenue</label>
                    <select id="revenue">
                        <option value="">All Revenue Levels</option>
                        <option value="0-100000">Under $100K</option>
                        <option value="100000-500000">$100K - $500K</option>
                        <option value="500000-1000000">$500K - $1M</option>
                        <option value="1000000-999999999">Over $1M</option>
                        <option value="unknown">Revenue Unknown</option>
                    </select>
                </div>
            </div>
            
            <div class="controls-grid">
                <div class="control-group">
                    <label>📍 Distance Tiers</label>
                    <div class="tier-filter">
                        <button class="tier-btn tier-1 active" data-tier="1">Tier 1 (0-10mi)</button>
                        <button class="tier-btn tier-2 active" data-tier="2">Tier 2 (10-20mi)</button>
                        <button class="tier-btn tier-3 active" data-tier="3">Tier 3 (20-30mi)</button>
                    </div>
                </div>

                <div class="control-group">
                    <label>🎪 Quick Expo Zone Filter</label>
                    <div class="zone-filter">
                        <button class="zone-btn wellness active" data-zone="Wellness Zone">🏥 Wellness</button>
                        <button class="zone-btn career active" data-zone="Career Zone">💼 Career</button>
                        <button class="zone-btn family active" data-zone="Family Resource Hub">👪 Family</button>
                        <button class="zone-btn community active" data-zone="Community Partners Pavilion">🤝 Community</button>
                    </div>
                </div>
            </div>
            
            <div class="button-group">
                <div class="view-toggle">
                    <button class="active" data-view="table">📊 Table View</button>
                    <button data-view="cards">📋 Card View</button>
                </div>
                <button class="btn btn-secondary" onclick="clearFilters()">🔄 Clear Filters</button>
                <button class="btn" onclick="exportCSV()">📥 Export CSV</button>
            </div>
        </section>

        <section id="results">
            <div class="table-container" id="table-view">
                <div class="table-wrapper">
                    <table id="orgs-table">
                        <thead>
                            <tr>
                                <th class="sortable" data-column="name">Organization Name</th>
                                <th class="sortable" data-column="phone">Phone</th>
                                <th class="sortable" data-column="website">Website</th>
                                <th class="sortable" data-column="category">Category</th>
                                <th class="sortable" data-column="expo_zone">Expo Zone</th>
                                <th class="sortable" data-column="city">City</th>
                                <th class="sortable" data-column="distance_tier">Distance Tier</th>
                                <th class="sortable" data-column="income_amount">Annual Revenue</th>
                                <th class="sortable" data-column="ein">EIN</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <!-- Table rows populated by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="cards-view" id="cards-view">
                <!-- Cards populated by JavaScript -->
            </div>
            
            <div class="no-results" id="no-results" style="display: none;">
                <p>No organizations match your current filters.</p>
                <button class="btn" onclick="clearFilters()">Clear Filters</button>
            </div>
        </section>

        <footer class="footer">
            <p>Data sourced from ProPublica Nonprofit Explorer API • Generated for Philadelphia Health Expo</p>
            <p>Distance tiers are estimates based on city location relative to the Convention Center</p>
            <p>Expo zones follow the Community Nonprofit Partners (CNP) model for comprehensive service delivery</p>
        </footer>
    </div>

    <script>
        // Embedded nonprofit data
        const nonprofitData = {data_placeholder};
        
        let filteredData = [...nonprofitData];
        let currentSort = { column: null, direction: 'asc' };
        let activeTiers = new Set(['1', '2', '3']);
        let activeZones = new Set(['Wellness Zone', 'Career Zone', 'Family Resource Hub', 'Community Partners Pavilion']);
        let currentView = 'table';

        // Initialize the dashboard
        function init() {
            updateStats();
            populateCategoryFilter();
            renderTable();
            setupEventListeners();
        }

        function updateStats() {
            const stats = calculateStats(nonprofitData);
            const statsContainer = document.getElementById('stats');
            
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${stats.total}</div>
                    <div class="stat-label">Total Organizations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.tier1}</div>
                    <div class="stat-label">Tier 1 (0-10mi)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.tier2}</div>
                    <div class="stat-label">Tier 2 (10-20mi)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.tier3}</div>
                    <div class="stat-label">Tier 3 (20-30mi)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.categories}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.expoZones}</div>
                    <div class="stat-label">Expo Zones</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.withPhone}</div>
                    <div class="stat-label">With Phone Number</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.avgRevenue}</div>
                    <div class="stat-label">Avg Revenue</div>
                </div>
            `;
        }

        function calculateStats(data) {
            const total = data.length;
            const tier1 = data.filter(org => org.distance_tier === 1).length;
            const tier2 = data.filter(org => org.distance_tier === 2).length;
            const tier3 = data.filter(org => org.distance_tier === 3).length;
            
            const categories = new Set(data.map(org => org.category)).size;
            const expoZones = new Set(data.map(org => org.expo_zone)).size;
            const withPhone = data.filter(org => org.phone).length;
            
            const revenueData = data.filter(org => org.income_amount > 0);
            const avgRevenue = revenueData.length > 0 
                ? formatCurrency(revenueData.reduce((sum, org) => sum + org.income_amount, 0) / revenueData.length)
                : 'N/A';
            
            return { total, tier1, tier2, tier3, categories, expoZones, withPhone, avgRevenue };
        }

        function populateCategoryFilter() {
            const categories = [...new Set(nonprofitData.map(org => org.category))].sort();
            const categorySelect = document.getElementById('category');
            
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        }

        function setupEventListeners() {
            // Search input
            document.getElementById('search').addEventListener('input', filterData);
            
            // Category filter
            document.getElementById('category').addEventListener('change', filterData);
            
            // Expo zone filter
            document.getElementById('expo-zone').addEventListener('change', filterData);
            
            // Revenue filter
            document.getElementById('revenue').addEventListener('change', filterData);
            
            // Tier filters
            document.querySelectorAll('.tier-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const tier = e.target.dataset.tier;
                    if (activeTiers.has(tier)) {
                        activeTiers.delete(tier);
                        e.target.classList.remove('active');
                    } else {
                        activeTiers.add(tier);
                        e.target.classList.add('active');
                    }
                    filterData();
                });
            });

            // Zone filters
            document.querySelectorAll('.zone-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const zone = e.target.dataset.zone;
                    if (activeZones.has(zone)) {
                        activeZones.delete(zone);
                        e.target.classList.remove('active');
                    } else {
                        activeZones.add(zone);
                        e.target.classList.add('active');
                    }
                    filterData();
                });
            });
            
            // View toggle
            document.querySelectorAll('.view-toggle button').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('.view-toggle button').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    currentView = e.target.dataset.view;
                    toggleView();
                });
            });
            
            // Table sorting
            document.querySelectorAll('.sortable').forEach(th => {
                th.addEventListener('click', (e) => {
                    const column = e.target.dataset.column;
                    sortTable(column);
                });
            });
        }

        function filterData() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const selectedCategory = document.getElementById('category').value;
            const selectedExpoZone = document.getElementById('expo-zone').value;
            const selectedRevenue = document.getElementById('revenue').value;
            
            filteredData = nonprofitData.filter(org => {
                // Search filter
                const matchesSearch = !searchTerm || 
                    org.name.toLowerCase().includes(searchTerm) ||
                    org.city.toLowerCase().includes(searchTerm);
                
                // Category filter
                const matchesCategory = !selectedCategory || org.category === selectedCategory;
                
                // Expo zone filter
                const matchesExpoZone = !selectedExpoZone || org.expo_zone === selectedExpoZone;
                
                // Revenue filter
                let matchesRevenue = true;
                if (selectedRevenue) {
                    if (selectedRevenue === 'unknown') {
                        matchesRevenue = !org.income_amount || org.income_amount === 0;
                    } else {
                        const [min, max] = selectedRevenue.split('-').map(Number);
                        matchesRevenue = org.income_amount >= min && org.income_amount <= max;
                    }
                }
                
                // Tier filter
                const matchesTier = activeTiers.has(org.distance_tier.toString());
                
                // Zone filter (quick buttons)
                const matchesZone = activeZones.has(org.expo_zone);
                
                return matchesSearch && matchesCategory && matchesExpoZone && matchesRevenue && matchesTier && matchesZone;
            });
            
            renderCurrentView();
        }

        function sortTable(column) {
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }
            
            filteredData.sort((a, b) => {
                let valueA = a[column];
                let valueB = b[column];
                
                // Handle numeric columns
                if (column === 'income_amount' || column === 'asset_amount' || column === 'distance_tier' || column === 'ein') {
                    valueA = Number(valueA) || 0;
                    valueB = Number(valueB) || 0;
                } else {
                    valueA = (valueA || '').toString().toLowerCase();
                    valueB = (valueB || '').toString().toLowerCase();
                }
                
                if (valueA < valueB) return currentSort.direction === 'asc' ? -1 : 1;
                if (valueA > valueB) return currentSort.direction === 'asc' ? 1 : -1;
                return 0;
            });
            
            updateSortHeaders();
            renderCurrentView();
        }

        function updateSortHeaders() {
            document.querySelectorAll('.sortable').forEach(th => {
                th.className = 'sortable';
                if (th.dataset.column === currentSort.column) {
                    th.classList.add(currentSort.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
                }
            });
        }

        function renderCurrentView() {
            if (currentView === 'table') {
                renderTable();
            } else {
                renderCards();
            }
        }

        function toggleView() {
            const tableView = document.getElementById('table-view');
            const cardsView = document.getElementById('cards-view');
            
            if (currentView === 'table') {
                tableView.style.display = 'block';
                cardsView.style.display = 'none';
                renderTable();
            } else {
                tableView.style.display = 'none';
                cardsView.style.display = 'grid';
                renderCards();
            }
        }

        function getZoneBadgeClass(zone) {
            if (zone === 'Wellness Zone') return 'zone-wellness';
            if (zone === 'Career Zone') return 'zone-career';
            if (zone === 'Family Resource Hub') return 'zone-family';
            return 'zone-community';
        }

        function renderTable() {
            const tbody = document.getElementById('table-body');
            const noResults = document.getElementById('no-results');
            
            if (filteredData.length === 0) {
                tbody.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }
            
            noResults.style.display = 'none';
            
            tbody.innerHTML = filteredData.map(org => `
                <tr>
                    <td><strong>${escapeHtml(org.name)}</strong></td>
                    <td>${org.phone ? `<a href="tel:${org.phone.replace(/[^\\d]/g, '')}" class="link-button">${org.phone}</a>` : 'N/A'}</td>
                    <td>${org.website ? `<a href="${org.website}" target="_blank" class="link-button">Visit Site</a>` : 'N/A'}</td>
                    <td>${escapeHtml(org.category)}</td>
                    <td><span class="zone-badge ${getZoneBadgeClass(org.expo_zone)}">${org.expo_zone}</span></td>
                    <td>${escapeHtml(org.city)}</td>
                    <td><span class="tier-badge tier-${org.distance_tier}">Tier ${org.distance_tier}</span></td>
                    <td>${formatCurrency(org.income_amount)}</td>
                    <td>${org.ein}</td>
                </tr>
            `).join('');
        }

        function renderCards() {
            const cardsView = document.getElementById('cards-view');
            const noResults = document.getElementById('no-results');
            
            if (filteredData.length === 0) {
                cardsView.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }
            
            noResults.style.display = 'none';
            
            cardsView.innerHTML = filteredData.map(org => `
                <div class="org-card">
                    <h3>${escapeHtml(org.name)}</h3>
                    <div class="details">
                        <div class="detail-row">
                            <span class="detail-label">Phone:</span>
                            <span>${org.phone ? `<a href="tel:${org.phone.replace(/[^\\d]/g, '')}" class="link-button">${org.phone}</a>` : 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Website:</span>
                            <span>${org.website ? `<a href="${org.website}" target="_blank" class="link-button">Visit Site</a>` : 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Category:</span>
                            <span>${escapeHtml(org.category)}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Expo Zone:</span>
                            <span class="zone-badge ${getZoneBadgeClass(org.expo_zone)}">${org.expo_zone}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Location:</span>
                            <span>${escapeHtml(org.city)}, ${org.state}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Distance:</span>
                            <span class="tier-badge tier-${org.distance_tier}">Tier ${org.distance_tier}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Revenue:</span>
                            <span>${formatCurrency(org.income_amount)}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">EIN:</span>
                            <span>${org.ein}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Found via:</span>
                            <span>${escapeHtml(org.found_via)}</span>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function clearFilters() {
            document.getElementById('search').value = '';
            document.getElementById('category').value = '';
            document.getElementById('expo-zone').value = '';
            document.getElementById('revenue').value = '';
            
            activeTiers = new Set(['1', '2', '3']);
            activeZones = new Set(['Wellness Zone', 'Career Zone', 'Family Resource Hub', 'Community Partners Pavilion']);
            
            document.querySelectorAll('.tier-btn').forEach(btn => {
                btn.classList.add('active');
            });
            
            document.querySelectorAll('.zone-btn').forEach(btn => {
                btn.classList.add('active');
            });
            
            filteredData = [...nonprofitData];
            renderCurrentView();
        }

        function exportCSV() {
            const headers = [
                'Organization Name', 'Phone', 'Website', 'Category', 'Expo Zone', 'City', 'State', 
                'Distance Tier', 'Annual Revenue', 'Assets', 'EIN', 'NTEE Code', 'Found Via'
            ];
            const csvContent = [
                headers.join(','),
                ...filteredData.map(org => [
                    `"${(org.name || '').replace(/"/g, '""')}"`,
                    `"${org.phone || ''}"`,
                    `"${org.website || ''}"`,
                    `"${(org.category || '').replace(/"/g, '""')}"`,
                    `"${(org.expo_zone || '').replace(/"/g, '""')}"`,
                    `"${org.city || ''}"`,
                    org.state || '',
                    org.distance_tier || '',
                    org.income_amount || 0,
                    org.asset_amount || 0,
                    org.ein || '',
                    `"${org.ntee_code || ''}"`,
                    `"${org.found_via || ''}"`
                ].join(','))
            ].join('\\n');
            
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `philadelphia-health-expo-nonprofits-${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function formatCurrency(amount) {
            if (!amount || amount === 0) return 'N/A';
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(amount);
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
'''

# Convert data to JSON string
import json
data_json = json.dumps(organizations, indent=2)

# Replace placeholder in template
final_html = html_template.replace('{data_placeholder}', data_json)

# Write the new dashboard
with open('index.html', 'w') as f:
    f.write(final_html)

print("Dashboard rebuilt with expanded data and features!")
print("Key improvements:")
print("- Expanded from 128 to 299 organizations")
print("- Added Expo Zone categorization and filtering")
print("- Added website column (where available)")
print("- Enhanced phone number display with clickable tel: links")
print("- Improved responsive design")
print("- Added quick zone filter buttons")
print("- Enhanced stats display")
print("- Updated styling and layout")