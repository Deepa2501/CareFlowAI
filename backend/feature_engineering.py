def create_features(df):

    df['transfer_efficiency'] = df['Children transferred to HHS'] / (df['Children in CBP custody'] + 1)

    df['discharge_effectiveness'] = df['Children discharged'] / (df['Children in HHS care'] + 1)

    df['inflow'] = df['Children in CBP custody']
    df['outflow'] = df['Children discharged']

    df['backlog'] = df['inflow'] - df['outflow']

    df['backlog_trend'] = df['backlog'].rolling(7).mean()

    df = df.fillna(0)

    return df