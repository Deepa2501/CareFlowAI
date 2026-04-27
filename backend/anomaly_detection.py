from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    features = df[['inflow', 'outflow', 'backlog']]

    model = IsolationForest(contamination=0.05, random_state=42)

    df['anomaly'] = model.fit_predict(features)

    df['anomaly_flag'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

    return df