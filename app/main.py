import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="CareFlow AI", page_icon="🧠", layout="wide")

# ===== THEME =====
from styles import get_css
st.markdown(get_css(), unsafe_allow_html=True)

from components import kpi_card, kpi_row, metric_item, metrics_row, exec_summary_box
from tabs import (render_overview, render_data_preview, render_backlog,
    render_forecast, render_simulation, render_alerts, render_monthly,
    render_trends, render_insights, render_bottleneck)
from backend.data_processing import clean_columns, load_data, clean_data, rename_columns
from backend.feature_engineering import create_features
from backend.anomaly_detection import detect_anomalies


# ===== DUMMY DATA GENERATOR =====
def generate_dummy_data():
    dates = pd.date_range(start="2023-01-01", periods=30)
    cbp = np.random.randint(100, 150, 30)
    transferred = (cbp * np.random.uniform(0.6, 0.9, 30)).astype(int)
    discharged = (transferred * np.random.uniform(0.7, 0.95, 30)).astype(int)
    return pd.DataFrame({
        "Date": dates,
        "Children apprehended and placed in CBP custody*": cbp,
        "Children in CBP custody": cbp,
        "Children transferred out of CBP custody": transferred,
        "Children in HHS care": (cbp - transferred * 0.3).astype(int),
        "Children discharged from HHS care": discharged
    })


# ===== COLUMN RESOLVER =====
def pick_column(frame, candidates):
    for name in candidates:
        if name in frame.columns:
            return name
    raise KeyError(f"Missing columns. Tried: {candidates}. Available: {list(frame.columns)}")


# ===== SIDEBAR =====
st.sidebar.markdown("""
<div style="text-align:center;padding:10px 0 16px;">
    <span style="font-size:2rem;">🧠</span><br/>
    <span style="font-size:1.3rem;font-weight:700;
        background:linear-gradient(135deg,#22d3ee,#6366f1);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        CareFlow AI
    </span><br/>
    <span style="font-size:0.72rem;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;">
        Analytics Dashboard
    </span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section"><h4>📂 Data Source</h4></div>', unsafe_allow_html=True)

bundled_btn = st.sidebar.button("📦 Use Bundled Dataset", key="bundled", use_container_width=True)
dummy_btn = st.sidebar.button("🎲 Generate Dummy Data", key="dummy", use_container_width=True)
uploaded_file = st.sidebar.file_uploader("📄 Upload CSV", type=["csv"], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section"><h4>⚙️ Forecast Settings</h4></div>', unsafe_allow_html=True)
forecast_days = st.sidebar.slider("Forecast Horizon (days)", 7, 60, 30)
model_type = st.sidebar.radio("Forecast Method", ["Prophet", "ARIMA"])

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section"><h4>🎯 KPI Thresholds</h4></div>', unsafe_allow_html=True)
if "min_eff" not in st.session_state: st.session_state.min_eff = 0.8
if "min_discharge" not in st.session_state: st.session_state.min_discharge = 0.6
if "min_throughput" not in st.session_state: st.session_state.min_throughput = 0.5
min_eff = st.sidebar.slider("Min Transfer Efficiency", 0.0, 1.0, st.session_state.min_eff)
min_discharge = st.sidebar.slider("Min Discharge Effectiveness", 0.0, 1.0, st.session_state.min_discharge)
min_throughput = st.sidebar.slider("Min Pipeline Throughput", 0.0, 1.0, st.session_state.min_throughput)
st.session_state.min_eff = min_eff
st.session_state.min_discharge = min_discharge
st.session_state.min_throughput = min_throughput


# ===== DATA LOADING =====
df = None

if bundled_btn:
    st.session_state["data_source"] = "bundled"
if dummy_btn:
    st.session_state["data_source"] = "dummy"
if uploaded_file is not None:
    st.session_state["data_source"] = "upload"
    st.session_state["uploaded_file"] = uploaded_file

source = st.session_state.get("data_source", None)

if source == "bundled":
    with st.spinner("Loading bundled dataset..."):
        df = load_data()
        df = clean_data(df)
    st.sidebar.success("✅ Bundled dataset loaded")
elif source == "dummy":
    with st.spinner("Generating dummy data..."):
        df = generate_dummy_data()
        df = clean_columns(df)
        df = rename_columns(df)
        df = clean_data(df)
    st.sidebar.success("✅ Dummy data generated")
elif source == "upload":
    uf = st.session_state.get("uploaded_file")
    if uf is not None:
        with st.spinner("Processing upload..."):
            df = load_data()
            df = clean_data(df)
        st.sidebar.success("✅ CSV uploaded successfully")
else:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <span style="font-size:4rem;">🧠</span>
        <h1 style="background:linear-gradient(135deg,#22d3ee,#6366f1);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            font-size:2.5rem;margin:16px 0 8px;">CareFlow AI</h1>
        <p style="color:#94a3b8;font-size:1.1rem;max-width:500px;margin:0 auto 30px;">
            Intelligent analytics for child care transition pipeline monitoring.
            Select a data source from the sidebar to get started.
        </p>
        <div style="display:flex;gap:24px;justify-content:center;flex-wrap:wrap;">
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(148,163,184,0.08);
                border-radius:14px;padding:24px;width:180px;">
                <div style="font-size:2rem;margin-bottom:8px;">📦</div>
                <div style="color:#22d3ee;font-weight:600;">Bundled Data</div>
                <div style="color:#94a3b8;font-size:0.8rem;margin-top:4px;">Pre-loaded dataset</div>
            </div>
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(148,163,184,0.08);
                border-radius:14px;padding:24px;width:180px;">
                <div style="font-size:2rem;margin-bottom:8px;">🎲</div>
                <div style="color:#22d3ee;font-weight:600;">Dummy Data</div>
                <div style="color:#94a3b8;font-size:0.8rem;margin-top:4px;">Synthetic sample</div>
            </div>
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(148,163,184,0.08);
                border-radius:14px;padding:24px;width:180px;">
                <div style="font-size:2rem;margin-bottom:8px;">📄</div>
                <div style="color:#22d3ee;font-weight:600;">Upload CSV</div>
                <div style="color:#94a3b8;font-size:0.8rem;margin-top:4px;">Your own data</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if df is None:
    st.stop()


# ===== FEATURE ENGINEERING =====
df = create_features(df)
df = detect_anomalies(df)

# Resolve column names
date_col = pick_column(df, ["Date", "date"])
apprehended_col = pick_column(df, ["Children apprehended", "children apprehended",
    "Children apprehended and placed in cbp custody", "children apprehended and placed in cbp custody"])
cbp_col = pick_column(df, ["Children in CBP custody", "children in cbp custody"])
hhs_col = pick_column(df, ["Children in HHS care", "children in hhs care"])
discharged_col = pick_column(df, ["Children discharged", "Children discharged from HHS care",
    "children discharged", "children discharged from hhs care"])

# Rolling averages
df['7d_avg_apprehensions'] = df[apprehended_col].rolling(window=7).mean()
df['7d_avg_discharges'] = df[discharged_col].rolling(window=7).mean()


# ===== KPI HERO SECTION =====
avg_eff = df['transfer_efficiency'].mean()
avg_disch = df['discharge_effectiveness'].mean()
transferred_col_name = 'Children transferred to HHS'
avg_throughput = (df[discharged_col].sum() / (df[cbp_col].sum() + 1)) * 100
cur_backlog = int(df['backlog'].iloc[-1])
stability = float(df[discharged_col].rolling(7).std().iloc[-1]) if len(df) >= 7 else 0

eff_color = "green" if avg_eff >= min_eff else "red"
disch_color = "green" if avg_disch >= min_discharge else "red"
tp_color = "green" if avg_throughput / 100 >= min_throughput else "red"
bl_color = "green" if cur_backlog <= 0 else "red"

cards = [
    kpi_card("Avg Transfer Efficiency", f"{avg_eff:.1%}", f"Target ≥ {min_eff:.0%}", eff_color),
    kpi_card("Avg Discharge Effectiveness", f"{avg_disch:.1%}", f"Target ≥ {min_discharge:.0%}", disch_color),
    kpi_card("Avg Pipeline Throughput", f"{avg_throughput:.1f}%", f"Target ≥ {min_throughput:.0%}", tp_color),
    kpi_card("Current Backlog", f"{cur_backlog:+d}", "Most recent observation", bl_color),
    kpi_card("Stability Score", f"{stability:.1f}", "7-day σ of discharges", ""),
]
st.markdown(kpi_row(cards), unsafe_allow_html=True)

# Summary metrics
total_app = int(df[apprehended_col].sum())
total_disch = int(df[discharged_col].sum())
total_cbp = int(df[cbp_col].sum())
peak_bl = int(df['backlog'].max())
peak_date = df.loc[df['backlog'].idxmax(), date_col]
peak_date_str = pd.to_datetime(peak_date).strftime('%Y-%m-%d') if pd.notna(peak_date) else "N/A"

metrics = [
    metric_item("Total Apprehensions", f"{total_app:,}"),
    metric_item("Total Discharges", f"{total_disch:,}"),
    metric_item("Total CBP Transfers", f"{total_cbp:,}"),
    metric_item("Peak Backlog", f"{peak_bl}", f"↑ on {peak_date_str}"),
]
st.markdown(metrics_row(metrics), unsafe_allow_html=True)

# Executive summary
parts = []
if cur_backlog > 30: parts.append("High backlog detected — intake exceeds discharge capacity.")
if avg_eff < 0.5: parts.append("Transfer delays observed in CBP→HHS pipeline.")
if avg_disch > 0.8: parts.append("Discharge system is performing well.")
if not parts: parts.append("System is stable and operating efficiently across all stages.")
st.markdown(exec_summary_box(" ".join(parts)), unsafe_allow_html=True)


# ===== TABS =====
tab_names = ["Overview", "Data Preview", "Backlog", "Forecast", "Simulation",
    "Alerts", "Monthly", "Trends", "Insights", "Bottleneck Analysis"]
tabs = st.tabs(tab_names)

with tabs[0]: render_overview(df, date_col, apprehended_col, cbp_col, hhs_col, discharged_col)
with tabs[1]: render_data_preview(df)
with tabs[2]: render_backlog(df, date_col)
with tabs[3]: render_forecast(df, model_type, forecast_days, cbp_col)
with tabs[4]: render_simulation(df)
with tabs[5]: render_alerts(df)
with tabs[6]: render_monthly(df, date_col, cbp_col, discharged_col)
with tabs[7]: render_trends(df, date_col, apprehended_col, discharged_col)
with tabs[8]: render_insights(df)
with tabs[9]: render_bottleneck(df, date_col, cbp_col, hhs_col, discharged_col)