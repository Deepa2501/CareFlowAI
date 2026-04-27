import numpy as np
import pandas as pd
import warnings
from statsmodels.tsa.arima.model import ARIMA


def _fallback_forecast(data, periods=14):
    history = data[['ds', 'y']].sort_values('ds').reset_index(drop=True)
    if history.empty:
        return pd.DataFrame(columns=['ds', 'yhat'])

    inferred_freq = pd.infer_freq(history['ds']) or 'D'
    future_dates = pd.date_range(
        start=history['ds'].iloc[-1],
        periods=periods + 1,
        freq=inferred_freq
    )[1:]

    window = min(7, len(history))
    baseline = float(history['y'].tail(window).mean())

    trend_window = min(14, len(history))
    trend_values = history['y'].tail(trend_window).to_numpy(dtype=float)
    slope = 0.0
    if len(trend_values) > 1:
        slope = (trend_values[-1] - trend_values[0]) / (len(trend_values) - 1)

    future_yhat = baseline + slope * np.arange(1, periods + 1)

    history_out = history.rename(columns={'y': 'yhat'})[['ds', 'yhat']]
    future_out = pd.DataFrame({'ds': future_dates, 'yhat': future_yhat})
    return pd.concat([history_out, future_out], ignore_index=True)


def prophet_forecast(df, column, periods=14):
    data = df[['Date', column]].rename(columns={'Date': 'ds', column: 'y'})
    data['ds'] = pd.to_datetime(data['ds'], errors='coerce')
    data['y'] = pd.to_numeric(data['y'], errors='coerce')
    data = data.dropna(subset=['ds', 'y'])

    if data.empty:
        raise ValueError(f"No valid data points available for forecasting column '{column}'.")

    try:
        from prophet import Prophet
        model = Prophet()
        model.fit(data)
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        return forecast[['ds', 'yhat']]
    except Exception:
        return _fallback_forecast(data, periods=periods)

def arima_forecast(df, column, periods=14):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")

    normalized_date_map = {
        str(col).strip().lower(): col for col in df.columns
    }

    date_col = normalized_date_map.get('date')
    if date_col is not None:
        date_series = pd.to_datetime(df[date_col], errors='coerce')
    elif isinstance(df.index, pd.DatetimeIndex):
        date_series = pd.to_datetime(df.index, errors='coerce')
    else:
        raise ValueError("No date column found. Expected a column named 'Date'/'date' or a DatetimeIndex.")

    data = pd.DataFrame({
        'ds': date_series,
        'y': pd.to_numeric(df[column], errors='coerce')
    }).dropna(subset=['ds', 'y']).sort_values('ds')

    if data.empty:
        raise ValueError(f"No valid data points available for forecasting column '{column}'.")

    data = data.drop_duplicates(subset=['ds'], keep='last').set_index('ds')
    inferred_freq = pd.infer_freq(data.index)
    data = data.asfreq(inferred_freq or 'D').ffill()

    if len(data) < 5:
        return _fallback_forecast(data.reset_index(), periods=periods)

    candidate_orders = [
        (2, 1, 2),
        (1, 1, 1),
        (1, 1, 0),
        (0, 1, 1),
        (0, 1, 0),
    ]

    model_fit = None
    for order in candidate_orders:
        try:
            model = ARIMA(data['y'], order=order)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                model_fit = model.fit()
            break
        except Exception:
            model_fit = None

    if model_fit is None:
        return _fallback_forecast(data.reset_index(), periods=periods)

    forecast = model_fit.forecast(steps=periods)
    last_date = data.index[-1]

    future_dates = pd.date_range(
        start=last_date,
        periods=periods + 1,
        freq='D'
    )[1:]

    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': forecast
    })

    return forecast_df