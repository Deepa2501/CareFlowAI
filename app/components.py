"""HTML component helpers for the CareFlowAI dashboard."""


def kpi_card(label, value, sub="", color_class=""):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color_class}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""


def kpi_row(cards_html):
    return f'<div class="kpi-row">{"".join(cards_html)}</div>'


def metric_item(label, value, sub=""):
    return f"""
    <div class="metric-item">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="sub">{sub}</div>
    </div>"""


def metrics_row(items_html):
    return f'<div class="metrics-row">{"".join(items_html)}</div>'


def section_header(title, color="cyan"):
    return f"""
    <div class="section-header">
        <div class="bar {color}"></div>
        <h3>{title}</h3>
    </div>"""


def alert_card(title, desc, rec, level="warning"):
    icon = {"critical": "🔴", "warning": "🟠", "success": "✅"}.get(level, "🔵")
    return f"""
    <div class="alert-card {level}">
        <div class="title">{icon} {title}</div>
        <div class="desc">{desc}</div>
        <div class="rec">💡 {rec}</div>
    </div>"""


def insight_card(title, body, priority="medium", border_color=None):
    style = f'border-left-color: {border_color};' if border_color else ''
    return f"""
    <div class="insight-card" style="{style}">
        <div class="badge {priority}">{priority.upper()} PRIORITY</div>
        <div class="title" style="font-weight:600;font-size:0.95rem;margin-bottom:6px;">{title}</div>
        <div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">{body}</div>
    </div>"""


def exec_summary_box(text):
    return f"""
    <div class="exec-summary">
        🧠 <strong>Executive Summary</strong><br/>{text}
    </div>"""
