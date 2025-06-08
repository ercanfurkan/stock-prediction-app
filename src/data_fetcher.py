import requests
import pandas as pd
from config import API_KEY, BASE_URL, START_DATE, END_DATE

def build_tiingo_url(ticker: str, fmt="csv") -> str:
    return f"{BASE_URL}{ticker}/prices?startDate={START_DATE}&endDate={END_DATE}&format={fmt}&token={API_KEY}"

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    url = build_tiingo_url(ticker)
    print(f"Fetching data from: {url}")
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return pd.read_csv(url)

