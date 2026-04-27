def generate_alerts(df):

    alerts = []

    latest = df.iloc[-1]

    if latest['backlog'] > df['backlog'].mean():
        alerts.append("🔴 High backlog")

    if latest['transfer_efficiency'] < 0.5:
        alerts.append("🟠 Low transfer efficiency")

    if latest['anomaly_flag'] == 1:
        alerts.append("🚨 Anomaly detected")

    return alerts