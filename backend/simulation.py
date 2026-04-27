def simulate(df, t_boost=0.2, d_boost=0.2):

    sim = df.copy()

    sim['sim_transfer'] = sim['Children transferred to HHS'] * (1 + t_boost)
    sim['sim_discharge'] = sim['Children discharged'] * (1 + d_boost)

    sim['sim_backlog'] = sim['Children in CBP custody'] - sim['sim_discharge']

    return sim