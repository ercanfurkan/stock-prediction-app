import pandas as pd
import ta

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'])
    return df

def add_technical_indicators(df):
    df = df.copy()
    df["RSI"] = ta.momentum.RSIIndicator(df["adjClose"]).rsi()
    macd = ta.trend.MACD(df["adjClose"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    boll = ta.volatility.BollingerBands(df["adjClose"])
    df["BOLL_UP"] = boll.bollinger_hband()
    df["BOLL_DOWN"] = boll.bollinger_lband()
    df["BOLL_MID"] = boll.bollinger_mavg()
    return df

def add_mov_avgs(df):
    df = df.copy()
    df["MA-5"] = df["adjClose"].rolling(window=5).mean()
    df["MA-15"] = df["adjClose"].rolling(window=15).mean()
    df["MA-30"] = df["adjClose"].rolling(window=30).mean()
    df["MA-60"] = df["adjClose"].rolling(window=60).mean()
    df["MA-90"] = df["adjClose"].rolling(window=90).mean()
    df["MA-120"] = df["adjClose"].rolling(window=120).mean()
    df["MA-150"] = df["adjClose"].rolling(window=150).mean()
    return df
