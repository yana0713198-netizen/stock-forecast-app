import yfinance as yf
import pandas as pd
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA

def predict_stock(ticker: str, model_name: str = "prophet", df_file=None):
    # 過去6ヶ月株価取得
    if df_file is not None:
        df = df_file
    else:
        data = yf.download(ticker, period="6mo")
        if data.empty:
            print(f"⚠️ yfinance returned no data for ticker={ticker}")
            return []
        df = pd.DataFrame({"ds": data.index, "y": data["Close"]}).reset_index(drop=True)

    if model_name.lower() == "prophet":
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        result = forecast[['ds', 'yhat']].tail(30).to_dict(orient="records")
        print("✅ Prophet forecast sample:", result[:3])  # ← デバッグ用
        return result

    elif model_name.lower() == "arima":
        model = ARIMA(df['y'], order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(30)
        df_forecast = pd.DataFrame({
            "ds": pd.date_range(df['ds'].iloc[-1], periods=30, freq="D"),
            "yhat": forecast
        })
        result = df_forecast.to_dict(orient="records")
        print("✅ ARIMA forecast sample:", result[:3])  # ← デバッグ用
        return result

    else:
        # デフォルト：過去値の平均を返す
        mean_val = df['y'].mean()
        result = [{"ds": d, "yhat": mean_val} for d in pd.date_range(df['ds'].iloc[-1], periods=30, freq="D")]
        print("✅ Mean forecast sample:", result[:3])  # ← デバッグ用
        return result
