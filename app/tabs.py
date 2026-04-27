"""Tab rendering functions for CareFlowAI dashboard."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from components import section_header, alert_card, insight_card


def render_overview(df, date_col, apprehended_col, cbp_col, hhs_col, discharged_col):
    st.markdown(section_header("Pipeline Load Overview", "cyan"), unsafe_allow_html=True)
    fig = go.Figure()
    traces = [
        (apprehended_col, "CBP Apprehensions", "#22d3ee", "solid"),
        (cbp_col, "In CBP Custody", "#fb923c", "dot"),
        (hhs_col, "In HHS Care", "#fbbf24", "solid"),
        (discharged_col, "HHS Discharges", "#34d399", "solid"),
    ]
    for col, name, color, dash in traces:
        fig.add_trace(go.Scatter(x=df[date_col], y=df[col], mode='lines',
            name=name, line=dict(color=color, width=2, dash=dash)))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', y=1.12),
        margin=dict(l=40, r=20, t=40, b=40), height=380)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section_header("Intake vs Discharge Trends", "blue"), unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df[date_col], y=df[apprehended_col], mode='lines',
            name='Daily Apprehensions', line=dict(color='#f43f5e', width=1)))
        if '7d_avg_apprehensions' in df.columns:
            fig2.add_trace(go.Scatter(x=df[date_col], y=df['7d_avg_apprehensions'], mode='lines',
                name='7-Day Avg Apprehensions', line=dict(color='#f43f5e', width=3)))
        fig2.add_trace(go.Scatter(x=df[date_col], y=df[discharged_col], mode='lines',
            name='Daily Discharges', line=dict(color='#34d399', width=1)))
        if '7d_avg_discharges' in df.columns:
            fig2.add_trace(go.Scatter(x=df[date_col], y=df['7d_avg_discharges'], mode='lines',
                name='7-Day Avg Discharges', line=dict(color='#34d399', width=3)))
        fig2.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(l=40, r=20, t=20, b=40))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown(section_header("Backlog Accumulation Rate", "red"), unsafe_allow_html=True)
        bl = df['backlog'].copy()
        colors = ['#f43f5e' if v > 0 else '#34d399' for v in bl]
        fig3 = go.Figure(go.Bar(x=df[date_col], y=bl, marker_color=colors, name='Backlog'))
        fig3.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height=320, margin=dict(l=40, r=20, t=20, b=40))
        st.plotly_chart(fig3, use_container_width=True)


def render_data_preview(df):
    st.markdown(section_header("Data Preview", "cyan"), unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=500)


def render_backlog(df, date_col):
    st.markdown(section_header("Backlog Trend", "orange"), unsafe_allow_html=True)
    recent = df['backlog'].iloc[-1]
    prev = df['backlog'].iloc[-7] if len(df) > 7 else df['backlog'].iloc[0]
    direction = "📈 Increasing" if recent > prev else "📉 Decreasing"
    st.markdown(f"**Trend:** {direction} (Current: **{int(recent)}**, 7d ago: **{int(prev)}**)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df['backlog'], mode='lines',
        name='Backlog', line=dict(color='#fb923c', width=2), fill='tozeroy',
        fillcolor='rgba(251,146,60,0.1)'))
    if 'backlog_trend' in df.columns:
        fig.add_trace(go.Scatter(x=df[date_col], y=df['backlog_trend'], mode='lines',
            name='7-Day Avg', line=dict(color='#f43f5e', width=2, dash='dash')))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=40, r=20, t=20, b=40))
    st.plotly_chart(fig, use_container_width=True)


def render_forecast(df, model_type, forecast_days, cbp_col):
    from backend.forecasting import arima_forecast, prophet_forecast
    st.markdown(section_header(f"Forecast ({model_type})", "green"), unsafe_allow_html=True)
    with st.spinner("Running forecast model..."):
        if model_type == "Prophet":
            forecast = prophet_forecast(df, cbp_col, forecast_days)
        else:
            forecast = arima_forecast(df, cbp_col, forecast_days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines',
        name='Forecast', line=dict(color='#22d3ee', width=2), fill='tozeroy',
        fillcolor='rgba(34,211,238,0.08)'))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=40, r=20, t=20, b=40))
    st.plotly_chart(fig, use_container_width=True)

    csv = forecast.to_csv(index=False)
    st.download_button("📥 Download Forecast CSV", csv, "forecast.csv", "text/csv")


def render_simulation(df):
    from backend.simulation import simulate
    st.markdown(section_header("What-If Simulation", "blue"), unsafe_allow_html=True)
    if "t" not in st.session_state: st.session_state.t = 0.2
    if "d" not in st.session_state: st.session_state.d = 0.2
    c1, c2 = st.columns(2)
    with c1: t = st.slider("Transfer Rate Increase", 0.0, 1.0, st.session_state.t, key="sim_t")
    with c2: d = st.slider("Discharge Rate Increase", 0.0, 1.0, st.session_state.d, key="sim_d")
    st.session_state.t = t
    st.session_state.d = d
    sim_df = simulate(df, t, d)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim_df['Date'], y=df['backlog'], mode='lines',
        name='Current Backlog', line=dict(color='#fb923c', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=sim_df['Date'], y=sim_df['sim_backlog'], mode='lines',
        name='Simulated Backlog', line=dict(color='#22d3ee', width=2), fill='tozeroy',
        fillcolor='rgba(34,211,238,0.08)'))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=40, r=20, t=20, b=40))
    st.plotly_chart(fig, use_container_width=True)


def render_alerts(df):
    st.markdown(section_header("Alerts & Recommendations", "red"), unsafe_allow_html=True)
    backlog = df['backlog'].iloc[-1]
    eff = df['transfer_efficiency'].iloc[-1]
    disch = df['discharge_effectiveness'].iloc[-1]
    has_anomaly = df['anomaly_flag'].iloc[-1] == 1 if 'anomaly_flag' in df.columns else False
    cards = []
    if backlog > 30:
        cards.append(alert_card("High Backlog Detected",
            f"Current backlog is {int(backlog)}, significantly above the target threshold of 30.",
            "Increase discharge rate or speed up processing from CBP to HHS.", "critical"))
    if eff < 0.5:
        cards.append(alert_card("Low Transfer Efficiency",
            f"Transfer efficiency is {eff:.1%}, below the 50% target.",
            "Improve transfer pipeline or reduce delays between CBP and HHS.", "warning"))
    if disch < 0.6:
        cards.append(alert_card("Low Discharge Effectiveness",
            f"Discharge effectiveness is {disch:.1%}, below the 60% target.",
            "Increase sponsor placement rate or optimize case processing.", "warning"))
    if has_anomaly:
        cards.append(alert_card("Anomaly Detected",
            "The anomaly detection model flagged the latest data point as unusual.",
            "Investigate recent operational changes that may have caused this deviation.", "critical"))
    if not cards:
        cards.append(alert_card("System Operating Normally",
            "All KPIs are within acceptable ranges. No anomalies detected.",
            "Continue monitoring for sustained performance.", "success"))
    st.markdown("".join(cards), unsafe_allow_html=True)


def render_monthly(df, date_col, cbp_col, discharged_col):
    st.markdown(section_header("Monthly Summary", "cyan"), unsafe_allow_html=True)
    df_m = df.copy()
    df_m['month'] = pd.to_datetime(df_m[date_col]).dt.to_period('M').astype(str)
    transferred_col = 'Children transferred to HHS'
    cols_to_agg = {cbp_col: 'sum', discharged_col: 'sum'}
    if transferred_col in df_m.columns:
        cols_to_agg[transferred_col] = 'sum'
    monthly = df_m.groupby('month').agg(cols_to_agg).reset_index()
    monthly['month'] = pd.to_datetime(monthly['month'])
    monthly = monthly.sort_values('month')
    monthly['month'] = monthly['month'].dt.strftime('%b %Y')
    y_cols = [c for c in [cbp_col, transferred_col, discharged_col] if c in monthly.columns]
    fig = px.bar(monthly, x='month', y=y_cols, barmode='group',
        color_discrete_sequence=['#22d3ee', '#fb923c', '#34d399'])
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', legend_title_text='', height=420,
        margin=dict(l=40, r=20, t=20, b=40))
    st.plotly_chart(fig, use_container_width=True)


def render_trends(df, date_col, apprehended_col, discharged_col):
    st.markdown(section_header("Intake vs Discharge Trends (7-Day Rolling)", "green"), unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df[apprehended_col], mode='lines',
        name='Daily Apprehensions', line=dict(color='#f43f5e', width=1)))
    if '7d_avg_apprehensions' in df.columns:
        fig.add_trace(go.Scatter(x=df[date_col], y=df['7d_avg_apprehensions'], mode='lines',
            name='7-Day Avg Apprehensions', line=dict(color='#f43f5e', width=3)))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[discharged_col], mode='lines',
        name='Daily Discharges', line=dict(color='#34d399', width=1)))
    if '7d_avg_discharges' in df.columns:
        fig.add_trace(go.Scatter(x=df[date_col], y=df['7d_avg_discharges'], mode='lines',
            name='7-Day Avg Discharges', line=dict(color='#34d399', width=3)))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['backlog'], mode='lines',
        name='Backlog', line=dict(color='#fb923c', dash='dash', width=2)))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=420, margin=dict(l=40, r=20, t=20, b=40),
        legend=dict(orientation='h', y=1.1))
    st.plotly_chart(fig, use_container_width=True)


def render_insights(df):
    st.markdown(section_header("AI-Powered Insights", "blue"), unsafe_allow_html=True)
    insights = []
    bl = df['backlog']
    eff = df['transfer_efficiency']
    disch = df['discharge_effectiveness']

    bl_trend = bl.iloc[-7:].mean() - bl.iloc[-14:-7].mean() if len(df) >= 14 else 0
    if bl_trend > 5:
        insights.append(insight_card("Backlog Trend Accelerating",
            f"Average backlog increased by {bl_trend:.1f} over the past week compared to the prior week. "
            "This upward trend suggests intake is consistently outpacing discharge capacity.",
            "high", "#f43f5e"))
    elif bl_trend < -5:
        insights.append(insight_card("Backlog Declining — Positive Signal",
            f"Average backlog decreased by {abs(bl_trend):.1f} over the past week. "
            "Discharge rates are catching up with intake volumes.",
            "low", "#34d399"))

    avg_eff = eff.mean()
    if avg_eff < 0.5:
        insights.append(insight_card("Transfer Pipeline Bottleneck",
            f"Average transfer efficiency is {avg_eff:.1%}, well below the 50% target. "
            "Children are spending longer in CBP custody than necessary.",
            "high", "#f43f5e"))
    elif avg_eff >= 0.8:
        insights.append(insight_card("Transfer Pipeline Operating Efficiently",
            f"Average transfer efficiency is {avg_eff:.1%}, exceeding the 80% target. "
            "The CBP-to-HHS handoff process is working well.",
            "low", "#34d399"))

    avg_disch = disch.mean()
    if avg_disch < 0.6:
        insights.append(insight_card("Discharge Rate Needs Improvement",
            f"Average discharge effectiveness is {avg_disch:.1%}. "
            "Consider increasing sponsor placement capacity or streamlining case reviews.",
            "medium", "#fb923c"))

    if 'anomaly_flag' in df.columns:
        anomaly_pct = df['anomaly_flag'].mean() * 100
        if anomaly_pct > 8:
            insights.append(insight_card("Elevated Anomaly Rate",
                f"{anomaly_pct:.1f}% of observations flagged as anomalous (expected ≤5%). "
                "This may indicate systemic operational irregularities.",
                "high", "#f43f5e"))

    vol_cv = df['backlog'].std() / (df['backlog'].mean() + 1)
    if vol_cv > 0.5:
        insights.append(insight_card("High Volatility in Pipeline",
            f"Backlog coefficient of variation is {vol_cv:.2f}, indicating unstable flow. "
            "Consider implementing buffer capacity or smoothing intake scheduling.",
            "medium", "#fb923c"))
    else:
        insights.append(insight_card("Stable Pipeline Operations",
            f"Backlog coefficient of variation is {vol_cv:.2f}, indicating consistent flow patterns.",
            "low", "#34d399"))

    if not insights:
        insights.append(insight_card("System Performance Normal",
            "All metrics are within expected ranges. No significant patterns detected.", "low", "#34d399"))

    st.markdown("".join(insights), unsafe_allow_html=True)


def render_bottleneck(df, date_col, cbp_col, hhs_col, discharged_col):
    st.markdown(section_header("Pipeline Bottleneck Analysis", "red"), unsafe_allow_html=True)

    transferred_col = 'Children transferred to HHS'
    avg_cbp = df[cbp_col].mean()
    avg_trans = df[transferred_col].mean() if transferred_col in df.columns else 0
    avg_hhs = df[hhs_col].mean()
    avg_disch = df[discharged_col].mean()

    stages = ['CBP Intake', 'CBP → HHS Transfer', 'HHS Care', 'HHS Discharge']
    values = [avg_cbp, avg_trans, avg_hhs, avg_disch]
    max_v = max(values) if max(values) > 0 else 1
    colors = []
    for v in values:
        ratio = v / max_v
        if ratio < 0.3:
            colors.append('#f43f5e')
        elif ratio < 0.6:
            colors.append('#fb923c')
        else:
            colors.append('#34d399')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section_header("Average Stage Volume", "orange"), unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=stages, y=values, marker_color=colors, text=[f"{v:.0f}" for v in values],
            textposition='outside'))
        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(l=40, r=20, t=20, b=80),
            yaxis_title='Avg Daily Count')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(section_header("Stage Efficiency Flow", "cyan"), unsafe_allow_html=True)
        eff_transfer = (avg_trans / avg_cbp * 100) if avg_cbp > 0 else 0
        eff_discharge = (avg_disch / avg_hhs * 100) if avg_hhs > 0 else 0
        eff_pipeline = (avg_disch / avg_cbp * 100) if avg_cbp > 0 else 0
        eff_names = ['CBP→HHS Transfer Rate', 'HHS Discharge Rate', 'End-to-End Pipeline']
        eff_vals = [eff_transfer, eff_discharge, eff_pipeline]
        eff_colors = ['#f43f5e' if v < 30 else '#fb923c' if v < 60 else '#34d399' for v in eff_vals]
        fig2 = go.Figure(go.Bar(x=eff_names, y=eff_vals, marker_color=eff_colors,
            text=[f"{v:.1f}%" for v in eff_vals], textposition='outside'))
        fig2.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(l=40, r=20, t=20, b=80),
            yaxis_title='Efficiency %')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(section_header("Pipeline Flow Over Time", "green"), unsafe_allow_html=True)
    fig3 = go.Figure()
    flow_traces = [(cbp_col, "CBP Custody", "#22d3ee"), (hhs_col, "HHS Care", "#fbbf24"),
        (discharged_col, "Discharged", "#34d399")]
    if transferred_col in df.columns:
        flow_traces.insert(1, (transferred_col, "Transferred", "#fb923c"))
    for col, name, color in flow_traces:
        fig3.add_trace(go.Scatter(x=df[date_col], y=df[col], mode='lines', name=name,
            line=dict(color=color, width=2), stackgroup='one'))
    fig3.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=40, r=20, t=20, b=40),
        legend=dict(orientation='h', y=1.1))
    st.plotly_chart(fig3, use_container_width=True)
