def get_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #111827;
    --bg-card: rgba(17, 24, 39, 0.85);
    --border: rgba(56, 189, 248, 0.08);
    --accent-cyan: #22d3ee;
    --accent-red: #f43f5e;
    --accent-green: #34d399;
    --accent-orange: #fb923c;
    --accent-blue: #60a5fa;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(148, 163, 184, 0.08);
}

html, body, .stApp {
    background: linear-gradient(135deg, #0a0e17 0%, #0f172a 50%, #0a0e17 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(56, 189, 248, 0.12) !important;
    margin: 1rem 0 !important;
}

/* Sidebar section cards */
.sidebar-section {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    backdrop-filter: blur(12px);
}
.sidebar-section h4 {
    color: var(--accent-cyan);
    margin: 0 0 10px 0;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
}

/* ===== KPI CARDS ===== */
.kpi-row { display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }
.kpi-card {
    flex: 1; min-width: 170px;
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px 18px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    border-color: rgba(56, 189, 248, 0.2);
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
    border-radius: 16px 16px 0 0;
}
.kpi-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-secondary);
    font-weight: 600;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.kpi-value.red {
    background: linear-gradient(135deg, var(--accent-red), var(--accent-orange));
    -webkit-background-clip: text;
}
.kpi-value.green {
    background: linear-gradient(135deg, var(--accent-green), #a3e635);
    -webkit-background-clip: text;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin-top: 6px;
}

/* ===== SUMMARY METRICS ROW ===== */
.metrics-row { display: flex; gap: 24px; flex-wrap: wrap; margin: 10px 0 24px; }
.metric-item { text-align: center; flex: 1; min-width: 120px; }
.metric-item .label { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; }
.metric-item .value { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
.metric-item .sub { font-size: 0.7rem; color: var(--accent-green); }

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 10px 18px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-red) !important;
    border-bottom: 2px solid var(--accent-red) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-primary) !important; }

/* ===== SECTION HEADERS ===== */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 20px 0 14px;
}
.section-header .bar { width: 4px; height: 24px; border-radius: 2px; }
.section-header .bar.cyan { background: var(--accent-cyan); }
.section-header .bar.red { background: var(--accent-red); }
.section-header .bar.green { background: var(--accent-green); }
.section-header .bar.orange { background: var(--accent-orange); }
.section-header h3 {
    margin: 0; font-size: 1.15rem; font-weight: 600;
    color: var(--accent-cyan);
}

/* ===== ALERT CARDS ===== */
.alert-card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
    border-left: 4px solid;
    transition: all 0.3s ease;
}
.alert-card:hover { transform: translateX(4px); }
.alert-card.critical { border-left-color: var(--accent-red); }
.alert-card.warning { border-left-color: var(--accent-orange); }
.alert-card.success { border-left-color: var(--accent-green); }
.alert-card .title { font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }
.alert-card .desc { font-size: 0.82rem; color: var(--text-secondary); }
.alert-card .rec { font-size: 0.82rem; color: var(--accent-cyan); margin-top: 8px; }

/* ===== INSIGHT CARDS ===== */
.insight-card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    border-left: 4px solid var(--accent-blue);
    transition: all 0.3s ease;
}
.insight-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.2); }
.insight-card .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}
.insight-card .badge.high { background: rgba(244,63,94,0.15); color: var(--accent-red); }
.insight-card .badge.medium { background: rgba(251,146,60,0.15); color: var(--accent-orange); }
.insight-card .badge.low { background: rgba(52,211,153,0.15); color: var(--accent-green); }

/* ===== EXECUTIVE SUMMARY ===== */
.exec-summary {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(99, 102, 241, 0.08));
    border: 1px solid rgba(56, 189, 248, 0.12);
    border-radius: 14px;
    padding: 18px 22px;
    margin: 16px 0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.exec-summary strong { color: var(--accent-cyan); }

/* ===== DATAFRAME ===== */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ===== GENERAL ===== */
div.block-container { padding-top: 1.5rem; max-width: 1200px; }
.stSlider > div { color: var(--accent-blue); }
.stRadio > label { color: var(--text-secondary) !important; }

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .kpi-row { flex-direction: column; }
    .kpi-card { min-width: 100%; }
    .metrics-row { flex-direction: column; gap: 12px; }
    div.block-container { padding: 0.5rem 0.8rem; }
}
@media (max-width: 480px) {
    .kpi-value { font-size: 1.5rem; }
    .kpi-card { padding: 14px 12px; }
}
</style>
"""
